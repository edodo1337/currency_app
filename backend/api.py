from sanic import Blueprint
import utils
from serializers import GetCurrencyModel, ConvertRequestModel, ConvertResponseModel
from sanic_transmute import add_route,  APIException, add_route, describe



api_blueprint = Blueprint('api', url_prefix='/api')

@describe(paths="/course/{currency}", methods=['GET'])
async def get_currency(request, currency: str) -> GetCurrencyModel:
    db = await utils.get_db()
    doc = await db.currency_data.find_one({'char_code': currency.upper()})
    if not doc:
        raise APIException('currency not found', code=400)
    else:
        return GetCurrencyModel({ 'currency': doc["char_code"], 'rub_course': doc["value"]})

@describe(paths="/convert", methods=['POST'])
async def convert(request, data: ConvertRequestModel) -> ConvertResponseModel:
    try:
        data.validate()
    except Exception as e:
        raise APIException(e.messages, code=400)

    db = await utils.get_db()
    from_cur = await db.currency_data.find_one({'char_code': data.from_currency.upper()})
    to_cur = await db.currency_data.find_one({'char_code': data.to_currency.upper()})

    to_cur_value = None
    from_cur_value = None

    if data.from_currency.upper() == "RUB":
        from_cur_value = 1
    else:
        if not from_cur:
            raise APIException('from_currency not found', code=400)
        else:
            from_cur_value = from_cur['value']
    
    if data.to_currency.upper() == "RUB":
        to_cur_value = 1
    else:
        if not to_cur:
            raise APIException('to_currency not found', code=400)
        else:
            to_cur_value = to_cur['value']
    
    result = from_cur_value * data.amount / to_cur_value

    return ConvertResponseModel({'currency': data.to_currency, 'amount': result})


add_route(api_blueprint, get_currency)
add_route(api_blueprint, convert)