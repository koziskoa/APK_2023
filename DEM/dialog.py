from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from QPoint3DF import *

class InputDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Enter Contour Parameters")
        self.zmin = QLineEdit(self)
        self.zmax = QLineEdit(self)
        self.dz = QLineEdit(self)
        self.ok_button = QPushButton("Ok", self)
        self.cancel_button = QPushButton("Cancel", self)

        layout = QFormLayout(self)
        layout.addRow("Minimum altitude", self.zmin)
        layout.addRow("Maximum altitude", self.zmax)
        layout.addRow("Step", self.dz)
        layout.addRow(self.ok_button)
        layout.addRow(self.cancel_button)

        self.ok_button.clicked.connect(self.okButtonClicked)
        self.cancel_button.clicked.connect(self.cancelButtonClicked)

    def okButtonClicked(self):
        self.accept()

    def cancelButtonClicked(self):
        self.reject()

    def getInputs(self):
        return self.zmin.text(), self.zmax.text(), self.dz.text()
