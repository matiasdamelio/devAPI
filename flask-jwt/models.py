# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 10:51:48 2019

@author: mdamelio
"""

from app import db
import datetime
from passlib.hash import pbkdf2_sha256 as sha256

class UserModel(db.Model):
    __tablename__ = 'dev_users'
    __table_args__ = {'schema': 'tableau'}
    
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()
    
    @classmethod
    def find_idcuenta(cls, username):
        return cls.query.filter_by(username = username).first().id
    
    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                    'username': x.username,
                    'password': x.password
            }
        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}
    
    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}
        
    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
    
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
    
class Bid_OrderBookModel(db.Model):
    __tablename__ = 'dev_orderbook_bid'
    __table_args__ = {'schema': 'tableau'}
    
    idOrden = db.Column(db.Integer, primary_key = True)
    ticker = db.Column(db.String(120), nullable = False)
    fecha = db.Column(db.DateTime, nullable = False)
    cantidad = db.Column(db.Integer, nullable = False)
    precio = db.Column(db.Float, nullable = False)
    plazo = db.Column(db.Integer, nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def find_ordenes(cls, ticker, plazo, precio):
        def to_json(x):
            return {
                    'idOrden':x.idOrden,
                    'Ticker':x.ticker,
                    'Precio':x.precio,
                    'Cantidad':x.cantidad,
                    'Fecha':str(x.fecha)}
#        return list(map(lambda x: to_json(x), Bid_OrderBookModel.query.filter_by(ticker = ticker).filter_by(plazo = plazo).filter(Bid_OrderBookModel.precio >= precio).
#                        order_by(Bid_OrderBookModel.precio.desc()).order_by(Bid_OrderBookModel.fecha).all()))
        ordenes = Bid_OrderBookModel.query.filter_by(ticker = ticker).filter_by(plazo = plazo).filter(Bid_OrderBookModel.precio >= precio).\
            order_by(Bid_OrderBookModel.precio.desc()).order_by(Bid_OrderBookModel.fecha).all()
        if len(ordenes) > 0:
            return list(map(lambda x: to_json(x), ordenes))
        else:
            return {}
    
    @classmethod   
    def remove(cls, idorden):
        cls.query.filter_by(idOrden = idorden).delete()
        db.session.commit()
        
    @classmethod
    def lista_tickers(cls):
        query = db.session.query(Bid_OrderBookModel.ticker.distinct().label("ticker"))
#        query = Bid_OrderBookModel.query.with_entities(Bid_OrderBookModel.ticker, Bid_OrderBookModel.plazo).distinct().all()
        ticker = [row.ticker for row in query.all()]
        
        return ticker
    
    @classmethod
    def best_bid(cls, ticker, plazo):
        return Bid_OrderBookModel.query.filter_by(ticker = ticker).filter_by(plazo = plazo).order_by(Bid_OrderBookModel.precio.desc()).first()

    @classmethod
    def lista(cls):
        def to_json(x):
            return {
                    'Ticker':x.ticker,
                    'Precio':x.precio,
                    'Cantidad':x.cantidad,
                    'Plazo':x.plazo}        
        lista = Bid_OrderBookModel.query.all()
        if len(lista) > 0:
            return (list(map(lambda x: to_json(x), lista)))
        else:
            return {}
        
    @classmethod
    def find(cls, idOrden):
        return cls.query.filter_by(idOrden = idOrden).first()
    
    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}
        
class Ask_OrderBookModel(db.Model):
    __tablename__ = 'dev_orderbook_ask'
    __table_args__= {'schema': 'tableau'}
    
    idOrden = db.Column(db.Integer, primary_key = True)
    ticker = db.Column(db.String(120), nullable = False)
    fecha = db.Column(db.DateTime, nullable = False)
    cantidad = db.Column(db.Integer, nullable = False)
    precio = db.Column(db.Float, nullable = False)
    plazo = db.Column(db.Integer, nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def find_ordenes(cls, ticker, plazo, precio):
        def to_json(x):
            return {
                    'idOrden':x.idOrden,
                    'Ticker':x.ticker,
                    'Precio':x.precio,
                    'Cantidad':x.cantidad,
                    'Fecha':str(x.fecha)}
#        return list(map(lambda x: to_json(x), Ask_OrderBookModel.query.filter_by(ticker = ticker).filter_by(plazo = plazo).filter(Ask_OrderBookModel.precio <= precio).
#                        order_by(Ask_OrderBookModel.precio).order_by(Ask_OrderBookModel.fecha).all()))
        ordenes = Ask_OrderBookModel.query.filter_by(ticker = ticker).filter_by(plazo = plazo).filter(Ask_OrderBookModel.precio <= precio).\
            order_by(Ask_OrderBookModel.precio).order_by(Ask_OrderBookModel.fecha).all()
        if len(ordenes) > 0:
            return list(map(lambda x: to_json(x), ordenes))
        else:
            return {}
    
    @classmethod
    def lista_tickers(cls):
        query = db.session.query(Ask_OrderBookModel.ticker.distinct().label("ticker"))
        ticker = [row.ticker for row in query.all()]
#        query = Ask_OrderBookModel.query.with_entities(Ask_OrderBookModel.ticker, Ask_OrderBookModel.plazo).distinct().all()
        
        return ticker
    
    @classmethod
    def remove(cls, idorden):
        cls.query.filter_by(idOrden = idorden).delete()
        db.session.commit()    
        
    @classmethod
    def best_ask(cls, ticker, plazo):
        return Ask_OrderBookModel.query.filter_by(ticker = ticker).filter_by(plazo = plazo).order_by(Ask_OrderBookModel.precio.desc()).first()
        
    @classmethod
    def lista(cls):
        def to_json(x):
            return {
                    'Ticker':x.ticker,
                    'Precio':x.precio,
                    'Cantidad':x.cantidad,
                    'Plazo':x.plazo}        
        lista = Ask_OrderBookModel.query.all()
        if len(lista) > 0:
            return (list(map(lambda x: to_json(x), lista)))
        else:
            return {}
        
    @classmethod
    def find(cls, idOrden):
        return cls.query.filter_by(idOrden = idOrden).first()
    
    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}
    
class OrderModel(db.Model):
    __tablename__ = 'dev_operations'
    __table_args__ = {'schema': 'tableau'}
    
    idOrden = db.Column(db.Integer, primary_key = True)
    idCuenta = db.Column(db.Integer, nullable = False)
    tipoOperacion = db.Column(db.Integer, nullable = False)
    ticker = db.Column(db.String(120), nullable = False)
    plazo = db.Column(db.Integer, nullable = False)
    idMoneda = db.Column(db.Integer, nullable = False)
    cantidad = db.Column(db.Integer, nullable = False)
    cantidadOperada = db.Column(db.Integer)
    precio = db.Column(db.Float, nullable = False)
    estado = db.Column(db.String(120))
    fecha = db.Column(db.DateTime, nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def find_by_idorden(cls, idOrden):
        return cls.query.filter_by(idOrden = idOrden).first()
    
    @classmethod
    def find_cancelar(cls, idOrden, idCuenta):
        return cls.query.filter_by(idCuenta = idCuenta).filter_by(idOrden = idOrden).first()
    
    @classmethod
    def find_by_idcuenta(cls, idCuenta):
        return cls.query.filter_by(idCuenta = idCuenta).all()
    
    @classmethod
    def find_ordenes(cls, ticker, estado, plazo, tipooperacion):
        def to_json(x):
            return {
                    'idOrden':x.idOrden,
                    'Ticker':x.ticker,
                    'Precio':x.precio,
                    'PrecioOperado':-1,
                    'Plazo':'CI' if x.plazo == 0 else '24 hs' if x.plazo == 1 else '48 hs',
                    'Moneda':'Pesos' if x.idMoneda == 1 else 'Dolares',
                    'Estado': x.estado,
                    'Cantidad':x.cantidad,
                    'CantidadOperada':x.cantidadOperada,
                    'Cancelable':1,
                    'Monto':x.precio*x.cantidad,
                    'Fecha':str(x.fecha),
                    'Operacion':'Compra' if x.tipoOperacion == 1 else 'Venta'}
        return list(map(lambda x: to_json(x), OrderModel.query.filter_by(ticker = ticker).filter_by(plazo = plazo).filter_by(tipoOperacion = tipooperacion).
                        filter_by(estado = estado).filter(OrderModel.fecha >= datetime.datetime.now().date()).all()))
    
    @classmethod
    def return_all_by_idcuenta(cls, idCuenta):
        def to_json(x):
            return {
                    'idOrden':x.idOrden,
                    'Ticker':x.ticker,
                    'Precio':x.precio,
                    'PrecioOperado':-1,
                    'Plazo':'CI' if x.plazo == 0 else '24 hs' if x.plazo == 1 else '48 hs',
                    'Moneda':'Pesos' if x.idMoneda == 1 else 'Dolares',
                    'Estado': x.estado,
                    'Cantidad':x.cantidad,
                    'CantidadOperada':x.cantidadOperada,
                    'Cancelable':1,
                    'Monto':x.precio*x.cantidad,
                    'Fecha':str(x.fecha),
                    'Operacion':'Compra' if x.tipoOperacion == 1 else 'Venta'}
        return list(map(lambda x: to_json(x), OrderModel.query.filter_by(idCuenta = idCuenta).all()))
    
    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}
        
    
class RevokedTokenModel(db.Model):
    __tablename__ = 'dev_revoked_tokens'
    __table_args__ = {'schema': 'tableau'}
    
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))
    
    def add(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)