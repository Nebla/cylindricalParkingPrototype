__author__ = 'adrian'

from PyQt4 import QtGui
from parking_app.UI.PlatformUI import PlatformUI
from parking_app.UI.SlotUI import SlotUI

import parking_app.Common as Common


class ParkingSlotsUI(QtGui.QWidget):

    def __init__(self, parkingSlots):
        super(ParkingSlotsUI, self).__init__()
        self.__parkingSlots = parkingSlots
        self.__slots_ui = None
        self.init_ui()

    def init_ui(self):
        v_layout = QtGui.QVBoxLayout()

        parking_slots = self.__parkingSlots.data
        levels = parking_slots.get_length()
        self.__parkingSlots.data = parking_slots

        self.__slots_ui = [SlotUI() for i in range(levels)]
        [v_layout.addWidget(slot) for slot in self.__slots_ui]

        self.setLayout(v_layout)

    def updateSlot(self, level, vehicle_patent, vehicle_weight):
        print("Should update SlotUI")
        self.__slots_ui[level].updateUI(vehicle_patent, vehicle_weight)