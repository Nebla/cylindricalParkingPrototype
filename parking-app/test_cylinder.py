__author__ = 'fsoler'
import unittest
from Common import Cylinder, Vehicle, Weights, Sector


class TestCylinderFunctions(unittest.TestCase):
    def setUp(self):
        self.columns = 1
        self.levels = 3
        self.cylinder = self.CylinderExtension(self.levels, self.columns)

    def test_cylinder_well_initialized(self):
        self.assertEqual(self.cylinder.get_amount_columns(), self.columns,
                         "the columns quantity does not match")
        self.assertEqual(self.cylinder.get_amount_levels(), self.levels,
                         "the levels quantity does not match")
        self.assertEqual(self.cylinder.get_actual_weight(), 0,
                         "the weight must be initialized with 0")
        self.assertEqual(self.cylinder.get_amount_occupied(), 0,
                         "the amount occupied must be 0")
        qtty_platforms = self.columns * self.levels
        self.assertEqual(self.cylinder.get_amount_platforms(), qtty_platforms,
                         "the platform quantity does not match")
        self.assertTrue(self.cylinder.has_space())

    def test_adding_one_car(self):

        self.assertEqual(self.cylinder.get_amount_occupied(), 0,
                         "the amount occupied must be 0")

        car = Vehicle(1, Weights.heavy)
        [level, column] = self.cylinder.get_position_to_save_car(Sector.lower)
        hours = 3
        self.cylinder.add_car(car, level, column, hours)

        self.assertEqual(self.cylinder.get_amount_occupied(), 1,
                         "the amount occupied must be 1")
        self.assertEqual(self.cylinder.get_actual_weight(), Weights.heavy.value,
                         "the weight must be initialized with 0")

    def test_adding_two_cars_in_same_platform(self):
        car = Vehicle(1, Weights.heavy)
        level = 1
        column = 0
        hours = 3
        self.cylinder.add_car(car, level, column, hours)

        self.assertRaises(Exception, self.cylinder.add_car, car, level, column, hours)

    def test_get_position_to_save_car(self):
        hours = 1
        pos = self.cylinder.get_position_to_save_car(hours)
        self.assertEqual(pos, Sector.lower)

        hours = 2.8
        pos = self.cylinder.get_position_to_save_car(hours)
        self.assertEqual(pos, Sector.lower)

        hours = 3
        pos = self.cylinder.get_position_to_save_car(hours)
        self.assertEqual(pos, Sector.middle)

        hours = 11.9
        pos = self.cylinder.get_position_to_save_car(hours)
        self.assertEqual(pos, Sector.middle)

        hours = 12
        pos = self.cylinder.get_position_to_save_car(hours)
        self.assertEqual(pos, Sector.high)

        hours = 50
        pos = self.cylinder.get_position_to_save_car(hours)
        self.assertEqual(pos, Sector.high)


    def test_get_car(self):
        self.fail()

    def test_get_two_cars_from_same_platform(self):
        self.fail()

    def test_sector_has_space(self):
        self.fail()

    def test_sector_has_no_space(self):
        self.fail()

    def test_completing_cylinder(self):
        car = Vehicle(1, Weights.heavy)
        level = 0
        column = 0
        hours = 3

        self.assertTrue(self.cylinder.has_space())
        self.cylinder.add_car(car, level, column, hours)
        self.assertTrue(self.cylinder.has_space())

        level = 1
        self.cylinder.add_car(car, level, column, hours)
        self.assertTrue(self.cylinder.has_space())

        level = 2
        self.cylinder.add_car(car, level, column, hours)
        self.assertFalse(self.cylinder.has_space())

    class CylinderExtension(Cylinder):

        def __init__(self, levels, columns):
            super().__init__(levels, columns)

        def get_amount_columns(self):
            return self._qttyColumns

        def get_amount_levels(self):
            return self._qttyLevels

        def get_amount_occupied(self):
            return self._qttyOccupied

        def get_amount_platforms(self):
            return self._qttyPlatforms

        def get_actual_weight(self):
            return self._totalWeight

if __name__ == '__main__':
    unittest.main()