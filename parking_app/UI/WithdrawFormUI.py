__author__ = 'adrian'

from PyQt4 import QtGui
from PyQt4 import QtCore

import random

class WithdrawFormUI(QtGui.QWidget):

    def __init__(self, parent=None):
        super(WithdrawFormUI, self).__init__(parent)
        self.initUI()

    def initUI(self):

        self.setWindowTitle('Withdraw Car')
        self.setWindowIcon(QtGui.QIcon('Logo.png'))

        # Patente
        patenteLayout = QtGui.QHBoxLayout()
        lbl1 = QtGui.QLabel("Patente",self)
        self.patente = QtGui.QLineEdit(self)
        self.patente.setInputMask(">AAA-999")
        patenteLayout.addWidget(lbl1)
        patenteLayout.addWidget(self.patente)

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
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

    def acept(self):
        print('Aceptar')
        # Enviar los datos al estacionamiento

    def cancel(self):
        print('Cancelar')
        self.close()

