#!/usr/bin/env node
/* eslint-disable no-console */
const fs = require("node:fs");
const path = require("node:path");
const readline = require("node:readline/promises");

function safeMkdirp(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function ensureDirNotFile(dirPath) {
  if (!fs.existsSync(dirPath)) return;
  const st = fs.statSync(dirPath);
  if (st.isDirectory()) return;

  const backupPath = `${dirPath}.bak.${Date.now()}`;
  fs.renameSync(dirPath, backupPath);
}

function writeFileIfMissing(filePath, content) {
  if (fs.existsSync(filePath)) return false;
  safeMkdirp(path.dirname(filePath));
  fs.writeFileSync(filePath, content, "utf8");
  return true;
}

function ensureMarkdownSection(filePath, heading, linesToInsert) {
  const headingLine = `## ${heading}`;
  const text = fs.existsSync(filePath) ? fs.readFileSync(filePath, "utf8") : "";
  if (text.includes(headingLine)) return false;

  const insertion = `\n${headingLine}\n\n${linesToInsert.join("\n")}\n`;
  const out = text.trimEnd() + insertion + "\n";
  safeMkdirp(path.dirname(filePath));
  fs.writeFileSync(filePath, out, "utf8");
  return true;
}

function scaffoldAgentSkills(repoRoot) {
  // 1) Skill docs (Gemini / Codex / Cursor)
  const skills = [
    {
      dir: path.join(repoRoot, ".gemini", "skills", "init-kb"),
      file: "SKILL.md",
      // NOTE: keep this string free of unescaped backticks (it lives inside a JS template string).
      content:
        "---\n" +
        "name: init-kb\n" +
        "description: Initializes Kanboard config for this repo (asks for host/user/token/project, writes kanboard_setup/.env, tests connection via getVersion).\n" +
        "---\n" +
        "\n" +
        "# init-kb Skill\n" +
        "\n" +
        "Use when Kanboard configuration is missing or a new developer/environment needs a one-command setup.\n" +
        "\n" +
        "## What it does\n" +
        "- Runs `npm run init-kb` to collect `KANBOARD_URL`, `KANBOARD_USER`, `KANBOARD_TOKEN`, `KANBOARD_PROJECT`\n" +
        "- Writes them to `kanboard_setup/.env` (the source of truth for Kanboard tooling in this repo)\n" +
        "- Tests the JSON-RPC connection by calling `getVersion`\n" +
        "\n" +
        "## Usage\n" +
        "- Interactive:\n" +
        "  - `npm install`\n" +
        "  - `npm run init-kb`\n" +
        "\n" +
        "- Non-interactive (CI / pipe):\n" +
        "  - `node ./bin/init-kb.js --host <HOST> --user <USER> --token <TOKEN> [--project <NAME>] [--no-test]`\n" +
        "  - alias: `--url <JSONRPC_ENDPOINT>`\n" +
        "\n" +
        "## Notes\n" +
        "- Never commit `kanboard_setup/.env` (it contains secrets). Use `kanboard_setup/.env.example` for sharing defaults.\n"
    },
    {
      dir: path.join(repoRoot, ".codex", "skills", "init-kb"),
      file: "SKILL.md",
      content:
        "---\n" +
        "name: init-kb\n" +
        "description: Interactive Kanboard initializer (writes kanboard_setup/.env and tests JSON-RPC via getVersion).\n" +
        "---\n" +
        "\n" +
        "# init-kb Skill (Codex)\n" +
        "\n" +
        "Use when Kanboard credentials/config are missing or a new environment needs setup.\n" +
        "\n" +
        "## Workflow\n" +
        "- Run `npm install` (once per clone)\n" +
        "- Run `npm run init-kb`\n" +
        "- Confirm `kanboard_setup/.env` was created/updated\n" +
        "- Confirm the connection test succeeded (`getVersion`)\n" +
        "\n" +
        "## Non-interactive mode\n" +
        "- `node ./bin/init-kb.js --host <HOST> --user <USER> --token <TOKEN> [--project <NAME>] [--env-path <PATH>] [--no-test]`\n" +
        "- alias: `--url <JSONRPC_ENDPOINT>`\n" +
        "\n" +
        "## Security\n" +
        "- Treat `KANBOARD_TOKEN` as secret.\n" +
        "- Never commit `kanboard_setup/.env` (use `kanboard_setup/.env.example` instead).\n"
    },
    {
      dir: path.join(repoRoot, ".cursor", "skills", "init-kb"),
      file: "SKILL.md",
      content:
        "---\n" +
        "name: init-kb\n" +
        "description: One-command Kanboard setup for this repo (writes kanboard_setup/.env, tests getVersion, enables kb tooling).\n" +
        "---\n" +
        "\n" +
        "# init-kb Skill (Cursor)\n" +
        "\n" +
        "Use this when a developer/agent needs Kanboard access configured for this workspace.\n" +
        "\n" +
        "## What to run\n" +
        "- `npm install`\n" +
        "- `npm run init-kb`\n" +
        "\n" +
        "This writes `kanboard_setup/.env` used by `kanboard_setup/kb_manager.py`.\n" +
        "\n" +
        "## Non-interactive mode\n" +
        "- `node ./bin/init-kb.js --host <HOST> --user <USER> --token <TOKEN> [--project <NAME>] [--no-test]`\n" +
        "- alias: `--url <JSONRPC_ENDPOINT>`\n" +
        "\n" +
        "## Important\n" +
        "- Do not commit `kanboard_setup/.env` (contains secrets).\n"
    },
    {
      dir: path.join(repoRoot, ".gemini", "skills", "kb-backlog-review"),
      file: "SKILL.md",
      content:
        "---\n" +
        "name: kb-backlog-review\n" +
        "description: Fetches Kanboard Backlog, selects top tasks, generates handoff briefs, and summarizes findings.\n" +
        "---\n" +
        "\n" +
        "# kb-backlog-review Skill\n" +
        "\n" +
        "Use when the user asks to review Kanboard tickets/backlog for this repo (e.g. “pobierz zgłoszenia”, “sprawdź zgłoszenia”, “przejrzyj backlog”).\n" +
        "\n" +
        "## Preflight\n" +
        "- If `kanboard_setup/.env` is missing or Kanboard calls fail, run `npm run init-kb` and retry.\n" +
        "\n" +
        "## Commands\n" +
        "- `python3 kanboard_setup/kb_manager.py list \"<KANBOARD_PROJECT>\" Backlog`\n" +
        "- `python3 kanboard_setup/kb_manager.py handoff <ID>`\n" +
        "\n" +
        "## Deliverable\n" +
        "- Fetch and summarize **all** Backlog tasks.\n" +
        "- Generate `handoff` briefs for **all** Backlog tasks (avoid `--force` unless asked).\n"
    },
    {
      dir: path.join(repoRoot, ".codex", "skills", "kb-backlog-review"),
      file: "SKILL.md",
      content:
        "---\n" +
        "name: kb-backlog-review\n" +
        "description: Fetches Kanboard Backlog, selects top tasks, generates handoff briefs, and summarizes findings.\n" +
        "---\n" +
        "\n" +
        "# kb-backlog-review (Codex)\n" +
        "\n" +
        "Use this when the user asks any of: “pobierz zgłoszenia”, “sprawdź zgłoszenia”, “przejrzyj backlog”, “pobierz listę zadań z Kanboard”, “sprawdź co jest w Backlogu”.\n" +
        "\n" +
        "## Preflight (must do before fetching)\n" +
        "1. Check Kanboard config: `kanboard_setup/.env` exists and has `KANBOARD_URL`, `KANBOARD_USER`, `KANBOARD_TOKEN`.\n" +
        "2. If config is missing OR any Kanboard call fails: run `npm install` (if needed) then `npm run init-kb`, and retry.\n" +
        "\n" +
        "## Commands (repo standard)\n" +
        "- List backlog:\n" +
        "  - `python3 kanboard_setup/kb_manager.py list \"<KANBOARD_PROJECT>\" Backlog`\n" +
        "\n" +
        "## Required behavior\n" +
        "- Fetch **all** tasks in Backlog (not just top 3).\n" +
        "- Summarize **each** task (ID + title + 1-line note).\n" +
        "- Generate `handoff` **for all Backlog tasks**:\n" +
        "  - `python3 kanboard_setup/kb_manager.py handoff <ID>`\n" +
        "\n" +
        "## Safety (large backlogs)\n" +
        "- If Backlog is very large, generate handoffs in batches (e.g. 10 at a time) until done.\n" +
        "- If a handoff folder already exists, do not delete it unless explicitly requested (avoid `--force` by default).\n" +
        "\n" +
        "## Expected output\n" +
        "- Handoff folders under `handoff/` for all Backlog tasks (each with `brief.md`)\n" +
        "- A summary covering all tasks.\n"
    },
    {
      dir: path.join(repoRoot, ".cursor", "skills", "kb-backlog-review"),
      file: "SKILL.md",
      content:
        "---\n" +
        "name: kb-backlog-review\n" +
        "description: Fetches Kanboard Backlog, selects top tasks, generates handoff briefs, and summarizes findings.\n" +
        "---\n" +
        "\n" +
        "# kb-backlog-review (Cursor)\n" +
        "\n" +
        "Use when asked to check Kanboard submissions/tickets.\n" +
        "\n" +
        "## Preflight\n" +
        "- If `kanboard_setup/.env` is missing or Kanboard calls fail: run `npm run init-kb` and retry.\n" +
        "\n" +
        "## Commands\n" +
        "- `python3 kanboard_setup/kb_manager.py list \"<KANBOARD_PROJECT>\" Backlog`\n" +
        "- `python3 kanboard_setup/kb_manager.py handoff <ID>`\n" +
        "\n" +
        "## Output\n" +
        "- Briefs in `handoff/` for **all** Backlog tasks + summary of **all** tasks.\n"
    }
  ];

  // Handle pathological case: ".codex" exists as file in some repos.
  ensureDirNotFile(path.join(repoRoot, ".codex"));
  ensureDirNotFile(path.join(repoRoot, ".cursor"));
  ensureDirNotFile(path.join(repoRoot, ".gemini"));

  let createdCount = 0;
  for (const s of skills) {
    const did = writeFileIfMissing(path.join(s.dir, s.file), s.content);
    if (did) createdCount += 1;
  }

  // 2) Lightweight “where is init” breadcrumbs (Claude + Gemini root docs)
  const commonLines = [
    "- Setup: `npm install` → `npm run init-kb`",
    "- Konfiguracja ląduje w `kanboard_setup/.env` (sekrety; nie commitować)"
  ];

  const claudePath = path.join(repoRoot, "CLAUDE.md");
  const geminiPath = path.join(repoRoot, "GEMINI.md");
  const didClaude = ensureMarkdownSection(claudePath, "Kanboard (quick init)", commonLines);
  const didGemini = ensureMarkdownSection(geminiPath, "Kanboard (quick init)", commonLines);

  return { createdCount, didClaude, didGemini };
}

function parseArgs(argv) {
  const out = {
    host: undefined,
    url: undefined,
    user: undefined,
    token: undefined,
    project: undefined,
    envPath: undefined,
    noTest: false
  };

  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--no-test") out.noTest = true;
    else if (a === "--host") out.host = argv[++i];
    else if (a === "--url") out.url = argv[++i];
    else if (a === "--user") out.user = argv[++i];
    else if (a === "--token") out.token = argv[++i];
    else if (a === "--project") out.project = argv[++i];
    else if (a === "--env-path") out.envPath = argv[++i];
    else if (a === "--help" || a === "-h") {
      out.help = true;
    }
  }

  return out;
}

