__author__ = 'fsoler'
import parking_app.Common as Common


class SharedCylinder():

    def __init__(self, sh_data, mutex):
        self.__cylinder = sh_data
        self.__mutex = mutex

    @property
    def cylinder(self):
        self.__mutex.acquire()
        return self.__cylinder

    @cylinder.setter
    def cylinder(self, cylinder):
        self.__cylinder = cylinder
        self.__mutex.release()
