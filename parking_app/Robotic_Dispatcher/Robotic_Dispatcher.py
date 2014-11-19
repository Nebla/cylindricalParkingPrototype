__author__ = 'fsoler'
import parking_app.Common as Common
import sys

class RoboticDispatcher():
    def __init__(self, qtty_cylinders):
        self.__sh_buff = [self.SharedBuffer(cyl_id, Common.Id_input) for cyl_id in len(qtty_cylinders)]
        self.__cylinders = [self.SharedCylinder(cyl_id) for cyl_id in len(qtty_cylinders)]

    def initialize(self):
        #todo
        pass

    def obtainCar(self):
        #TODO
        return True

    def buffers_occupied(self):
        pass

    def sleep(self):
        #todo
        pass

    def get_available_buffers(self):
        #todo
        pass

    def save_car(self, car_and_hours, cyl_id):
        self.__sh_buff[cyl_id].buffer = car_and_hours

    def run(self):
        while True:
            # falta que chequee por cylinders llenos
            car_and_hours = self.obtainCar()
            if self.buffers_occupied():
                self.sleep()
            cylinders = self.get_available_buffers()
            weights = [cyl.weight for cyl in cylinders]
            cyl_id = cylinders[weights.index(min(weights))].id
            self.save_car(car_and_hours, cyl_id)

    class SharedBuffer():

        def __init__(self, cylinder_id, buffer_id):
            #todo
            self.__buffer = None

        @property
        def buffer(self):
            #here i must block the shared memory
            #todo
            return self.__buffer

        @buffer.setter
        def buffer(self, cylinder):
            #todo
            self.__buffer = cylinder
            # here i must release the shared memory

    class SharedCylinder():
        def __init__(self, cylinder_id):
            self.__cylinder = Common.Cylinder(cylinder_id)

        @property
        def cylinder(self):
            #here i must block the shared memory
            return self.__cylinder

        @cylinder.setter
        def cylinder(self, cylinder):
            #todo
            self.__cylinder = cylinder
            # here i must release the shared memory


if __name__ == "__init__":
    dispatcher_controller = RoboticDispatcher(sys.argv[1])
    dispatcher_controller.initialize()
    dispatcher_controller.run()
