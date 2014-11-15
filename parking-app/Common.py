__author__ = 'fsoler'
from enum import Enum
import time
import calendar


'''
esta clase alarma es para reordenar los autos o sacarlos, el mensaje pone la alarma en deliver
'''


class Alarm(Enum):
    deliver = 0
    lessThan15Min = 1
    oneLevelDown = 2
    twoLevelDown = 3


class Weights(Enum):
    empty = 0
    veryLight = 300
    light = 700
    heavy = 1500
    veryHeavy = 3100


class Sector(Enum):
    lower = 0
    middle = 1
    high = 2

    # it would be better add a function that determines the sector from hours


class Vehicle():

    def __init__(self, patent, weight=Weights['veryLight']):
        self._patent = patent
        self._weight = weight

    def get_weight(self):
        return self._weight.value

    def has_this_patent(self, patent):
        return self._patent == patent


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

    #length_of_stay expressed in horas
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


class Cylinder():

    def __init__(self, levels=6, columns=3):
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

    def get_position_to_save_car(self, sector):
        level_range = self.__calculate_range_levels(sector)
        col_weights = [sum([self.__platforms[lvl][col].get_weight() for lvl in level_range])
                       for col in range(self._qttyColumns)]

        temp_platforms = self.__platforms
        for _ in range(self._qttyColumns):
            col = col_weights.index(min(col_weights))
            #aca hago un for de los niveles para ver si encuentro lugar
            for lvl in level_range:
                if temp_platforms[lvl][col].is_empty():
                    return [col, lvl]
            col_weights.pop(col)
            [temp_platforms[lvl].pop(col) for lvl in level_range]

        return None

    def get_car(self, level, column):
        self._qttyOccupied -= 1
        car = self.__platforms[level][column].remove_car()
        self._totalWeight -= car.get_weight()
        return car

    def sector_has_space(self, sector):
        level_range = self.__calculate_range_levels(sector)
        occupied_list = [col for col in range(self._qttyColumns) for lvl in
                         level_range if self.__platforms[lvl][col].is_empty()]
        return False if occupied_list else True

    def has_space(self):
        return self._qttyOccupied != self._qttyPlatforms

    def get_level_type(self, level):
        min_level = self.__calculate_min_level(level)
        return Sector(min_level + 1)

    def __calculate_min_level(self, level):
        return int(Sector.high*level/self._qttyLevels) - 1

    def __calculate_sector(self, level):
        min_level = self.__calculate_min_level(level)
        return range(min_level, min_level + Sector.high)

    def __calculate_range_levels(self, sector):
        min_level = int(sector.value * self._qttyLevels / len(Sector))
        return list(range(min_level, min_level + len(Sector)))