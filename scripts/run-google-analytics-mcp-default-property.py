#!/usr/bin/env python3
"""Run the Google Analytics MCP server with a project-level default GA4 property.

If ``GA4_PROPERTY_ID`` is set, reporting tools can omit ``property_id`` and the
wrapper will inject the project default automatically.
"""

from __future__ import annotations

import asyncio
import inspect
import json
import os
from functools import wraps

from analytics_mcp.tools.admin.info import (
    get_account_summaries,
    get_property_details,
    list_google_ads_links,
    list_property_annotations,
)
from analytics_mcp.tools.reporting.core import (
    _run_report_description,
    run_report,
)
from analytics_mcp.tools.reporting.metadata import (
    get_custom_dimensions_and_metrics,
)
from analytics_mcp.tools.reporting.realtime import (
    _run_realtime_report_description,
    run_realtime_report,
)
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type
from mcp import types as mcp_types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio


DEFAULT_PROPERTY_ID = os.environ.get("GA4_PROPERTY_ID")


def _with_default_property_id(fn):
    """Return a wrapper that injects GA4_PROPERTY_ID when property_id is omitted."""

    signature = inspect.signature(fn)
    parameters = []
    for param in signature.parameters.values():
        if param.name == "property_id":
            parameters.append(
                param.replace(default=None, annotation=int | str | None)
            )
        else:
            parameters.append(param)

    wrapped_signature = signature.replace(parameters=parameters)

    @wraps(fn)
    async def wrapper(*args, **kwargs):
        bound = wrapped_signature.bind_partial(*args, **kwargs)
        property_id = bound.arguments.get("property_id")

        if property_id is None:
            if not DEFAULT_PROPERTY_ID:
                raise ValueError(
                  "property_id is required and GA4_PROPERTY_ID is not set."
              )
            bound.arguments["property_id"] = DEFAULT_PROPERTY_ID

        return await fn(*bound.args, **bound.kwargs)

    wrapper.__signature__ = wrapped_signature
    return wrapper


run_report_with_default = _with_default_property_id(run_report)
run_realtime_report_with_default = _with_default_property_id(run_realtime_report)
get_custom_dimensions_and_metrics_with_default = _with_default_property_id(
    get_custom_dimensions_and_metrics
)
get_property_details_with_default = _with_default_property_id(get_property_details)
list_google_ads_links_with_default = _with_default_property_id(list_google_ads_links)
list_property_annotations_with_default = _with_default_property_id(
    list_property_annotations
)

run_report_tool = FunctionTool(run_report_with_default)
run_report_tool.description = _run_report_description() + (
    "\n\nProject default: if GA4_PROPERTY_ID is set, property_id can be omitted."
)

run_realtime_report_tool = FunctionTool(run_realtime_report_with_default)
run_realtime_report_tool.description = _run_realtime_report_description() + (
    "\n\nProject default: if GA4_PROPERTY_ID is set, property_id can be omitted."
)

tools = [
    FunctionTool(get_account_summaries),
    FunctionTool(list_google_ads_links_with_default),
    FunctionTool(get_property_details_with_default),
    FunctionTool(list_property_annotations_with_default),
    FunctionTool(get_custom_dimensions_and_metrics_with_default),
    run_report_tool,
    run_realtime_report_tool,
]

tool_map = {tool.name: tool for tool in tools}
app = Server(name="Google Analytics MCP Server")
mcp_tools = [adk_to_mcp_tool_type(tool) for tool in tools]


def sanitize_mcp_schema_properties(node: dict) -> None:
    """Ensure `additionalProperties` is a boolean for broad MCP compatibility."""

    if not isinstance(node, dict):
        return

    if "additionalProperties" in node:
        value = node["additionalProperties"]
        if not isinstance(value, bool):
            node["additionalProperties"] = True

    for child in node.values():
        if isinstance(child, dict):
            sanitize_mcp_schema_properties(child)
        elif isinstance(child, list):
            for element in child:
                if isinstance(element, dict):
                    sanitize_mcp_schema_properties(element)


for tool in mcp_tools:
    if tool.inputSchema == {}:
        tool.inputSchema = {"type": "object", "properties": {}}

    for prop in tool.inputSchema.get("properties", {}).values():
        if "anyOf" in prop and prop.get("type") == "null":
            del prop["type"]

    sanitize_mcp_schema_properties(tool.inputSchema)

    if tool.name == "run_report":
        tool.inputSchema["required"] = [
            "date_ranges",
            "dimensions",
            "metrics",
        ]
    elif tool.name == "run_realtime_report":
        tool.inputSchema["required"] = ["dimensions", "metrics"]


@app.list_tools()
async def list_tools() -> list[mcp_types.Tool]:
    return mcp_tools


@app.call_tool()
async def call_mcp_tool(name: str, arguments: dict) -> list[mcp_types.Content]:
    if name in tool_map:
        tool = tool_map[name]
        try:
            adk_tool_response = await tool.run_async(
                args=arguments,
                tool_context=None,
            )
            response_text = json.dumps(adk_tool_response, indent=2)
            return [mcp_types.TextContent(type="text", text=response_text)]
        except Exception as exc:
            error_text = json.dumps({"error": f"Failed to execute tool '{name}': {exc}"})
            return [mcp_types.TextContent(type="text", text=error_text)]

    error_text = json.dumps({"error": f"Tool '{name}' not implemented by this server."})
    return [mcp_types.TextContent(type="text", text=error_text)]


async def run_server_async() -> None:
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=app.name,
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def run_server() -> None:
    asyncio.run(run_server_async())


if __name__ == "__main__":
    try:
        asyncio.run(run_server_async())
    except KeyboardInterrupt:
        print("\nMCP Server (stdio) stopped by user.")
    except Exception:
        import traceback

        print("MCP Server (stdio) encountered an error:")
        traceback.print_exc()
    finally:
        print("MCP Server (stdio) process exiting.")
