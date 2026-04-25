#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path


ROLE_CHOICES: list[tuple[str, str]] = [
    ("architecture", "Architektura / decyzje cross-cutting"),
    ("backend", "Backend / API / DB"),
    ("frontend", "Frontend / UI"),
    ("extension", "Browser extension (MV3)"),
    ("integrations", "Integracje / adaptery"),
    ("devops", "DevOps / deploy / CI"),
    ("qa", "QA / test plan / regresja"),
]


def print_usage() -> None:
    print(
        "Komendy:\n"
        "  assign <handoff_dir|brief_path>   # przypisz role/AI do brief.md\n"
        "\n"
        "Przyklady:\n"
        "  python3 kanboard_setup/handoff_manager.py assign handoff/123_fix_login\n"
        "  python3 kanboard_setup/handoff_manager.py assign handoff/123_fix_login/brief.md\n"
    )


def _prompt_choice(prompt: str, default: str = "") -> str:
    if not sys.stdin.isatty():
        return default
    hint = f" [{default}]" if default else ""
    value = input(f"{prompt}{hint}: ").strip()
    return value or default


def prompt_role() -> str:
    if not sys.stdin.isatty():
        return ""
    print("Wybierz rolę:")
    for idx, (role, label) in enumerate(ROLE_CHOICES, start=1):
        print(f"{idx}. {role} — {label}")
    while True:
        raw = input("Rola (numer lub nazwa): ").strip().lower()
        if not raw:
            print("Rola nie może być pusta.")
            continue
        if raw.isdigit():
            i = int(raw)
            if 1 <= i <= len(ROLE_CHOICES):
                return ROLE_CHOICES[i - 1][0]
        for role, _label in ROLE_CHOICES:
            if raw == role:
                return role
        print("Nieznana rola.")


def default_ai_for_role(role: str) -> str:
    role = (role or "").strip().lower()
    env_key = f"AI_ROLE_{role.upper()}"
    env_value = (os.environ.get(env_key) or "").strip()
    if env_value:
        return env_value
    return {
        "architecture": "Claude",
        "backend": "Gemini",
        "frontend": "Codex",
        "extension": "Codex",
        "integrations": "Gemini",
        "devops": "Gemini",
        "qa": "Cursor",
    }.get(role, "")


def default_fallback_for_role(role: str) -> str:
    role = (role or "").strip().lower()
    return {
        "architecture": "Gemini -> Codex -> Cursor",
        "backend": "Claude -> Codex -> Cursor",
        "frontend": "Cursor -> Gemini -> Claude",
        "extension": "Gemini -> Cursor -> Claude",
        "integrations": "Claude -> Codex -> Cursor",
        "devops": "Claude -> Codex -> Cursor",
        "qa": "Codex -> Gemini -> Claude",
    }.get(role, "")


def resolve_brief_path(arg: str) -> Path:
    p = Path(arg)
    if p.is_dir():
        return p / "brief.md"
    return p


def _upsert_field(text: str, field: str, value: str) -> str:
    value = value.strip()
    pattern = re.compile(rf"^\*\*{re.escape(field)}:\*\*.*$", re.MULTILINE)
    line = f"**{field}:** {value}" if value else f"**{field}:**"
    if pattern.search(text):
        return pattern.sub(line, text, count=1)

    # Wstaw po **Kolumna:** jeśli istnieje, inaczej na początku metadanych.
    insert_after = re.search(r"^\*\*Kolumna:\*\*.*$", text, flags=re.MULTILINE)
    if insert_after:
        idx = insert_after.end()
        return text[:idx] + "\n" + line + text[idx:]

    # fallback: po **URL:**
    insert_after = re.search(r"^\*\*URL:\*\*.*$", text, flags=re.MULTILINE)
    if insert_after:
        idx = insert_after.end()
        return text[:idx] + "\n" + line + text[idx:]

    # ostatecznie na górze
    return line + "\n" + text


def assign(target: str) -> int:
    brief_path = resolve_brief_path(target)
    if not brief_path.exists():
        print(f"Brak pliku: {brief_path}")
        return 1

    text = brief_path.read_text(encoding="utf-8")
    role = prompt_role()
    suggested = _prompt_choice("Suggested AI", default_ai_for_role(role))
    fallback = _prompt_choice("Fallback", default_fallback_for_role(role))

    text = _upsert_field(text, "Rola", role)
    text = _upsert_field(text, "Suggested AI", suggested)
    text = _upsert_field(text, "Fallback", fallback)

    brief_path.write_text(text, encoding="utf-8")
    print("OK")
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print_usage()
        return 1

    cmd = sys.argv[1]
    if cmd == "assign":
        if len(sys.argv) < 3:
            print_usage()
            return 1
        return assign(sys.argv[2])

    print_usage()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
