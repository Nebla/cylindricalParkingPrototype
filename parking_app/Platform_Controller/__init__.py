__author__ = 'fsoler'

from parking_app.Platform_Controller.Platform_Controller import PlatformController


def start(qtty_cyl, levels, columns, sh_cylinders, mutex_cyl, sh_alarms, mutex_alarms):
    platform_controller = PlatformController(qtty_cyl)
    platform_controller.initialize(sh_cylinders, mutex_cyl, sh_alarms,
                                   mutex_alarms)
    platform_controller.run()
