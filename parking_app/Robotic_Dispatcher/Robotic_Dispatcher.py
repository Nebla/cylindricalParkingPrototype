__author__ = 'fsoler'
import parking_app.Common as Common

class RoboticDispatcher():
    def __init__(self):
        #TODO
        pass

    def obtainCar(self):
        #TODO
        return True

    def buffers_occupied(self):
        #todo
        pass

    def sleep(self):
        #todo
        pass

    def get_available_cylinders(self):
        #todo
        pass

    def saveCar(self, car_and_hours):
        #todo
        pass

    def run(self):
        while True:
            car_and_hours = self.obtainCar()
            if self.buffers_occupied():
                self.sleep()
            cylinders = self.get_available_cylinders()
            weights = [cyl.weight for cyl in cylinders]
            buff_index = cylinders[weights.index(min(weights))].id
            self.saveCar(car_and_hours)

if __name__ == "__init__":
    dispatcher_controller = RoboticDispatcher()
    dispatcher_controller.initialize()
    dispatcher_controller.run()
    