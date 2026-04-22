#!/usr/bin/env python3
import json
import os
import re
import sys
import shutil
from base64 import b64encode
from pathlib import Path

import requests


_env_file = Path(__file__).parent / ".env"
if _env_file.exists():
    for _line in _env_file.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _key, _value = _line.split("=", 1)
            os.environ.setdefault(_key.strip(), _value.strip())


URL = os.environ.get("KANBOARD_URL", "http://192.168.0.170:8080/jsonrpc.php")
USER = os.environ.get("KANBOARD_USER", "jsonrpc")
TOKEN = os.environ.get("KANBOARD_TOKEN")
DEFAULT_PROJECT = os.environ.get("KANBOARD_PROJECT", "WorksOnMine")


class KanboardAgent:
    def __init__(self, url: str, user: str, token: str | None):
        if not token:
            raise ValueError("Brak KANBOARD_TOKEN (ustaw zmienna srodowiskowa).")

        self.url = url
        auth = f"{user}:{token}"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {b64encode(auth.encode()).decode()}",
        }
        self._project_ids: dict[str, int] = {}
        self._columns_by_project: dict[int, list[dict]] = {}

    def _call(self, method: str, params: dict | None = None):
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "id": 1,
            "params": params or {},
        }

        try:
            response = requests.post(self.url, headers=self.headers, json=payload, timeout=10)
            response.raise_for_status()
            body = response.json()
            if "error" in body:
                raise Exception(body["error"]["message"])
            return body.get("result")
        except Exception as exc:
            raise Exception(f"Blad polaczenia: {exc}") from exc

    def _project_cache_key(self, project_ref: str | int) -> str:
        return str(project_ref).strip().lower()

    def get_project_id(self, project_ref: str | int) -> int | None:
        if isinstance(project_ref, int) or str(project_ref).isdigit():
            return int(project_ref)

        cache_key = self._project_cache_key(project_ref)
        if cache_key in self._project_ids:
            return self._project_ids[cache_key]

        projects = self._call("getAllProjects") or []
        for project in projects:
            if project.get("name", "").strip().lower() == cache_key:
                project_id = int(project["id"])
                self._project_ids[cache_key] = project_id
                return project_id
        return None

    def get_project_name(self, project_ref: str | int) -> str | None:
        project_id = self.get_project_id(project_ref)
        if not project_id:
            return None

        projects = self._call("getAllProjects") or []
        for project in projects:
            if int(project.get("id", 0)) == project_id:
                return project.get("name")
        return None

    def _columns_for_project(self, project_id: int) -> list[dict]:
        if project_id not in self._columns_by_project:
            self._columns_by_project[project_id] = self._call("getColumns", {"project_id": project_id}) or []
        return self._columns_by_project[project_id]

    def _resolve_column_id(self, project_id: int, column_ref: str | int | None) -> int | None:
        if column_ref is None or column_ref == "":
            return None

        if isinstance(column_ref, int) or str(column_ref).isdigit():
            return int(column_ref)

        columns = self._columns_for_project(project_id)
        column_key = str(column_ref).strip().lower()
        for column in columns:
            if column.get("title", "").strip().lower() == column_key:
                return int(column["id"])
        return None

    def create_project(self, project_name: str) -> int:
        project_id = self.get_project_id(project_name)
        if project_id:
            return project_id

        project_id = int(self._call("createProject", {"name": project_name}))
        try:
            user = self._call("getUserByName", {"username": "admin"})
            if user:
                self._call(
                    "addProjectUser",
                    {"project_id": project_id, "user_id": int(user["id"]), "role": "project-manager"},
                )
        except Exception:
            pass
        return project_id

    def add_task(self, project_name: str, title: str, description: str = ""):
        project_id = self.get_project_id(project_name)
        if not project_id:
            raise Exception(f"Projekt {project_name} nie istnieje.")
        return self._call(
            "createTask",
            {"title": title, "project_id": project_id, "description": description},
        )

    def add_comment(self, task_id: str | int, content: str):
        return self._call("createComment", {"task_id": int(task_id), "user_id": 1, "content": content})

    def get_task(self, task_id: str | int):
        return self._call("getTask", {"task_id": int(task_id)})

    def remove_task(self, task_id: str | int):
        return self._call("removeTask", {"task_id": int(task_id)})

    def list_tasks(self, project_ref: str | int, column_ref: str | int | None = None):
        project_id = self.get_project_id(project_ref)
        if not project_id:
            return []

        tasks = self._call("getAllTasks", {"project_id": project_id}) or []
        column_id = self._resolve_column_id(project_id, column_ref)

        if column_ref not in (None, "") and column_id is None:
            available = ", ".join(column.get("title", "") for column in self._columns_for_project(project_id))
            raise Exception(f"Kolumna '{column_ref}' nie istnieje. Dostepne: {available}")

        if column_ref not in (None, ""):
            tasks = [task for task in tasks if int(task.get("column_id", 0)) == column_id]

        return [
            {
                "id": task["id"],
                "title": task.get("title", f"Task #{task['id']}"),
                "column_id": task.get("column_id"),
            }
            for task in tasks
        ]

    def get_task_files(self, task_id: str | int) -> list[dict]:
        return self._call("getAllTaskFiles", {"task_id": int(task_id)}) or []

    def get_task_file_blob(self, file_id: str | int) -> bytes:
        b64 = self._call("downloadTaskFile", {"file_id": int(file_id)}) or ""
        from base64 import b64decode
        return b64decode(b64)

    def move_task(self, task_id: str | int, column_ref: str | int):
        task = self.get_task(task_id)
        project_id = int(task["project_id"])
        column_id = self._resolve_column_id(project_id, column_ref)

        if not column_id:
            available = ", ".join(column.get("title", "") for column in self._columns_for_project(project_id))
            raise Exception(f"Kolumna '{column_ref}' nie istnieje. Dostepne: {available}")

        return self._call(
            "moveTaskPosition",
            {
                "project_id": project_id,
                "task_id": int(task_id),
                "column_id": column_id,
                "position": 1,
                "swimlane_id": int(task.get("swimlane_id", 1)),
            },
        )

    def claim_tasks(
        self,
        project_ref: str | int = DEFAULT_PROJECT,
        column_ref: str | int | None = "Backlog",
        limit: int = 1,
    ):
        claimed = []
        tasks = self.list_tasks(project_ref, column_ref)

        for task_summary in tasks[: max(limit, 0)]:
            task = self.get_task(task_summary["id"])
            task_files = self.get_task_files(task["id"])
            handoff_path = write_handoff(task, task_files=task_files, agent=self)
            self.move_task(task["id"], "Work in Progress")
            claimed.append((int(task["id"]), handoff_path))

        return claimed


