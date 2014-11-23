__author__ = 'adrian'

import sys
from PyQt4 import QtGui

from parking_app.UI.CylinderUI import CylinderUI
from parking_app.UI.CarFormUI import CarFormUI
from parking_app.UI.ParkingSlotsUI import ParkingSlotsUI

import Common as Common

class ParkingUI(QtGui.QMainWindow):

    def __init__(self):
        super(ParkingUI, self).__init__()
        self.initUI()

    def initUI(self):

        self.resize(600, 600)
        self.center()

        self.setWindowTitle('Parking')
        self.setWindowIcon(QtGui.QIcon('Logo.png'))

        self.createMenu()
        self.createToolbar()

        # Se muestra Error en caso de que haya algun problema con algun cilindro
        self.statusBar().showMessage('Normal')

        self.cylinder1 = CylinderUI(Common.Cylinder(1))
        self.cylinder2 = CylinderUI(Common.Cylinder(2))
        self.cylinder3 = CylinderUI(Common.Cylinder(3))

        self.parkingSlots = ParkingSlotsUI(Common.ParkingSlots());

        # main layout
        self.mainLayout = QtGui.QHBoxLayout()

        # add all main to the main vLayout
        self.mainLayout.addWidget(self.cylinder1)
        self.mainLayout.addWidget(self.cylinder2)
        self.mainLayout.addWidget(self.cylinder3)
        self.mainLayout.addWidget(self.parkingSlots)

        # central widget
        centralWidget = QtGui.QWidget()
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)

        self.show()

    def createMenu(self):
        fileMenu = self.menuBar().addMenu('&File')

        exitAction = QtGui.QAction(QtGui.QIcon('Exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        fileMenu.addAction(exitAction)

        simulateMenu = self.menuBar().addMenu('&Simulate')

        alarmAction = QtGui.QAction(QtGui.QIcon('Warning.png'), 'Alarma Aleatoria', self)
        alarmAction.triggered.connect(self.createCustomAlarm);

        newCarAction= QtGui.QAction(QtGui.QIcon('Logo.png'), 'Estacionar Vehiculo', self)
        newCarAction.triggered.connect(self.addNewCar);

        withdrawCarAction= QtGui.QAction(QtGui.QIcon('Car.png'), 'Retirar Vehiculo', self)
        withdrawCarAction.triggered.connect(self.withdrawCar);

        simulateMenu.addAction(alarmAction)
        simulateMenu.addAction(newCarAction)
        simulateMenu.addAction(withdrawCarAction)

    def createToolbar(self):

        exitAction = QtGui.QAction(QtGui.QIcon('Exit.png'), 'Salir', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QtGui.qApp.quit)

        alarmAction = QtGui.QAction(QtGui.QIcon('Warning.png'), 'Alarma Aleatoria', self)
        alarmAction.triggered.connect(self.createCustomAlarm)

        newCarAction= QtGui.QAction(QtGui.QIcon('Logo.png'), 'Estacionar Vehiculo', self)
        newCarAction.triggered.connect(self.addNewCar)

        withdrawCarAction= QtGui.QAction(QtGui.QIcon('Car.png'), 'Retirar Vehiculo', self)
        withdrawCarAction.triggered.connect(self.withdrawCar);

        exitToolbar = self.addToolBar('Exit')
        exitToolbar.addAction(exitAction)

        simulateToolbar = self.addToolBar('Simulate')
        simulateToolbar.addAction(alarmAction)
        simulateToolbar.addAction(newCarAction)
        simulateToolbar.addAction(withdrawCarAction)

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
        self.carForm = CarFormUI()
        self.carForm.resize(400, 200)
        self.carForm.move(50,50)
        self.carForm.show()

    def withdrawCar(self):
        print("Muestra pop up para retirar un auto")

def main():
    app = QtGui.QApplication(sys.argv)
    levels = 6
    columns = 3
    qtty_cylinders = 4
    parkingUI = ParkingUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()