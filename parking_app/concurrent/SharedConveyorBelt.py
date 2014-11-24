__author__ = 'fsoler'


class SharedConveyorBelt():

    def __init__(self, conveyor_id):
        self.__cylinder = None

    def initialize(self, conveyor_id):
        #todo
        pass

    def add(self, info):
        #here i must block the shared memory
        pass

    def get(self, receiver_id):
        #todo
        pass
        # here i must release the shared memory
