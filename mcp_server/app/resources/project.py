import json
from pathlib import Path
from fastmcp import FastMCP


# инициализация MCP сервера
mcp = FastMCP('Project Resources')

# путь до файлов Для тестирования MCP
data_dir = (Path(__file__).parent.parent.parent / 'data')


@mcp.resource('docs://readme')
def get_readme() -> str:
    """Возвращает README проекта"""
    with open(data_dir / 'documents' / "README.md", 'r') as f:
        return f.read()
