__author__ = 'fsoler'
import parking_app.Common as Common


class SharedCylinder():

    def __init__(self, cylinder_id):
        self.__cylinder = Common.Cylinder(cylinder_id)

    @property
    def cylinder(self):
        #here i must block the shared memory
        return self.__cylinder

    @cylinder.setter
    def cylinder(self, cylinder):
        #todo
        self.__cylinder = cylinder
        # here i must release the shared memory
