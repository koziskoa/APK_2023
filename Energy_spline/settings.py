from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

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
    def __init__(self, prevdmin, previters, prevalpha, prevbeta, prevgamma, prevlamb, *args, **kwargs):
        """Constructs QDialog window."""
        super().__init__(*args, **kwargs)
        # Initialize necessary objects
        from draw import Draw
        d = Draw()
        self.setWindowTitle("Energy Spline Properties")
        self.dmin = QLineEdit(self)
        self.iters = QLineEdit(self)
        self.alpha = QLineEdit(self)
        self.beta = QLineEdit(self)
        self.gamma = QLineEdit(self)
        self.lamb = QLineEdit(self)
        self.ok_button = QPushButton("Ok", self)
        self.cancel_button = QPushButton("Cancel", self)
        # Set previously used values as placeholder text
        self.dmin.setPlaceholderText(str(prevdmin))
        self.iters.setPlaceholderText(str(previters))
        self.alpha.setPlaceholderText(str(prevalpha))
        self.beta.setPlaceholderText(str(prevbeta))
        self.gamma.setPlaceholderText(str(prevgamma))
        self.lamb.setPlaceholderText(str(prevlamb))
        # Create layout
        layout = QFormLayout(self)
        layout.addRow("Minimum distance", self.dmin)
        layout.addRow("No. of iterations", self.iters)
        layout.addRow("Alpha", self.alpha)
        layout.addRow("Beta", self.beta)
        layout.addRow("Gamma", self.gamma)
        layout.addRow("Lambda", self.lamb)
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
        return self.dmin.text(), self.iters.text(), self.alpha.text(), self.beta.text(), self.gamma.text(), self.lamb.text()