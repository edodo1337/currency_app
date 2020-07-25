from sanic import Blueprint
from sanic.response import file, json
from db import db

api_blueprint = Blueprint('api', url_prefix='/api')


@api_blueprint.route(methods=['GET'], uri='/course/<currency>')
async def get_currency(request, currency):
    return json({'msg': 'hi from blueprint'})
