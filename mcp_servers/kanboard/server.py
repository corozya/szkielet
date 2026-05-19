import os
import re
import sys
from dataclasses import dataclass
from base64 import b64encode
from typing import Any, Optional
from pathlib import Path
from urllib.parse import urlparse
import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
REPO_ROOT = Path(__file__).parent.parent.parent
ENV_FILE = REPO_ROOT / "kanboard_setup/.env"
load_dotenv(ENV_FILE)

mcp = FastMCP("Kanboard")


@dataclass(frozen=True)
class KanboardConfig:
    url: str
    user: str
    token: str
    project: str
    env_file: str


@dataclass(frozen=True)
class ConnectionStatus:
    url: str
    user: str
    project: str
    env_file: str
    token_set: bool
    token_length: int

    def render(self) -> str:
        token_preview = "set" if self.token_set else "missing"
        project = self.project or "(not set)"
        url = self.url or "(not set)"
        user = self.user or "(not set)"
        return (
            "Kanboard connection config\n"
            f"- KANBOARD_URL: {url}\n"
            f"- KANBOARD_USER: {user}\n"
            f"- KANBOARD_PROJECT: {project}\n"
            f"- ENV_FILE: {self.env_file}\n"
            f"- KANBOARD_TOKEN: {token_preview} (length={self.token_length})"
        )


