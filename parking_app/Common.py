__author__ = 'fsoler'
from enum import Enum
import time
import calendar
from PyQt4 import QtCore
import copy

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
    stay = 0
    deliver = 1
    oneLevelDown = 2
    twoLevelDown = 3
    lessThanMarginTime = 4


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
    # level, column, vehicle id, vehicle weight
    update = QtCore.pyqtSignal(int, int, str, int)

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

        self.update.emit(lvl, col, car.get_patent(), car.get_weight())
        return True
    
    def get_car(self, lvl, col):
        if self.__slots[lvl][col] is None:
            raise Exception("can not get a car from free slot")
        self.update.emit(lvl, col, "", Weights.empty.value)
        car = self.__slots[lvl][col]
        self.__slots[lvl][col] = None
        return car

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

    def get_patent(self):
        patent = self._patent
        return patent

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

    @staticmethod
    def __sec2min(seconds):
        return seconds / 60

    # length_of_stay expressed in hours
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

    def get_remaining_time_in_minutes(self):
        seconds = self.get_remaining_time()
        return self.__sec2min(seconds)

    def get_remaining_time(self):
        seconds = calendar.timegm(time.strptime(self.__timeOut, self.TimeFormat))
        return seconds - time.time()

    def is_empty(self):
        return not self.__isOccupied

    def level(self):
        level = self.__level
        return level

    def column(self):
        column = self.__column
        return column


    def vehicle(self):
        vehicle = self.__vehicle
        return vehicle


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
        result = self.__get_position_to_save_car([sector])
        print(result)
        if result is not None:
            return result

        sector_list = [sector for sector in Sector]
        sector_list.remove(sector)
        result = self.__get_position_to_save_car(sector_list)
        print(result)
        if result is None:
            raise Exception("all platforms are occupied")
        return result

    def __get_position_to_save_car(self, sector_list):
        for sector in sector_list:
            level_range = self.__calculate_range_levels(sector)
            col_weights = [sum([self.__platforms[lvl][col].get_weight() for lvl in level_range])
                           for col in range(self._qttyColumns)]

            temp_platforms = copy.deepcopy(self.__platforms)
            for _ in range(self._qttyColumns):
                col = col_weights.index(min(col_weights))
                # aca hago un for de los niveles para ver si encuentro lugar
                for lvl in level_range:
                    if temp_platforms[lvl][col].is_empty():
                        return [lvl, col]
                col_weights.pop(col)
                [temp_platforms[lvl].pop(col) for lvl in level_range]


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

    def weight(self):
        weight = self._totalWeight
        return weight

    def id(self):
        my_id = self.__id
        return my_id

    def qtty_levels(self):
        levels = self._qttyLevels
        return levels

    def qtty_columns(self):
        columns = self._qttyColumns
        return columns

    def platforms(self):
        platforms = self.__platforms
        return platforms