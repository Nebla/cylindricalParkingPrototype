__author__ = 'adrian'

from PyQt4 import QtGui
from PyQt4 import QtCore

from parking_app.UI.WarningConfirmationUI import WarningConfirmationUI

import parking_app.Common as Common

import random

class PlatformUI(QtGui.QWidget):

    def __init__(self, platform):
        super(PlatformUI, self).__init__()
        self.platform = platform
        self.initUI()

    def initUI(self):

        self.status = random.randint(0,2)

        color = QtGui.QColor(150, 150, 150)

        if not self.platform.is_empty():
            color = QtGui.QColor(100, 100, 255)

            vertical = QtGui.QVBoxLayout()
            horizontal = QtGui.QHBoxLayout()

            # Vehicle ID
            lbl1 = QtGui.QLabel(self.platform.vehicle.patent,self)
            #vertical.addWidget(lbl1)

            horizontal.addWidget(lbl1)

            # Alarm
            self.warningButton = QtGui.QPushButton()
            self.warningButton.setIcon(QtGui.QIcon('Warning.png'))
            self.warningButton.setIconSize(QtCore.QSize(15,15))
            self.warningButton.clicked.connect(self.showAlarmOffConfirmation)
            self.warningButton.setVisible(False)
            horizontal.addWidget(self.alarmButton)

            vertical.addLayout(horizontal)

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


            lbl2 = QtGui.QLabel(self)
            pixmap2 = QtGui.QPixmap(vehicleName)
            pixmap2 = pixmap2.scaled(40, 40, QtCore.Qt.KeepAspectRatio)
            lbl2.setPixmap(pixmap2)

            vertical.addWidget(lbl2)

            self.setLayout(vertical)

        self.setBackgroundColor(color)


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
