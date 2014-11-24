__author__ = 'adrian'

from PyQt4 import QtGui
from PyQt4 import QtCore

import random

class WarningConfirmationUI(QtGui.QWidget):

    stopAlarm = QtCore.pyqtSignal()

    def __init__(self,parent=None):
        super(WarningConfirmationUI, self).__init__(parent)
        self.initUI()

    def initUI(self):

        self.setWindowTitle('Alarm')
        self.setWindowIcon(QtGui.QIcon('Logo.png'))

        verticalLayout = QtGui.QVBoxLayout()

        # Titulo
        titleLabel = QtGui.QLabel("Alarma",self)
        titleFont = QtGui.QFont()
        titleFont.setBold(True)
        titleFont.setPixelSize(20)
        titleFont.setItalic(True)
        titleLabel.setFont(titleFont)

        # Mensaje
        messageLabel = QtGui.QLabel("Esta seguro que desea apagar esta alarma?",self)

        # Boton de aceptar y cancelar
        buttonLayout = QtGui.QHBoxLayout()
        aceptButton = QtGui.QPushButton('Aceptar')
        aceptButton.clicked.connect(self.acept)
        cancelButton = QtGui.QPushButton('Cancelar')
        cancelButton.clicked.connect(self.cancel)

        buttonLayout.addWidget(aceptButton)
        buttonLayout.addWidget(cancelButton)

        verticalLayout.addWidget(titleLabel)
        verticalLayout.addWidget(messageLabel)
        verticalLayout.addLayout(buttonLayout)

        self.setLayout(verticalLayout)


    def acept(self):
        print('Aceptar')
        self.stopAlarm.emit()
        self.close()

    def cancel(self):
        print('Cancelar')
        self.close()
