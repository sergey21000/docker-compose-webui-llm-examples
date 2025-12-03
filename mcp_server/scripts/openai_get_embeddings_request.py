'''
Получение эмбеддингов текстов через отправку запроса через OpenAI к серверу Infinity
'''

from openai import OpenAI
from loguru import logger


# адрес сервера для получения эмбедингов
EMBEDDINGS_URL = 'http://127.0.0.1:7997'
# клиент OpenAI для отправки запросов (у Infinity тоже есть свой клиент)
embeddings_client = OpenAI(base_url=EMBEDDINGS_URL, api_key= '-')
# примеры текстов
texts = [
    'Привет, как дела?',
    'Текст 2',
]
# отправка запроса на сервер и получение эмбедингов
response = embeddings_client.embeddings.create(
    model='local',  # любое имя
    input=texts,
    extra_body=dict(
        normalize=True,
    )
)
# извлечение векторов-списков
embeddings: list[list[float]] = [data.embedding for data in response.data]
logger.info(len(embeddings))
logger.info(len(embeddings[0]))
logger.info(embeddings[0][:10])
logger.info('==================')
logger.info(response)


# пример ответа:
# 2
# 768
# [-0.03696243464946747, 0.06095292046666145, 0.07807589322328568, 0.045233964920043945, -0.09052897244691849]
# ==================
# CreateEmbeddingResponse(
    # data=[
        # Embedding(embedding=[-0.03696243464946747, 0.06095292046666145,56, ...], index=0, object='embedding'),
        # Embedding(embedding=[-0.035774484276771545, 0.014941646717488766, ...], index=1, object='embedding')
    # ], 
# model='Alibaba-NLP/gte-multilingual-base', object='list', usage=Usage(prompt_tokens=24, total_tokens=24), id='infinity-726acb25-d87b-482a-92c5-1eebcde20c59', created=1763905470)