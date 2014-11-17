__author__ = 'adrian'

from PyQt4 import QtGui
from UI.SlotUI import SlotUI

class CylinderUI(QtGui.QWidget):

    def __init__(self):
        super(CylinderUI, self).__init__()

        self.initUI()

    def initUI(self):

        grid = QtGui.QGridLayout()
        self.setLayout(grid)


        positions = [(i,j) for i in range(6) for j in range(3)]

        for position in positions:
            slot = SlotUI()
            grid.addWidget(slot, *position)


        #self.resize(300, 300)
        #self.setAutoFillBackground(True)
        #p = self.palette()
        #p.setColor(self.backgroundRole(), QtGui.QColor(200, 0, 0))
        #self.setPalette(p)


"""
    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()

    def drawRectangles(self, qp):

        color = QtGui.QColor(0, 0, 0)
        color.setNamedColor('#d4d4d4')
        qp.setPen(color)

        qp.setBrush(QtGui.QColor(200, 0, 0))
        qp.drawRect(10, 15, 90, 60)

        qp.setBrush(QtGui.QColor(255, 80, 0, 160))
        qp.drawRect(130, 15, 90, 60)

        qp.setBrush(QtGui.QColor(25, 0, 90, 200))
        qp.drawRect(250, 15, 90, 60)
"""