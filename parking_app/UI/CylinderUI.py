__author__ = 'adrian'

from PyQt4 import QtGui
from parking_app.UI.PlatformUI import PlatformUI

import parking_app.Common as Common

class CylinderUI(QtGui.QWidget):

    def __init__(self, cylinder):
        super(CylinderUI, self).__init__()
        self.cylinder = cylinder
        self.init_ui()

    def init_ui(self):

        grid = QtGui.QGridLayout()
        self.setLayout(grid)


        self.platformsUI = [[PlatformUI() for col in
                             range(self.cylinder.qtty_columns())]
                            for lvl in range(self.cylinder.qtty_levels())]

        [[grid.addWidget(self.platformsUI[lvl][col], *[lvl, col]) for col in
                             range(self.cylinder.qtty_columns())]
                            for lvl in range(self.cylinder.qtty_levels())]



        #self.resize(300, 300)
        #self.setAutoFillBackground(True)
        #p = self.palette()
        #p.setColor(self.backgroundRole(), QtGui.QColor(200, 0, 0))
        #self.setPalette(p)

    def updatePlatform(self, level, column, vehicle_patent, vehicle_weight, alarm):
        self.platformsUI[level][column].updateUI(vehicle_patent, vehicle_weight, alarm)