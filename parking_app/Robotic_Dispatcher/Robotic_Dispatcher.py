__author__ = 'fsoler'
import sys
import time
import parking_app.Common as Common
import parking_app.concurrent.SharedBuffer as ShBuff
import parking_app.concurrent.SharedCylinder as ShCyl
import parking_app.concurrent.SharedConveyorBelt as ShCon
import parking_app.concurrent.SharedHandler as ShHan

from PyQt4 import QtCore

class RoboticDispatcher(QtCore.QThread):

    def __init__(self, qtty_cylinders):
        QtCore.QThread.__init__(self)
        self.__qtty_cylinders = qtty_cylinders
        self.__sh_buff = None
        self.__cylinders = None
        self.__sh_conveyor = None

    def initialize(self, sh_cylinders, mutex_sh_cylinders, conveyor, sh_buffers, mutex_sh_buffers):
        self.__sh_buff = [ShHan.SharedHandler(sh_buffers[i], mutex_sh_buffers[i]) for i in range(len(sh_buffers))]
        self.__cylinders = [ShHan.SharedHandler(sh_cylinders[i], mutex_sh_cylinders[i]) for i in range(len(sh_cylinders))]
        self.__sh_conveyor = conveyor

    def obtain_car_and_hours(self):
        print ("Robotic dispatcher - obtaining car an hours")
        return self.__sh_conveyor.get(True, None)

    def get_available_cylinders(self):
        ran_cyl = range(self.__qtty_cylinders)
        cylinders = [self.__cylinders[i].data for i in ran_cyl]

        available_cyl = [cylinders[i] for i in ran_cyl if cylinders[i].has_space()]
        [cylinders.remove(available_cyl[i]) for i in range(len(available_cyl))]
        self.__return_cylinders(cylinders)
        return available_cyl

    def buffers_are_occupied(self, available_cyl=None):
        buffers = self.__get_buffers(available_cyl)
        return False if [i for i in range(len(buffers))
                         if buffers[i][0] is None] else True

    def sleepSeconds(self, seconds):
        #todo
        time.sleep(seconds)

    def get_available_buffers(self, available_cyl=None):
        buffers = self.__get_buffers(available_cyl)
        return [buffers[i] for i in range(len(buffers))
                if buffers[i] is not None]

    def __return_cylinders(self, cylinders):
        for i in range(len(cylinders)):
            self.__cylinders[cylinders[i].id()].data = cylinders[i]

    def __get_buffers(self, available_cyl=None):
        cylinders = range(self.__qtty_cylinders) if available_cyl is None \
            else [available_cyl[i].id() for i in range(len(available_cyl))]

        buffers = [self.__sh_buff[cyl_id].data for cyl_id in cylinders]

        for cyl_id in cylinders:
            self.__sh_buff[cyl_id].data = buffers[cyl_id]
        return buffers

    def save_car(self, car_and_hours, cyl_id, available_cyl=None):
        if available_cyl is not None:
            self.__return_cylinders(available_cyl)
        car_hours = self.__sh_buff[cyl_id].data
        car_hours[0] = car_and_hours[0]
        car_hours[1] = car_and_hours[1]
        self.__sh_buff[cyl_id].data = car_hours

    def run(self):
        print("Start running robot dispatcher")
        while True:
            car_and_hours = self.obtain_car_and_hours()
            print("Robot dispatcher - Obtain car and hours to store in buffer")
            available_cylinders = self.get_available_cylinders()
            while self.buffers_are_occupied(available_cylinders):
                print("Robot dispatcher - Waiting for available cylinders")
                self.sleep(2)
                available_cylinders = self.get_available_cylinders()

            weights = [cyl.weight for cyl in available_cylinders]
            cyl_id = available_cylinders[weights.index(min(weights))].id()
            self.save_car(car_and_hours, cyl_id, available_cylinders)
            print("Robot dispatcher - Saved car")

"""
def start(qtty_cylinders, cylinders, mutex_cylinders, deliver_queue, buffers, mutex_buffers):

    qtty_cylinders = sys.argv[1]
    cylinders = sys.argv[2]
    mutex_cylinders = sys.argv[3]
    deliver_queue = sys.argv[4]
    buffers = sys.argv[5]
    mutex_buffers = sys.argv[6]

    dispatcher_controller = RoboticDispatcher(qtty_cylinders)
    dispatcher_controller.initialize(cylinders, mutex_cylinders,
                                         deliver_queue, buffers, mutex_buffers)
    dispatcher_controller.run()
"""