function isNonEmptyString(v) {
  return typeof v === "string" && v.trim().length > 0;
}

function normalizeUrl(input) {
  const raw = String(input || "").trim();
  if (!raw) return "";
  // If user pastes base URL, append /jsonrpc.php
  // If scheme is missing, assume http://
  const withScheme = raw.includes("://") ? raw : `http://${raw}`;
  try {
    const u = new URL(withScheme);
    if (u.pathname === "/" || u.pathname === "") {
      u.pathname = "/jsonrpc.php";
    }
    return u.toString();
  } catch {
    return raw;
  }
}

function baseFromEndpointUrl(input) {
  const raw = String(input || "").trim();
  if (!raw) return "";
  const withScheme = raw.includes("://") ? raw : `http://${raw}`;
  try {
    const u = new URL(withScheme);
    return u.origin;
  } catch {
    return raw;
  }
}

function parseEnvFile(text) {
  const map = new Map();
  const lines = text.split(/\r?\n/);
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const idx = trimmed.indexOf("=");
    if (idx === -1) continue;
    const key = trimmed.slice(0, idx).trim();
    const value = trimmed.slice(idx + 1).trim();
    if (key) map.set(key, value);
  }
  return map;
}

function serializeEnv(map, originalText) {
  // Keep comments/unknown lines; only update/add known keys.
  const keysToEnsure = ["KANBOARD_URL", "KANBOARD_USER", "KANBOARD_TOKEN", "KANBOARD_PROJECT"];
  const existingLines = (originalText || "").split(/\r?\n/);
  const outLines = [];
  const seen = new Set();

  for (const line of existingLines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#") || !trimmed.includes("=")) {
      outLines.push(line);
      continue;
    }

    const idx = trimmed.indexOf("=");
    const key = trimmed.slice(0, idx).trim();
    if (keysToEnsure.includes(key)) {
      outLines.push(`${key}=${map.get(key) ?? ""}`);
      seen.add(key);
    } else {
      outLines.push(line);
    }
  }

  for (const key of keysToEnsure) {
    if (!seen.has(key) && map.has(key)) outLines.push(`${key}=${map.get(key)}`);
  }

  // Always end with newline
  return outLines.join("\n").replace(/\n?$/, "\n");
}

