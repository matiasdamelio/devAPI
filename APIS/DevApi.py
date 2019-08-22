# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 13:37:30 2019

@author: mdamelio
"""
   
import requests  

def registration(base_urlParam, username, password):
    
    base_url = base_urlParam
    
    final_url = "{0}/registration".format(base_url)
    payload = {'username':username, 'password':password}
    headers = {'content-type': 'application/json'}
    
    response = requests.post(final_url, json = payload, headers = headers)
    
    if response.status_code == 200:
        print(response.json()['message'])
        return 0
    else:
        print(response.json()['message'])
        return -1

def init(base_urlParam, usernameParam, password, codigo4DParam, marketdata_handlerParam):
    
    global AccessToken, base_url, username, marketdata_handler
    
    base_url = base_urlParam
    username = usernameParam
    marketdata_handler = marketdata_handlerParam
    
    final_url = "{0}/login".format(base_url)
    payload = {'username':username, 'password':password}
    headers = {'content-type': 'application/json'}
    
    print("Iniciando sesion para usuario " + username)
    
    response = requests.post(final_url, json = payload, headers = headers)
    
    if response.status_code == 200:
        AccessToken = response.json()['access_token']
        print("Login exitoso.")
        return 0
    else:
        print("Error en login. " + response.json()['message'])
        return -1

def logout():
    print('Logging OUT')
    headers = {'Content-type': 'application/json', 'Accept':'application/json', 'Authorization': 'Bearer ' + AccessToken}
    final_url = '{0}/logout/access'.format(base_url)
    response = requests.post(final_url, headers = headers)
    try:
        if response.status_code == 200:
            print('Logout correcto!')
            print(response.json()['message'])
            return 0
        else:
            print(response.json()['message'])
            return -1
    except:
        return -1

def operarBYMA(idCuenta, TipoOperacion, Ticker, Plazo, Cantidad, Precio, idMoneda):
    print("Operando ",Cantidad," ",Ticker+"@",Precio, " - Operacion de", "Compra" if TipoOperacion==1 else "Venta")
    headers = {"Content-type": "application/json", "Accept": "application/json", 'Authorization': 'Bearer ' + AccessToken}
    final_url="{0}/operar".format(base_url)
    payload = {"idCuenta": idCuenta, "tipoOperacion": TipoOperacion,"ticker": Ticker, "plazo": Plazo, "idMoneda": idMoneda, "cantidad": Cantidad, "precio": Precio} 
    response = requests.post(final_url, json = payload, headers = headers)
#    print(response.json())
    if(response.status_code == 200):
        idOrden = response.json()["idOrden"]
        print("Confirmando Orden ",idOrden)
        final_url="{0}/confirmar".format(base_url)
        payload = {"idOrden":idOrden, "ticker": Ticker, "plazo": Plazo, "tipooperacion": TipoOperacion,"plazo": Plazo,"cantidad": Cantidad, "precio": Precio}
#        print(payload)
        response = requests.put(final_url, json = payload, headers = headers)
        if(response.status_code == 200):
            print(response.json())
            return idOrden
        else:
            print("Error confirmando operacion")
            return -1        
    else:	
        print("Error insertando operacion")
        print(response.status_code, response.reason)
        return -1 #response.json()["Descripcion"]

def cancelarOrden(idCuenta, idOrden):
    print("Cancelando Orden",idOrden,"de la cuenta",idCuenta)
    headers = {"Content-type": "application/json", "Accept": "application/json", 'Authorization': 'Bearer ' + AccessToken}
    final_url="{0}/cancelar".format(base_url)
    payload = {"idCuenta":idCuenta, "idOrden":idOrden}
    response = requests.put(final_url, json=payload, headers=headers)
    if(response.status_code == 200):
        print(response.json()["message"])
        return idOrden
    else:	
        print("Error cancelando orden")
        print(response.status_code, response.reason)
        print(response.json()["message"])
        return -1    

def estadodecuenta(idCuenta, fecha):
	headers = {"Accept": "application/json", 'Authorization': 'Bearer ' + AccessToken}
	payload = {"idCuenta":idCuenta, "username":username}
	final_url="{0}/estadodecuenta".format(base_url)
	response = requests.get(final_url, json=payload, headers=headers)
	if(response.status_code == 200):
		return response.json()
	else:	
		print("Error obteniendo tenencia")
		print(response.status_code, response.reason)
		return response.json()
    
def GetMarketData(marketdata_handler):
    data = []
    headers = {"Content-type": "application/json", "Accept": "application/json", "Authorization": "Bearer " + AccessToken}
    final_url = "{0}/getmarketdata".format(base_url)
    response = requests.get(final_url, headers = headers)
    response = requests.get(final_url, headers = headers)
    if(response.status_code == 200):
        for c in response.json()['cotizaciones']:
            data.append(marketdata_handler(3, c))
    return data

def Borrar():
    headers = {"Accept": "application/json", 'Authorization': 'Bearer ' + AccessToken}
    final_url="{0}/borrartodo".format(base_url)
    response = requests.delete(final_url, headers = headers)
    if(response.status_code == 200):
        return 0
    else:
        return -1