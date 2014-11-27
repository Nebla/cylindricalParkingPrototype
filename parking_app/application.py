__author__ = 'adrian'

import sys

from PyQt4 import QtGui
from PyQt4 import QtCore

import time

from parking_app.UI.CylinderUI import CylinderUI
from parking_app.UI.CarFormUI import CarFormUI
from parking_app.UI.ParkingSlotsUI import ParkingSlotsUI
from parking_app.UI.WithdrawFormUI import WithdrawFormUI

import parking_app.Common as Common
import parking_app.Platform_Controller as Platform_Controller
import parking_app.Robotic_Dispatcher as Robotic_Dispatcher
import parking_app.Robotic_Hand as Robotic_Hand
import parking_app.Robotic_Deliverer as Robotic_Deliverer
import parking_app.concurrent.SharedHandler as ShHan

import parking_app.concurrent.SharedAlarms as SharedAlarms

from multiprocessing.managers import BaseManager
from multiprocessing import Process, Lock, Queue, Array, Manager, SimpleQueue, Pipe
import queue
import copy


class ParkingUI(QtGui.QMainWindow):

    def __init__(self, qtty_cylinders,  levels, columns, qtty_slots):
        super(ParkingUI, self).__init__()

        self.cylindersUI = []

        cylinders = []
        for i in range(qtty_cylinders):
            cylinder_manager = CylinderManager()
            cylinder_manager.start()
            cylinders.append(cylinder_manager.Cylinder(i, levels, columns))

        parking_manager = ParkingSlotManager()
        parking_manager.start()
        parking_slot = parking_manager.ParkingSlots(qtty_slots)

        self.__input_queue = Queue()
        deliver_queue = Queue()

        mutex_cylinders = [Lock() for _ in range(qtty_cylinders)]
        mutex_alarms = [Lock() for _ in range(qtty_cylinders)]
        mutex_buffers = [Lock() for _ in range(qtty_cylinders)]
        mutex_parking_slot = Lock()

        alarms = [[None for _ in range(columns)] for _ in range(levels)]
        alarms = [copy.deepcopy(alarms) for _ in range(qtty_cylinders)]
        car_and_hours = [None, None]

        sh_alarms = [Manager().list(alarms[i]) for i in range(qtty_cylinders)]
        sh_buffers = [Manager().list(car_and_hours) for _ in range(qtty_cylinders)]

        platform_controller = Platform_Controller.PlatformController(qtty_cylinders)
        platform_controller.initialize(cylinders, mutex_cylinders, sh_alarms,
                                       mutex_alarms)
        QtCore.QObject.connect(platform_controller, QtCore.SIGNAL('update(int, int, int, QString, int, int)'), self.updateUI)
        platform_controller.start()

        dispatcher_controller = Robotic_Dispatcher.RoboticDispatcher(qtty_cylinders)

        dispatcher_controller.initialize(cylinders, mutex_cylinders,
                                         self.__input_queue, sh_buffers, mutex_buffers)
        dispatcher_controller.start()

        robotic_deliverer_controller = Robotic_Deliverer.RoboticDeliverer()
        robotic_deliverer_controller.initialize(deliver_queue, parking_slot,
                                                mutex_parking_slot)

        self.__parking_slot = ShHan.SharedHandler(parking_slot, mutex_parking_slot)
        self.__parking_slot_UI = ParkingSlotsUI(self.__parking_slot)
        QtCore.QObject.connect(robotic_deliverer_controller, QtCore.SIGNAL('update(int, QString, int)'),
                               self.__parking_slot_UI.updateSlot)
        robotic_deliverer_controller.start()

        for i in range(qtty_cylinders):
            hand_controller = Robotic_Hand.RoboticHand(i, levels, columns)
            hand_controller.initialize(cylinders[i], mutex_cylinders[i], sh_buffers[i],
                                       mutex_buffers[i], sh_alarms[i], mutex_alarms[i], deliver_queue)
            QtCore.QObject.connect(hand_controller, QtCore.SIGNAL('update(int, int, int, QString, int, int)'), self.updateUI)
            hand_controller.start()
            time.sleep(1)

        # va a ser raro el connect dado que el update esta dentro de la clase de parking slot, si anda genial, si no anda
        # hay que hacer que el metodo devuelva col y lvl para la visual.

        self.__cylinders = [ShHan.SharedHandler(cylinders[i], mutex_cylinders[i]) for i in range(len(cylinders))]

        self.init_ui()

    def init_ui(self):

        self.resize(600, 600)
        self.center()

        self.setWindowTitle('Parking')
        self.setWindowIcon(QtGui.QIcon('Logo.png'))

        self.create_menu()
        self.create_toolbar()

        # main layout
        main_layout = QtGui.QHBoxLayout()

        # cylinder_layout = QtGui.QHBoxLayout()
        # Se muestra Error en caso de que haya algun problema con algun cilindro
        self.statusBar().showMessage('Normal')

        for i in self.__cylinders:
            cylinder = i.data
            cylinderUI = CylinderUI(cylinder)
            main_layout.addWidget(cylinderUI)
            self.cylindersUI.append(cylinderUI)
            i.data = cylinder

        #main_layout.addLayout(cylinder_layout)
        #main_layout.addWidget(ParkingSlotsUI(self.__parking_slot))
        self.__parking_slot_UI.setMaximumWidth(100)
        main_layout.addWidget(self.__parking_slot_UI)

        # central widget
        central_widget = QtGui.QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.show()

    def create_menu(self):
        file_menu = self.menuBar().addMenu('&File')

        exit_action = QtGui.QAction(QtGui.QIcon('Exit.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(QtGui.qApp.quit)

        file_menu.addAction(exit_action)

        simulate_menu = self.menuBar().addMenu('&Simulate')

        alarm_action = QtGui.QAction(QtGui.QIcon('Warning.png'), 'Alarma Aleatoria', self)
        alarm_action.triggered.connect(self.createCustomAlarm)

        new_car_action = QtGui.QAction(QtGui.QIcon('Logo.png'), 'Estacionar Vehiculo', self)
        new_car_action.triggered.connect(self.addNewCar)

        withdraw_car_action = QtGui.QAction(QtGui.QIcon('Car.png'), 'Retirar Vehiculo', self)
        withdraw_car_action.triggered.connect(self.withdrawCar)

        simulate_menu.addAction(alarm_action)
        simulate_menu.addAction(new_car_action)
        simulate_menu.addAction(withdraw_car_action)

    def create_toolbar(self):

        exit_action = QtGui.QAction(QtGui.QIcon('Exit.png'), 'Salir', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(QtGui.qApp.quit)

        alarm_action = QtGui.QAction(QtGui.QIcon('Warning.png'), 'Alarma Aleatoria', self)
        alarm_action.triggered.connect(self.createCustomAlarm)

        new_car_action = QtGui.QAction(QtGui.QIcon('Logo.png'), 'Estacionar Vehiculo', self)
        new_car_action.triggered.connect(self.addNewCar)

        withdraw_car_action= QtGui.QAction(QtGui.QIcon('Car.png'), 'Retirar Vehiculo', self)
        withdraw_car_action.triggered.connect(self.withdrawCar)

        exit_toolbar = self.addToolBar('Exit')
        exit_toolbar.addAction(exit_action)

        simulate_toolbar = self.addToolBar('Simulate')
        simulate_toolbar.addAction(alarm_action)
        simulate_toolbar.addAction(new_car_action)
        simulate_toolbar.addAction(withdraw_car_action)

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def createCustomAlarm(self):
        # Show that the slot has been called.
        print("Creando un error aleatorio")

    def addNewCar(self):
        print("Muestra pop up para agregar un nuevo auto")
        self.car_form = CarFormUI(self.__input_queue)
        self.car_form.resize(400, 200)
        self.car_form.move(150,150)
        self.car_form.show()

    def withdrawCar(self):
        print("Muestra pop up para retirar un auto")
        self.withdraw_car_form = WithdrawFormUI(self.__parking_slot)
        self.withdraw_car_form.resize(400, 200)
        self.withdraw_car_form.move(150,150)
        QtCore.QObject.connect(self.withdraw_car_form, QtCore.SIGNAL('update(int, QString, int)'),
                               self.__parking_slot_UI.updateSlot)
        self.withdraw_car_form.show()

    def updateUI(self, cylinder, level, column, vehicle_patent, vehicle_weight, alarm):
        #print("Should update ui - cylinder %d level %d column %d patent %s"%(cylinder, level, column, vehicle_patent))
        self.cylindersUI[cylinder].updatePlatform(level, column, vehicle_patent, vehicle_weight, alarm)


class CylinderManager(BaseManager):
    pass

CylinderManager.register("Cylinder", Common.Cylinder)


class ParkingSlotManager(BaseManager):
    pass

ParkingSlotManager.register("ParkingSlots", Common.ParkingSlots)


def main():
    # we must use the bounded semaphore
    app = QtGui.QApplication(sys.argv)
    levels = 6
    columns = 3
    qtty_cylinders = 3
    qtty_slots = 10

    parkingUI = ParkingUI(qtty_cylinders,  levels, columns, qtty_slots)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()