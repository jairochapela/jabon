import logging
from spyne import Application, rpc, ServiceBase, Integer, Unicode, Double
from spyne import Iterable
from spyne.protocol.soap import Soap11
from spyne.error import InvalidInputError
from spyne.server.wsgi import WsgiApplication
from model import EuroExchangeRate

#
# Demostración de programación de un servicio web SOAP con Spyne.
#

logging.basicConfig(level=logging.DEBUG)

# Carga de valores desde CSV
EuroExchangeRate.load_from_csv('eurofxref.csv')

# Clase de servicio SOAP con dos métodos:
# - currencies: devuelve un iterable con las divisas disponibles
# - convert_currency: convierte una cantidad de una divisa a otra
class CurrencyExchangeService(ServiceBase):

    # Método remoto para obtener una lista de divisas.
    # Devuelve un iterable de cadenas Unicode, que finalmente se serializará en XML.
    @rpc(_returns=Iterable(Unicode))
    def currencies(ctx):
        for c in EuroExchangeRate.get_currencies():
            yield c
    
    # Método remoto para convertir una cantidad de una divisa a otra.
    # Recibe tres parámetros:
    # - from_currency: divisa de origen
    # - to_currency: divisa de destino
    # - amount: cantidad a convertir
    # Devuelve un valor Double con el resultado de la conversión, que finalmente se serializará en XML.
    @rpc(Unicode, Unicode, Double, _returns=Double)
    def convert_currency(ctx, from_currency, to_currency, amount):
        try:
            from_rate = EuroExchangeRate.get_rate(from_currency)
            to_rate = EuroExchangeRate.get_rate(to_currency)
            return to_rate/from_rate * amount
        except ValueError as e:
            raise InvalidInputError(e.message, e.args[0])


# Creación de la aplicación SOAP
application = Application([CurrencyExchangeService],
    tns='gal.jairochapela.currencyexchange',
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