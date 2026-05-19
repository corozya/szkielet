#!/usr/bin/env node
/* eslint-disable no-console */
"use strict";

const fs = require("node:fs");
const path = require("node:path");
const readline = require("node:readline/promises");

const REPO_ROOT = path.resolve(__dirname, "..");
const CWD = process.cwd();

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function ask(rl, question, defaultVal) {
  const hint = defaultVal ? ` [${defaultVal}]` : "";
  return rl.question(`  ${question}${hint}: `).then((a) => a.trim() || defaultVal || "");
}

function readEnvFile(envPath) {
  const map = new Map();
  if (!fs.existsSync(envPath)) return map;
  for (const line of fs.readFileSync(envPath, "utf8").split(/\r?\n/)) {
    const t = line.trim();
    if (!t || t.startsWith("#") || !t.includes("=")) continue;
    const idx = t.indexOf("=");
    map.set(t.slice(0, idx).trim(), t.slice(idx + 1).trim().replace(/^"|"$/g, ""));
  }
  return map;
}

function writeEnvMerge(envPath, updates) {
  fs.mkdirSync(path.dirname(envPath), { recursive: true });
  const existing = readEnvFile(envPath);
  for (const [k, v] of Object.entries(updates)) {
    if (v !== undefined && v !== "") existing.set(k, v);
  }
  const lines = [];
  for (const [k, v] of existing) lines.push(`${k}=${v}`);
  fs.writeFileSync(envPath, lines.join("\n") + "\n", "utf8");
}

function ensureGitignore(entry) {
  const giPath = path.join(CWD, ".gitignore");
  const content = fs.existsSync(giPath) ? fs.readFileSync(giPath, "utf8") : "";
  if (!content.split("\n").some((l) => l.trim() === entry)) {
    fs.appendFileSync(giPath, `\n${entry}\n`);
  }
}

function patchMcpJson(mcpJsonPath, serverName, serverEntry) {
  let obj = {};
  if (fs.existsSync(mcpJsonPath)) {
    try { obj = JSON.parse(fs.readFileSync(mcpJsonPath, "utf8")); } catch {}
  }
  fs.mkdirSync(path.dirname(mcpJsonPath), { recursive: true });
  obj.mcpServers = obj.mcpServers || {};
  obj.mcpServers[serverName] = serverEntry;
  fs.writeFileSync(mcpJsonPath, JSON.stringify(obj, null, 2) + "\n", "utf8");
}

function detectHosts() {
  const present = [];
  if (fs.existsSync(path.join(CWD, ".claude"))) present.push("claude");
  if (fs.existsSync(path.join(CWD, ".cursor"))) present.push("cursor");
  if (fs.existsSync(path.join(CWD, ".gemini"))) present.push("gemini");
  if (fs.existsSync(path.join(CWD, ".codex")) || fs.existsSync(path.join(CWD, "codex.json"))) present.push("codex");
  return present.length ? present : ["claude"];
}

function hostMcpPath(host) {
  if (host === "claude") return path.join(CWD, ".claude", "mcp.json");
  if (host === "cursor") return path.join(CWD, ".cursor", "mcp.json");
  if (host === "gemini") return path.join(CWD, ".gemini", "settings.json");
  if (host === "codex") return path.join(CWD, "mcp.json");
  return null;
}

async function selectIntegrations(rl, integrations) {
  console.log("\nDostępne integracje MCP:\n");
  integrations.forEach((i, idx) => {
    console.log(`  ${idx + 1}. ${i.name.padEnd(16)} — ${i.description}`);
  });
  console.log("\nWybierz numery (np. 1,3,4) lub 'all' dla wszystkich:");
  const input = (await rl.question("  > ")).trim();
  if (input.toLowerCase() === "all") return integrations;
  const selected = input
    .split(/[,\s]+/)
    .map((s) => parseInt(s, 10) - 1)
    .filter((n) => !isNaN(n) && n >= 0 && n < integrations.length)
    .map((n) => integrations[n]);
  return [...new Map(selected.map((s) => [s.name, s])).values()];
}

// ---------------------------------------------------------------------------
// Integration definitions
// ---------------------------------------------------------------------------

