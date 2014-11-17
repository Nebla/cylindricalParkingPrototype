from unittest import TestCase
from parking_app.Common import Vehicle, Weights

__author__ = 'fsoler'


class TestVehicle(TestCase):
    def setUp(self):
        self.patent = 1
        self.car = Vehicle(self.patent, Weights.heavy)

    def test_get_weight(self):
        self.assertNotEqual(self.car.get_weight(), Weights.veryHeavy.value)
        self.assertNotEqual(self.car.get_weight(), Weights.light.value)
        self.assertNotEqual(self.car.get_weight(), Weights.veryLight.value)
        self.assertEqual(self.car.get_weight(), Weights.heavy.value)

    def test_has_this_patent(self):
        patent = 2
        self.assertFalse(self.car.has_this_patent(patent))
        self.assertTrue(self.car.has_this_patent(self.patent))