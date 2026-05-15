from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import mysql.connector
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

REPO_ROOT = Path(__file__).parent.parent.parent
ENV_FILE = REPO_ROOT / ".env"
load_dotenv(ENV_FILE)

mcp = FastMCP("MySQL")

READ_ONLY_PREFIXES = {
    "select",
    "show",
    "describe",
    "desc",
    "explain",
    "with",
    "values",
}

WRITE_PREFIXES = {
    "insert",
    "update",
    "delete",
    "create",
    "alter",
    "drop",
    "truncate",
    "rename",
    "replace",
    "grant",
    "revoke",
    "commit",
    "rollback",
    "set",
    "use",
    "flush",
    "lock",
    "unlock",
    "call",
    "prepare",
    "execute",
    "deallocate",
    "handler",
}


@dataclass(frozen=True)
class MySQLConfig:
    host: str
    port: int
    user: str
    password: str
    database: str
    connect_timeout: int
    charset: str
    env_file: str


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


def get_config(env_path: Path = ENV_FILE) -> MySQLConfig:
    file_values = read_env_file(env_path)
    host = (file_values.get("MYSQL_HOST") or os.environ.get("MYSQL_HOST", "127.0.0.1")).strip()
    port_raw = (file_values.get("MYSQL_PORT") or os.environ.get("MYSQL_PORT", "3306")).strip()
    user = (file_values.get("MYSQL_USER") or os.environ.get("MYSQL_USER", "root")).strip() or "root"
    password = (file_values.get("MYSQL_PASSWORD") or os.environ.get("MYSQL_PASSWORD", "")).strip()
    database = (file_values.get("MYSQL_DATABASE") or os.environ.get("MYSQL_DATABASE", "")).strip()
    connect_timeout_raw = (
        file_values.get("MYSQL_CONNECT_TIMEOUT")
        or os.environ.get("MYSQL_CONNECT_TIMEOUT", "10")
    ).strip()
    charset = (file_values.get("MYSQL_CHARSET") or os.environ.get("MYSQL_CHARSET", "utf8mb4")).strip() or "utf8mb4"

    try:
        port = int(port_raw)
    except ValueError as exc:
        raise ValueError(f"MYSQL_PORT must be an integer, got: {port_raw!r}") from exc

    try:
        connect_timeout = int(connect_timeout_raw)
    except ValueError as exc:
        raise ValueError(
            f"MYSQL_CONNECT_TIMEOUT must be an integer, got: {connect_timeout_raw!r}"
        ) from exc

    return MySQLConfig(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        connect_timeout=connect_timeout,
        charset=charset,
        env_file=str(env_path),
    )


def validate_config(config: MySQLConfig | None = None) -> None:
    config = config or get_config()
    missing: list[str] = []
    if not config.host:
        missing.append("MYSQL_HOST")
    if not config.user:
        missing.append("MYSQL_USER")

    if missing:
        raise ValueError(
            "MySQL MCP requires configuration. Set "
            + ", ".join(missing)
            + " in .env or the process environment before starting MCP."
        )

    if config.port <= 0:
        raise ValueError("MYSQL_PORT must be greater than 0.")

    if config.connect_timeout <= 0:
        raise ValueError("MYSQL_CONNECT_TIMEOUT must be greater than 0.")


def normalize_database(database: Optional[str], config: MySQLConfig) -> str:
    return (database or config.database or "").strip()


def connect(database: Optional[str] = None):
    config = get_config()
    validate_config(config)
    kwargs: dict[str, Any] = {
        "host": config.host,
        "port": config.port,
        "user": config.user,
        "password": config.password,
        "connection_timeout": config.connect_timeout,
        "charset": config.charset,
        "use_unicode": True,
    }
    selected_database = normalize_database(database, config)
    if selected_database:
        kwargs["database"] = selected_database
    return mysql.connector.connect(**kwargs)


def to_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, default=str)


def first_sql_keyword(sql: str) -> str:
    stripped = sql.strip()
    stripped = re.sub(r"^/\*.*?\*/\s*", "", stripped, flags=re.S)
    while stripped.startswith("--") or stripped.startswith("#"):
        newline = stripped.find("\n")
        if newline == -1:
            return ""
        stripped = stripped[newline + 1 :].lstrip()
    stripped = stripped.lstrip("(; \t\r\n")
    match = re.match(r"([A-Za-z]+)", stripped)
    return match.group(1).lower() if match else ""


def ensure_read_only(sql: str) -> None:
    if not sql or not sql.strip():
        raise ValueError("SQL query is required.")

    keyword = first_sql_keyword(sql)
    if not keyword:
        raise ValueError("Unable to determine the SQL statement type.")

    if keyword in WRITE_PREFIXES or keyword not in READ_ONLY_PREFIXES:
        raise ValueError(
            "This MySQL MCP server is read-only. Allowed statement types are: "
            "SELECT, SHOW, DESCRIBE, DESC, EXPLAIN, WITH, VALUES."
        )

    normalized = sql.strip()
    if ";" in normalized[:-1]:
        raise ValueError("Multiple SQL statements are not allowed.")


