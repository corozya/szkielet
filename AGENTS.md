# 🤖 Project Orchestrator (Main Agent)

Routing: `docs/teams/AI_ROUTING.md`  
Operacje / workflow: `docs/teams/AGENT_GUIDE.md`


---

## 👥 The Expert Team (Roles)

| Agent | Role File | Competency |
|-------|-----------|------------|
| **Architect** | `docs/teams/ARCHITECTURE.md` | High-level design, planning, system-wide logic. |

---

## 📡 Communication Protocol (Handoff)
1. **Generalist** analyzes task -> writes to `handoff/TASK_ID.md`.
2. **Specialists** read their Role File + `handoff/TASK_ID.md`.
3. **Specialists** perform work -> Update `handoff/` status.
4. **Generalist** verifies and closes the task.

---

## 🏛 Operational Standards

### 📍 Source of Truth
1. **Codebase:** The primary source of truth for the application state.
3. **Documentation (`docs/teams/`):** The source of truth for **rules, architecture, and roles**.

### 📦 Repository Management (Git)
- **Commits:** Every Expert Agent is responsible for committing their own changes.
  - *Format:* `feat(scope): brief description` or `fix(scope): brief description`.
- **Finalization & Push:** The **Main Agent (Generalist)** or **DevOps Agent** is responsible for the final push to the repository after task verification.
- **Never Push to Production Directly:** All changes must go through the `beta` environment/tag first (see `DEVOPS.md`).

---

## ⚡ Token Efficiency Mandates (CRITICAL)
- **`rtk` Proxy (automatic):** BeforeTool hook transparently rewrites all terminal commands through `rtk` — no manual prefix needed. Binary: `/home/corozya/.local/bin/rtk`.
  - Meta commands (call directly): `rtk gain` (savings stats), `rtk gain --history`, `rtk discover` (missed savings).
- **Grep before Read:** Never read a whole file to find one thing.
- **No Re-reads:** Do not re-read files already loaded in session unless they changed or exact correctness is required.
- **Surgical Access:** Prefer diffs, slices (line ranges), and symbol-level reads over full-file reads.
- **No Filler:** Direct, technical answers only. Skip conversational filler and restating the user.

---

## 📂 Project Structure (Quick Map)
- `/docs/teams` -> Role definitions & Guides
- `/handoff` -> Active task communication
