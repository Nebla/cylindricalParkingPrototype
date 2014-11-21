__author__ = 'fsoler'
import parking_app.Common as Common
import parking_app.concurrent.SharedConveyorBelt as ShCon
import parking_app.concurrent.SharedParkingSlot as ShPark


class RoboticDeliverer():

    def __init__(self):
        self.__sh_conveyor = None
        self.__sh_slots = None
        #TODO
        pass

    def initialize(self):
        self.__sh_conveyor = ShCon.SharedConveyorBelt(Common.Conveyor_input_id)
        self.__sh_slots = ShPark.SharedParkingSlots()

    def obtain_car(self):
        return self.__sh_conveyor.get(Common.Robotic_deliverer_id)

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

if __name__ == "__init__":
    robitc_deliverer_controller = RoboticDeliverer()
    robitc_deliverer_controller.initialize()
    robitc_deliverer_controller.run()