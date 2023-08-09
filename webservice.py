import logging
logging.basicConfig(level=logging.DEBUG)

from spyne import Application, rpc, ServiceBase, Integer, Unicode, Double
from spyne import Iterable
from spyne.protocol.soap import Soap11
from spyne.error import InvalidInputError
from spyne.server.wsgi import WsgiApplication

rates = {
    'EUR': 1.0,
    'USD': 1.1,
    'GBP': 0.9,
    'INR': 80.0,
    'AUD': 1.6,
    'CAD': 1.5,
    'SGD': 1.5,
    'CHF': 1.1,
    'MYR': 4.5,
    'JPY': 120.0,
    'CNY': 7.8,
    'NZD': 1.7,
    'THB': 35.0,
    'HUF': 330.0,
    'AED': 4.0,
    'HKD': 8.5,
    'MXN': 21.0,
    'ZAR': 16.0,
    'PHP': 55.0,
    'SEK': 10.0,
    'IDR': 16000.0,
    'SAR': 4.0,
    'BRL': 4.5,
    'TRY': 6.0,
    'KES': 110.0,
    'KRW': 1300.0,
    'EGP': 20.0,
    'IQD': 1300.0,
    'NOK': 10.0,
    'KWD': 0.3,
    'RUB': 70.0,
    'DKK': 7.5,
    'PKR': 160.0,
    'ILS': 4.0,
    'PLN': 4.0,
}


class HelloWorldService(ServiceBase):
    @rpc(_returns=Iterable(Unicode))
    def currencies(ctx):
        for c in rates.keys():
            yield c

    @rpc(Integer, Integer, _returns=Integer)
    def multiply(ctx, x, y):
        return x * y
    
    @rpc(Unicode, Unicode, Double, _returns=Double)
    def convert_currency(ctx, from_currency, to_currency, amount):
        # import requests
        # url = 'https://api.exchangeratesapi.io/latest?base={}&symbols={}'.format(from_currency, to_currency)
        # response = requests.get(url)
        # data = response.json()
        # return data['rates'][to_currency] * amount
        if not from_currency in rates:
            raise InvalidInputError('Currency not supported', from_currency)
        if not to_currency in rates:
            raise InvalidInputError('Currency not supported', to_currency)
        return rates[to_currency]/rates[from_currency] * amount

application = Application([HelloWorldService],
    tns='spyne.examples.hello',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

if __name__ == '__main__':
    # You can use any Wsgi server. Here, we chose
    # Python's built-in wsgi server but you're not
    # supposed to use it in production.
    from wsgiref.simple_server import make_server

    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()