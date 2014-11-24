__author__ = 'adrian'

from PyQt4 import QtGui
import parking_app.Common as Common

from multiprocessing import Queue

class CarFormUI(QtGui.QWidget):

    def __init__(self, input_queue):
        super(CarFormUI, self).__init__()
        self.__input_queue = input_queue

        self.initUI()

    def initUI(self):

        self.setWindowTitle('New Car')
        self.setWindowIcon(QtGui.QIcon('Logo.png'))

        # Patente
        patenteLayout = QtGui.QHBoxLayout()
        lbl1 = QtGui.QLabel("Patente",self)
        self.patente = QtGui.QLineEdit(self)
        #self.patente.setValidator(PatentValidator())
        self.patente.setInputMask(">AAA-999")
        #self.patente.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        patenteLayout.addWidget(lbl1)
        patenteLayout.addWidget(self.patente)

        # Horas
        hoursLayout = QtGui.QHBoxLayout()
        lbl2 = QtGui.QLabel("Cantidad de horas",self)

        optionsLayout = QtGui.QVBoxLayout()
        self.estadia = QtGui.QRadioButton("Estadia")
        self.estadia.toggled.connect(self.estadiaSelected)

        self.mediaEstadia = QtGui.QRadioButton("Media Estadia")
        self.mediaEstadia.toggled.connect(self.estadiaSelected)

        otherOptionLayout = QtGui.QHBoxLayout()
        self.otro = QtGui.QRadioButton("Otro")
        self.otro.setChecked(True)
        self.otro.toggled.connect(self.otroSelected)
        self.otroSpinBox = QtGui.QSpinBox()
        self.otroSpinBox.setMinimum(1)
        self.otroSpinBox.setMaximum(1440)

        otherOptionLayout.addWidget(self.otro)
        otherOptionLayout.addWidget(self.otroSpinBox)

        optionsLayout.addWidget(self.estadia)
        optionsLayout.addWidget(self.mediaEstadia)
        optionsLayout.addLayout(otherOptionLayout)

        hoursLayout.addWidget(lbl2)
        hoursLayout.addLayout(optionsLayout)

        #Tipo de vehiculo
        self.__vehicle = QtGui.QComboBox()
        self.__vehicle.addItem('Moto')
        self.__vehicle.addItem('Auto')
        self.__vehicle.addItem('Camioneta')
        self.__vehicle.addItem('Utilitario')

        # Boton de aceptar y cancelar
        buttonLayout = QtGui.QHBoxLayout()
        aceptButton = QtGui.QPushButton('Aceptar')
        aceptButton.clicked.connect(self.acept)
        cancelButton = QtGui.QPushButton('Cancelar')
        cancelButton.clicked.connect(self.cancel)

        buttonLayout.addWidget(aceptButton)
        buttonLayout.addWidget(cancelButton)

        layout = QtGui.QVBoxLayout()
        layout.addLayout(patenteLayout)
        layout.addLayout(hoursLayout)
        layout.addWidget(self.__vehicle)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

    def otroSelected(self):
        self.otroSpinBox.setEnabled(True)

    def estadiaSelected(self):
        self.otroSpinBox.setEnabled(False)

    def getWeight(self):
        if self.__vehicle.currentIndex() == 0:
            return Common.Weights.veryLight
        elif self.__vehicle.currentIndex() == 1:
            return Common.Weights.light
        elif self.__vehicle.currentIndex() == 2:
            return Common.Weights.heavy
        elif self.__vehicle.currentIndex() == 3:
            return Common.Weights.veryHeavy

    def acept(self):
        print('Car Form UI - Aceptar - Enviar los datos al estacionamiento')
        # Enviar los datos al estacionamiento
        hours = int(self.otroSpinBox.text())
        if self.estadia.isChecked():
            hours = 720
        elif self.mediaEstadia.isChecked():
            hours = 360

        vehicle = Common.Vehicle(self.patente.text(), self.getWeight())
        self.__input_queue.put([vehicle, hours/60])
        print('Car Form UI - Aceptar - Enviados los datos al estacionamiento')
        self.close()

    def cancel(self):
        print('Cancelar')
        self.close()

