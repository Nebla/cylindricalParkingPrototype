__author__ = 'fsoler'


class SharedHandler():
        def __init__(self, shared_data, mutex_data):
            self.__sh_data = shared_data
            self.__mutex = mutex_data

        @property
        def data(self):
            self.__mutex.acquire()
            return self.__sh_data

        @data.setter
        def data(self, data):
            self.__sh_data = data
            self.__mutex.release()