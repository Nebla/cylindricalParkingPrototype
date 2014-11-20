__author__ = 'fsoler'
import parking_app.Common as Common
import parking_app.concurrent.SharedBuffer as ShBuff
import parking_app.concurrent.SharedCylinder as ShCyl
import sys


class RoboticDispatcher():
    def __init__(self, qtty_cylinders):
        self.__qtty_cylinders = qtty_cylinders
        self.__sh_buff = None
        self.__cylinders = None

    def initialize(self):
        self.__sh_buff = [ShBuff.SharedBuffer(cyl_id, Common.Id_input)
                          for cyl_id in len(self.__qtty_cylinders)]
        self.__cylinders = [ShCyl.SharedCylinder(cyl_id)
                            for cyl_id in len(self.__qtty_cylinders)]

    def obtainCar(self):
        #TODO
        return True

    def get_available_cylinders(self):
        ran_cyl = range(self.__qtty_cylinders)
        cylinders = [self.__cylinders[i].cylinder for i in ran_cyl]

        #for i in ran_cyl:
        #    self.__cylinders[i].cylinder = cylinders[i]

        return [cylinders[i] for i in ran_cyl if cylinders[i].has_space()]
        #return [i for i in ran_cyl if cylinders[i].has_space()]

    def buffers_are_occupied(self, available_cyl=None):
        buffers = self.__get_buffers(available_cyl)
        return False if [i for i in range(len(buffers))
                         if buffers[i] is None] else True

    def sleep(self):
        #todo
        pass

    def get_available_buffers(self, available_cyl=None):
        buffers = self.__get_buffers(available_cyl)
        return [buffers[i] for i in range(len(buffers))
                if buffers[i] is not None]

    def __get_buffers(self, available_cyl=None):
        cylinders = range(self.__qtty_cylinders) if available_cyl is None \
            else available_cyl

        buffers = [self.__sh_buff[cyl_id].buffer for cyl_id in cylinders]

        for cyl_id in cylinders:
            self.__sh_buff[cyl_id].buffer = buffers[cyl_id]
        return buffers

    def save_car(self, car_and_hours, cyl_id):
        buffer = self.__sh_buff[cyl_id].buffer
        buffer = car_and_hours
        self.__sh_buff[cyl_id].buffer = buffer

    def run(self):
        while True:
            car_and_hours = self.obtainCar()

            available_cylinders = self.get_available_cylinders()
            while self.buffers_are_occupied(available_cylinders):
                self.sleep()
                available_cylinders = self.get_available_cylinders()

            #cylinders = self.get_available_cylinders()
            weights = [cyl.weight for cyl in available_cylinders]
            cyl_id = available_cylinders[weights.index(min(weights))].id
            self.save_car(car_and_hours, cyl_id)

if __name__ == "__init__":
    dispatcher_controller = RoboticDispatcher(sys.argv[1])
    dispatcher_controller.initialize()
    dispatcher_controller.run()
