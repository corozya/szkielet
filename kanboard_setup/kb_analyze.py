#!/usr/bin/env python3
import os
import re
import sys
import subprocess

# Ścieżka do Twojego głównego menedżera
KB_MANAGER = "kanboard_setup/kb_manager.py"

def find_backlog_file():
    # Szukamy typowych nazw plików z backlogiem
    candidates = ["BACKLOG.md", "TODO.md", "tasks.md", "docs/plan-projektu.md"]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

def parse_backlog(filepath):
    tasks = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    current_section = "Ogólne"
    for line in lines:
        # Wykrywanie sekcji (jako kategorie/tagi)
        section_match = re.match(r'^#+\s+(.*)', line)
        if section_match:
            current_section = section_match.group(1).strip()
            continue
            
        # Wykrywanie zadań (np. - [ ] Zadanie)
        task_match = re.match(r'^\s*-\s*\[\s*\]\s+(.*)', line)
        if task_match:
            title = task_match.group(1).strip()
            tasks.append({
                "title": title,
                "desc": f"Zadanie zaimportowane z sekcji: {current_section}"
            })
    return tasks

def main():
    project_name = os.path.basename(os.getcwd())
    backlog_file = find_backlog_file()
    
    if not backlog_file:
        print("❌ Nie znaleziono pliku backlogu (BACKLOG.md lub TODO.md).")
        return

    print(f"🔍 Analizuję plik: {backlog_file} dla projektu: {project_name}...")
    tasks = parse_backlog(backlog_file)
    
    if not tasks:
        print("📭 Nie znaleziono nowych zadań do importu (szukam linii zaczynających się od '- [ ]').")
        return

    print(f"Found {len(tasks)} tasks. Starting import to Kanboard...")
    
    for t in tasks:
        print(f"  ➕ Dodaję: {t['title']}...")
        # Wywołujemy kb_manager.py add-task "Projekt" "Tytuł" "Opis"
        subprocess.run([
            "python3", KB_MANAGER, "add-task", project_name, t['title'], t['desc']
        ])

    print("✅ Synchronizacja zakończona!")

if __name__ == "__main__":
    main()
