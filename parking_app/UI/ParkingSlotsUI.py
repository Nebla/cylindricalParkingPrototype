__author__ = 'adrian'

from PyQt4 import QtGui
from parking_app.UI.PlatformUI import PlatformUI
from parking_app.UI.SlotUI import SlotUI

import parking_app.Common as Common


class ParkingSlotsUI(QtGui.QWidget):

    #def __init__(self, parkingSlots):
    def __init__(self):
        super(ParkingSlotsUI, self).__init__()
        #self.parkingSlots = parkingSlots
        self.initUI()

    def initUI(self):
        vLayout = QtGui.QVBoxLayout()

        self.slotsUI = [None]*10
        for i in range(10):
            slot = SlotUI()
            self.slotsUI[i] = slot
            vLayout.addWidget(slot);

        self.setLayout(vLayout)

    def updateSlot(self, level, column, vehicle_patent, vehicle_weight):
        print("Should update SlotUI")
        self.slotUI[level].updateUI(vehicle_patent, vehicle_weight)