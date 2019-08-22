# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 13:00:49 2019

@author: mdamelio
"""

import APIS.DevApi as dev

def on_marketdata(tipo, data):
    if(tipo == 1):
        #aca va el codigo de manejo de market data
        return(data["ticker"],data["plazo"],data["mo"],data["cc"],data["pc"],data["pv"],data["cv"],data["u"],data["ant"],data["v"])
    if(tipo == 2):
        #aca va el manejo de indice bonos si es necesario.
        #print("Bonos", data)
        return(data["ticker"],data["plazo"],data["mo"],data["cc"],data["pc"],data["pv"],data["cv"],data["u"],data["ant"],data["v"])
    if(tipo == 3):
        #aca va el manejo de indice bonos si es necesario.
        #print("Watch", data)
        return(data["ticker"],data["plazo"],"",data["cc"],data["pc"],data["pv"],data["cv"],data["u"],data["ant"],data["v"])
    if(tipo == 4):
        #aca va el manejo de indice bonos si es necesario.
        #print("Watch", data)
        return(data["ticker"],data["plazo"],data["u"])

dev.init('http://127.0.0.1:5000', 'mdamelio', 'matias2010', 0, on_marketdata) 
dev.operarBYMA(idCuenta = 2, TipoOperacion = 1, Ticker = 'AF20', Plazo = 2, Cantidad = 250, Precio = 41.5, idMoneda = 1) # idOrden = 1
dev.operarBYMA(idCuenta = 2, TipoOperacion = 1, Ticker = 'AO20', Plazo = 0, Cantidad = 6000, Precio = 41.06, idMoneda = 1) # idOrden = 2
dev.operarBYMA(idCuenta = 2, TipoOperacion = 2, Ticker = 'AY24', Plazo = 0, Cantidad = 1500, Precio = 32.345, idMoneda = 1) # idOrden = 3
dev.operarBYMA(idCuenta = 2, TipoOperacion = 1, Ticker = 'AY24', Plazo = 2, Cantidad = 780, Precio = 32.4, idMoneda = 1) # idOrden = 4
dev.operarBYMA(idCuenta = 2, TipoOperacion = 1, Ticker = 'AY24', Plazo = 2, Cantidad = 750, Precio = 32.4, idMoneda = 1) # idOrden = 5
dev.operarBYMA(idCuenta = 2, TipoOperacion = 2, Ticker = 'PBA25', Plazo = 0, Cantidad = 575, Precio = 0.788, idMoneda = 1) # idOrden = 6
dev.operarBYMA(idCuenta = 2, TipoOperacion = 1, Ticker = 'PBA25', Plazo = 2, Cantidad = 575, Precio = 0.7765, idMoneda = 1) # idOrden = 7
estado2 = dev.estadodecuenta(2)
dev.logout()

dev.init('http://127.0.0.1:5000', 'test', 'test', 0, on_marketdata)   
dev.operarBYMA(idCuenta = 1, TipoOperacion = 2, Ticker = 'AF20', Plazo = 2, Cantidad = 300, Precio = 41.5, idMoneda = 1) # idOrden = 8 # Deberian sobrar 50
dev.operarBYMA(idCuenta = 1, TipoOperacion = 2, Ticker = 'AO20', Plazo = 0, Cantidad = 5500, Precio = 41, idMoneda = 1) # idOrden = 9 # Deberian sobrar 50 
dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'AY24', Plazo = 0, Cantidad = 1500, Precio = 32.3, idMoneda = 1) # idOrden = 10 # No se deberia ejecutar
dev.operarBYMA(idCuenta = 1, TipoOperacion = 2, Ticker = 'AY24', Plazo = 2, Cantidad = 780, Precio = 32.4, idMoneda = 1) # idOrden = 11 # Deberia quedar en 0
dev.operarBYMA(idCuenta = 1, TipoOperacion = 2, Ticker = 'AY24', Plazo = 2, Cantidad = 750, Precio = 32.4, idMoneda = 1) # idOrden = 12 # Deberian sobrar 0
dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'PBA25', Plazo = 0, Cantidad = 575, Precio = 0.788, idMoneda = 1) # idOrden = 13 # 0
dev.operarBYMA(idCuenta = 1, TipoOperacion = 2, Ticker = 'PBA25', Plazo = 2, Cantidad = 575, Precio = 0.7765, idMoneda = 1) # idOrden = 14 # 0
estado1 = dev.estadodecuenta(1)
dev.logout()

dev.init('http://127.0.0.1:5000', 'test', 'test', 0, on_marketdata)   
dev.cancelarOrden(1, 8)
dev.logout()
dev.init('http://127.0.0.1:5000', 'mdamelio', 'matias2010', 0, on_marketdata) 
dev.cancelarOrden(2, 2)
dev.logout()

dev.init('http://127.0.0.1:5000', 'test', 'test', 0, on_marketdata)   
dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'AY24', Plazo = 0, Cantidad = 1500, Precio = 32, idMoneda = 1)
data = dev.GetMarketData(on_marketdata)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'AY24', Plazo = 0, Cantidad = 300, Precio = 33, idMoneda = 1)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'AY24', Plazo = 0, Cantidad = 200, Precio = 33, idMoneda = 1)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'AY24', Plazo = 0, Cantidad = 1100, Precio = 34, idMoneda = 1)

data = dev.GetMarketData(on_marketdata)

dev.init('http://173.31.1.142:5000', 'test', 'test', 0, on_marketdata)  