async function jsonRpcCall({ url, user, token, method, params }) {
  const auth = Buffer.from(`${user}:${token}`, "utf8").toString("base64");
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Basic ${auth}`
    },
    body: JSON.stringify({
      jsonrpc: "2.0",
      method,
      id: 1,
      params: params || {}
    })
  });

  const text = await res.text();
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}: ${text.slice(0, 400)}`);
  }

  let body;
  try {
    body = JSON.parse(text);
  } catch {
    throw new Error(`Niepoprawna odpowiedź JSON: ${text.slice(0, 400)}`);
  }

  if (body && body.error) {
    throw new Error(body.error.message || JSON.stringify(body.error));
  }
  return body?.result;
}

async function main() {
  const repoRoot = path.resolve(__dirname, "..");
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    console.log(
      [
        "init-kb — konfiguracja Kanboard dla tego repo",
        "",
        "Tryb interaktywny (zalecany):",
        "  npm run init-kb",
        "",
        "Tryb nieinteraktywny (CI / pipe):",
        "  node ./bin/init-kb.js --host <HOST> --user <USER> --token <TOKEN> [--project <NAME>] [--env-path <PATH>] [--no-test]",
        "  (alias: --url <JSONRPC_ENDPOINT>)",
        "",
        "Zmienne .env:",
        "  KANBOARD_URL, KANBOARD_USER, KANBOARD_TOKEN, KANBOARD_PROJECT",
        ""
      ].join("\n")
    );
    return;
  }

  const envPath = args.envPath
    ? path.resolve(process.cwd(), String(args.envPath))
    : path.join(repoRoot, "kanboard_setup", ".env");
  const envDir = path.dirname(envPath);
  fs.mkdirSync(envDir, { recursive: true });

  const originalText = fs.existsSync(envPath) ? fs.readFileSync(envPath, "utf8") : "";
  const current = parseEnvFile(originalText);

  const isInteractive = Boolean(process.stdin.isTTY);
  if (!isInteractive) {
    // Important: awaiting readline.question doesn't keep the event loop alive with closed stdin.
    const url = normalizeUrl(args.host) || normalizeUrl(args.url) || current.get("KANBOARD_URL") || "";
    const user = String(args.user || current.get("KANBOARD_USER") || "").trim();
    const token = String(args.token || current.get("KANBOARD_TOKEN") || "").trim();
    const project = String(args.project || current.get("KANBOARD_PROJECT") || "").trim();

    if (!isNonEmptyString(url) || !isNonEmptyString(user) || !isNonEmptyString(token)) {
      throw new Error(
        "Brak interaktywnego TTY. Podaj flagi: --host (lub --url) --user --token (opcjonalnie --project / --env-path)."
      );
    }

    if (!args.noTest) {
      console.log("Test połączenia...");
      const version = await jsonRpcCall({ url, user, token, method: "getVersion" });
      console.log(`OK: Kanboard getVersion = ${String(version)}`);
    }

    const next = new Map(current);
    next.set("KANBOARD_URL", url);
    next.set("KANBOARD_USER", user);
    next.set("KANBOARD_TOKEN", token);
    next.set("KANBOARD_PROJECT", project);

    const outText = serializeEnv(next, originalText);
    fs.writeFileSync(envPath, outText, "utf8");
    console.log(`Zapisano: ${path.relative(repoRoot, envPath)}`);
    const scaff = scaffoldAgentSkills(repoRoot);
    if (scaff.createdCount || scaff.didClaude || scaff.didGemini) {
      console.log(
        `Zaktualizowano skills/docs: created_skills=${scaff.createdCount}, CLAUDE.md=${scaff.didClaude ? "yes" : "no"}, GEMINI.md=${scaff.didGemini ? "yes" : "no"}`
      );
    }
    return;
  }

  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  try {
    console.log("");
    console.log("init-kb: konfiguracja Kanboard (kanboard_setup/.env)");
    console.log("");

    const defaultEndpoint = current.get("KANBOARD_URL") || "http://127.0.0.1:8080/jsonrpc.php";
    const defaultHost = baseFromEndpointUrl(defaultEndpoint) || "http://127.0.0.1:8080";
    const defaultUser = current.get("KANBOARD_USER") || "jsonrpc";
    const defaultProject = current.get("KANBOARD_PROJECT") || "";

    const hostInput = await rl.question(`Host Kanboard (base URL) [${defaultHost}]: `);
    const url = normalizeUrl(hostInput) || defaultEndpoint;
    if (!isNonEmptyString(url)) throw new Error("KANBOARD_URL nie może być puste.");

    const userInput = await rl.question(`Użytkownik API [${defaultUser}]: `);
    const user = (userInput || defaultUser).trim();
    if (!isNonEmptyString(user)) throw new Error("KANBOARD_USER nie może być puste.");

    let token = (current.get("KANBOARD_TOKEN") || "").trim();
    if (!token) {
      token = (await rl.question("Token API (KANBOARD_TOKEN): ")).trim();
    } else {
      const reuse = (await rl.question("Znaleziono KANBOARD_TOKEN w .env — użyć istniejącego? [Y/n]: ")).trim();
      if (reuse.toLowerCase() === "n" || reuse.toLowerCase() === "no") {
        token = (await rl.question("Token API (KANBOARD_TOKEN): ")).trim();
      }
    }
    if (!isNonEmptyString(token)) throw new Error("KANBOARD_TOKEN nie może być puste.");

    const projectInput = await rl.question(`Nazwa projektu (KANBOARD_PROJECT) [${defaultProject || "puste"}]: `);
    const project = projectInput.trim() || defaultProject;

    const next = new Map(current);
    next.set("KANBOARD_URL", url);
    next.set("KANBOARD_USER", user);
    next.set("KANBOARD_TOKEN", token);
    next.set("KANBOARD_PROJECT", project);

    if (!args.noTest) {
      console.log("");
      console.log("Test połączenia...");
      const version = await jsonRpcCall({ url, user, token, method: "getVersion" });
      console.log(`OK: Kanboard getVersion = ${String(version)}`);
    }

    const outText = serializeEnv(next, originalText);
    fs.writeFileSync(envPath, outText, "utf8");
    console.log("");
    console.log(`Zapisano: ${path.relative(repoRoot, envPath)}`);
    const scaff = scaffoldAgentSkills(repoRoot);
    if (scaff.createdCount || scaff.didClaude || scaff.didGemini) {
      console.log(
        `Zaktualizowano skills/docs: created_skills=${scaff.createdCount}, CLAUDE.md=${scaff.didClaude ? "yes" : "no"}, GEMINI.md=${scaff.didGemini ? "yes" : "no"}`
      );
    }
    console.log("Gotowe. Możesz używać narzędzi w kanboard_setup/ (np. kb_manager.py).");
    console.log("");
  } finally {
    rl.close();
  }
}

main().catch((err) => {
  console.error("");
  console.error(`Błąd init-kb: ${err && err.message ? err.message : String(err)}`);
  process.exitCode = 1;
});

