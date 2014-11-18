__author__ = 'fsoler'
import parking_app.Common as Common


class RoboticHand():
    def __init__(self, cylinder_id):
        self.__shared_cylinder = self.SharedCylinder(cylinder_id)
        self.__sh_buff_input = self.SharedBuffer(cylinder_id, Common.Id_input)
        self.__sh_buff_output = self.SharedBuffer(cylinder_id, Common.Id_output)
        self._id = id

    def car_to_deliver(self):
        #TODO
        return False

    def get_car_to_deliver(self):
        #todo
        return True

    def deliver_car(self, car):
        if self.__sh_buff_output.buffer is None:
            self.__sh_buff_output.buffer = car
        #todo if is occupied, this processor must wait till is empty

    def car_to_save(self):
        return self.__sh_buff_input.buffer is not None

    def get_car_to_save(self):
        car_and_hour = self.__sh_buff_input.buffer
        self.__sh_buff_input.buffer = None
        return car_and_hour

    def save_car(self, car, hours):
        cylinder = self.__shared_cylinder.cylinder
        [lvl, col] = cylinder.get_position_to_save_car(hours)
        cylinder.add_car(car, lvl, col, hours)
        self.__shared_cylinder.cylinder = cylinder

    def run(self):
        while True:
            while self.car_to_deliver():
                car = self.get_car_to_deliver()
                self.deliver_car(car)
            if self.car_to_save():

                [car, hours] = self.get_car_to_save()
                self.save_car(car, hours)

            can_reorder = not (self.car_to_save() or self.car_to_deliver()
                               or self.car_to_reorder())
            if can_reorder and self.car_to_reorder():
                [car, sector_to_save] = self.get_car_to_reorder()
                self.save_car(car, sector_to_save)

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
    hand_controller = RoboticHand()
    hand_controller.initialize()
    hand_controller.run()