def print_usage() -> None:
    print(
        "Dostepne komendy: list, show, handoff, claim, move\n"
        "handoff <id> [--force]\n"
        "Legacy aliasy: init, add-task, comment"
    )


def print_list(tasks: list[dict]) -> None:
    for task in tasks:
        print(f"{task['id']}\t{task['title']}")


def print_task(task: dict) -> None:
    print(json.dumps(task, ensure_ascii=False, separators=(",", ":")))


def slugify(text: str, max_length: int = 80) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return slug[:max_length] or "task"


def _format_console_logs(console_logs: list[dict], limit: int = 20) -> list[str]:
    lines = []
    for log in console_logs[:limit]:
        log_type = log.get("type") or log.get("level") or "log"
        msg = log.get("msg") or log.get("message") or ""
        lines.append(f"- [{log_type}] {msg}")
    if len(console_logs) > limit:
        lines.append(f"- ... i jeszcze {len(console_logs) - limit} wpisów")
    return lines


def _format_network_logs(network_logs: list[dict], limit: int = 10) -> list[str]:
    lines = []
    for log in network_logs[:limit]:
        method = log.get("method") or "GET"
        url = log.get("url") or ""
        status = log.get("status") or ""
        duration = f" ({log['duration']}ms)" if log.get("duration") is not None else ""
        lines.append(f"- [{method}] {url} -> {status}{duration}")
    if len(network_logs) > limit:
        lines.append(f"- ... i jeszcze {len(network_logs) - limit} wpisów")
    return lines


