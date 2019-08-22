# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 10:51:59 2019

@author: mdamelio
"""
import datetime
from flask_restful import Resource, reqparse
from models import UserModel, RevokedTokenModel, OrderModel, Bid_OrderBookModel, Ask_OrderBookModel
from flask_jwt_extended import (create_access_token, create_refresh_token, 
                                jwt_required, jwt_refresh_token_required, 
                                get_jwt_identity, get_raw_jwt)
from flask import request
from app import db
from itertools import chain, repeat
import pandas as pd

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {'message':'User {} already exists'.format(data['username'])}
        
        new_user = UserModel(
                username = data['username'],
                password = UserModel.generate_hash(data['password'])
        )
        
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                    'message': 'User {} was created'.format(data['username']),
                    'access_token': access_token,
                    'refresh_token': refresh_token
            }
        except:
            return {'message': 'Something went wrong'}, 500
        
        return data
    
class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        
        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return {'message':'User {} doesn\'t exist'.format(data['username'])}
        
        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {'message':'Logged in as {}'.format(current_user.username),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                    }
        else:
            return {'message': 'Wrong credentials'}, 400

      
class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500
      
        
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token' : access_token}            
      
class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()

    def delete(self):
        return UserModel.delete_all()
                  
class Operar(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()
                       
        new_order = OrderModel(
            idCuenta = int(data['idCuenta']),
            tipoOperacion = int(data['tipoOperacion']),
            ticker = data['ticker'],
            plazo = int(data['plazo']),
            idMoneda = int(data['idMoneda']),
            cantidad = int(data['cantidad']),
            precio = float(data['precio']),
            fecha = datetime.datetime.now(),
            cantidadOperada = -1,
            estado = 'En Ejecucion'
        )
               
        try:
            new_order.save_to_db()
            idOrden = new_order.idOrden
            ticker = new_order.ticker
            fecha = new_order.fecha
            cantidad = new_order.cantidad
            precio = new_order.precio
            plazo = new_order.plazo
            tipo = new_order.tipoOperacion
            
            if tipo == 1:
                new_bookEntry = Bid_OrderBookModel(idOrden = idOrden, fecha = fecha, cantidad = cantidad, precio = precio, plazo = plazo, ticker = ticker)
            elif tipo == 2:
                new_bookEntry = Ask_OrderBookModel(idOrden = idOrden, fecha = fecha, cantidad = cantidad, precio = precio, plazo = plazo, ticker = ticker)            
            
            new_bookEntry.save_to_db()
            
            return {
                    'message': 'Orden ingresada correctamente. Número: {}'.format(new_bookEntry.idOrden),
                    'idOrden': new_bookEntry.idOrden
            }
        except:
            return {'message': 'Something went wrong'}, 500
        
        return data
        
class Cancelar(Resource):
    @jwt_required
    def put(self):
        data = request.get_json()
        
        try:
            orden = OrderModel.find_cancelar(data['idOrden'], data['idCuenta'])
            idOrden = orden.idOrden
            tipo = orden.tipoOperacion
            
            if orden.cantidadOperada == -1 and orden.estado != 'Ejecutada':
                orden.estado = 'Cancelada'
            elif orden.cantidadOperada > 0 and orden.estado != 'Ejecutada':
                orden.estado = 'Parcialmente Cancelada'     
                
            db.session.commit()
            
            if tipo == 1:
                Bid_OrderBookModel.remove(idOrden)
            elif tipo == 2:
                Ask_OrderBookModel.remove(idOrden)
            
            return {'message':'Cancelación solicitada para la orden {}'.format(data['idOrden'])}
        except:
            return {'message':'Something went wrong'}, 500
                
class EstadoDeCuenta(Resource):
    @jwt_required
    def get(self):
        data = request.get_json()
        
        idcuenta = UserModel.find_idcuenta(data['username'])
        
        try:
            if idcuenta == data['idCuenta']:
                ordenes = OrderModel.return_all_by_idcuenta(data['idCuenta'])
                return {'Cotizacion':{}, 'liquidez':{}, 'ordenes':ordenes, 'tenencia':{}, 'tenenciaActual':{}, 'tenenciaAnterior':{}}
            else:
                return {'Descripcion': 'Acceso Denegado', 'CodigoError': -1004}, 403
        except:
            return {'Descripcion': 'Acceso Denegado', 'CodigoError': -1004}, 403
                        
class getMarketData(Resource):
    @jwt_required
    def get(self):
        try:
            tickers_ask = Ask_OrderBookModel.lista_tickers()
            tickers_bid = Bid_OrderBookModel.lista_tickers()
          
            lista_tickers = list(set(tickers_ask + tickers_bid))
            plazos = [0, 1, 2]
            
            df = pd.DataFrame(columns = ['ticker', 'plazo', 'cc', 'pc', 'pv', 'cv', 'u', 'ant', 'v'])
            
            df['ticker'] = list(chain.from_iterable(zip(*repeat(lista_tickers, 3))))
            df['plazo'] = plazos*len(lista_tickers)
            df[['cc', 'pc', 'pv', 'cv', 'u', 'ant', 'v']] = -1
            
            for tick in tickers_bid:
                for pl in plazos:
                    best = Bid_OrderBookModel.best_bid(tick, pl)
                    if best != None:
                        df.loc[(df.ticker == tick) & (df.plazo == pl),'pc'] = best.precio
                        df.loc[(df.ticker == tick) & (df.plazo == pl),'cc'] = best.cantidad
            
            for tick in tickers_ask:
                for pl in plazos:
                    best = Ask_OrderBookModel.best_ask(tick, pl)
                    if best != None:
                        df.loc[(df.ticker == tick) & (df.plazo == pl),'pv'] = best.precio
                        df.loc[(df.ticker == tick) & (df.plazo == pl),'cv'] = best.cantidad
    
            plazos = ['CI', '24hs', '48hs']
            df['plazo'] = plazos*len(lista_tickers)
            
            return {'cotizaciones': df.to_dict(orient='row'), 'indice': []}
        
        except:
            return {'message': 'Error'}, 400
                    
class ConfirmarOperacion(Resource):
    @jwt_required
    def put(self):
        data = request.get_json()
                
        try:
            ticker = data['ticker']
            plazo = data['plazo']
            tipo = data['tipooperacion']
            cantidad = data['cantidad']
            precio = data['precio']
            idorden = data['idOrden']
                        
            if tipo == 1:
                
                orderbook = Ask_OrderBookModel.find_ordenes(ticker, plazo, precio)
                if len(orderbook) == 0:
                    return {'message': 'Order {} submitted'.format(idorden)}, 200
                
                filled = 0
                consumed_asks = []
                
                if precio >= min([x['Precio'] for x in orderbook]):    
                    
                    for i in range(len(orderbook)):
                        ask = orderbook[i]
                        
                        if ask['Precio'] > precio:
                            continue # Precio del ask demasiado alto
                        elif filled == cantidad:
                            break # La orden ya se lleno
                            
                        if filled + ask['Cantidad'] <= cantidad:
                            filled += ask['Cantidad']
                            consumed_asks.append(ask)
                        elif filled + ask['Cantidad'] > cantidad:
                            volume = cantidad - filled
                            filled += volume
                            
                            orden = Ask_OrderBookModel.find(ask['idOrden'])
                            orden.cantidad -= volume
                            db.session.commit()
                            
                            orden = OrderModel.find_by_idorden(ask['idOrden'])
                            if orden.cantidadOperada != -1:
                                orden.cantidadOperada += volume
                            else:
                                orden.cantidadOperada = volume
                            db.session.commit()
                                                                           
                    if filled < cantidad:
                        orden = Bid_OrderBookModel.find(idorden)
                        orden.cantidad = cantidad - filled
                        db.session.commit()
                        orden = OrderModel.find_by_idorden(idorden)
                        orden.cantidadOperada = filled
                        db.session.commit()                        
                    elif filled == cantidad:
                        print(filled)
                        Bid_OrderBookModel.remove(idorden)
                        orden = OrderModel.find_by_idorden(idorden)
                        print(orden.estado, orden.cantidadOperada)
                        orden.estado = 'Ejecutada'
                        orden.cantidadOperada = cantidad
                        db.session.commit()
                        print(orden.estado, orden.cantidadOperada)
                        
                    for ask in consumed_asks:
                        Ask_OrderBookModel.remove(ask['idOrden'])
                        orden = OrderModel.find_by_idorden(ask['idOrden'])
                        orden.estado = 'Ejecutada'
                        orden.cantidadOperada = orden.cantidad
                        db.session.commit()
                        
                if filled >0:
                    return {'message':'Order {} filled.'.format(idorden)}, 200
                else:
                    return {'message': 'Order {} submitted'.format(idorden)}, 200
                        
            elif tipo == 2:
                
                orderbook = Bid_OrderBookModel.find_ordenes(ticker, plazo, precio)
                if len(orderbook) == 0:
                    return {'message': 'Order {} submitted'.format(idorden)}, 200
               
                filled = 0
                consumed_bids = []
                
                if precio <= max([x['Precio'] for x in orderbook]):
                    
                    for i in range(len(orderbook)):
                        bid = orderbook[i]
                        
                        if bid['Precio'] < precio:
                            continue
                        elif filled == cantidad:
                            break
                        
                        if filled + bid['Cantidad'] <= cantidad:
                            filled += bid['Cantidad']
                            consumed_bids.append(bid)
                        elif filled + bid['Cantidad'] > cantidad:
                            volume = cantidad - filled
                            filled += volume
                            
                            orden = Bid_OrderBookModel.find(bid['idOrden'])
                            orden.cantidad -= volume
                            db.session.commit()
                            
                            orden = OrderModel.find_by_idorden(bid['idOrden'])
                            if orden.cantidadOperada != -1:
                                orden.cantidadOperada += volume
                            else:
                                orden.cantidadOperada = volume
                            db.session.commit()
                            
                    if filled < cantidad:
                        orden = Ask_OrderBookModel.find(idorden)
                        orden.cantidad = cantidad - filled
                        db.session.commit()
                        orden = OrderModel.find_by_idorden(idorden)
                        orden.cantidadOperada = filled
                        db.session.commit()                        
                    elif filled == cantidad:
                        Ask_OrderBookModel.remove(idorden)
                        orden = OrderModel.find_by_idorden(idorden)
                        orden.estado = 'Ejecutada'
                        orden.cantidadOperada = cantidad
                        db.session.commit()
                        
                    for bid in consumed_bids:
                        Bid_OrderBookModel.remove(bid['idOrden'])
                        orden = OrderModel.find_by_idorden(bid['idOrden'])
                        orden.estado = 'Ejecutada'
                        orden.cantidadOperada = orden.cantidad
                        db.session.commit()
                        
                if filled >0:
                    return {'message':'Order {} filled.'.format(idorden)}, 200
                else:
                    return {'message': 'Order {} submitted'.format(idorden)}, 200                 
                        
        except:
            return {'Something went wrong'}, 500
        
class BorrarTodo(Resource):
        def delete(self):
            try:
                ordenes = OrderModel.delete_all()
                print(ordenes['message'])
                ask = Ask_OrderBookModel.delete_all()
                print(ask['message'])
                bid = Bid_OrderBookModel.delete_all()
                print(bid['message'])
                return 0
            except:
                return {'Something went wrong'}, 500