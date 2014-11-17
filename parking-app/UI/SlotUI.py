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
            label = QtGui.QLabel()
            pixmap = QtGui.QPixmap("Clock.png")
            pixmap = pixmap.scaled(15, 15, QtCore.Qt.KeepAspectRatio)
            label.setPixmap(pixmap)
            label.move(15,15)




        elif value == 2:
            color = QtGui.QColor(150, 150, 150)
        else:
            color = QtGui.QColor(0, 0, 0)

        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)