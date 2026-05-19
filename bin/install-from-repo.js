#!/usr/bin/env node
/* eslint-disable no-console */
"use strict";

const fs = require("node:fs");
const path = require("node:path");
const readline = require("node:readline/promises");

const CWD = process.cwd();
const MANIFEST_FILE = "scaffold-manifest.json";

// ---------------------------------------------------------------------------
// GitHub helpers (zero deps — Node 18+ fetch)
// ---------------------------------------------------------------------------

function parseRepoUrl(input) {
  const s = input.trim().replace(/\.git$/, "");
  // "owner/repo"
  if (/^[^/]+\/[^/]+$/.test(s)) {
    const [owner, repo] = s.split("/");
    return { owner, repo, branch: "main" };
  }
  // "https://github.com/owner/repo"
  try {
    const u = new URL(s.includes("://") ? s : `https://${s}`);
    if (u.hostname === "github.com") {
      const parts = u.pathname.replace(/^\//, "").split("/");
      if (parts.length >= 2) {
        return { owner: parts[0], repo: parts[1], branch: "main" };
      }
    }
  } catch {}
  return null;
}

async function fetchRaw(owner, repo, branch, filePath, token) {
  const url = `https://raw.githubusercontent.com/${owner}/${repo}/${branch}/${filePath}`;
  const headers = { "User-Agent": "scaffold-installer" };
  if (token) headers["Authorization"] = `token ${token}`;
  const res = await fetch(url, { headers });
  if (res.status === 404) throw new Error(`Plik nie znaleziony: ${filePath} (branch: ${branch})`);
  if (!res.ok) throw new Error(`HTTP ${res.status} dla ${filePath}`);
  return res.text();
}

async function fetchManifest(owner, repo, token) {
  // Try main then master
  for (const branch of ["main", "master"]) {
    try {
      const text = await fetchRaw(owner, repo, branch, MANIFEST_FILE, token);
      return { manifest: JSON.parse(text), branch };
    } catch (e) {
      if (!e.message.includes("nie znaleziony") && !e.message.includes("404")) throw e;
    }
  }
  throw new Error(`Nie znaleziono ${MANIFEST_FILE} w repo (sprawdzono gałęzie main i master).`);
}

// ---------------------------------------------------------------------------
// Filesystem helpers
// ---------------------------------------------------------------------------

function readEnvFile(envPath) {
  const map = new Map();
  if (!fs.existsSync(envPath)) return map;
  for (const line of fs.readFileSync(envPath, "utf8").split(/\r?\n/)) {
    const t = line.trim();
    if (!t || t.startsWith("#") || !t.includes("=")) continue;
    const idx = t.indexOf("=");
    map.set(t.slice(0, idx).trim(), t.slice(idx + 1).trim());
  }
  return map;
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

// ---------------------------------------------------------------------------
// Interactive helpers
// ---------------------------------------------------------------------------

function ask(rl, question, defaultVal) {
  const hint = defaultVal ? ` [${defaultVal}]` : "";
  return rl.question(`  ${question}${hint}: `).then((a) => a.trim() || defaultVal || "");
}

async function selectIntegrations(rl, integrations) {
  console.log("\nDostępne integracje:\n");
  integrations.forEach((i, idx) => {
    const badge = i.type === "mcp" ? "[MCP]" : i.type === "agent" ? "[Agent]" : "[Workflow]";
    console.log(`  ${String(idx + 1).padStart(2)}. ${badge.padEnd(10)} ${i.name.padEnd(20)} — ${i.description}`);
  });
  console.log("\nWybierz numery (np. 1,3) lub 'all':");
  const input = (await rl.question("  > ")).trim();
  if (input.toLowerCase() === "all") return integrations;
  return input
    .split(/[,\s]+/)
    .map((s) => parseInt(s, 10) - 1)
    .filter((n) => !isNaN(n) && n >= 0 && n < integrations.length)
    .map((n) => integrations[n])
    .filter((v, i, a) => a.indexOf(v) === i);
}

// ---------------------------------------------------------------------------
// Install logic
// ---------------------------------------------------------------------------

async function installIntegration(integration, { owner, repo, branch, token, rl, hosts, forceOverwrite }) {
  const results = { files: [], skipped: [], errors: [] };

  // Download files
  for (const filePath of integration.files || []) {
    const destPath = path.join(CWD, filePath);
    const exists = fs.existsSync(destPath);

    if (exists && !forceOverwrite) {
      const ans = await ask(rl, `${filePath} już istnieje. Nadpisać?`, "n");
      if (ans.toLowerCase() !== "y" && ans.toLowerCase() !== "tak") {
        results.skipped.push(filePath);
        continue;
      }
    }

    try {
      const content = await fetchRaw(owner, repo, branch, filePath, token);
      fs.mkdirSync(path.dirname(destPath), { recursive: true });
      fs.writeFileSync(destPath, content, "utf8");
      results.files.push(filePath);
    } catch (e) {
      results.errors.push(`${filePath}: ${e.message}`);
    }
  }

  // Patch MCP configs for mcp-type integrations
  if (integration.type === "mcp" && integration.mcp_entry) {
    for (const host of hosts) {
      const mcpPath = hostMcpPath(host);
      if (!mcpPath) continue;
      patchMcpJson(mcpPath, integration.id, integration.mcp_entry);
      console.log(`    ✓ Dodano do ${host}: ${path.relative(CWD, mcpPath)}`);
    }
  }

  // Agent type — copy to agents/ and optionally patch skill files
  if (integration.type === "agent") {
    console.log(`    ℹ  Agent zainstalowany w: ${(integration.files || []).join(", ")}`);
    console.log(`    ℹ  Uruchom: /agent ${integration.id.replace("-agent", "")} (jeśli masz skill)`);
  }

  return results;
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

  try {
    console.log("\n=== Instalator ze zdalnego repo ===\n");

    // Read optional GITHUB_TOKEN from .env
    const localEnv = readEnvFile(path.join(CWD, ".env"));
    const token = localEnv.get("GITHUB_TOKEN") || process.env.GITHUB_TOKEN || "";

    // Get repo URL
    const repoInput = await ask(rl, "URL repozytorium GitHub (np. owner/repo lub https://github.com/owner/repo)");
    if (!repoInput) { console.log("Anulowano."); return; }

    const parsed = parseRepoUrl(repoInput);
    if (!parsed) {
      console.error("  ✗ Nie można sparsować URL repozytorium.");
      process.exitCode = 1;
      return;
    }

    console.log(`\n  Pobieranie manifestu z ${parsed.owner}/${parsed.repo}...`);
    const { manifest, branch } = await fetchManifest(parsed.owner, parsed.repo, token || undefined);
    parsed.branch = branch;

    console.log(`  ✓ ${manifest.name} — ${manifest.description}`);

    if (!manifest.integrations?.length) {
      console.log("  Brak dostępnych integracji w tym repo.");
      return;
    }

    const selected = await selectIntegrations(rl, manifest.integrations);
    if (!selected.length) { console.log("\nNie wybrano niczego. Koniec."); return; }

    const hosts = detectHosts();
    console.log(`\n  Wykryte hosty AI: ${hosts.join(", ")}`);

    const forceAns = await ask(rl, "Nadpisać istniejące pliki bez pytania?", "n");
    const forceOverwrite = forceAns.toLowerCase() === "y" || forceAns.toLowerCase() === "tak";

    const summary = [];
    for (const integration of selected) {
      console.log(`\n── ${integration.name} (${integration.type}) ──`);
      const r = await installIntegration(integration, {
        owner: parsed.owner, repo: parsed.repo, branch, token: token || undefined,
        rl, hosts, forceOverwrite,
      });
      if (r.files.length) console.log(`  ✓ Pobrano: ${r.files.join(", ")}`);
      if (r.skipped.length) console.log(`  ⤼  Pominięto: ${r.skipped.join(", ")}`);
      if (r.errors.length) r.errors.forEach((e) => console.error(`  ✗ ${e}`));
      if (integration.setup_cmd) console.log(`  → Uruchom teraz: ${integration.setup_cmd}`);
      if (integration.python_deps?.length) {
        console.log(`  → Zainstaluj Python deps: pip install ${integration.python_deps.join(" ")}`);
      }
      summary.push({ name: integration.name, files: r.files.length, errors: r.errors.length });
    }

    console.log("\n=== Podsumowanie ===");
    for (const s of summary) {
      const status = s.errors ? "⚠ " : "✓";
      console.log(`  ${status} ${s.name} — ${s.files} plików`);
    }
    console.log("\nUruchom ponownie hosta AI, żeby załadował nowe MCP serwery.\n");

  } finally {
    rl.close();
  }
}

main().catch((err) => {
  console.error(`\nBłąd: ${err.message || err}`);
  process.exitCode = 1;
});
