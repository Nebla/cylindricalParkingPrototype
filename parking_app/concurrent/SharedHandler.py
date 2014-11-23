__author__ = 'fsoler'


class SharedHandler():
        def __init__(self, shared_data, mutex_data):
            self.__sh_data = shared_data
            self.__mutex = mutex_data

        @property
        def alarms(self):
            self.__mutex.acquire()
            return self.__sh_data

        @alarms.setter
        def alarms(self, alarms):
            self.__sh_data = alarms
            self.__mutex.release()