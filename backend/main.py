__author__ = 'adrian'

import sys
import web
import logging

from parking import parking

# Mapping between the urls used by the frontend to objects on the backend
urls = (
    '/parking', 'parking',
    '/parking/car', 'carWithdraw'
)

def init_loggers():
    # set up logging for the example
    logger = logging.getLogger('CylindricalParking')
    logger.setLevel(logging.DEBUG)

    consoleHandler = logging.StreamHandler(stream=sys.stdout)
    consoleHandler.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s%(message)s'))
    logger.addHandler(consoleHandler)


def init_webserver():
    #
    app = web.application(urls, globals())
    app.run()


def main():
    init_loggers()

    # Initialize the rule engine framework
    logging.getLogger('CylindricalParking').debug('Start Parking backend.')
    # Initialize the web server and listen to requests
    init_webserver()


if __name__ == '__main__':
    main()
