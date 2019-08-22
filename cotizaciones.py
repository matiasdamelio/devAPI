# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 14:28:02 2019

@author: mdamelio
"""

from gui_ui import Ui_MainWindow

import APIS.DevApi as dev

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtGui, QtWidgets, QtCore

import sys
import time
from itertools import chain, repeat

global logueado

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

def setColorRow(table, rowIndex, color):
    for j in range(table.columnCount()):
        table.item(rowIndex, j).setBackground(color)

class Loop(QThread):
    
    signalModificacion = pyqtSignal(object)

    
    def __init__(self):
        QThread.__init__(self)
        self.running = True
       
    def run(self):
        
        while self.running:
        
            data = dev.GetMarketData(on_marketdata)
            
            self.signalModificacion.emit(data) 
            
            time.sleep(1)
    

class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.title = 'DevAPI - Cotizaciones'
        self.initUI()
        self.show()
        self.closeEvent
        
    def initUI(self):
        
        global logueado
        logueado = False
        
        self.threads = []
        
        self.setWindowTitle(self.title)
        self.setGeometry(200,30,700,1000)
    
        self.cargarTabla()
        self.tableWidget.setEnabled(False)
        
        user = 'mdamelio'
        passw = 'matias2019'
        codigo = 1111
        
        dev.init('http://173.31.3.76:5000', user, passw, codigo, on_marketdata)
        
        self.tableWidget.setEnabled(True)
                       
        self.workerLoop = Loop()
        self.workerLoop.signalModificacion.connect(self.modificarTabla)

        self.threads.append(self.workerLoop)
        self.workerLoop.start()
                
    def modificarTabla(self, data):
        
        
        rows = self.tableWidget.rowCount()      
        
        for i in range(len(data)):
                           
            for row in range(rows):
                if (data[i][0] == self.tableWidget.item(row,0).text()) and (data[i][1] == self.tableWidget.item(row,1).text()):
                    rowTicker = row
                    
            valor = '' if data[i][3] <= 0 else str(data[i][3])
            self.tableWidget.item(rowTicker, 2).setText(valor)
            valor = '' if data[i][4] <= 0 else str(data[i][4])
            self.tableWidget.item(rowTicker, 3).setText(valor)
            valor = '' if data[i][5] <= 0 else str(data[i][5])
            self.tableWidget.item(rowTicker, 4).setText(valor)
            valor = '' if data[i][6] <= 0 else str(data[i][6])
            self.tableWidget.item(rowTicker, 5).setText(valor)

    def cargarTabla(self):        
        
        self.tableWidget.setColumnCount(6)
        
        tickers = ['A2E7', 'AA21', 'AA22', 'AA37', 'AA46', 'AC17', 'AF20', 'AO20', 'AY24',
                   'BDC24', 'BPLD', 'DICA', 'DICP', 'DICY', 'PARY', 'PBA25', 'TC25P', 'TVPY']
        
        plazos = ['CI', '24hs', '48hs']
        
        tickers_lista = list(chain.from_iterable(zip(*repeat(tickers, 3))))
        plazos_lista = plazos*len(tickers)
        
        self.tableWidget.setRowCount(len(tickers_lista))
        self.tableWidget.setHorizontalHeaderLabels(('Ticker','Plazo','Cant. Compra','Compra','Venta','Cant. Venta'))
        
        row = 0
        for ticker in tickers_lista:
            cellinfo = QtWidgets.QTableWidgetItem(ticker)  
            cellinfo.setFlags(QtCore.Qt.ItemIsEnabled)
                                       
            plazo = QtWidgets.QTableWidgetItem(plazos_lista[row])
            cc = QtWidgets.QTableWidgetItem()
            pc = QtWidgets.QTableWidgetItem()
            pv = QtWidgets.QTableWidgetItem()  
            cv = QtWidgets.QTableWidgetItem()  

            self.tableWidget.setItem(row,0,cellinfo)     
            self.tableWidget.setItem(row,1,plazo) 
            self.tableWidget.setItem(row,2,cc) 
            self.tableWidget.setItem(row,3,pc) 
            self.tableWidget.setItem(row,4,pv) 
            self.tableWidget.setItem(row,5,cv) 

            
            cellinfo.setTextAlignment(QtCore.Qt.AlignCenter)
            plazo.setTextAlignment(QtCore.Qt.AlignCenter)
            cc.setTextAlignment(QtCore.Qt.AlignCenter)
            pc.setTextAlignment(QtCore.Qt.AlignCenter)
            pv.setTextAlignment(QtCore.Qt.AlignCenter)
            cv.setTextAlignment(QtCore.Qt.AlignCenter)
                                                 
            row += 1
                            
        rows = self.tableWidget.rowCount()
        self.tableWidget.blockSignals(True)
        for row in range(rows):
            for i in range(0,6):                
                flags = self.tableWidget.item(row,i).flags()
                flags &= ~QtCore.Qt.ItemIsEnabled
                self.tableWidget.item(row,i).setFlags(flags) 
        self.tableWidget.blockSignals(False)
               
        for row in range(rows):
            if row % 2:
                setColorRow(self.tableWidget, row, QtGui.QColor(135,216,230,150))
        

if __name__ == "__main__":
#    settings.init()
    app = QApplication(sys.argv)
    form = MainWindow()
    sys.exit(app.exec_())