const INTEGRATIONS = [
  {
    name: "kanboard",
    description: "Zarządzanie zadaniami (backlog, tworzenie, handoff)",
    envFile: () => path.join(CWD, "kanboard_setup", ".env"),
    mcpEntry: (env) => ({
      command: "python3",
      args: [path.join(REPO_ROOT, "mcp_servers", "kanboard", "server.py")],
      cwd: CWD,
    }),
    async configure(rl) {
      console.log("\n  Kanboard — podaj dane połączenia:");
      const envPath = path.join(CWD, "kanboard_setup", ".env");
      const cur = readEnvFile(envPath);
      const url = await ask(rl, "URL JSON-RPC (np. https://kb.example.com/jsonrpc.php)", cur.get("KANBOARD_URL"));
      const user = await ask(rl, "Użytkownik API", cur.get("KANBOARD_USER") || "jsonrpc");
      const token = await ask(rl, "Token API", cur.get("KANBOARD_TOKEN") ? "****" : "");
      const project = await ask(rl, "Domyślny projekt (opcjonalnie)", cur.get("KANBOARD_PROJECT"));
      const realToken = token === "****" ? cur.get("KANBOARD_TOKEN") : token;
      if (!url || !realToken) throw new Error("KANBOARD_URL i KANBOARD_TOKEN są wymagane.");
      writeEnvMerge(envPath, { KANBOARD_URL: url, KANBOARD_USER: user, KANBOARD_TOKEN: realToken, KANBOARD_PROJECT: project });
      ensureGitignore("kanboard_setup/.env");
      return { saved: `kanboard_setup/.env` };
    },
  },
  {
    name: "mysql",
    description: "Dostęp read-only do bazy MySQL projektu",
    mcpEntry: () => ({
      command: "bash",
      args: ["scripts/run-mysql-mcp.sh"],
      cwd: CWD,
    }),
    async configure(rl) {
      console.log("\n  MySQL — dane bazy danych:");
      const envPath = path.join(CWD, ".env");
      const cur = readEnvFile(envPath);
      const host = await ask(rl, "Host MySQL", cur.get("DB_HOST") || "localhost");
      const port = await ask(rl, "Port", cur.get("DB_PORT") || "3306");
      const user = await ask(rl, "Użytkownik", cur.get("DB_USER"));
      const pass = await ask(rl, "Hasło", cur.get("DB_PASS") ? "****" : "");
      const name = await ask(rl, "Nazwa bazy", cur.get("DB_NAME"));
      const realPass = pass === "****" ? cur.get("DB_PASS") : pass;
      writeEnvMerge(envPath, { DB_HOST: host, DB_PORT: port, DB_USER: user, DB_PASS: realPass, DB_NAME: name });
      ensureGitignore(".env");
      return { saved: `.env` };
    },
  },
  {
    name: "analytics",
    description: "Google Analytics 4 (raporty, dane ruchu)",
    mcpEntry: () => ({
      command: "bash",
      args: ["scripts/run-google-analytics-mcp.sh"],
      cwd: CWD,
    }),
    async configure(rl) {
      console.log("\n  Google Analytics — wymaga pliku service account JSON.");
      const envPath = path.join(CWD, ".env");
      const cur = readEnvFile(envPath);
      const keyFile = await ask(rl, "Ścieżka do service account JSON", cur.get("GOOGLE_APPLICATION_CREDENTIALS") || "credentials/ga-service-account.json");
      const propertyId = await ask(rl, "GA4 Property ID (np. 123456789)", cur.get("GA4_PROPERTY_ID"));
      writeEnvMerge(envPath, { GOOGLE_APPLICATION_CREDENTIALS: keyFile, GA4_PROPERTY_ID: propertyId });
      return { saved: `.env`, note: `Umieść plik klucza w: ${keyFile}` };
    },
  },
  {
    name: "gsc",
    description: "Google Search Console (indeksowanie, zapytania SEO)",
    mcpEntry: () => ({
      command: "bash",
      args: ["scripts/run-search-console-mcp.sh"],
      cwd: CWD,
    }),
    async configure(rl) {
      console.log("\n  Google Search Console — wymaga pliku service account JSON.");
      const envPath = path.join(CWD, ".env");
      const cur = readEnvFile(envPath);
      const keyFile = await ask(rl, "Ścieżka do service account JSON", cur.get("GSC_CREDENTIALS") || "credentials/gsc-service-account.json");
      const siteUrl = await ask(rl, "Site URL (np. https://example.com)", cur.get("GSC_SITE_URL"));
      writeEnvMerge(envPath, { GSC_CREDENTIALS: keyFile, GSC_SITE_URL: siteUrl });
      return { saved: `.env`, note: `Umieść plik klucza w: ${keyFile}` };
    },
  },
  {
    name: "sentry",
    description: "Sentry — błędy i incydenty produkcyjne",
    mcpEntry: () => ({
      command: "bash",
      args: ["scripts/run-sentry-mcp.sh"],
      cwd: CWD,
    }),
    async configure(rl) {
      console.log("\n  Sentry — token API:");
      const envPath = path.join(CWD, ".env");
      const cur = readEnvFile(envPath);
      const token = await ask(rl, "Sentry Auth Token", cur.get("SENTRY_AUTH_TOKEN") ? "****" : "");
      const org = await ask(rl, "Sentry Organization slug", cur.get("SENTRY_ORG"));
      const realToken = token === "****" ? cur.get("SENTRY_AUTH_TOKEN") : token;
      writeEnvMerge(envPath, { SENTRY_AUTH_TOKEN: realToken, SENTRY_ORG: org });
      ensureGitignore(".env");
      return { saved: `.env` };
    },
  },
  {
    name: "facebook",
    description: "Facebook Pages — posty i komentarze",
    mcpEntry: () => ({
      command: "bash",
      args: ["scripts/run-facebook-mcp.sh"],
      cwd: CWD,
    }),
    async configure(rl) {
      console.log("\n  Facebook — token dostępu do strony:");
      const envPath = path.join(CWD, ".env");
      const cur = readEnvFile(envPath);
      const token = await ask(rl, "Facebook Page Access Token", cur.get("FACEBOOK_PAGE_TOKEN") ? "****" : "");
      const pageId = await ask(rl, "Facebook Page ID", cur.get("FACEBOOK_PAGE_ID"));
      const realToken = token === "****" ? cur.get("FACEBOOK_PAGE_TOKEN") : token;
      writeEnvMerge(envPath, { FACEBOOK_PAGE_TOKEN: realToken, FACEBOOK_PAGE_ID: pageId });
      ensureGitignore(".env");
      return { saved: `.env` };
    },
  },
  {
    name: "memory",
    description: "Trwała pamięć dla agentów AI (lokalny plik JSON)",
    mcpEntry: () => ({
      command: "bash",
      args: ["scripts/run-memory-mcp.sh"],
      cwd: CWD,
    }),
    async configure() {
      return { note: "Brak konfiguracji — gotowe." };
    },
  },
  {
    name: "filesystem",
    description: "Dostęp do plików projektu (read/write) dla AI",
    mcpEntry: () => ({
      command: "bash",
      args: ["scripts/run-filesystem-mcp.sh"],
      cwd: CWD,
    }),
    async configure() {
      return { note: "Brak konfiguracji — gotowe." };
    },
  },
];

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

  try {
    console.log("\n=== Kreator integracji MCP ===");
    console.log(`Katalog projektu: ${CWD}\n`);

    const selected = await selectIntegrations(rl, INTEGRATIONS);
    if (!selected.length) {
      console.log("\nNie wybrano żadnych integracji. Koniec.\n");
      return;
    }

    const hosts = detectHosts();
    console.log(`\nWykryte hosty AI: ${hosts.join(", ")}\n`);

    const results = [];
    for (const integration of selected) {
      console.log(`\n── ${integration.name.toUpperCase()} ──`);
      try {
        const info = await integration.configure(rl);
        // Patch all detected AI host configs
        for (const host of hosts) {
          const mcpPath = hostMcpPath(host);
          if (!mcpPath) continue;
          patchMcpJson(mcpPath, integration.name, integration.mcpEntry());
          console.log(`  ✓ ${host}: ${path.relative(CWD, mcpPath)}`);
        }
        if (info?.saved) console.log(`  ✓ credentials: ${info.saved}`);
        if (info?.note) console.log(`  ℹ  ${info.note}`);
        results.push({ name: integration.name, ok: true });
      } catch (err) {
        console.error(`  ✗ Błąd: ${err.message}`);
        results.push({ name: integration.name, ok: false, error: err.message });
      }
    }

    console.log("\n=== Podsumowanie ===");
    for (const r of results) {
      console.log(`  ${r.ok ? "✓" : "✗"} ${r.name}${r.error ? " — " + r.error : ""}`);
    }
    console.log("\nGotowe! Uruchom ponownie hosta AI, żeby załadował nowe serwery MCP.\n");

  } finally {
    rl.close();
  }
}

main().catch((err) => {
  console.error(`\nBłąd: ${err.message || err}`);
  process.exitCode = 1;
});
