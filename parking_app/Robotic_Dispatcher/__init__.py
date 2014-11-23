__author__ = 'fsoler'

from parking_app.Robotic_Dispatcher.Robotic_Dispatcher import RoboticDispatcher

def start(qtty_cylinders, cylinders, mutex_cylinders, deliver_queue, buffers, mutex_buffers):
    dispatcher_controller = RoboticDispatcher(qtty_cylinders)
    dispatcher_controller.initialize(cylinders, mutex_cylinders,
                                         deliver_queue, buffers, mutex_buffers)
    dispatcher_controller.run()
