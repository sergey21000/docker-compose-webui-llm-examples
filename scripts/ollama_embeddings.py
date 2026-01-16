# https://docs.ollama.com/capabilities/embeddings#python

import ollama
from loguru import logger


# модель из ollama list
# https://ollama.com/
model = 'embeddinggemma'

# тексты
texts = [
    'Что изображено на картинке?',
    'Предложение для примера',
]

# получение эмбеддингов текстов
response: ollama.EmbedResponse = ollama.embed(
    model=model,
    input=texts,
)

logger.info(f'Кол-во эмбеддингов: {len(response['embeddings'])}')
logger.info(f'Размерность эмбеддингов: {len(response['embeddings'][0])}')
logger.info(f'Объект, возвращаемый методом ollama.embed: {response}')

# 2026-01-16 14:22:08.075 | INFO     | __main__:<module>:23 - Кол-во эмбеддингов: 2
# 2026-01-16 14:22:08.078 | INFO     | __main__:<module>:24 - Размерность эмбеддингов: 768
# 2026-01-16 14:22:08.079 | INFO     | __main__:<module>:25 - Объект, возвращаемый методом ollama.embed: model='embeddinggemma' created_at=None done=None done_reason=None total_duration=5212866877 load_duration=5031111830 prompt_eval_count=16 prompt_eval_duration=None eval_count=None eval_duration=None embeddings=[[-0.11074852, ..., -0.0058481134], [-0.11367593, ..., -0.030320313]]
