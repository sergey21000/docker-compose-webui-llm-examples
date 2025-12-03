'''
Получение эмбеддингов запроса и векторный поиск  
Запускать как модуль:  
python -m mcp_server.scripts.upload_texts_and_search
'''

import os
import sys
from pathlib import Path

from qdrant_client import QdrantClient
from openai import OpenAI
from loguru import logger

from mcp_server.app.utils import RagUtils


# ================= ИНИЦИАЛИЗАЦИЯ КЛИЕНТОВ =================

# назввание коллекции Qdrant
collection_name = 'documents'
# клиент для векторной БД Qdrant
vectorstore_client = QdrantClient(
    url=os.getenv('QDRANT_URL', 'http://127.0.0.1:6333'),
    check_compatibility=False,
)
logger.info(f'Существует ли коллекция {collection_name}: {vectorstore_client.collection_exists(collection_name)}')
logger.info(f'Список имеющихся коллекций: {vectorstore_client.get_collections()}')

# клиент для сервера получения эмбедингов
# в данном примере OpenAI - но у Infinity также есть свой клиент
embeddings_client = OpenAI(
    base_url=os.getenv('EMBEDDINGS_URL', 'http://127.0.0.1:7997'),
    api_key= '-',
)


# ================= ЗАГРУЗКА ТЕКСТОВ В БД ==================

# путь до файлов для тестирования MCP 
# директория /data в docker контейнере - на две папки выше чем main.py
data_dir = (Path(__file__).parent.parent / 'data')
text_file_path = data_dir / 'documents' / 'documents.txt'
logger.info(f'Путь до файла с текстами: {text_file_path}')
if not text_file_path.exists():
    raise FileNotFoundError(f'Файл с текстами для RAG {text_file_path} не найден')

# загрузка текстов в векторную базу данных из файла
RagUtils.upload_texts_to_db_from_file(
    vectorstore_client=vectorstore_client,
    embeddings_client=embeddings_client,
    text_file_path=text_file_path,
    collection_name=collection_name,
)


# ========== ПОИСК РЕЛЕВАНТНЫХ ЗАПРОСУ ТЕКСТОВ ==============

# текст запроса
query_text = 'Какие риски упоминаются в документах?'

# поиск похожих текстов
qdrant_search_result_points = RagUtils.search_relevant_texts(
    vectorstore_client=vectorstore_client,
    embeddings_client=embeddings_client,
    query_text=query_text,
    collection_name=collection_name,
    limit=3,
)
logger.info(f'Результат векторного поиска Qdrant: {qdrant_search_result_points}')

# ----------------------------------------------
# финальный список результатов для удобства
results = []
for point in qdrant_search_result_points:
    results.append({
        'id': point.id,
        'score': point.score,
        'payload': point.payload,
        'text': point.payload.get('text', ''),
    })


# Collection documents exists:  True
# Collections: collections=[CollectionDescription(name='documents')]
# 768
# [ScoredPoint(id=2, version=1, score=0.6730564, payload={'text': 'Основные риски включают кибератаки и изменения регуляторной среды.', 'metadata': {'source': 'risk_report.pdf'}}, vector=None, shard_key=None, order_value=None), ScoredPoint(id=1, version=1, score=0.4087016, payload={'text': 'Компания планирует увеличить инвестиции в ИИ-технологии на 30% в следующем году.', 'metadata': {'source': 'strategy_2024.pdf'}}, vector=None, shard_key=None, order_value=None)]
# [{'id': 2, 'score': 0.6730564, 'payload': {'text': 'Основные риски включают кибератаки и изменения регуляторной среды.', 'metadata': {'source': 'risk_report.pdf'}}, 'text': 'Основные риски включают кибератаки и изменения регуляторной среды.'}, {'id': 1, 'score': 0.4087016, 'payload': {'text': 'Компания планирует увеличить инвестиции в ИИ-технологии на 30% в следующем году.', 'metadata': {'source': 'strategy_2024.pdf'}}, 'text': 'Компания планирует увеличить инвестиции в ИИ-технологии на 30% в следующем году.'}]


