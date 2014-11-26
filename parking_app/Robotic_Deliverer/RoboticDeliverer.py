__author__ = 'fsoler'
import sys
import parking_app.concurrent.SharedHandler as ShHan
from PyQt4 import QtCore


class RoboticDeliverer(QtCore.QThread):

    # level, column, vehicle id, vehicle weight
    update = QtCore.pyqtSignal(int, str, int)

    def __init__(self):
        super(RoboticDeliverer, self).__init__()

        self.__sh_conveyor = None
        self.__sh_slots = None

    def initialize(self, conveyor, sh_slots, mutex_slots):
        self.__sh_conveyor = conveyor
        self.__sh_slots = ShHan.SharedHandler(sh_slots, mutex_slots)

    def obtain_car(self):
        return self.__sh_conveyor.get()

    def place_car_into_garage(self, car):
        parking_slots = self.__sh_slots.data
        lvl = parking_slots.save_car(car)
        self.__sh_slots.data = parking_slots
        result = lvl >= 0
        if result:
            print("emit in lvl %d with patent %s and weight %f" % (lvl, car.get_patent(), car.get_weight()))
            self.update.emit(lvl, car.get_patent(), car.get_weight())
        return result

    def wait_for_place_into_garage(self):
        #TODO
        pass

    def run(self):
        print("Start running robotic deliverer")
        while True:
            car = self.obtain_car()
            print("Robotic deliverer: car is obtained")
            if not self.place_car_into_garage(car):
                self.wait_for_place_into_garage()
                self.place_car_into_garage(car)

"""
if __name__ == "__init__":
    input_queue = sys.argv[1]
    parking_slot = sys.argv[2]
    mutex_parking_slot = sys.argv[3]

    robotic_deliverer_controller = RoboticDeliverer()
    robotic_deliverer_controller.initialize(input_queue, parking_slot,
                                            mutex_parking_slot)
    robotic_deliverer_controller.run()
"""