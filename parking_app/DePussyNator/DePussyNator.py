__author__ = 'fsoler'

class DePussyNator():

    def __init__(self):
        #TODO
        pass

    def initialize(self):
        #TODO
        pass

    def obtainCar(self):
        #TODO
        return True

    def placeCarIntoGarage(self, car):
        #TODO
        pass

    def waitForPlaceIntoGarage(self):
        #TODO
        pass

if __name__ == "__init__":
    pussyNatorController = DePussyNator()
    pussyNatorController.initialize()
    while True:
        car = pussyNatorController.obtainCar()
        if not pussyNatorController.placeCarIntoGarage(car):
            pussyNatorController.waitForPlaceIntoGarage()
            pussyNatorController.placeCarIntoGarage(car)