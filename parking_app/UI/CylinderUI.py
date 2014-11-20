__author__ = 'adrian'

from PyQt4 import QtGui
from parking_app.UI.PlatformUI import PlatformUI

import parking_app.Common as Common

class CylinderUI(QtGui.QWidget):

    def __init__(self, cylinder):
        super(CylinderUI, self).__init__()
        self.cylinder = cylinder
        self.initUI()

    def initUI(self):

        grid = QtGui.QGridLayout()
        self.setLayout(grid)

        positions = [(i, j) for i in range(self.cylinder.qtty_levels) for j in range(self.cylinder.qtty_columns)]

        platforms = self.cylinder.platforms
        for [lvl, col] in positions:
            platformUI = PlatformUI(platforms[lvl][col])
            grid.addWidget(platformUI, *[lvl, col])



        #self.resize(300, 300)
        #self.setAutoFillBackground(True)
        #p = self.palette()
        #p.setColor(self.backgroundRole(), QtGui.QColor(200, 0, 0))
        #self.setPalette(p)
