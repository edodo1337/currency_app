import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from urllib.request import urlopen
from xml.etree.ElementTree import parse

db = AsyncIOMotorClient('localhost', 27017, username='user', password='password')['testdb']


async def f():
    coll = db.currency_data
    # old_document = await coll.find_one({'i': 50})
    # item_info = {'test': 'hello', 'value': 5}
    # result = await db.currency_data.insert_one(item_info)
    # print("Result", result.inserted_id)

    async for doc in coll.find():
        print(doc)

    # item_info = {'test': 'world', 'value': 10}
    # result = await db.currency_data.insert_one(item_info)
    #
    # item_info = {'test': 'asd', 'value': 10}
    # result = await db.currency_data.insert_one(item_info)
    #
    # print(result)
    #
    # old_document = await coll.find_one({'test': 'asd'})
    # print(old_document)
    # await coll.update_one()


async def pr1():
    while True:
        print("HELLO1")
        await asyncio.sleep(1)


async def pr():
    while True:
        print("HELLO")
        await asyncio.sleep(1)

loop = asyncio.get_event_loop()

loop.create_task(pr())

loop.run_forever()

loop.create_task(pr1())

loop.run_forever()