def _format_task_files(task_files: list[dict], limit: int = 20) -> list[str]:
    lines = []
    for task_file in task_files[:limit]:
        if not isinstance(task_file, dict):
            continue
        file_id = task_file.get("id") or task_file.get("file_id") or ""
        name = (
            task_file.get("name")
            or task_file.get("filename")
            or task_file.get("file_name")
            or (f"Plik #{file_id}" if file_id else "Plik bez nazwy")
        )
        size = task_file.get("size") or task_file.get("filesize")
        url = task_file.get("url") or task_file.get("link") or task_file.get("download_url")
        path = task_file.get("path") or task_file.get("file_path")

        details = []
        if size is not None:
            details.append(f"{size} B")
        if file_id:
            details.append(f"id={file_id}")
        if path:
            details.append(f"path={path}")

        suffix = f" ({', '.join(details)})" if details else ""
        if url:
            lines.append(f"- {name}{suffix}: {url}")
        else:
            lines.append(f"- {name}{suffix}")

    if len(task_files) > limit:
        lines.append(f"- ... i jeszcze {len(task_files) - limit} plików")
    return lines


def _task_file_url(task_file: dict) -> str:
    if not isinstance(task_file, dict):
        return ""
    return task_file.get("url") or task_file.get("link") or task_file.get("download_url") or ""


def _looks_like_image(task_file: dict) -> bool:
    if not isinstance(task_file, dict):
        return False
    mime_type = str(task_file.get("mime_type") or task_file.get("mimetype") or "").lower()
    if mime_type.startswith("image/"):
        return True

    name = str(
        task_file.get("name")
        or task_file.get("filename")
        or task_file.get("file_name")
        or ""
    ).lower()
    return name.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg"))


def _pick_screenshot_reference(task_files: list[dict]) -> str:
    for task_file in task_files:
        if not isinstance(task_file, dict):
            continue
        if _looks_like_image(task_file):
            name = (
                task_file.get("name")
                or task_file.get("filename")
                or task_file.get("file_name")
                or ""
            )
            path = task_file.get("path") or task_file.get("file_path")
            if path:
                return f"{name} (KB path: {path})" if name else f"KB path: {path}"
            return _task_file_url(task_file) or name
    return ""


def _task_file_name(task_file: dict) -> str:
    if not isinstance(task_file, dict):
        return "file_unknown"
    return str(
        task_file.get("name")
        or task_file.get("filename")
        or task_file.get("file_name")
        or f"file_{task_file.get('id') or task_file.get('file_id') or 'unknown'}"
    )


def _safe_filename(name: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "_", name).strip("._-")
    return cleaned or "file"


def _download_task_files(
    agent: KanboardAgent,
    task_id: str | int,
    task_files: list[dict],
    assets_dir: Path,
) -> list[dict]:
    assets_dir.mkdir(parents=True, exist_ok=True)
    downloaded = []

    for task_file in task_files:
        if not isinstance(task_file, dict):
            downloaded.append({"local_path": ""})
            continue
        file_id = task_file.get("id") or task_file.get("file_id")
        if not file_id:
            downloaded.append({**task_file, "local_path": ""})
            continue

        source_name = _task_file_name(task_file)
        base_name = _safe_filename(source_name)
        suffix = Path(source_name).suffix
        if suffix and not Path(base_name).suffix:
            base_name += suffix

        local_path = assets_dir / f"{task_id}_{file_id}_{base_name}"
        if not local_path.exists():
            local_path.write_bytes(agent.get_task_file_blob(file_id))

        downloaded.append({**task_file, "local_path": str(local_path)})

    return downloaded


def _split_user_actions(description: str) -> tuple[str, str, int]:
    text = (description or "").strip()
    marker = "\n**User Actions:**\n"
    if marker not in text:
        return text, "", 0

    head, tail = text.split(marker, 1)
    user_actions_block = tail.strip()
    action_count = sum(1 for line in user_actions_block.splitlines() if line.lstrip().startswith("- ["))
    return head.rstrip(), user_actions_block, action_count


def _write_text_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _summarize_text(text: str, max_length: int = 160) -> str:
    compact = " ".join((text or "").split())
    if len(compact) <= max_length:
        return compact
    return compact[: max_length - 1].rstrip() + "…"


def _extract_device_info(text: str) -> list[str]:
    lines = (text or "").splitlines()
    device_info = []
    in_section = False

    for line in lines:
        stripped = line.strip()
        if stripped == "**Device Info:**":
            in_section = True
            continue
        if in_section and stripped.startswith("**") and stripped.endswith(":**") and stripped != "**Device Info:**":
            break
        if in_section and stripped.startswith("- "):
            entry = stripped[2:].strip()
            if entry.startswith("URL:"):
                device_info.append(entry)
            elif entry.startswith("Viewport:"):
                device_info.append(entry)
            elif entry.startswith("Browser:"):
                device_info.append(entry)
            elif entry.startswith("Language:"):
                device_info.append(entry)
    return device_info


