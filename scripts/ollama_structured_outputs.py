import requests
from loguru import logger

from ollama import chat
from ollama import ChatResponse

from pydantic import BaseModel, Field


# класс продукта с содержанием БЖУ
class Product(BaseModel):
    name: str = Field(..., description='Название продукта')
    protein_g_per_100g: float = Field(..., description='Белки на 100 г продукта')
    fat_g_per_100g: float = Field(..., description='Жиры на 100 г продукта')
    carbs_g_per_100g: float = Field(..., description='Углеводы на 100 г продукта')


# список продуктов
class ProductList(BaseModel):
    products: list[Product]


# системный промт (опционально)
system_prompt = ''

# основной промт
prompt = (
    'Назови ТОП-3 продукта с высоким содержанием белка и укажи их БЖУ на 100 г'
    # 'Ответ дай строго в структурированном виде.'
)
# сообщения для подачи в модель / история переписки
messages = []
if system_prompt:
    messages.append({'role': 'system', 'content': system_prompt})
messages.append({'role': 'user', 'content': prompt})

# модель из Ollama list
model = 'qwen3:4b'

# генерация ответа модели с structured outputs
response: ChatResponse = chat(
    model=model,
    messages=messages,
    # формат вывода
    format=ProductList.model_json_schema(),
    think=False,
    options={
        'temperature': 0.2,
    }
)

result = ProductList.model_validate_json(response.message.content)

for p in result.products:
    logger.info(
        f'{p.name}: '
        f'Белки {p.protein_g_per_100g} г, '
        f'Жиры {p.fat_g_per_100g} г, '
        f'Углеводы {p.carbs_g_per_100g} г, '
    )

# Говяжья печень: Белки 20.5 г, Жиры 10.2 г, Углеводы 0.0 г,
# Сыр фета: Белки 25.5 г, Жиры 28.0 г, Углеводы 0.0 г,
# Куриная грудка (без кожи): Белки 23.0 г, Жиры 3.0 г, Углеводы 0.0 г,

logger.info('=================================')

logger.info(f'Необработанный ответ модели: {result}')

# 2026-01-13 11:33:09.119 | INFO     | __main__:<module>:68 - Необработанный ответ модели: products=[Product(name='Говяжья печень', protein_g_per_100g=20.5, fat_g_per_100g=10.2, carbs_g_per_100g=0.0), Product(name='Сыр фета', protein_g_per_100g=26.5, fat_g_per_100g=28.0, carbs_g_per_100g=0.0), Product(name='Куриная грудка (без кожи)', protein_g_per_100g=23.0, fat_g_per_100g=3.0, carbs_g_per_100g=0.0)]
