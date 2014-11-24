from unittest import TestCase
from parking_app.Common import Platform, Vehicle, Weights

__author__ = 'fsoler'


class TestPlatform(TestCase):
    def setUp(self):
        self.patent = 1
        self.hours = 3
        self.car = Vehicle(self.patent, Weights.heavy)
        self.level = 1
        self.column = 3
        self.platform = Platform(self.level, self.column)

    def test_get_level(self):
        self.assertEqual(self.platform.level(), self.level)

    def test_save_car(self):
        hours = 3

        self.assertTrue(self.platform.is_empty())
        self.platform.save_car(self.car, hours)
        self.assertFalse(self.platform.is_empty())

    def test_save_two_cars(self):
        hours = 3
        self.platform.save_car(self.car, hours)

        self.assertRaises(Exception, self.platform.save_car, self.car, hours)

    def test_remove_car_from_empty_platform(self):
        self.assertRaises(Exception, self.platform.remove_car)

    def test_get_weight(self):
        self.assertEqual(self.platform.get_weight(), 0, "the platform must have not weight since is empty")

        hours = 3
        self.platform.save_car(self.car, hours)

        self.assertEqual(self.platform.get_weight(), self.car.get_weight(), "the platform must have the same weight")

    def test_get_elapsed_time(self):
        hours = 3
        self.platform.save_car(self.car, hours)

        self.assertAlmostEqual(self.platform.get_elapsed_time(), 0, None, "hello", 0.002)

    def test_get_remaining_time(self):
        hours = 24
        self.platform.save_car(self.car, hours)

        self.assertAlmostEqual(self.platform.get_remaining_time(), hours, None, "hello", 0.002)

    def test_is_empty(self):
        hours = 3
        self.platform.save_car(self.car, hours)

        self.assertFalse(self.platform.is_empty())