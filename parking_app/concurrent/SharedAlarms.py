__author__ = 'fsoler'


class SharedAlarms():
        def __init__(self, shared_data, mutex_data):
            self.__alarms = shared_data
            self.__mutex = mutex_data

        @property
        def alarms(self):
            self.__mutex.acquire()
            return self.__alarms

        @alarms.setter
        def alarms(self, alarms):
            #todo
            self.__alarms = alarms
            self.__mutex.release()
