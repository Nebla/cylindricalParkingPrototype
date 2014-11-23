__author__ = 'fsoler'
import sys
import parking_app.Common as Common
import parking_app.concurrent.SharedHandler as ShHan


class RoboticHand():
    def __init__(self, cylinder_id, qtty_levels, qtty_columns):
        self._id = cylinder_id
        self._qtty_levels = qtty_levels
        self._qtty_columns = qtty_columns
        self.__shared_cylinder = None
        self.__sh_buff_input = None
        self.__sh_conveyor = None
        self.__shared_alarms = None

    def initialize(self, sh_cylinder, mutex_sh_cylinder, sh_buffer, mutex_sh_buffer,
                   sh_alarms, mutex_sh_alarms, conveyor):
        self.__shared_cylinder = ShHan.SharedHandler(sh_cylinder, mutex_sh_cylinder)
        self.__sh_buff_input = ShHan.SharedHandler(sh_buffer, mutex_sh_buffer)
        self.__sh_conveyor = conveyor
        self.__shared_alarms = ShHan.SharedHandler(sh_alarms, mutex_sh_alarms)

    def car_to_deliver(self):
        f = lambda x: x == Common.Alarm.deliver
        return self.__car_to_alarm(f)

    def get_car_to_deliver(self):
        f = lambda x: x == Common.Alarm.deliver
        platforms = self.__get_platforms(f)
        [level, column] = platforms[0]

        cylinder = self.__shared_cylinder.cylinder
        car = cylinder.get_car(level, column)
        self.__shared_cylinder.cylinder = cylinder

        return car

    def deliver_car(self, car):
        self.__sh_conveyor.add(car)

    def car_to_save(self):
        car_and_hours = self.__sh_buff_input.buffer
        self.__sh_buff_input.buffer = car_and_hours
        return car_and_hours is not None

    def get_car_to_save(self):
        car_and_hour = self.__sh_buff_input.buffer
        self.__sh_buff_input.buffer = None
        return car_and_hour

    def save_car(self, car, hours):
        cylinder = self.__shared_cylinder.cylinder
        [lvl, col] = cylinder.get_position_to_save_car(hours)
        cylinder.add_car(car, lvl, col, hours)
        self.__shared_cylinder.cylinder = cylinder

    def get_car_to_reorder(self):
        f = lambda x: x == Common.Alarm.oneLevelDown or Common.Alarm.twoLevelDown
        platforms_to_reorder = self.__get_platforms(f)

        [level, column] = platforms_to_reorder[0]
        car = self.__get_car_from_platform(level, column)

        cylinder = self.__shared_cylinder.cylinder
        hours = cylinder.get_remaining_time(level, column)
        self.__shared_cylinder.cylinder = cylinder
        return [car, hours]

    def car_to_reorder(self):
        f = lambda x: x == Common.Alarm.oneLevelDown or Common.Alarm.twoLevelDown
        return self.__car_to_alarm(f)

    def little_time_to_deliver(self):
        f = lambda x: x == Common.Alarm.lessThanMarginTime
        return self.__car_to_alarm(f)

    def __car_to_alarm(self, f):
        alarms = self.__shared_alarms.alarms

        for lvl in range(self._qtty_levels):
            if [col for col in range(self._qtty_columns) if f(alarms[lvl][col])]:
                self.__shared_alarms.alarms = alarms
                return True

        self.__shared_alarms.alarms = alarms
        return False

    def __get_car_from_platform(self, lvl, col):
        cylinder = self.__shared_cylinder.cylinder
        car = cylinder.get_car(lvl, col)
        self.__shared_cylinder.cylinder = cylinder
        return car

    def __get_platforms(self, f):
        alarms = self.__shared_alarms.alarms

        platforms = [[lvl, col] for lvl in range(self._qtty_levels)
                     for col in range(self._qtty_columns)
                     if f(alarms[lvl][col])]
        self.__shared_alarms.alarms = alarms
        return platforms

    def run(self):
        while True:
            while self.car_to_deliver():
                car = self.get_car_to_deliver()
                self.deliver_car(car)
            if self.car_to_save():

                [car, hours] = self.get_car_to_save()
                self.save_car(car, hours)

            can_reorder = not (self.car_to_save() or self.car_to_deliver()
                               or self.little_time_to_deliver())
            if can_reorder and self.car_to_reorder():
                [car, hours] = self.get_car_to_reorder()
                self.save_car(car, hours)

if __name__ == "__init__":
    hand_id = sys.argv[1]
    total_levels = sys.argv[2]
    total_columns = sys.argv[3]
    cylinder = sys.argv[4]
    mutex_cylinder = sys.argv[5]
    buffer = sys.argv[7]
    mutex_buffer = sys.argv[6]
    queue = sys.argv[8]
    alarms = sys.argv[9]
    mutex_alarms = sys.argv[10]
    hand_controller = RoboticHand(hand_id, total_levels, total_columns)
    hand_controller.initialize(cylinder, mutex_cylinder, buffer, mutex_buffer,
                               alarms, mutex_alarms, queue)
    hand_controller.run()
