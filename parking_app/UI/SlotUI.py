__author__ = 'adrian'

from PyQt4 import QtGui
from PyQt4 import QtCore

import random

class SlotUI(QtGui.QWidget):

    def __init__(self):
        super(SlotUI, self).__init__()
        self.initUI()

    def initUI(self):
        self.setAutoFillBackground(True)

        p = self.palette()

        value = random.randint(0,2)

        color = QtGui.QColor(150, 150, 150)
        if value == 0:
            color = QtGui.QColor(0, 255, 0)
        elif value == 1:
            color = QtGui.QColor(0, 0, 255)
            lbl1 = QtGui.QLabel(self)
            pixmap = QtGui.QPixmap("Clock.png")
            pixmap = pixmap.scaled(30, 30, QtCore.Qt.KeepAspectRatio)
            lbl1.setPixmap(pixmap)
            lbl1.move(0, 0)
        elif value == 2:
            color = QtGui.QColor(150, 150, 150)
        else:
            color = QtGui.QColor(0, 0, 0)

        if (value == 0 or value == 1):
            #We show de current vehicle
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
            lbl2.move(0, 40)

        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)
