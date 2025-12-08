from pathlib import Path
from datetime import date
from fastmcp import FastMCP
from loguru import logger


# инициализация MCP сервера
mcp = FastMCP('Service tools')

# путь до файлов для тестирования MCP 
# директория mcp_server/data - в docker контейнере это /data
data_dir = (Path(__file__).parent.parent.parent / 'data')
text_file_path = data_dir / 'documents' / 'documents.txt'
logger.debug(f'Путь до файла с текстами: {text_file_path}')
if not text_file_path.exists():
    raise FileNotFoundError(f'Файл с текстами для RAG {text_file_path} не найден')


@mcp.tool()
def get_current_date() -> str:
    '''Показывает текущую дату'''
    return str(date.today())


@mcp.tool()
def get_requirements() -> str:
    """Показывает список библиотек из файла requirements.txt проекта"""
    with open(data_dir / 'documents' / 'requirements.txt', 'r') as f:
        return f.read()


@mcp.tool()
def calculate_expression(expression: str) -> str:
    '''
    Вычисляет математическое выражение.
    
    Args:
        expression: Математическое выражение (например: "2 + 2" или "100 * 0.2")
    '''
    logger.debug(f'Пришедщий запрос в инструмент "calculate_expression": {expression}')
    try:
        # безопасное вычисление только математических операций
        allowed_chars = set('0123456789+-*/(). ')
        if not all(c in allowed_chars for c in expression):
            logger.error('Ошибка при вызове инструмента "calculate_expression": Недопустимые символы в выражении')
            return 'Ошибка при вызове инструмента "calculate_expression": Недопустимые символы в выражении'
        result = eval(expression, {'__builtins__': {}}, {})
        logger.debug(f'Результат вызова инструмента "calculate_expression": {expression} = {result}')
        return f'Результат: {expression} = {result}'
    except Exception as e:
        logger.error(f'Ошибка при вызове инструмента "calculate_expression": {e}')
        return f'Ошибка при вызове инструмента "calculate_expression":: {e}'


if __name__ == '__main__':
    port = int(os.getenv('MCP_PORT', '9000'))
    mcp.run(transport='http', host='127.0.0.1', port=port)
