'''
Вызов инструмента MCP для поиска похожих текстов
'''

import asyncio
from fastmcp import Client
from loguru import logger


# адрес MCP сервера
MCP_SERVER_URL = 'http://127.0.0.1:9000/mcp'
# текст запроса
query_text = 'Валютные риски'


async def test_search():
    async with Client(MCP_SERVER_URL) as client:
        # вызов инструмента "search_texts" из mcp_server/app/tools/rag_tools.py
        result = await client.call_tool(
            'search_texts',
            {'query': query_text},
        )
        logger.info(f'Результат вызова инструмента "search_texts": {result}')


asyncio.run(test_search())

