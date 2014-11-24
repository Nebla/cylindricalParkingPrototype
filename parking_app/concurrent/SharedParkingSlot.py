__author__ = 'fsoler'
import parking_app.Common as Common


class SharedParkingSlots():

    def __init__(self):
        #todo
        self.__slots = Common.ParkingSlots()

    @property
    def slots(self):
        #here i must block the shared memory
        #todo
        return self.__slots

    @slots.setter
    def slots(self, slots):
        #todo
        self.__slots = slots
        # here i must release the shared memory
