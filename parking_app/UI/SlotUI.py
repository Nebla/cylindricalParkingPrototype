__author__ = 'adrian'

from PyQt4 import QtGui
from PyQt4 import QtCore

from AlarmConfirmationUI import AlarmConfirmationUI

import random

class SlotUI(QtGui.QWidget):

    def __init__(self):
        super(SlotUI, self).__init__()
        self.initUI()

    def initUI(self):

        self.status = random.randint(0,2)
        self.setBackgroundColor()

        if (self.status == 0 or self.status == 1):
            vertical = QtGui.QVBoxLayout()

            horizontal = QtGui.QHBoxLayout()

            # Vehicle ID
            lbl1 = QtGui.QLabel("AAA-000",self)
            #vertical.addWidget(lbl1)

            horizontal.addWidget(lbl1)

            # Alarm
            self.alarmButton = QtGui.QPushButton();
            self.alarmButton.setIcon(QtGui.QIcon('Warning.png'))
            self.alarmButton.setIconSize(QtCore.QSize(15,15))
            self.alarmButton.clicked.connect(self.showAlarmOffConfirmation)
            horizontal.addWidget(self.alarmButton)

            vertical.addLayout(horizontal)

            # Current vehicle
            vehicle = random.randint(0,2)
            vehicleName = ''
            if vehicle == 0:
                vehicleName = 'CarSide.png'
            elif vehicle == 1:
                vehicleName = 'MotoSide.png'
            elif vehicle == 2:
                vehicleName = 'TrukSide.png'

            lbl2 = QtGui.QLabel(self)
            pixmap2 = QtGui.QPixmap(vehicleName)
            pixmap2 = pixmap2.scaled(40, 40, QtCore.Qt.KeepAspectRatio)
            lbl2.setPixmap(pixmap2)

            vertical.addWidget(lbl2)

            self.setLayout(vertical)

    def showAlarmOffConfirmation(self):
        self.confirmationMessage = AlarmConfirmationUI()
        self.confirmationMessage.resize(400, 200)
        self.confirmationMessage.move(50,50)

        QtCore.QObject.connect(self.confirmationMessage, QtCore.SIGNAL('stopAlarm()'), self.turnOffAlarm)

        self.confirmationMessage.show()
        print "Show pop up confirmation message"


    def turnOffAlarm(self):
        print "apagando"
        self.alarmButton.setHidden(True)


    def setBackgroundColor(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        color = QtGui.QColor(150, 150, 150)
        if self.status == 0:
            color = QtGui.QColor(0, 255, 0)
        elif self.status == 1:
            color = QtGui.QColor(100, 100, 255)
        elif self.status == 2:
            color = QtGui.QColor(150, 150, 150)
        else:
            color = QtGui.QColor(0, 0, 0)
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)
