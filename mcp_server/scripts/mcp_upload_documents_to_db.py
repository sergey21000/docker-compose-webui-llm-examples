'''
Вызов инструмента MCP который читает документы из файла и загружает в Qdrant
'''

import asyncio
from pathlib import Path
from fastmcp import Client
from loguru import logger


# адрес MCP сервера
MCP_SERVER_URL = 'http://127.0.0.1:9000/mcp'

# назввание коллекции Qdrant
collection_name = 'documents'
# удалять ли текущую коллекцию перед созданием новой
delete_current_collection = True

# путь до файлов для тестирования MCP
data_dir = (Path(__file__).parent.parent / 'data')
document_file = data_dir / 'documents' / 'documents.txt'


async def upload_documents_to_db_from_file():
    """Вызов инструмента MCP который читает документы из файла и загружает в Qdrant"""
    logger.info('Старт операции загрузки документов в БД через вызов MCP')
    async with Client(MCP_SERVER_URL) as client:
        result = await client.call_tool('upload_documents_to_db_from_file')
        logger.info(f'Статус операции загрузки документов в БД через вызов MCP: {result}')


asyncio.run(upload_documents_to_db_from_file())
