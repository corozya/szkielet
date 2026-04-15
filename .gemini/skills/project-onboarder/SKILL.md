---
name: project-onboarder
description: Onboards new projects by conducting an interview and updating core configuration files (GEMINI.md, CLAUDE.md, COMMON.md). Use when you need to initialize or update the project context for agents.
---

# Project Onboarder Skill

This skill guides you through the process of onboarding a new project by proactively analyzing requirements, proposing a tech stack, and updating the project's orchestration documents.

## 🚀 Workflow

### 1. Proactive Analysis & Interview
- **Analyze First**: Before asking questions, scan the workspace for existing configuration files (e.g., `package.json`, `composer.json`, `Cargo.toml`, `requirements.txt`, `.env`).
- **Propose Stack**: Based on the scan or user assumptions, formulate a proposed tech stack (Backend, Frontend, DB, Tools).
- **The Interview**: Present the proposed stack to the user for confirmation. Use [references/questions.md](references/questions.md) only to fill in the gaps or if the analysis is inconclusive.
- **Tip**: If you need more details to make a decision, ask specific, targeted questions.

### 2. Identify Files to Update
The standard files that MUST be updated are:
- `GEMINI.md`: Updates the "Project Structure" and "AI Identity".
- `CLAUDE.md`: Ensures consistency across agents.
- `docs/teams/COMMON.md`: Updates project-specific standards if needed.
- `docs/teams/AGENT_GUIDE.md`: (Optional) Update or create this file for ticket-based workflows.

### 3. Apply Updates (Surgical Editing)
Use the `replace` tool to perform surgical updates on existing files. 
- **GEMINI.md**: Replace placeholders like `[MAIN_MODULE_PATH]` and `[DESCRIPTION]` with real data derived from your analysis.
- **CLAUDE.md**: Ensure the `Role` and `Core Rules` sections match the confirmed project context.
- **COMMON.md**: Update the "Operational Standards" and "Repository Management" based on the detected environment.

### 4. Documentation Polish
Ensure all updated documentation is visually consistent and technically accurate. Offer to generate a `README.md` if it's missing.

## 🛠 Guidelines
- **Consistency**: Maintain the existing visual style (emojis, markdown structure).
- **Security**: NEVER ask for or save secrets/API keys. Remind the user to use `.env` files.
- **Verification**: After updating the files, summarize the changes and ask the user to verify.

## 📖 References
- [questions.md](references/questions.md): The standard onboarding interview questionnaire.