def build_handoff_markdown(
    task: dict,
    task_files: list[dict] | None = None,
    user_actions_path: Path | None = None,
    source_path: Path | None = None,
) -> str:
    task_id = task.get("id", "")
    title = task.get("title", f"Task #{task_id}")
    description = (task.get("description") or "").strip()
    description, user_actions_block, user_actions_count = _split_user_actions(description)
    device_info_lines = _extract_device_info(description)
    url = task.get("url", "")
    column_id = task.get("column_id", "")
    screenshot_url = task.get("screenshot_url", "") or _pick_screenshot_reference(task_files or [])
    console_logs = task.get("console_logs") or []
    network_logs = task.get("network_logs") or []
    task_files = task_files or []

    console_log_lines = _format_console_logs(console_logs)
    network_log_lines = _format_network_logs(network_logs)
    task_file_lines = _format_task_files(task_files)
    local_path_lines = [
        f"- {task_file['local_path']}"
        for task_file in task_files
        if isinstance(task_file, dict) and task_file.get("local_path")
    ]
    environment_lines = [f"- {line}" for line in device_info_lines] if device_info_lines else ["- brak"]
    user_actions_note = (
        f"- User Actions: {user_actions_count} kroków ({user_actions_path})"
        if user_actions_count
        else "- User Actions: brak"
    )
    description_summary = _summarize_text(description or "_Brak opisu_")

    return "\n".join([
        f"# {task_id}_{title}",
        "",
        "**Status:** Do zrobienia",
        f"**KB:** #{task_id}",
        f"**URL:** {url}" if url else "**URL:**",
        f"**Kolumna:** {column_id}" if column_id != "" else "**Kolumna:**",
        "",
        "## Start",
        "- Najpierw przeanalizuj zgłoszenie i powiązany kod.",
        "- Nie analizuj logów ani screenshotów automatycznie; sprawdzaj je tylko, gdy opis sugeruje problem w UI, renderowaniu albo konsoli.",
        "- Jeśli opis jest niejasny lub brakuje danych, najpierw dopytaj użytkownika.",
        "- Nie zaczynaj implementacji, dopóki zakres nie jest jasny.",
        "",
        "## Środowisko",
        *environment_lines,
        "",
        "## Opis",
        description_summary,
        "",
        "## Załączniki",
        f"- Screenshot: {screenshot_url}" if screenshot_url else "- Screenshot: brak",
        f"- Logi konsoli: {len(console_logs)} wpisów" if console_logs else "- Logi konsoli: brak",
        f"- Logi sieciowe: {len(network_logs)} wpisów" if network_logs else "- Logi sieciowe: brak",
        user_actions_note,
        "- Pliki z KB:",
        *(task_file_lines if task_file_lines else ["- brak"]),
        "- Lokalne pliki:",
        *(local_path_lines if local_path_lines else ["- brak"]),
        f"- Surowe dane: {source_path}" if source_path else "- Surowe dane: brak",
        "- Czytanie załączników tylko na żądanie lub gdy opis wskazuje, że są potrzebne.",
        "",
        "## Cel",
        "- Ustal zakres zmiany na podstawie zgłoszenia",
        "- Zapisz notatki techniczne w tym pliku",
        "",
        "## Zakończenie",
        "- Po zakończeniu pracy uruchom wymagane testy i sprawdź brak regresji.",
        "- Zacommituj własne zmiany z poprawnym prefiksem, np. `fix(scope): opis`.",
        "- Dodaj komentarz w KB z podsumowaniem wykonanej pracy i numerem commita.",
        "- Przenieś zgłoszenie w Kanboard do kolumny `Done`.",
        "- Komenda: `python3 kanboard_setup/kb_manager.py move [ID_ZADANIA] \"Done\"`.",
        "",
        "## Notatki",
        "",
    ])


