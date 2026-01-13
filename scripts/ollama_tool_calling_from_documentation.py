# https://docs.ollama.com/capabilities/tool-calling#parallel-tool-calling

from loguru import logger
from ollama import chat
from ollama import ChatResponse


def get_temperature(city: str) -> str:
    """Get the current temperature for a city

    Args:
    city: The name of the city

    Returns:
    The current temperature for the city
    """
    temperatures = {
        "New York": "22°C",
        "London": "15°C",
        "Tokyo": "18°C"
    }
    return temperatures.get(city, "Unknown")


def get_conditions(city: str) -> str:
    """Get the current weather conditions for a city

    Args:
    city: The name of the city

    Returns:
    The current weather conditions for the city
    """
    conditions = {
        "New York": "Partly cloudy",
        "London": "Rainy",
        "Tokyo": "Sunny"
    }
    return conditions.get(city, "Unknown")


model = 'qwen3:4b'
prompt = 'Каковы текущие погодные условия и температура в Нью-Йорке и Лондоне?'
messages = [{'role': 'user', 'content': prompt}]

response: ChatResponse = chat(
    model=model,
    messages=messages,
    tools=[get_temperature, get_conditions],
    think=False,
)
messages.append(response.message)
# logger.info(messages)

if response.message.tool_calls:
    for call in response.message.tool_calls:
        if call.function.name == 'get_temperature':
          result = get_temperature(**call.function.arguments)
        elif call.function.name == 'get_conditions':
            result = get_conditions(**call.function.arguments)
        else:
            result = 'Unknown tool'
        messages.append({'role': 'tool',  'tool_name': call.function.name, 'content': str(result)})
        logger.info(result)
        
    final_response: ChatResponse = chat(
        model=model,
        messages=messages,
        tools=[get_temperature, get_conditions],
        think=True,
    )
    print(final_response.message.content)


# 2026-01-12 20:16:11.441 | INFO     | __main__:<module>:68 - 22°C
# 2026-01-12 20:16:11.442 | INFO     | __main__:<module>:68 - Partly cloudy
# 2026-01-12 20:16:11.442 | INFO     | __main__:<module>:68 - 15°C
# 2026-01-12 20:16:11.442 | INFO     | __main__:<module>:68 - Rainy
# В Нью-Йорке текущая температура составляет 22°C, погода частично облаков. В Лондоне текущая температура — 15°C, погода дождливая.
