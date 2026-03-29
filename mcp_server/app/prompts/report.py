from fastmcp import FastMCP


# инициализация MCP сервера
mcp = FastMCP('Report promts')


@mcp.prompt
def explain_result(tool_name: str, tool_desc: str) -> str:
    """Объясняет результат работы инструмента"""
    return f"""
    Объясни пользователю простыми словами результат работы MCP инструмента '{tool_name}':
    
    Описание инструмента: {tool_desc}
    
    Сделай объяснение понятным и полезным.
    """
