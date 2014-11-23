__author__ = 'fsoler'
import sys
import parking_app.concurrent.SharedHandler as ShHan


class RoboticDeliverer():

    def __init__(self):
        self.__sh_conveyor = None
        self.__sh_slots = None

    def initialize(self, conveyor, sh_slots, mutex_slots):
        self.__sh_conveyor = conveyor
        self.__sh_slots = ShHan.SharedHandler(sh_slots, mutex_slots)

    def obtain_car(self):
        return self.__sh_conveyor.get()

    def place_car_into_garage(self, car):
        parking_slots = self.__sh_slots.slots
        result = parking_slots.save_car()
        self.__sh_slots.slots = parking_slots
        return result

    def wait_for_place_into_garage(self):
        #TODO
        pass

    def run(self):
        while True:
            car = self.obtain_car()
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