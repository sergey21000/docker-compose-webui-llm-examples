import os
import json
from typing import Any

from fastmcp import FastMCP

from logging_config import setup_logging
setup_logging()

from tools.rag_tools import mcp as rag_tools_mcp
from tools.service_tools import mcp as service_tools_mcp
from resources.project_resources import mcp as project_resources_mcp
from prompts.report_prompts import mcp as report_prompts_mcp


mcp = FastMCP('MCP examples')
mcp.mount(rag_tools_mcp, prefix=None)
mcp.mount(service_tools_mcp, prefix=None)
mcp.mount(project_resources_mcp, prefix=None)
mcp.mount(report_prompts_mcp, prefix=None)


if __name__ == '__main__':
    port = int(os.getenv('MCP_PORT', '9000'))
    mcp.run(transport='http', host='0.0.0.0', port=port)
