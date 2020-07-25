import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from urllib.request import urlopen
from xml.etree.ElementTree import parse


@asyncio.coroutine
def setup_db():
    print("HELLLLOOO", os.getenv('MONGO_DB'))
    db = AsyncIOMotorClient('localhost', 27017, username=os.getenv('MONGO_USER'), password=os.getenv('MONGO_PASSWORD'))[
        os.getenv('MONGO_DB')]

    return db


loop = asyncio.get_event_loop()
db = loop.run_until_complete(setup_db())


async def update_currency():
    data = urlopen('http://www.cbr.ru/scripts/XML_daily.asp')
    xmldoc = parse(data)

    coll = db.currency_data

    for item in xmldoc.iterfind('Valute'):
        char_code = item.findtext('CharCode')
        value = float(item.findtext('Value').replace(',', '.'))
        item_info = {'char_code': char_code, 'value': value}
        # old_document = await coll.find_one({'i': 50})
        print("OLD", item_info)
        # result = await db.currency_data.insert_one(item_info)


async def scheduled_task(timeout, task):
    while True:
        print("RUNNING TASK")
        await task()
        await asyncio.sleep(timeout)


# loop.run_until_complete(scheduled_task(60, update_currency))
# import threading
#
# loop = asyncio.get_event_loop()
#
# asyncio.ensure_future(scheduled_task(60, update_currency()))
#
