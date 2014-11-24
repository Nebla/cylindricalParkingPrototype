__author__ = 'adrian'

from PyQt4 import QtGui
from PyQt4 import QtCore

from parking_app.UI.WarningConfirmationUI import WarningConfirmationUI

import parking_app.Common as Common

import random

class PlatformUI(QtGui.QWidget):

    def __init__(self):
        super(PlatformUI, self).__init__()
        self.initUI()

    def initUI(self):

        vertical = QtGui.QVBoxLayout()
        horizontal = QtGui.QHBoxLayout()

        # Vehicle ID
        self.lbl_patente = QtGui.QLabel('AAAA',self)

        horizontal.addWidget(self.lbl_patente)

        # Alarm
        self.warningButton = QtGui.QPushButton()
        self.warningButton.setIcon(QtGui.QIcon('Warning.png'))
        self.warningButton.setIconSize(QtCore.QSize(15,15))
        self.warningButton.clicked.connect(self.showWarningOffConfirmation)
        self.warningButton.setVisible(False)

        horizontal.addWidget(self.warningButton)

        vertical.addLayout(horizontal)

        self.lbl_vehicle = QtGui.QLabel(self)
        vertical.addWidget(self.lbl_vehicle)

        self.setLayout(vertical)

        color = QtGui.QColor(150, 150, 150)
        self.setBackgroundColor(color)

        self.lbl_vehicle.setHidden(True)
        self.lbl_patente.setHidden(True)

    def showWarningOffConfirmation(self):
        self.confirmationMessage = WarningConfirmationUI()
        self.confirmationMessage.resize(400, 200)
        self.confirmationMessage.move(50,50)

        QtCore.QObject.connect(self.confirmationMessage, QtCore.SIGNAL('stopWarning()'), self.turnOffWarning)

        self.confirmationMessage.show()
        print("Mostrar mensaje de confirmacion")


    def turnOffWarning(self):
        print("Apagando warning")
        self.warningButton.setHidden(True)


    def setBackgroundColor(self, color):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)

    """"
    def update(self):

        color = QtGui.QColor(150, 150, 150)

        self.lbl_vehicle.setHidden(True)
        self.lbl_patente.setHidden(True)

        if not self.platform.is_empty():
            color = QtGui.QColor(100, 100, 255)

            # Vehicle ID
            self.lbl_patente.text(self.platform.vehicle.patent)
            #vertical.addWidget(lbl1)

            # Current vehicle
            vehicleName = ''
            if self.platform.get_weight() == Common.Weights.veryLight:
                vehicleName = 'MotoSide.png'
            elif self.platform.get_weight() == Common.Weights.light:
                vehicleName = 'CarSide.png'
            elif self.platform.get_weight() == Common.Weights.heavy:
                vehicleName = '.png'
            elif self.platform.get_weight() == Common.Weights.veryHeavy:
                vehicleName = 'TrukSide.png'

            pixmap2 = QtGui.QPixmap(vehicleName)
            pixmap2 = pixmap2.scaled(40, 40, QtCore.Qt.KeepAspectRatio)
            self.lbl_vehicle.setPixmap(pixmap2)

            self.lbl_vehicle.setHidden(False)
            self.lbl_patente.setHidden(False)

        self.setBackgroundColor(color)
    """

    def updateUI(self, vehicle_patent, vehicle_weight, alarm):
        color = QtGui.QColor(150, 150, 150)

        self.lbl_vehicle.setHidden(True)
        self.lbl_patente.setHidden(True)

        if vehicle_weight != Common.Weights.empty:

            if alarm == Common.Alarm.stay.value:
                color = QtGui.QColor(100,100,255)
            elif alarm == Common.Alarm.oneLevelDown.value:
                color = QtGui.QColor(150,100,255)
            elif alarm == Common.Alarm.twoLevelDown.value:
                color = QtGui.QColor(200,100,255)
            elif alarm == Common.Alarm.lessThanMarginTime.value:
                color = QtGui.QColor(255,100,255)
            elif alarm == Common.Alarm.deliver.value:
                color = QtGui.QColor(255,100,100)

            # Vehicle ID
            self.lbl_patente.setText(vehicle_patent)

            # Current vehicle
            vehicleName = ''
            if vehicle_weight == Common.Weights.veryLight.value:
                vehicleName = 'MotoSide.png'
            elif vehicle_weight == Common.Weights.light.value:
                vehicleName = 'CarSide.png'
            elif vehicle_weight == Common.Weights.heavy.value:
                vehicleName = 'AutoTruckSide.png'
            elif vehicle_weight == Common.Weights.veryHeavy.value:
                vehicleName = 'TrukSide.png'

            pixmap2 = QtGui.QPixmap(vehicleName)
            pixmap2 = pixmap2.scaled(40, 40, QtCore.Qt.KeepAspectRatio)
            self.lbl_vehicle.setPixmap(pixmap2)

            self.lbl_vehicle.setHidden(False)
            self.lbl_patente.setHidden(False)

        self.setBackgroundColor(color)