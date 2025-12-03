'''
Получение информации об инструментах, ресурсах и промтах MCP сервера
'''

import asyncio
from fastmcp import Client
from loguru import logger


# адрес MCP сервера
MCP_SERVER_URL = 'http://127.0.0.1:9000/mcp'


# функция получения информации об инструментах, ресурсах и промтах MCP сервера
async def get_tools():
    '''Получение информации об инструментах, ресурсах и промтах MCP сервера'''
    async with Client(MCP_SERVER_URL) as client:
        tools = await client.list_tools()
        resources = await client.list_resources()
        prompts = await client.list_prompts()
        
        logger.info(f'\nДоступно инструментов: {len(tools)}')
        for tool in tools:
            logger.info(f'Назввание: {tool.name}\nОписание: {tool.description}')
        logger.info('='*60)

        logger.info(f'\nДоступно ресурсов: {len(resources)}')
        for resource in resources:
            logger.info(f'Название: {resource.name}\nURI: {resource.uri}\nОписание: {resource.description}')
        logger.info('='*60)

        logger.info(f'\nДоступно промптов: {len(prompts)}')
        for prompt in prompts:
            logger.info(f'Название: {prompt.name}:\nОписание:{prompt.description}')
        logger.info('='*60)


asyncio.run(get_tools())