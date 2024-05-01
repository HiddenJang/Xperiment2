import asyncio
import aiohttp


from parsers.leon.leon_parser import LeonParser
from parsers.betboom.betboom_parser import BetboomParser

async def leon():
    async with aiohttp.ClientSession() as session:
        return await LeonParser(game_type='IceHockey').get_countries_list(session)

async def betboom():
    async with aiohttp.ClientSession() as session:
        return await BetboomParser(game_type=10).get_countries_list(session)

async def get_countries():
    task_1 = asyncio.create_task(leon())
    task_2 = asyncio.create_task(betboom())
    data = await asyncio.gather(task_1, task_2)

    countries = {'leon': [], 'betboom': []}
    for country in data[0]:
        countries['leon'].append(country['country_name'])
    for country in data[1]:
        countries['betboom'].append(country['country_name'])

    return countries

countries = asyncio.run(get_countries())
print(countries)

