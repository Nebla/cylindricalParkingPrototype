__author__ = 'fsoler'
import sys
import parking_app.Common as Common
import parking_app.concurrent.SharedCylinder as ShCyl
import parking_app.concurrent.SharedAlarms as ShAl


class PlatformController():

    def __init__(self, qtty_cylinders):
        self.__qtty_cylinders = qtty_cylinders
        self.__temporal_cylinder = None
        self.__cylinders = None
        self.__alarms = None

    def initialize(self, level, cols):
        self.__cylinders = [ShCyl.SharedCylinder(cyl_id)
                            for cyl_id in len(self.__qtty_cylinders)]
        self.__alarms = [ShAl.SharedAlarms(cyl_id, level, cols)
                         for cyl_id in len(self.__qtty_cylinders)]

    def get_cylinders_id(self):
        return range(self.__qtty_cylinders)

    def get_used_platforms(self, cylinder_id):
        self.__temporal_cylinder = self.__cylinders[cylinder_id].cylinder
        range_levels = range(self.__temporal_cylinder.qtty_levels)
        range_columns = range(self.__temporal_cylinder.qtty_columns)
        platforms = self.__temporal_cylinder.platforms
        return [platforms[lvl][col] for lvl in range_levels for col in range_columns
                if platforms[lvl][col] is not None]

    def set_alarm(self, cylinder, alarm, level, column):
        alarms = self.__alarms[cylinder].alarms
        alarms[level][column] = alarm
        self.__alarms[cylinder] = alarms

    def is_marked_to_leave(self, cylinder, platform):
        level = platform.level
        column = platform.column
        alarms = self.__alarms[cylinder].alarms
        self.__alarms[cylinder] = alarms
        return alarms[level][column] == Common.Alarm.deliver

    def get_sector_from_level(self, level):
        return self.__temporal_cylinder.calculate_sector(level)

    def return_used_platforms(self, cylinder_id, platforms):
        f = lambda x: [x.level, x.column]
        positions = [f(platform) for platform in platforms]

        for i in range(len(positions)):
            self.__temporal_cylinder.platforms[positions[i][0]][positions[i][1]] = platforms[i]

        self.__cylinders[cylinder_id].cylinder = self.__temporal_cylinder

    def sleep_one_minute(self):
        #todo
        pass

    def run(self):
        while True:
            for cyl_id in self.get_cylinders_id():
                platforms = self.get_used_platforms(cyl_id)
                for platform in platforms:
                    level = platform.level
                    column = platform.column
                    sector = self.get_sector_from_level(level)
                    remaining_time = platform.get_remaining_time()

                    if remaining_time <= 0:
                        self.set_alarm(cyl_id, Common.Alarm.deliver, level, column)
                    elif remaining_time <= Common.Margin_time:
                        self.set_alarm(cyl_id, Common.Alarm.lessThanMarginTime, level, column)

                    if sector != Common.Sector.lower and not self.is_marked_to_leave(cyl_id, platform):
                        for sec in Common.Sector:
                            if sec.value/2 > remaining_time:
                                sector_list = [i for i in Common.Sector]
                                lvl_down = sector_list.index(sector) - sector_list.index(sec)
                                if lvl_down > 0:
                                    self.set_alarm(cyl_id, Common.Alarm(lvl_down), level, column)
                                break
                self.return_used_platforms(cyl_id, platforms)
            self.sleep_one_minute()

if __name__ == "__init__":
    qtty_cyl = sys.argv[1]
    levels = sys.argv[2]
    columns = sys.argv[3]
    platform_controller = PlatformController(qtty_cyl)
    platform_controller.initialize(levels, columns)
    platform_controller.run()
