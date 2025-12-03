import os
from typing import Any
from pathlib import Path

from fastmcp import FastMCP
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.http.models.models import ScoredPoint
from openai import OpenAI
from loguru import logger


class RagUtils:
    # вспомогательная функция получения эмбедингов
    @staticmethod
    def get_embeddings_from_texts(embeddings_client: OpenAI, texts: list[str]) -> list[list[float]]:
        """Получение эмбеддингов OpenAI клиентом"""
        response = embeddings_client.embeddings.create(
            model='local',
            input=texts,
        )
        embeddings = [data.embedding for data in response.data]
        return embeddings
        
    
    # инструмент для загрузки документов в векторную БД
    @classmethod
    def upload_texts_to_db_from_file(
        cls,
        vectorstore_client: QdrantClient,
        embeddings_client: OpenAI,
        text_file_path: Path | str,
        collection_name: str,
    ) -> str:
        '''
        Загрузка текстов в векторную базу данных из файла.
        '''
        # чтение текста из файла
        text = text_file_path.read_text(encoding='utf-8')
        logger.debug(f'Содержимое файла {text_file_path}:\n{text}')
        # разбиваем текст на чанки (просто по абзацам)
        text_chunks = [chunk.strip() for chunk in text.split('\n') if chunk.strip()]
        logger.debug(f'Прочитано {len(text_chunks)} фрагментов текстов')
        # получаем эмбеддинги чанков текстов
        embeddings = cls.get_embeddings_from_texts(
            embeddings_client=embeddings_client,
            texts=text_chunks,
        )
        logger.debug(f'Получено {len(embeddings)} векторов для загрузки в БД:')
        # подготавливаем вектора и тексты для загрузки в БД Qdrant
        points = []
        for i, (text_chunk, embedding) in enumerate(zip(text_chunks, embeddings)):
            points.append({
                'id': i,
                'vector': embedding,
                'payload': {
                    'text': text_chunk,
                    'metadata': {'source': str(text_file_path), 'chunk_id': i}
                }
            })
        # удалить текущую коллекцию если она существует
        if vectorstore_client.collection_exists(collection_name):
            vectorstore_client.delete_collection(collection_name)
            logger.debug(f'Коллекция {collection_name} удалена')
        # создаем коллекцию если не существует
        if not vectorstore_client.collection_exists(collection_name):
            vectorstore_client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=len(embeddings[0]), distance=Distance.COSINE),
            )
            logger.debug(f'Коллекция {collection_name} создана')
        # загружаем вектора в Qdrant
        upsert_result = vectorstore_client.upsert(
            collection_name=collection_name,
            points=points,
            wait=True,
        )
        logger.debug(f'Результат загрузки данных в Qdrant: {upsert_result}')
        # return {'status': 'completed', 'uploaded': len(points)}
        return f'Успешно загружено {len(points)} фрагментов текста в коллекцию {collection_name}'


    @classmethod
    def search_relevant_texts(
        cls,
        vectorstore_client: QdrantClient,
        embeddings_client: OpenAI,
        query_text: str,
        collection_name: str,
        limit: int,
    ) -> list[ScoredPoint]:
        '''
        Ищет релевантные тексты в базе по семантическому запросу.

        Args:
            query_text (str): Текст запроса.
            limit (int): Какое количество релевантных фрагментов текста возвращать из БД.
        '''
        # получаем эмбеддинг для запроса
        embeddings = cls.get_embeddings_from_texts(
            embeddings_client=embeddings_client,
            texts=[query_text],
        )
        query_vector = embeddings[0]
        # поиск похожих текстов в Qdrant, возвращает список объектов ScoredPoint
        qdrant_search_result_points = vectorstore_client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=limit,
            with_payload=True,
        ).points
        return qdrant_search_result_points
