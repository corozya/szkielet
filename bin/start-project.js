#!/usr/bin/env node
/* eslint-disable no-console */
const fs = require("node:fs");
const path = require("node:path");
const readline = require("node:readline/promises");
const { spawnSync } = require("node:child_process");

function run(cmd, args, opts = {}) {
  const r = spawnSync(cmd, args, {
    stdio: "inherit",
    ...opts
  });
  if (r.status !== 0) {
    throw new Error(`Command failed: ${cmd} ${args.join(" ")}`);
  }
}

function parseRepoNameFromUrl(url) {
  const raw = String(url || "").trim();
  if (!raw) return "";
  // Supports https://host/org/repo(.git), git@host:org/repo(.git)
  const cleaned = raw.replace(/[#?].*$/, "").replace(/\/+$/, "");
  const last = cleaned.split("/").pop() || "";
  return last.replace(/\.git$/i, "");
}

function ensureAppsGitignored(repoRoot) {
  const gitignorePath = path.join(repoRoot, ".gitignore");
  const line = "apps/";
  const existing = fs.existsSync(gitignorePath) ? fs.readFileSync(gitignorePath, "utf8") : "";
  if (existing.split(/\r?\n/).some((l) => l.trim() === line)) return false;
  const out = existing.trimEnd() + (existing.trimEnd() ? "\n" : "") + line + "\n";
  fs.writeFileSync(gitignorePath, out, "utf8");
  return true;
}

async function main() {
  const repoRoot = path.resolve(__dirname, "..");
  const appsRoot = path.join(repoRoot, "apps");
  fs.mkdirSync(appsRoot, { recursive: true });

  const changed = ensureAppsGitignored(repoRoot);
  if (changed) {
    console.log("Dodano `apps/` do .gitignore (żeby nie commitować repo aplikacji).");
  }

  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const attached = [];

  try {
    console.log("");
    console.log("start-project: podłącz repozytoria do apps/ + init-kb");
    console.log("");

    while (true) {
      const url = (await rl.question("URL repo do podłączenia (puste = koniec): ")).trim();
      if (!url) break;

      const repoName = parseRepoNameFromUrl(url);
      if (!repoName) throw new Error("Nie umiem wyciągnąć nazwy repo z URL.");

      const target = path.join(appsRoot, repoName);
      if (fs.existsSync(target)) {
        throw new Error(`Katalog już istnieje: ${path.relative(repoRoot, target)} (nie nadpisuję).`);
      }

      console.log(`\nKlonuję → ${path.relative(repoRoot, target)}\n`);
      run("git", ["clone", "--branch", "main", url, target], { cwd: repoRoot });
      attached.push({ url, target });
      console.log("");
    }
  } finally {
    rl.close();
  }

  console.log("");
  console.log("Uruchamiam init-kb (zawsze)...");
  console.log("");
  run("npm", ["run", "-s", "init-kb"], { cwd: repoRoot });

  console.log("");
  console.log("Gotowe.");
  if (attached.length) {
    console.log("Podłączone repo:");
    for (const a of attached) {
      console.log(`- ${a.url} -> ${path.relative(repoRoot, a.target)}`);
    }
  } else {
    console.log("Nie podłączono żadnego repo (pominąłeś klonowanie).");
  }
  console.log("");
}

main().catch((err) => {
  console.error("");
  console.error(`Błąd start-project: ${err && err.message ? err.message : String(err)}`);
  process.exitCode = 1;
});

