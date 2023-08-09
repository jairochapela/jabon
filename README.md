# Servicio SOAP

Este programa despliega un servicio SOAP que permite la conversión entre divisas. El servicio en cuestión permite la invocación remota de un procedimiento que recibe una cantidad en una divisa y también la divisa a la que se desea realizar la conversión. Como resultado, el servicio entrega el valor del cambio para esa cantidad entre las dos divisas especificadas.

## Preparativos

Este programa depende de algunas librerías externas que han de instalarse para que el servicio funcione. Para ello, se procederá con el comando `pip install -r requirements.txt`. Si se desea trabajar con un entorno virtual de ejecución, la secuencia de comandos a introducir es la que sigue:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
(Adáptense estas órdenes al sistema o plataforma que proceda.)

## Puesta en marcha del servicio en un entorno de pruebas

Basta con ejecutar el programa `webservice.py` como un script normal. Desde el terminal:

```sh
python3 webservice.py
```

El servicio quedará operativo, sirviéndose en el puerto 8000, hasta que se interrumpa su ejecución.

## Prueba del servicio

Se recomienda utilizar una aplicación como SoapUI para realizar las pruebas. Para ello, se le indicará a este la ruta al WSDL que contiene las descripciones de las llamadas:

[http://localhost:8000/?wsdl](http://localhost:8000/?wsdl)

SoapUI identificará automáticamente todas las llamadas que ofrece el servicio web y creará los ficheros XML necesarios para invocarlo.
