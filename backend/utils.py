import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from urllib.request import urlopen
from xml.etree.ElementTree import parse


@asyncio.coroutine
def get_db():
    db = AsyncIOMotorClient('db', 27017, username=os.getenv('MONGO_USER'), password=os.getenv('MONGO_PASSWORD'))[
        os.getenv('MONGO_DB')]

    # db = AsyncIOMotorClient('localhost', 27017, username='user', password='password')['testdb']

    return db



async def update_currency():
    print("fetching data...")
    db = await get_db()
    data = urlopen('http://www.cbr.ru/scripts/XML_daily.asp')
    xmldoc = parse(data)

    coll = db.currency_data

    for item in xmldoc.iterfind('Valute'):
        char_code = item.findtext('CharCode')
        value = float(item.findtext('Value').replace(',', '.'))
        item_info = {'char_code': char_code, 'value': value}
        doc = await db.currency_data.find_one({'char_code': char_code})
        if doc:
            await db.currency_data.update_one({'char_code': char_code}, {'$set': {'value': value}})
        else:
            await db.currency_data.insert_one(item_info)



async def scheduled_task(timeout, task):
    while True:
        await task()
        await asyncio.sleep(timeout)


