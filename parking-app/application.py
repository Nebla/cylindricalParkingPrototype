__author__ = 'adrian'

import sys
from PyQt4 import QtGui

from UI.CylinderUI import CylinderUI

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

        cylinder1 = CylinderUI()
        cylinder2 = CylinderUI()
        cylinder3 = CylinderUI()

        # main layout
        self.mainLayout = QtGui.QHBoxLayout()

        # add all main to the main vLayout
        self.mainLayout.addWidget(cylinder1)
        self.mainLayout.addWidget(cylinder2)
        self.mainLayout.addWidget(cylinder3)

        # central widget
        centralWidget = QtGui.QWidget()
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)

        self.show()

    def createMenu(self):
        exitAction = QtGui.QAction(QtGui.QIcon('Exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        self.menuBar().addMenu('&File').addAction(exitAction)

    def createToolbar(self):
        exitAction = QtGui.QAction(QtGui.QIcon('Exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QtGui.qApp.quit)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)


    def center(self):

        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():

    app = QtGui.QApplication(sys.argv)
    parkingUI = ParkingUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()