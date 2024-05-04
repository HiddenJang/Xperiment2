import asyncio
import aiohttp

from parsers.leon.leon_parser import LeonParser
from parsers.betboom.betboom_parser import BetboomParser
from mapping import get_regions_map

######################## leon ##########################
async def get_regions_list_leon(game_type: str) -> dict:
    async with aiohttp.ClientSession() as session:
        return await LeonParser(game_type=game_type).get_regions_list(session)

async def get_leagues_list_leon(game_type: str) -> dict:
    async with aiohttp.ClientSession() as session:
        return await LeonParser(game_type=game_type).get_all_leagues_data(session)

async def get_region_events_leon(game_type: str, betline: str, market: str, region: str) -> dict:
    return await LeonParser(game_type=game_type, betline=betline, market=market, region=region).start_parse()

######################## betboom ##########################
async def get_regions_list_betboom(game_type: str) -> dict:
    async with aiohttp.ClientSession() as session:
        return await BetboomParser(game_type=game_type).get_regions_list(session)

async def get_leagues_list_betboom(game_type: str) -> dict:
    async with aiohttp.ClientSession() as session:
        return await BetboomParser(game_type=game_type).get_all_leagues_data(session)

async def get_region_events_betboom(game_type: str, betline: str, market: str, region: str) -> dict:
    return await BetboomParser(game_type=game_type, betline=betline, market=market, region=region).start_parse()

######## starters ############
async def get_regions(game_type: str):
    task_leon = asyncio.create_task(get_regions_list_leon(game_type=game_type))
    task_betboom = asyncio.create_task(get_regions_list_betboom(game_type=game_type))
    return await asyncio.gather(task_leon, task_betboom)

async def get_leagues(game_type: str):
    task_leon = asyncio.create_task(get_leagues_list_leon(game_type=game_type))
    task_betboom = asyncio.create_task(get_leagues_list_betboom(game_type=game_type))
    return await asyncio.gather(task_leon, task_betboom)

async def get_events(game_type: str, betline: str, market: str, regions_map: dict):
    for region_data in regions_map.values():
        region_leon = list(region_data.get('leon').keys())[0]
        region_betboom = list(region_data.get('betboom').keys())[0]
        task_leon = asyncio.create_task(get_region_events_leon(game_type=game_type, betline=betline, market=market, region=region_leon))
        task_betboom = asyncio.create_task(get_region_events_betboom(game_type=game_type, betline=betline, market=market, region=region_betboom))
        yield await asyncio.gather(task_leon, task_betboom)

async def task_starter(regions_map: dict):
    async for value in get_events(game_type="Soccer", betline='prematch', market='Тотал', regions_map=regions_map):
        print(value)


    # tasks = []
    # for region_data in regions_map.values():
    #     task = asyncio.create_task(get_events(game_type="Soccer", betline='prematch', market='Тотал', region_data=region_data))
    #     tasks.append(task)
    #     event = await task
        #print(event)

if __name__ == '__main__':
    import time
    import pprint
    ###### countries
    for _ in range(1):
        start_time = time.time()
        regions_data = asyncio.run(get_regions(game_type="Soccer"))
        regions_map = get_regions_map(regions_data)
        print(regions_map)
        print('regions mapping is done!')
        events = asyncio.run(task_starter(regions_map))

        stop_time = time.time() - start_time
        print(len(regions_map))
        print(events)
        print(len(events))
        print(stop_time)



