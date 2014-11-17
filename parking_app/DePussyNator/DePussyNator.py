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

    def run(self):
        while True:
            car = self.obtainCar()
            if not self.placeCarIntoGarage(car):
                self.waitForPlaceIntoGarage()
                self.placeCarIntoGarage(car)

if __name__ == "__init__":
    pussyNatorController = DePussyNator()
    pussyNatorController.initialize()
    pussyNatorController.run()
