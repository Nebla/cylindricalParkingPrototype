__author__ = 'fsoler'


class PlatformController():
    def __init__(self):
        #TODO
        pass

    def initialize(self):
        #TODO
        pass

    def getUsedPlatforms(self):
        #TODO
        pass

    def setAlarm(self):
        #TODO
        pass

    def isMarkedToLeave(self):
        #TODO
        pass

if __name__ == "__init__":
    platformController = PlatformController()
    platformController.initialize()
    while True:
        platforms = platformController.getUsedPlatforms()
        for platform in platforms:
            level = platform.getLevel()
            elapsedTime = platform.getElapsedTime()
            if times.getTimeLevel(level) <= elapsedTime:
                platformController.setAlarm(0)
            if times.getTimeLevel(level)- MarginTime <= elapsedTime:
                platformController.setAlarm(CarToLeave)
            if level != 1 and platformController.isMarkedToLeave(platform):
                for i in range(1, level):
                    if times.getTimeLevel(i)/2 > elapsedTime:
                        platformController.setAlarm(level - i)
                        break
        platformController.sleepOneMinute()