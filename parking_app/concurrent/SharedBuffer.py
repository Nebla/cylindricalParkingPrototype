__author__ = 'fsoler'


class SharedBuffer():

    def __init__(self, cylinder_id, buffer_id):
        #todo
        self.__buffer = None

    @property
    def buffer(self):
        #here i must block the shared memory
        #todo
        return self.__buffer

    @buffer.setter
    def buffer(self, cylinder):
        #todo
        self.__buffer = cylinder
        # here i must release the shared memory
