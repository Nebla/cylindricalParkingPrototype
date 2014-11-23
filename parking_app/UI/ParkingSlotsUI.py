__author__ = 'adrian'

from PyQt4 import QtGui
from UI.PlatformUI import PlatformUI

import Common as Common

class ParkingSlotsUI(QtGui.QWidget):

    def __init__(self, parkingSlots):
        super(ParkingSlotsUI, self).__init__()
        self.parkingSlots = parkingSlots
        self.initUI()

    def initUI(self):
        vLayout = QtGui.QVBoxLayout()

        self.setLayout(vLayout )

        """
        positions = [(i, j) for i in range(self.cylinder.qtty_levels) for j in range(self.cylinder.qtty_columns)]

        platforms = self.cylinder.platforms
        for [lvl, col] in positions:
            platformUI = PlatformUI(platforms[lvl][col])
            grid.addWidget(platformUI, *[lvl, col])
        """