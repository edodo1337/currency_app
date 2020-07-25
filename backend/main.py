from sanic import Sanic
from sanic import response as res
from sanic import response
from urllib.request import urlopen
from xml.etree.ElementTree import parse
import os
import asyncio
from api import api_blueprint
import utils
from sanic_transmute import describe, add_route, add_swagger, APIException


app = Sanic(__name__)


@app.route("/")
async def test(req):
    return res.text("I\'m a teapot", status=418)


app.blueprint(api_blueprint)

add_swagger(app, "/api/v1/swagger.json", "/api/v1/")

if __name__ == '__main__':
    print("Server running")
    server = app.create_server(host="0.0.0.0", port=8000, return_asyncio_server=True)
    loop = asyncio.get_event_loop()
    data_fetch = asyncio.ensure_future(utils.scheduled_task(60, utils.update_currency))
    server_task = asyncio.ensure_future(server)

    try:
        loop.run_forever()
    except:
        loop.stop()
