# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 14:38:53 2019

@author: mdamelio
"""

import DevApi as dev

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

dev.init('http://173.31.3.76:5000', 'test', 'test', 0, on_marketdata) 

dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'A2E7', Plazo = 2, Cantidad = 4000, Precio = 36.4, idMoneda = 1)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 2, Ticker = 'A2E7', Plazo = 2, Cantidad = 1000, Precio = 37, idMoneda = 1)

dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'AA22', Plazo = 2, Cantidad = 1, Precio = 0.6, idMoneda = 1)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 2, Ticker = 'AA22', Plazo = 2, Cantidad = 5543, Precio = 0.92, idMoneda = 1)

dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'AA37', Plazo = 0, Cantidad = 123, Precio = 33.12, idMoneda = 1)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'AA37', Plazo = 2, Cantidad = 123, Precio = 33.8, idMoneda = 1)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 2, Ticker = 'AA37', Plazo = 2, Cantidad = 450, Precio = 34.5, idMoneda = 1)

dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'AC17', Plazo = 0, Cantidad = 1000, Precio = 32, idMoneda = 1)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'AC17', Plazo = 2, Cantidad = 2000, Precio = 34, idMoneda = 1)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 2, Ticker = 'AC17', Plazo = 2, Cantidad = 49000, Precio = 34.5, idMoneda = 1)

dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'AF20', Plazo = 2, Cantidad = 3729, Precio = 42.2, idMoneda = 1)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 2, Ticker = 'AF20', Plazo = 2, Cantidad = 3729, Precio = 42.695, idMoneda = 1)

dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'AO20', Plazo = 0, Cantidad = 941, Precio = 42, idMoneda = 1)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 2, Ticker = 'AO20', Plazo = 0, Cantidad = 475, Precio = 42.15, idMoneda = 1)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'AO20', Plazo = 2, Cantidad = 2643, Precio = 42.32, idMoneda = 1)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 2, Ticker = 'AO20', Plazo = 2, Cantidad = 475, Precio = 42.395, idMoneda = 1)

dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'AY24', Plazo = 0, Cantidad = 2974, Precio = 33.04, idMoneda = 1)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 2, Ticker = 'AY24', Plazo = 0, Cantidad = 1859, Precio = 33.07, idMoneda = 1)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'AY24', Plazo = 2, Cantidad = 1818, Precio = 33.21, idMoneda = 1)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 2, Ticker = 'AY24', Plazo = 2, Cantidad = 13517, Precio = 33.24, idMoneda = 1)

dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'BPLD', Plazo = 2, Cantidad = 220, Precio = 27.4, idMoneda = 1)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 2, Ticker = 'BPLD', Plazo = 2, Cantidad = 280, Precio = 28.89, idMoneda = 1)

dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'DICA', Plazo = 0, Cantidad = 5000, Precio = 49.41, idMoneda = 1)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'DICA', Plazo = 2, Cantidad = 5000, Precio = 49.85, idMoneda = 1)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 2, Ticker = 'DICA', Plazo = 2, Cantidad = 8574, Precio = 50, idMoneda = 1)

dev.operarBYMA(idCuenta = 1, TipoOperacion = 2, Ticker = 'DICP', Plazo = 2, Cantidad = 5870, Precio = 9.9, idMoneda = 1)

dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'DICY', Plazo = 0, Cantidad = 200, Precio = 46.06, idMoneda = 1)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'DICY', Plazo = 2, Cantidad = 200, Precio = 47.01, idMoneda = 1)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 2, Ticker = 'DICY', Plazo = 2, Cantidad = 19541, Precio = 55, idMoneda = 1)

dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'PARY', Plazo = 2, Cantidad = 1960, Precio = 27.36, idMoneda = 1)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 2, Ticker = 'PARY', Plazo = 2, Cantidad = 10100, Precio = 27.6, idMoneda = 1)

dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'PBA25', Plazo = 2, Cantidad = 90000, Precio = 0.775, idMoneda = 1)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 2, Ticker = 'PBA25', Plazo = 2, Cantidad = 274000, Precio = 0.78, idMoneda = 1)

dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'TVPY', Plazo = 2, Cantidad = 500000, Precio = 1.7, idMoneda = 1)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 2, Ticker = 'TVPY', Plazo = 2, Cantidad = 1900, Precio = 1.8, idMoneda = 1)

#dev.operarBYMA(idCuenta = 1, TipoOperacion = 2, Ticker = 'DICA', Plazo = 1, Cantidad = 5000, Precio = 49.782, idMoneda = 1)
#dev.operarBYMA(idCuenta = 1, TipoOperacion = 1, Ticker = 'DICA', Plazo = 1, Cantidad = 15000, Precio = 49.9, idMoneda = 1)

dev.operarBYMA(idCuenta = 1, TipoOperacion = 2, Ticker = 'A2E7', Plazo = 0, Cantidad = 1000, Precio = 36.36, idMoneda = 1)
dev.operarBYMA(idCuenta = 1, TipoOperacion = 2, Ticker = 'AO20', Plazo = 1, Cantidad = 2168, Precio = 42.262, idMoneda = 1)
