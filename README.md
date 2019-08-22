# DevAPI

## Pasos antes de ejecutar:
- Setear la variable FLASK_APP:
  - set (export) FLASK_APP=app.py
- Cambiar variables de configuracion en flask-jwt/app.py:
  - SQLALCHEMY_DATABASE_URI
  - SECRET_KEY
  - JWT_SECRET_KEY
- Cambiar en tests/test.py, tests/test_arbitrajetasas.py, cotizaciones.py:
  - HOST
  - PORT
  
## Para ejecutarlo:
flask run --host=HOST

## Cotizaciones (cotizaciones.py):
Se pueden ver todas las puntas que hay para cada ticker en todos los plazos.