def write_handoff(
    task: dict,
    output_dir: Path | None = None,
    force: bool = False,
    task_files: list[dict] | None = None,
    agent: KanboardAgent | None = None,
) -> Path:
    output_dir = output_dir or Path.cwd() / "handoff"
    output_dir.mkdir(parents=True, exist_ok=True)

    task_id = task.get("id", "task")
    title = task.get("title", f"Task #{task_id}")
    task_dir = output_dir / f"{task_id}_{slugify(title)}"
    brief_path = task_dir / "brief.md"
    if task_dir.exists():
        if not force:
            raise FileExistsError(f"Katalog juz istnieje: {task_dir} (uzyj --force, aby nadpisac)")
        shutil.rmtree(task_dir)
    task_dir.mkdir(parents=True, exist_ok=True)

    if agent and task_files:
        assets_dir = task_dir / "assets"
        task_files = _download_task_files(agent, task_id, task_files, assets_dir)

    description = (task.get("description") or "").strip()
    _, user_actions_block, _ = _split_user_actions(description)
    user_actions_path = Path("assets/user_actions.md")
    source_path = Path("assets/source.md")
    _write_text_file(task_dir / source_path, description + "\n")
    if user_actions_block:
        _write_text_file(task_dir / user_actions_path, user_actions_block + "\n")

    brief_path.write_text(
        build_handoff_markdown(
            task,
            task_files=task_files,
            user_actions_path=user_actions_path if user_actions_block else None,
            source_path=source_path,
        ),
        encoding="utf-8",
    )
    return brief_path


def main() -> int:
    if len(sys.argv) < 2:
        print_usage()
        return 1

    agent = KanboardAgent(URL, USER, TOKEN)
    command = sys.argv[1]

    try:
        if command == "list":
            if len(sys.argv) < 3:
                raise Exception("Uzycie: list <project> [column]")
            project_ref = sys.argv[2]
            column_ref = sys.argv[3] if len(sys.argv) > 3 else None
            print_list(agent.list_tasks(project_ref, column_ref))
            return 0

        if command in {"show", "get"}:
            if len(sys.argv) < 3:
                raise Exception("Uzycie: show <task_id>")
            print_task(agent.get_task(sys.argv[2]))
            return 0

        if command == "handoff":
            if len(sys.argv) < 3:
                raise Exception("Uzycie: handoff <task_id> [--force]")

            force = "--force" in sys.argv[3:]
            task_id = sys.argv[2]
            task = agent.get_task(task_id)
            task_files = agent.get_task_files(task_id)
            expected_project_id = agent.get_project_id(DEFAULT_PROJECT)
            if expected_project_id is None or int(task.get("project_id", 0)) != expected_project_id:
                expected_name = agent.get_project_name(DEFAULT_PROJECT) or DEFAULT_PROJECT
                actual_name = agent.get_project_name(int(task.get("project_id", 0))) or task.get("project_id")
                raise Exception(f"Task #{task_id} nie nalezy do domyslnego projektu '{expected_name}' (jest: '{actual_name}').")

            target = write_handoff(task, force=force, task_files=task_files, agent=agent)
            print(target)
            return 0

        if command == "claim":
            column_ref = sys.argv[2] if len(sys.argv) > 2 else "Backlog"
            limit = int(sys.argv[3]) if len(sys.argv) > 3 else 1
            claimed = agent.claim_tasks(DEFAULT_PROJECT, column_ref, limit)
            if not claimed:
                print("NONE")
                return 0

            for task_id, handoff_path in claimed:
                print(f"{task_id}\t{handoff_path}")
            return 0

        if command == "move":
            if len(sys.argv) < 4:
                raise Exception("Uzycie: move <task_id> <column>")
            agent.move_task(sys.argv[2], sys.argv[3])
            print("OK")
            return 0

        if command == "init":
            if len(sys.argv) < 3:
                raise Exception("Uzycie: init <project_name>")
            print(agent.create_project(sys.argv[2]))
            return 0

        if command == "add-task":
            if len(sys.argv) < 5:
                raise Exception("Uzycie: add-task <project> <title> <description>")
            print(agent.add_task(sys.argv[2], sys.argv[3], sys.argv[4]))
            return 0

        if command == "comment":
            if len(sys.argv) < 4:
                raise Exception("Uzycie: comment <task_id> <content>")
            print(agent.add_comment(sys.argv[2], sys.argv[3]))
            return 0

        print_usage()
        return 1
    except Exception as exc:
        print(f"Blad: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
