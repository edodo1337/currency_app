from sanic import Sanic
from sanic import response as res
from sanic import response
from urllib.request import urlopen
from xml.etree.ElementTree import parse
import os
import asyncio
from api import api_blueprint
from db import db

app = Sanic(__name__)


@app.route("/")
async def test(req):
    return res.text("I\'m a teapot", status=418)


@app.route(methods=['GET'], uri='api/<valute>')
async def test(request, valute):
    data = urlopen('http://www.cbr.ru/scripts/XML_daily.asp')
    xmldoc = parse(data)

    valute_data = {}

    for item in xmldoc.iterfind('Valute'):
        char_code = item.findtext('CharCode')
        value = float(item.findtext('Value').replace(',', '.'))
        valute_data.update({char_code: value})

    amount = 10
    result = valute_data['AZN'] * amount / valute_data['USD']
    return response.json({"data": result})


@app.listener('testing')
def db_fetch(sanic, loop):
    loop = asyncio.get_event_loop()

    asyncio.ensure_future(scheduled_task(60, update_currency()))


app.blueprint(api_blueprint)

if __name__ == '__main__':
    print("YESSSSSSSSSSSS")
    app.run(host="0.0.0.0", port=8000)
