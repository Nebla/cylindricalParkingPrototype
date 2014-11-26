__author__ = 'adrian'

from PyQt4 import QtGui
from PyQt4 import QtCore

from parking_app.UI.WarningConfirmationUI import WarningConfirmationUI

import parking_app.Common as Common

import random

class SlotUI(QtGui.QWidget):

    def __init__(self):
        super(SlotUI, self).__init__()
        self.initUI()

    def initUI(self):

        vertical = QtGui.QVBoxLayout()


        # Vehicle ID
        self.btn_patente = QtGui.QPushButton('AAA-000',self)
        self.btn_patente.clicked.connect(self.withdraw_vehicle)


        self.lbl_vehicle = QtGui.QLabel(self)
        vertical.addWidget(self.lbl_vehicle)

        self.setLayout(vertical)

        color = QtGui.QColor(150, 150, 150)
        self.setBackgroundColor(color)

        self.btn_patente.setHidden(True)
        self.lbl_vehicle.setHidden(True)

    def withdraw_vehicle(self):

        print("Mostrar mensaje de confirmacion")


    def setBackgroundColor(self, color):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)

    def updateUI(self, vehicle_patent, vehicle_weight):


        self.lbl_vehicle.setHidden(False)
        self.btn_patente.setHidden(False)

        # Vehicle ID
        self.btn_patente.setText(vehicle_patent)

        # Current vehicle
        color = QtGui.QColor(100, 100, 255)

        vehicleName = ''
        if vehicle_weight == Common.Weights.veryLight.value:
            vehicleName = 'MotoSide.png'
        elif vehicle_weight == Common.Weights.light.value:
            vehicleName = 'CarSide.png'
        elif vehicle_weight == Common.Weights.heavy.value:
            vehicleName = 'AutoTruckSide.png'
        elif vehicle_weight == Common.Weights.veryHeavy.value:
            vehicleName = 'TrukSide.png'
        elif vehicle_weight == Common.Weights.empty.value:
            color = QtGui.QColor(150, 150, 150)
            self.lbl_vehicle.setHidden(False)
            self.btn_patente.setHidden(False)


        pixmap2 = QtGui.QPixmap(vehicleName)
        pixmap2 = pixmap2.scaled(40, 40, QtCore.Qt.KeepAspectRatio)
        self.lbl_vehicle.setPixmap(pixmap2)

        self.setBackgroundColor(color)
