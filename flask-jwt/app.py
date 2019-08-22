# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 10:50:09 2019

@author: mdamelio
"""

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import datetime

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://DB_USER:PASSWORD@HOST:PORT/DATABASE'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'XXXXX'

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all() 

app.config['JWT_SECRET_KEY'] = 'XXXXX'
jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)

@jwt.invalid_token_loader
def invalid_token_callback(invalid_token):
    return {'message': 'The token is invalid'}, 400

import models, resources

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.Operar, '/operar')
api.add_resource(resources.Cancelar, '/cancelar')
api.add_resource(resources.EstadoDeCuenta, '/estadodecuenta')
api.add_resource(resources.ConfirmarOperacion, '/confirmar')
api.add_resource(resources.getMarketData, '/getmarketdata')
api.add_resource(resources.BorrarTodo, '/borrartodo')

if __name__=='__main__':
    app.run()