def read_env_file(env_path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not env_path.exists():
        return values

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"')
    return values


def get_config(env_path: Path = ENV_FILE) -> KanboardConfig:
    file_values = read_env_file(env_path)
    return KanboardConfig(
        url=(file_values.get("KANBOARD_URL") or os.environ.get("KANBOARD_URL", "")).strip(),
        user=(file_values.get("KANBOARD_USER") or os.environ.get("KANBOARD_USER", "jsonrpc")).strip() or "jsonrpc",
        token=(file_values.get("KANBOARD_TOKEN") or os.environ.get("KANBOARD_TOKEN", "")).strip(),
        project=(file_values.get("KANBOARD_PROJECT") or os.environ.get("KANBOARD_PROJECT", "")).strip(),
        env_file=str(env_path),
    )


def validate_config(config: KanboardConfig | None = None) -> None:
    config = config or get_config()
    missing: list[str] = []
    if not config.url:
        missing.append("KANBOARD_URL")
    if not config.token:
        missing.append("KANBOARD_TOKEN")

    if missing:
        raise ValueError(
            "Kanboard MCP requires configuration. Set "
            + ", ".join(missing)
            + " in kanboard_setup/.env or the process environment before starting MCP."
        )

    parsed = urlparse(config.url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(
            "KANBOARD_URL must be an HTTP(S) JSON-RPC endpoint, for example "
            "http://127.0.0.1:8080/jsonrpc.php."
        )

    if parsed.port == 1:
        raise ValueError(
            "KANBOARD_URL still points to the placeholder port 1. "
            "Run npm run init-kb or set a real JSON-RPC endpoint before using Kanboard MCP."
        )


class KanboardAgent:
    def __init__(self, url: str, user: str, token: str):
        self.url = url
        auth = f"{user}:{token}"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {b64encode(auth.encode()).decode()}",
        }

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
                error = body["error"] or {}
                message = error.get("message", "Unknown Kanboard error")
                code = error.get("code")
                data = error.get("data")
                details = []
                if code is not None:
                    details.append(f"code={code}")
                if data is not None:
                    details.append(f"data={data}")
                suffix = f" ({'; '.join(details)})" if details else ""
                raise RuntimeError(f"Kanboard RPC '{method}' failed: {message}{suffix}")
            return body.get("result")
        except requests.RequestException as exc:
            response_text = ""
            if getattr(exc, "response", None) is not None and exc.response.text:
                response_text = f": {exc.response.text.strip()}"
            raise RuntimeError(f"Kanboard RPC '{method}' request failed: {exc}{response_text}") from exc
        except ValueError as exc:
            raise RuntimeError(f"Kanboard RPC '{method}' returned invalid JSON: {exc}") from exc
        except Exception as exc:
            raise RuntimeError(f"Kanboard RPC '{method}' failed: {exc}") from exc

    def test_connection(self) -> str:
        version = self._call("getVersion")
        if version is None:
            raise RuntimeError("Kanboard RPC 'getVersion' returned no result")
        return str(version)

_agent: Optional[KanboardAgent] = None
_agent_config: Optional[KanboardConfig] = None


validate_config()


def get_agent(config: KanboardConfig | None = None) -> KanboardAgent:
    global _agent, _agent_config
    config = config or get_config()
    if not _agent or _agent_config != config:
        _agent = KanboardAgent(config.url, config.user, config.token)
        _agent_config = config
    return _agent


def slugify(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', '_', text.lower()).strip('_')


def normalize_url(input_value: str | None) -> str:
    raw = str(input_value or "").strip()
    if not raw:
        return ""
    with_scheme = raw if "://" in raw else f"http://{raw}"
    try:
        parsed = urlparse(with_scheme)
        if parsed.path in {"", "/"}:
            return parsed._replace(path="/jsonrpc.php").geturl()
        return parsed.geturl()
    except Exception:
        return raw


def get_connection_status() -> ConnectionStatus:
    config = get_config()
    return ConnectionStatus(
        url=config.url,
        user=config.user,
        project=config.project,
        env_file=config.env_file,
        token_set=bool(config.token),
        token_length=len(config.token),
    )


def resolve_project_id(agent: KanboardAgent, project_ref: str) -> int:
    if str(project_ref).isdigit():
        return int(project_ref)

    project = agent._call("getProjectByName", {"name": str(project_ref)})
    if project and project.get("id"):
        return int(project["id"])

    raise RuntimeError(f"Kanboard project '{project_ref}' not found")


@mcp.tool()
def kanboard_connection_status() -> str:
    """Show Kanboard connection parameters and test the JSON-RPC connection."""
    agent = get_agent()
    status = get_connection_status()
    try:
        version = agent.test_connection()
        result = (
            f"{status.render()}\n"
            f"- connection_test: OK\n"
            f"- getVersion: {version}"
        )
        return result
    except Exception as exc:
        return f"{status.render()}\n- connection_test: FAILED\n- error: {exc}"


def log_startup_diagnostics() -> None:
    status = get_connection_status()
    print(status.render(), file=sys.stderr)
    try:
        version = get_agent().test_connection()
        print(f"- connection_test: OK", file=sys.stderr)
        print(f"- getVersion: {version}", file=sys.stderr)
    except Exception as exc:
        print("- connection_test: FAILED", file=sys.stderr)
        print(f"- error: {exc}", file=sys.stderr)

@mcp.tool()
def kanboard_get_backlog(project_ref: Optional[str] = None) -> str:
    """Get list of tasks from the Backlog column of a project."""
    agent = get_agent()
    ref = project_ref or get_config().project
    if not ref:
        return "Error: project_ref is required (no default set in .env)."

    try:
        project_id = resolve_project_id(agent, str(ref))
        board = agent._call("getBoard", {"project_id": project_id}) or []
        backlog_tasks: list[dict[str, Any]] = []

        for swimlane in board:
            for column in swimlane.get("columns", []):
                if str(column.get("title", "")).lower() == "backlog":
                    backlog_tasks.extend(column.get("tasks", []) or [])

        if not backlog_tasks:
            return "No tasks in Backlog."

        return "\n".join([f"#{task['id']}: {task['title']}" for task in backlog_tasks])
    except Exception as exc:
        return f"Error: {exc}"

@mcp.tool()
def kanboard_get_task(task_id: int) -> str:
    """Get detailed information about a specific task."""
    agent = get_agent()
    task = agent._call("getTask", {"task_id": task_id})
    if not task:
        return f"Error: Task #{task_id} not found."
    
    comments = agent._call("getAllComments", {"task_id": task_id}) or []
    comment_text = "\nComments:\n" + "\n".join([f"- {c['username']}: {c['comment']}" for c in comments]) if comments else ""
    
    return (
        f"Task #{task['id']}: {task['title']}\n"
        f"Description: {task.get('description', 'No description')}\n"
        f"Status: {task.get('column_title')}\n"
        f"URL: {task.get('url')}"
        f"{comment_text}"
    )

@mcp.tool()
def kanboard_create_task(title: str, description: Optional[str] = None, project_ref: Optional[str] = None) -> str:
    """Create a new task in Kanboard."""
    agent = get_agent()
    ref = project_ref or get_config().project
    if not ref:
        return "Error: project_ref is required."

    project_id = None
    if str(ref).isdigit():
        project_id = int(ref)
    else:
        projects = agent._call("getAllProjects") or []
        for p in projects:
            if p.get("name", "").lower() == str(ref).lower():
                project_id = int(p["id"])
                break
    
    if not project_id:
        return f"Error: Project '{ref}' not found."

    task_id = agent._call("createTask", {
        "title": title,
        "project_id": project_id,
        "description": description or ""
    })
    
    if not task_id:
        return "Error: Failed to create task."
    
    return f"Created task #{task_id}"

@mcp.tool()
def kanboard_move_task(task_id: int, column_name: str) -> str:
    """Move a task to a different column by column name."""
    agent = get_agent()
    task = agent._call("getTask", {"task_id": task_id})
    if not task:
        return f"Error: Task #{task_id} not found."
    
    project_id = int(task["project_id"])
    columns = agent._call("getColumns", {"project_id": project_id}) or []
    column = next((c for c in columns if c["title"].lower() == column_name.lower()), None)
    
    if not column:
        return f"Error: Column '{column_name}' not found in project."
    
    success = agent._call("moveTaskPosition", {
        "project_id": project_id,
        "task_id": task_id,
        "column_id": column["id"],
        "position": 1
    })
    
    return f"Moved task #{task_id} to {column_name}" if success else "Error: Failed to move task."

@mcp.tool()
def kanboard_delete_task(task_id: int, confirm: bool = False) -> str:
    """Delete a task from Kanboard. Requires explicit confirmation."""
    if not confirm:
        return (
            f"Refusing to delete task #{task_id} without confirmation. "
            "Call again with confirm=true to proceed."
        )

    agent = get_agent()
    task = agent._call("getTask", {"task_id": task_id})
    if not task:
        return f"Error: Task #{task_id} not found."

    success = agent._call("removeTask", {"task_id": task_id})
    return f"Deleted task #{task_id}" if success else f"Error: Failed to delete task #{task_id}."

@mcp.tool()
def kanboard_update_task(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[int] = None,
    due_date: Optional[str] = None,
) -> str:
    """Update title, description, priority or due_date of an existing task."""
    agent = get_agent()
    task = agent._call("getTask", {"task_id": task_id})
    if not task:
        return f"Error: Task #{task_id} not found."

    params: dict = {"id": task_id}
    if title is not None:
        params["title"] = title
    if description is not None:
        params["description"] = description
    if priority is not None:
        params["priority"] = priority
    if due_date is not None:
        params["date_due"] = due_date

    if len(params) == 1:
        return "Error: Provide at least one field to update (title, description, priority, due_date)."

    success = agent._call("updateTask", params)
    return f"Updated task #{task_id}" if success else f"Error: Failed to update task #{task_id}."


@mcp.tool()
def kanboard_get_all_tasks(project_ref: Optional[str] = None, column: Optional[str] = None) -> str:
    """Get all active tasks in a project, optionally filtered by column name."""
    agent = get_agent()
    ref = project_ref or get_config().project
    if not ref:
        return "Error: project_ref is required."

    try:
        project_id = resolve_project_id(agent, str(ref))
        board = agent._call("getBoard", {"project_id": project_id}) or []
        tasks: list[dict] = []

        for swimlane in board:
            for col in swimlane.get("columns", []):
                col_title = str(col.get("title", ""))
                if column and col_title.lower() != column.lower():
                    continue
                for task in col.get("tasks", []) or []:
                    tasks.append({"id": task["id"], "title": task["title"], "column": col_title})

        if not tasks:
            return "No tasks found."

        return "\n".join([f"#{t['id']} [{t['column']}]: {t['title']}" for t in tasks])
    except Exception as exc:
        return f"Error: {exc}"


@mcp.tool()
def kanboard_create_handoff(task_id: int) -> str:
    """Initialize a local handoff brief from a Kanboard task."""
    agent = get_agent()
    task = agent._call("getTask", {"task_id": task_id})
    if not task:
        return f"Error: Task #{task_id} not found."
    
    title_slug = slugify(task["title"])
    folder_name = f"{task_id}_{title_slug}"
    handoff_dir = REPO_ROOT / "handoff" / folder_name
    handoff_dir.mkdir(parents=True, exist_ok=True)
    
    brief_path = handoff_dir / "brief.md"
    if brief_path.exists():
        return f"Handoff already exists at {brief_path}"
    
    content = f"""# Brief: {task['title']}

**Task ID:** {task['id']}
**URL:** {task.get('url')}
**Kolumna:** {task.get('column_title')}
**Rola:**
**Suggested AI:**
**Fallback:**

## Opis zadania
{task.get('description') or 'Brak opisu.'}

## Status
- [ ] Implementacja
- [ ] Testy
- [ ] Weryfikacja
"""
    brief_path.write_text(content, encoding="utf-8")
    return f"Created local handoff at {brief_path}"


def serialize_env_file(current_text: str, updates: dict[str, str]) -> str:
    keys_to_ensure = ["KANBOARD_URL", "KANBOARD_USER", "KANBOARD_TOKEN", "KANBOARD_PROJECT"]
    existing_lines = current_text.splitlines()
    output_lines: list[str] = []
    seen: set[str] = set()

    for raw_line in existing_lines:
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            output_lines.append(raw_line)
            continue

        key, _ = line.split("=", 1)
        key = key.strip()
        if key in keys_to_ensure:
            output_lines.append(f"{key}={updates.get(key, '')}")
            seen.add(key)
        else:
            output_lines.append(raw_line)

    for key in keys_to_ensure:
        if key not in seen and key in updates:
            output_lines.append(f"{key}={updates[key]}")

    return "\n".join(output_lines).rstrip("\n") + "\n"


def render_kb_init_questions(config: KanboardConfig) -> str:
    lines = [
        "kb_init needs these answers:",
        f"- host/url: {config.url or '(required)'}",
        f"- user: {config.user or 'jsonrpc'}",
        f"- token: {'set' if config.token else '(required)'}",
        f"- project: {config.project or '(optional)'}",
        "",
        "Provide the missing values in the next `kb_init` call.",
        "Examples:",
        'kb_init(host="http://127.0.0.1:8080", token="...", project="My Project")',
        'kb_init(url="http://127.0.0.1:8080/jsonrpc.php", user="jsonrpc", token="...", project="My Project")',
    ]
    return "\n".join(lines)


@mcp.tool()
def kb_init(
    host: Optional[str] = None,
    url: Optional[str] = None,
    user: Optional[str] = None,
    token: Optional[str] = None,
    project: Optional[str] = None,
    env_path: Optional[str] = None,
    no_test: bool = False,
) -> str:
    """Initialize or update Kanboard parameters from MCP."""
    target_env = Path(env_path).expanduser().resolve() if env_path else ENV_FILE
    target_env.parent.mkdir(parents=True, exist_ok=True)

    current = get_config(target_env)
    next_url = normalize_url(host or url) or current.url
    next_user = (user or current.user or "jsonrpc").strip() or "jsonrpc"
    next_token = (token or current.token).strip()
    next_project = (project if project is not None else current.project).strip()

    pending = KanboardConfig(
        url=next_url,
        user=next_user,
        token=next_token,
        project=next_project,
        env_file=str(target_env),
    )

    if not pending.url or not pending.token:
        return render_kb_init_questions(pending)

    validate_config(pending)

    agent = KanboardAgent(pending.url, pending.user, pending.token)
    version = "skipped"
    if not no_test:
        version = agent.test_connection()

    existing_text = target_env.read_text(encoding="utf-8") if target_env.exists() else ""
    out_text = serialize_env_file(
        existing_text,
        {
            "KANBOARD_URL": pending.url,
            "KANBOARD_USER": pending.user,
            "KANBOARD_TOKEN": pending.token,
            "KANBOARD_PROJECT": pending.project,
        },
    )
    target_env.write_text(out_text, encoding="utf-8")

    os.environ["KANBOARD_URL"] = pending.url
    os.environ["KANBOARD_USER"] = pending.user
    os.environ["KANBOARD_TOKEN"] = pending.token
    os.environ["KANBOARD_PROJECT"] = pending.project

    global _agent, _agent_config
    _agent = agent
    _agent_config = pending

    status = get_connection_status().render()
    result = (
        f"{status}\n"
        f"- init: OK\n"
        f"- saved: {target_env}\n"
        f"- getVersion: {version}"
    )
    return result

if __name__ == "__main__":
    log_startup_diagnostics()
    mcp.run()
