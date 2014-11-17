__author__ = 'adrian'

from PyQt4 import QtGui
from PyQt4 import QtCore

import random

class CarFormUI(QtGui.QWidget):

    def __init__(self):
        super(CarFormUI, self).__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle('New Car')

        # Patente
        patenteLayout = QtGui.QHBoxLayout()
        lbl1 = QtGui.QLabel("Patente",self)
        self.patente = QtGui.QTextEdit(self)
        self.patente.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        patenteLayout.addWidget(lbl1)
        patenteLayout.addWidget(self.patente)

        #Tipo de vehiculo
        vehicle = QtGui.QComboBox()
        vehicle.addItem('Moto')
        vehicle.addItem('Auto')
        vehicle.addItem('Camioneta')
        vehicle.addItem('Camion')

        # Boton de aceptar y cancelar
        buttonLayout = QtGui.QHBoxLayout()
        aceptButton = QtGui.QPushButton('Aceptar')
        aceptButton.clicked.connect(self.acept)
        cancelButton = QtGui.QPushButton('Cancelar')
        cancelButton.clicked.connect(self.cancel)

        buttonLayout.addWidget(aceptButton)
        buttonLayout.addWidget(cancelButton)

        layout = QtGui.QVBoxLayout()
        layout.addLayout(patenteLayout)
        layout.addWidget(vehicle)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)


    def acept(self):
        print('Aceptar')
        # Enviar los datos al estacionamiento

    def cancel(self):
        print('Cancelar')
        self.close()