def connection_summary(config: MySQLConfig) -> str:
    database = config.database or "(not set)"
    password_state = "set" if config.password else "missing"
    return (
        "MySQL connection config\n"
        f"- MYSQL_HOST: {config.host or '(not set)'}\n"
        f"- MYSQL_PORT: {config.port}\n"
        f"- MYSQL_USER: {config.user or '(not set)'}\n"
        f"- MYSQL_DATABASE: {database}\n"
        f"- MYSQL_CHARSET: {config.charset}\n"
        f"- ENV_FILE: {config.env_file}\n"
        f"- MYSQL_PASSWORD: {password_state}"
    )


def log_startup_diagnostics() -> None:
    config = get_config()
    print(connection_summary(config), file=sys.stderr)
    try:
        conn = connect()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT 1 AS ok")
                row = cursor.fetchone()
                value = row[0] if row else None
                print("- connection_test: OK", file=sys.stderr)
                print(f"- select_1: {value}", file=sys.stderr)
            finally:
                cursor.close()
        finally:
            conn.close()
    except Exception as exc:
        print("- connection_test: FAILED", file=sys.stderr)
        print(f"- error: {exc}", file=sys.stderr)


@mcp.tool()
def mysql_connection_status() -> str:
    """Show MySQL connection parameters and test the connection."""
    config = get_config()
    try:
        conn = connect()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT DATABASE()")
                current_database = cursor.fetchone()
                cursor.execute("SELECT 1")
                test_row = cursor.fetchone()
            finally:
                cursor.close()
        finally:
            conn.close()

        current_database_value = current_database[0] if current_database else None
        test_value = test_row[0] if test_row else None
        return (
            f"{connection_summary(config)}\n"
            f"- connection_test: OK\n"
            f"- current_database: {current_database_value}\n"
            f"- select_1: {test_value}"
        )
    except Exception as exc:
        return f"{connection_summary(config)}\n- connection_test: FAILED\n- error: {exc}"


@mcp.tool()
def mysql_list_databases() -> str:
    """List available MySQL databases."""
    conn = connect()
    try:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SHOW DATABASES")
            rows = cursor.fetchall()
        finally:
            cursor.close()
    finally:
        conn.close()

    return to_json(
        {
            "row_count": len(rows),
            "databases": rows,
        }
    )


@mcp.tool()
def mysql_list_tables(database: Optional[str] = None) -> str:
    """List tables in a database."""
    config = get_config()
    target_database = normalize_database(database, config)
    if not target_database:
        return "Error: database is required (set MYSQL_DATABASE or pass database)."

    conn = connect(target_database)
    try:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT TABLE_NAME, TABLE_TYPE
                FROM information_schema.tables
                WHERE table_schema = %s
                ORDER BY TABLE_NAME
                """,
                (target_database,),
            )
            rows = cursor.fetchall()
        finally:
            cursor.close()
    finally:
        conn.close()

    return to_json(
        {
            "database": target_database,
            "row_count": len(rows),
            "tables": rows,
        }
    )


@mcp.tool()
def mysql_describe_table(table: str, database: Optional[str] = None) -> str:
    """Describe columns for a table."""
    config = get_config()
    target_database = normalize_database(database, config)
    if not target_database:
        return "Error: database is required (set MYSQL_DATABASE or pass database)."

    table_name = table.strip()
    if not table_name:
        return "Error: table is required."

    conn = connect(target_database)
    try:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_KEY, EXTRA
                FROM information_schema.columns
                WHERE table_schema = %s AND table_name = %s
                ORDER BY ORDINAL_POSITION
                """,
                (target_database, table_name),
            )
            rows = cursor.fetchall()
        finally:
            cursor.close()
    finally:
        conn.close()

    return to_json(
        {
            "database": target_database,
            "table": table_name,
            "row_count": len(rows),
            "columns": rows,
        }
    )


@mcp.tool()
def mysql_query(sql: str, database: Optional[str] = None, limit: int = 100) -> str:
    """Run a read-only MySQL query and return the result set as JSON."""
    ensure_read_only(sql)
    if limit <= 0:
        return "Error: limit must be greater than 0."
    if limit > 1000:
        limit = 1000

    config = get_config()
    target_database = normalize_database(database, config)
    conn = connect(target_database)
    try:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(sql)
            if not getattr(cursor, "with_rows", True):
                return to_json(
                    {
                        "database": target_database or None,
                        "row_count": 0,
                        "truncated": False,
                        "columns": [],
                        "rows": [],
                    }
                )

            rows = cursor.fetchmany(limit + 1)
            truncated = len(rows) > limit
            rows = rows[:limit]
            columns = [str(name) for name in getattr(cursor, "column_names", ()) or ()]
            result_rows = [{str(key): value for key, value in row.items()} for row in rows]
        finally:
            cursor.close()
    finally:
        conn.close()

    return to_json(
        {
            "database": target_database or None,
            "row_count": len(result_rows),
            "truncated": truncated,
            "columns": columns,
            "rows": result_rows,
        }
    )


validate_config()
log_startup_diagnostics()


if __name__ == "__main__":
    mcp.run()
