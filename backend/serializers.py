from schematics import types
from schematics.models import Model

class GetCurrencyModel(Model):
    currency = types.StringType()
    rub_course = types.FloatType()


class ConvertRequestModel(Model):
    from_currency = types.StringType()
    to_currency = types.StringType()
    amount = types.FloatType()

    
class ConvertResponseModel(Model):
    currency = types.StringType()
    amount = types.FloatType()