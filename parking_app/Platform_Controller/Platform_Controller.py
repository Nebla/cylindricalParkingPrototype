__author__ = 'fsoler'
import parking_app.Common as Common


class PlatformController():
    def __init__(self):
        #TODO
        pass

    def initialize(self):
        #TODO
        pass

    def get_used_platforms(self):
        #TODO
        return [Common.Platform(1,1)]

    def set_alarm(self, alarm):
        pass

    def is_marked_to_leave(self, platform):
        #TODO
        return False

    def get_sector_from_level(self, level):
        #todo
        # once the cylinder is obtained, here is executed calculate_sector method
        return False

    def sleep_one_minute(self):
        #todo
        pass

    def run(self):
        while True:
            platforms = self.get_used_platforms()
            for platform in platforms:
                level = platform.level
                sector = self.get_sector_from_level(level)
                remaining_time = platform.get_remaining_time()

                if remaining_time <= 0:
                    self.set_alarm(Common.Alarm.deliver)
                elif remaining_time <= Common.Margin_time:
                    self.set_alarm(Common.Alarm.lessThanMarginTime)

                if sector != Common.Sector.lower and not self.is_marked_to_leave(platform):
                    for sec in Common.Sector:
                        if sec.value/2 > remaining_time:
                            sector_list = [i for i in Common.Sector]
                            lvl_down = sector_list.index(sector) - sector_list.index(sec)
                            if lvl_down > 0:
                                self.set_alarm(Common.Alarm(lvl_down))
                            break
            self.sleep_one_minute()

if __name__ == "__init__":
    platform_controller = PlatformController()
    platform_controller.initialize()
    platform_controller.run()
