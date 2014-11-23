__author__ = 'adrian'

import sys

from PyQt4 import QtGui
from PyQt4 import QtCore

from parking_app.UI.CylinderUI import CylinderUI
from parking_app.UI.CarFormUI import CarFormUI
from parking_app.UI.ParkingSlotsUI import ParkingSlotsUI

import parking_app.Common as Common
import parking_app.Platform_Controller as Platform_Controller
import parking_app.Robotic_Dispatcher as Robotic_Dispatcher
import parking_app.Robotic_Hand as Robotic_Hand
import parking_app.Robotic_Deliverer as Robotic_Deliverer

import parking_app.concurrent.SharedAlarms as SharedAlarms

from multiprocessing.managers import BaseManager
from multiprocessing import Process, Lock, Queue, Array, Manager


class ParkingUI(QtGui.QMainWindow):

    def __init__(self, cylinders, parking_slot, input_queue):
        super(ParkingUI, self).__init__()
        self.__cylinders = cylinders
        self.__input_queue = input_queue
        self.__parking_slot = parking_slot
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

        # Se muestra Error en caso de que haya algun problema con algun cilindro
        self.statusBar().showMessage('Normal')

        for cylinder in self.__cylinders:
            main_layout.addWidget(CylinderUI(cylinder))

        main_layout.addWidget(ParkingSlotsUI(self.__parking_slot))

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
        alarm_action.triggered.connect(self.createCustomAlarm);

        new_car_action = QtGui.QAction(QtGui.QIcon('Logo.png'), 'Estacionar Vehiculo', self)
        new_car_action.triggered.connect(self.addNewCar);

        withdraw_car_action = QtGui.QAction(QtGui.QIcon('Car.png'), 'Retirar Vehiculo', self)
        withdraw_car_action.triggered.connect(self.withdrawCar);

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
        withdraw_car_action.triggered.connect(self.withdrawCar);

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
        car_form = CarFormUI()
        car_form.resize(400, 200)
        car_form.move(50,50)
        car_form.show()

    def withdrawCar(self):
        print("Muestra pop up para retirar un auto")


class CylinderManager(BaseManager):
    pass

CylinderManager.register("Cylinder", Common.Cylinder)

class ParkingSlotManager(BaseManager):
    pass

ParkingSlotManager.register("ParkingSlot", Common.ParkingSlots)

def main():
    # we must use the bounded semaphore
    app = QtGui.QApplication(sys.argv)
    levels = 6
    columns = 3
    qtty_cylinders = 4
    qtty_slots = 10

    cylinders = []
    for i in range(qtty_cylinders):
        cylinder_manager = CylinderManager()
        cylinder_manager.start()
        cylinders.append(cylinder_manager.Cylinder(i, levels, columns))

    parking_manager = ParkingSlotManager()
    parking_manager.start()
    parking_slot = parking_manager.ParkingSlot(qtty_slots)

    input_queue = Queue()
    deliver_queue = Queue()

    mutex_cylinders = [Lock() for _ in range(qtty_cylinders)]
    mutex_alarms = [[Lock() for _ in range(columns)] for _ in range(levels)]
    mutex_buffers = [Lock() for _ in range(qtty_cylinders)]
    mutex_parking_slot = Lock()

    alarms = [[None for _ in range(columns)] for _ in range(levels)]
    car_and_hours = [None, None]

    sh_alarms = [Manager().list(alarms) for _ in range(qtty_cylinders)]
    sh_buffers = [Manager().list(car_and_hours) for _ in range(qtty_cylinders)]

    processes = []
    processes.append(Process(target=Platform_Controller, args=(
        qtty_cylinders, levels, columns, cylinders, mutex_cylinders, sh_alarms, mutex_alarms)))
    processes.append(Process(target=Robotic_Deliverer, args=(
        input_queue, parking_slot, mutex_parking_slot)))
    processes.append(Process(target=Robotic_Dispatcher, args=(
        qtty_cylinders, cylinders, mutex_cylinders, deliver_queue, sh_buffers, mutex_buffers)))

    for i in range(qtty_cylinders):
        processes.append(Process(target=Robotic_Hand, args=(
            i, levels, columns, cylinders[i], mutex_cylinders[i], sh_buffers[i],
            mutex_buffers[i], deliver_queue, sh_alarms[i], mutex_alarms[i])))

    [process.start() for process in processes]

    parkingUI = ParkingUI(cylinders, parking_slot, input_queue)

    for p in processes:
        p.join()


if __name__ == '__main__':
    main()