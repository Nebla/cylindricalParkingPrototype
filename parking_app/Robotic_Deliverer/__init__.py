__author__ = 'fsoler'

from parking_app.Robotic_Deliverer.RoboticDeliverer import RoboticDeliverer

def start(input_queue, parking_slot, mutex_parking_slot):

    robotic_deliverer_controller = RoboticDeliverer()
    robotic_deliverer_controller.initialize(input_queue, parking_slot,
                                            mutex_parking_slot)
    robotic_deliverer_controller.run()