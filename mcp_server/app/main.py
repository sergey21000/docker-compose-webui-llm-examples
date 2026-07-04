import os

import uvicorn
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from fastmcp import FastMCP

from logging_config import setup_logging
setup_logging()

from tools.rag import mcp as rag_tools_mcp
from tools.service import mcp as service_tools_mcp
from resources.project import mcp as project_resources_mcp
from prompts.report import mcp as report_prompts_mcp


mcp = FastMCP('MCP examples')

mcp.mount(rag_tools_mcp, prefix=None)
mcp.mount(service_tools_mcp, prefix=None)
mcp.mount(project_resources_mcp, prefix=None)
mcp.mount(report_prompts_mcp, prefix=None)

middleware=[
    Middleware(
        CORSMiddleware,
        # ['*'] для теста; в проде указать ['http://127.0.0.1:8080']
        allow_origins=['*'],
        allow_methods=['*'],
        allow_headers=['*'],
        expose_headers=['Mcp-Session-Id'],
    ),
]


if __name__ == '__main__':
    port = int(os.getenv('MCP_PORT', '9000'))
    mcp.run(
        transport='http',
        host='0.0.0.0',
        port=port,
        path='/mcp',
        middleware=middleware,
    )

    # вариант запуска через uvicorn
    # app = mcp.http_app(path='/mcp', middleware=middleware)
    # uvicorn.run(app, host='0.0.0.0', port=port)
    