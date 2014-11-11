__author__ = 'adrian'

import logging
import json

class parking:
    def GET(self):
        # Here we should return a json with the parking status
        logging.getLogger('CylindricalParking').debug('Ask for parking status.')
        return json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}]);


class carWithdraw:
    def POST(self, carId):
        # Send a request to the server to withdraw the car
        logging.getLogger('CylindricalParking').debug('Ask for car withdraw.')
        return json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}]);