from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from QPoint3DF import *

class InputDialog(QDialog):
    """
    A class used to create contour settings dialog.
    ...

    Methods
    ----------
    okButtonClicked():
       Emits accept signal on button click.

    cancelButtonClicked():
       Emits reject signal on button click.

    getInputs():
       Returns input values.
        """
    def __init__(self, *args, **kwargs):
        """Constructs QDialog window."""
        super().__init__(*args, **kwargs)
        # Initialize necessary objects
        self.setWindowTitle("Contour Properties")
        self.zmin = QLineEdit(self)
        self.zmax = QLineEdit(self)
        self.dz = QLineEdit(self)
        self.ok_button = QPushButton("Ok", self)
        self.cancel_button = QPushButton("Cancel", self)
        # Create layout
        layout = QFormLayout(self)
        layout.addRow("Minimum altitude [m]", self.zmin)
        layout.addRow("Maximum altitude [m]", self.zmax)
        layout.addRow("Step [m]", self.dz)
        layout.addRow(self.ok_button)
        layout.addRow(self.cancel_button)
        # Connect signals to slots
        self.ok_button.clicked.connect(self.okButtonClicked)
        self.cancel_button.clicked.connect(self.cancelButtonClicked)

    def okButtonClicked(self):
        """Emits accept signal on button click."""
        self.accept()

    def cancelButtonClicked(self):
        """Emits reject signal on button click."""
        self.reject()

    def getInputs(self):
        """Returns input values."""
        return self.zmin.text(), self.zmax.text(), self.dz.text()