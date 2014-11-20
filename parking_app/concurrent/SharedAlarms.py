__author__ = 'fsoler'


class SharedAlarms():
        def __init__(self, cylinder_id, qtty_levels, qtty_columns):
            self.__cylinder_id = cylinder_id
            self.__alarms = [[None for _ in range(qtty_columns)] for _ in range(qtty_levels)]

        @property
        def alarms(self):
            #here i must block the shared memory
            return self.__alarms

        @alarms.setter
        def alarms(self, alarms):
            #todo
            self.__alarms = alarms
            # here i must release the shared memory
