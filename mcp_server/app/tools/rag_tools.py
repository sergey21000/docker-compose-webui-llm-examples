import os
from typing import Any
from pathlib import Path

from fastmcp import FastMCP
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.http.models.models import ScoredPoint
from openai import OpenAI
from loguru import logger

from utils import RagUtils


# инициализация MCP сервера
mcp = FastMCP('MCP Tools')

# клиент для векторной БД Qdrant
vectorstore_client = QdrantClient(
    url=os.getenv('VECTORSTORE_URL', 'http://127.0.0.1:6333'),
    check_compatibility=False,
)
# назввание коллекции Qdrant - в данном упрощенном примере берется глобально
collection_name = 'documents'

# клиент для сервера получения эмбедингов
# в данном примере OpenAI - но у Infinity также есть свой клиент
embeddings_client = OpenAI(
    base_url=os.getenv('EMBEDDINGS_URL', 'http://127.0.0.1:7997'),
    api_key='-',
)

# путь до файлов для тестирования MCP 
# директория mcp_server/data - в docker контейнере это /data
data_dir = (Path(__file__).parent.parent.parent / 'data')
text_file_path = data_dir / 'documents' / 'documents.txt'
logger.debug(f'Путь до файла с текстами: {text_file_path}')
if not text_file_path.exists():
    raise FileNotFoundError(f'Файл с текстами для RAG {text_file_path} не найден')


# инструмент для поиска похожих запросу документов по векторной БД
# чем хуже модель тем больше вероятность что она может передать
# данные для иснтрумента в неправильном формате
# например вместо строки query gemma4:3b из Ollama иногда передает словарь
@mcp.tool()
def search_texts(query: str) -> str:
    '''
    Поиск релевантных текстов в базе данных.

    Args:
        query (str): Текст запроса.
    '''
    logger.debug(f'Пришедщий запрос в инструмент "search_texts": {query}')
    
    # парсинг запроса если вдруг в query пришел словарь вместо строки
    # AnythingLLM бывает присылает словарь вместо строки
    # если пришел словарь то чтобы функция сработала надо добавить аннотацию query: str | dict
    # if isinstance(query, dict):
        # query = query.get('title') or query.get('value') or query.get('query')
        # if isinstance(query, dict):
            # query = query.get('value', str(query))
    # else:
        # query = str(query)
    
    # получение релевантных текстов
    qdrant_search_result_points: list[ScoredPoint] = RagUtils.search_relevant_texts(
        vectorstore_client=vectorstore_client,
        embeddings_client=embeddings_client,
        query_text=query,
        collection_name=collection_name,
        limit=3,
    )
    if not qdrant_search_result_points:
        return 'По запросу ничего не найдено.'
    # получение найденных фрагментов текста в один текст
    result_texts = [hit.payload.get('text', '') for hit in qdrant_search_result_points]
    # соединение найденных фрагментов текста в один текст
    result_text = '\n\n'.join(result_texts)
    logger.debug(f'Результат вызова инструмента "search_texts": {result_text}')
    return result_text


# инструмент для загрузки документов в векторную БД
@mcp.tool()
def upload_texts() -> str:
    '''
    Загрузка текстов в векторную базу данных из файла.
    '''
    return RagUtils.upload_texts_to_db_from_file(
        vectorstore_client=vectorstore_client,
        embeddings_client=embeddings_client,
        text_file_path=text_file_path,
        collection_name=collection_name,
    )

if __name__ == '__main__':
    port = int(os.getenv('MCP_PORT', '9000'))
    mcp.run(transport='http', host='127.0.0.1', port=port)
