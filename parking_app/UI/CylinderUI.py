__author__ = 'adrian'

from PyQt4 import QtGui
from UI.PlatformUI import PlatformUI

import parking_app.Common as Common

class CylinderUI(QtGui.QWidget):

    def __init__(self):
        super(CylinderUI, self).__init__()
        self.cylinder = Common.Cylinder()
        self.initUI()

    def initUI(self):

        grid = QtGui.QGridLayout()
        self.setLayout(grid)


        positions = [(i,j) for i in range(6) for j in range(3)]

        for position in positions:
            platformUI = PlatformUI(self.cylinder.__platforms[position(i)][position(j)])
            grid.addWidget(platformUI, *position)



        #self.resize(300, 300)
        #self.setAutoFillBackground(True)
        #p = self.palette()
        #p.setColor(self.backgroundRole(), QtGui.QColor(200, 0, 0))
        #self.setPalette(p)
