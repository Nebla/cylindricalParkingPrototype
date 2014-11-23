__author__ = 'fsoler'
from enum import Enum
import time
import calendar

'''
esta clase alarma es para reordenar los autos o sacarlos, el mensaje pone la alarma en deliver
'''
# this is the margin time to deliver the car, in seconds
Margin_time = 9000
Input_id = 1
Conveyor_input_id = 1
Conveyor_output_id = 2
Robotic_dispatcher_id = 3
Robotic_deliverer_id = 4


class Alarm(Enum):
    deliver = 0
    oneLevelDown = 1
    twoLevelDown = 2
    lessThanMarginTime = 3


class Weights(Enum):
    empty = 0
    veryLight = 300
    light = 700
    heavy = 1500
    veryHeavy = 3100


class Sector(Enum):
    lower = 3
    middle = 12
    high = 9999


class ParkingSlots():
    def __init__(self, quantity_slots=10):
        self.__levels = 2
        self.__columns = int(quantity_slots/self.__levels)
        self.__slots = [[None for _ in range(self.__columns)]
                        for _ in range(self.__levels)]

    def save_car(self, car):
        free_slots = self.__get_index_free_spaces()
        if not free_slots:
            return False
        [lvl, col] = free_slots[0]
        self.__slots[lvl][col] = car
        return True
    
    def get_car(self, lvl, col):
        #todo
        pass

    def __get_index_free_spaces(self):
        levels = range(self.__levels)
        columns = range(self.__columns)
        return [[lvl, col] for lvl in levels for col in columns
                if self.__slots[lvl][col] is not None]

class Vehicle():
    def __init__(self, patent, weight=Weights['veryLight']):
        self._patent = patent
        self._weight = weight

    def get_weight(self):
        return self._weight.value

    def has_this_patent(self, patent):
        return self._patent == patent

    @property
    def patent(self):
        return self._patent


class Platform():
    TimeFormat = "%y-%m-%dT%H:%M:%S +0000"

    def __init__(self, level, column):
        self.__level = level
        self.__column = column
        self.__isOccupied = False
        self.__timeIn = None
        self.__timeOut = None
        self.__vehicle = Vehicle(0, Weights.empty)

    @staticmethod
    def __hour2sec(hours):
        return hours * 3600

    @staticmethod
    def __sec2hour(seconds):
        return seconds / 3600

    # length_of_stay expressed in horas
    def save_car(self, car, length_of_stay):
        if self.__isOccupied:
            raise Exception("this platform is occupied, can not add a car")

        self.__vehicle = car
        self.__isOccupied = True
        self.__timeIn = time.strftime(self.TimeFormat, time.gmtime(time.time()))
        self.__timeOut = time.strftime(self.TimeFormat, time.gmtime(time.time() + self.__hour2sec(length_of_stay)))

    def remove_car(self):
        if not self.__isOccupied:
            raise Exception("this platform is not occupied, can not remove a car")

        self.__isOccupied = False
        car = self.__vehicle
        return car

    def get_weight(self):
        return self.__vehicle.get_weight()

    def get_elapsed_time(self):
        seconds = calendar.timegm(time.strptime(self.__timeIn, self.TimeFormat))
        return self.__sec2hour(time.time() - seconds)

    def get_remaining_time(self):
        seconds = calendar.timegm(time.strptime(self.__timeOut, self.TimeFormat))
        return self.__sec2hour(seconds - time.time())

    def is_empty(self):
        return not self.__isOccupied

    @property
    def level(self):
        return self.__level

    @property
    def vehicle(self):
        return self.__vehicle


class Cylinder():
    def __init__(self, cylinder_id, levels=6, columns=3):
        self.__id = cylinder_id
        self.__platforms = [[Platform(lvl, column) for column in range(columns)] for lvl in range(levels)]
        self._qttyLevels = levels
        self._qttyColumns = columns
        self._qttyPlatforms = levels * columns
        self._qttyOccupied = 0
        self._totalWeight = 0

    def add_car(self, car, level, column, length_of_stay):
        self.__platforms[level][column].save_car(car, length_of_stay)
        self._qttyOccupied += 1
        self._totalWeight += car.get_weight()

    '''
    def get_position_to_save_car(self, level):
        level_range = self.__calculate_sector(level)
        col_weights = [sum([self.__platforms[lvl][col]for lvl in level_range])
                       for col in range(self._qttyColumns)]
        return col_weights.index(min(col_weights))
    '''

    def get_position_to_save_car(self, length_of_stay):
        sector = self.__get_sector_from_time(length_of_stay)
        level_range = self.__calculate_range_levels(sector)
        col_weights = [sum([self.__platforms[lvl][col].get_weight() for lvl in level_range])
                       for col in range(self._qttyColumns)]

        temp_platforms = self.__platforms
        for _ in range(self._qttyColumns):
            col = col_weights.index(min(col_weights))
            # aca hago un for de los niveles para ver si encuentro lugar
            for lvl in level_range:
                if temp_platforms[lvl][col].is_empty():
                    return [lvl, col]
            col_weights.pop(col)
            [temp_platforms[lvl].pop(col) for lvl in level_range]

        return None

    def get_remaining_time(self, level, column):
        return self.__platforms[level][column].get_remaining_time()

    def get_car(self, level, column):
        self._qttyOccupied -= 1
        car = self.__platforms[level][column].remove_car()
        self._totalWeight -= car.get_weight()
        return car

    def sector_has_space(self, sector):
        level_range = self.__calculate_range_levels(sector)
        free_list = [col for col in range(self._qttyColumns) for lvl in
                     level_range if self.__platforms[lvl][col].is_empty()]
        return True if free_list else False

    def has_space(self):
        return self._qttyOccupied != self._qttyPlatforms

    def calculate_sector(self, level):
        sector_list = [sec for sec in Sector]
        index = int(len(Sector)*level/self._qttyLevels)
        return sector_list[index]

    @staticmethod
    def __get_sector_from_time(length_of_stay):
        for sector in Sector:
            if sector.value > length_of_stay:
                return sector
        return Sector.high

    def __calculate_range_levels(self, sector):
        index = [i for i in Sector].index(sector)
        len_sector = int(self._qttyLevels / len(Sector))
        min_level = int(index * len_sector)
        return list(range(min_level, min_level + len_sector))

    @property
    def weight(self):
        return self._totalWeight

    @property
    def id(self):
        return self.__id

    @property
    def qtty_levels(self):
        return self._qttyLevels

    @property
    def qtty_columns(self):
        return self._qttyColumns

    @property
    def platforms(self):
        return self.__platforms