""" 
This program serves for creating and computing digital elevation model (DEM) from a point cloud. 
As part of the programme it is possible to compute contour lines, slope and aspect of DEM.
"""

from PyQt6 import QtCore, QtGui, QtWidgets
from draw import Draw
from Edge import *
from QPoint3DF import *
from algorithms import *
from dialog import *
import csv

class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.showMaximized()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainForm.sizePolicy().hasHeightForWidth())
        MainForm.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(parent=MainForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Canvas = Draw(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Canvas.sizePolicy().hasHeightForWidth())
        self.Canvas.setSizePolicy(sizePolicy)
        self.Canvas.setObjectName("Canvas")
        self.horizontalLayout.addWidget(self.Canvas)
        MainForm.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainForm)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 815, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAnalysis = QtWidgets.QMenu(parent=self.menubar)
        self.menuAnalysis.setObjectName("menuAnalysis")
        self.menuSettings = QtWidgets.QMenu(parent=self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuView = QtWidgets.QMenu(parent=self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuHelp = QtWidgets.QMenu(parent=self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainForm.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainForm)
        self.statusbar.setObjectName("statusbar")
        MainForm.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(parent=MainForm)
        self.toolBar.setObjectName("toolBar")
        MainForm.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.actionOpen = QtGui.QAction(parent=MainForm)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/open_file.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExit = QtGui.QAction(parent=MainForm)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/exit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionExit.setIcon(icon1)
        self.actionExit.setObjectName("actionExit")
        self.actionCreate_DMT = QtGui.QAction(parent=MainForm)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/triangles2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionCreate_DMT.setIcon(icon2)
        self.actionCreate_DMT.setObjectName("actionCreate_DMT")
        self.actionCreate_lines = QtGui.QAction(parent=MainForm)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/contours2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionCreate_lines.setIcon(icon3)
        self.actionCreate_lines.setObjectName("actionCreate_lines")
        self.actionAnalyze_aspect = QtGui.QAction(parent=MainForm)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/orientation2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionAnalyze_aspect.setIcon(icon4)
        self.actionAnalyze_aspect.setObjectName("actionAnalyze_aspect")
        self.actionAnalyze_slope = QtGui.QAction(parent=MainForm)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/slope2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionAnalyze_slope.setIcon(icon5)
        self.actionAnalyze_slope.setObjectName("actionAnalyze_slope")
        self.actionContourSettings = QtGui.QAction(parent=MainForm)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icons/settings.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionContourSettings.setIcon(icon6)
        self.actionContourSettings.setObjectName("actionContourSettings")
        self.actionClear = QtGui.QAction(parent=MainForm)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("icons/clear.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClear.setIcon(icon7)
        self.actionClear.setObjectName("actionClear")
        self.actionAbout = QtGui.QAction(parent=MainForm)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("icons/about.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionAbout.setIcon(icon8)
        self.actionAbout.setObjectName("actionAbout")
        self.actionClearSlopeAspect = QtGui.QAction(parent=MainForm)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("icons/clearslopeaspect.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClearSlopeAspect.setIcon(icon9)
        self.actionClearSlopeAspect.setObjectName("actionClearSlopeAspect")
        self.actionClearContours = QtGui.QAction(parent=MainForm)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("icons/clearcontours.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClearContours.setIcon(icon10)
        self.actionClearContours.setObjectName("actionClearContours")
        self.actionShowContourLabels = QtGui.QAction(parent=MainForm)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("icons/contourlabels.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionShowContourLabels.setIcon(icon11)
        self.actionShowContourLabels.setObjectName("actionShowContourLabels")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuAnalysis.addAction(self.actionCreate_DMT)
        self.menuAnalysis.addAction(self.actionCreate_lines)
        self.menuAnalysis.addAction(self.actionAnalyze_aspect)
        self.menuAnalysis.addAction(self.actionAnalyze_slope)
        self.menuSettings.addAction(self.actionContourSettings)
        self.menuView.addAction(self.actionClearContours)
        self.menuView.addAction(self.actionShowContourLabels)
        self.menuView.addAction(self.actionClearSlopeAspect)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionClear)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAnalysis.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionCreate_DMT)
        self.toolBar.addAction(self.actionCreate_lines)
        self.toolBar.addAction(self.actionAnalyze_slope)
        self.toolBar.addAction(self.actionAnalyze_aspect)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionContourSettings)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClearContours)
        self.toolBar.addAction(self.actionShowContourLabels)
        self.toolBar.addAction(self.actionClearSlopeAspect)
        self.toolBar.addAction(self.actionClear)
        
        # connect singals and slots
        self.actionCreate_DMT.triggered.connect(self.runDT)
        self.actionCreate_lines.triggered.connect(self.runContourLines)
        self.actionAnalyze_slope.triggered.connect(self.runSlope)
        self.actionAnalyze_aspect.triggered.connect(self.runAspect)
        self.actionClear.triggered.connect(self.clearButton)
        self.actionAbout.triggered.connect(self.aboutClick)
        self.actionExit.triggered.connect(self.exitClick)
        self.actionContourSettings.triggered.connect(self.runContourSettings)
        self.actionOpen.triggered.connect(self.processFile)
        self.actionClearSlopeAspect.triggered.connect(self.clearSlopeAspectClick)
        self.actionClearContours.triggered.connect(self.clearContoursClick)
        self.actionShowContourLabels.triggered.connect(self.showContourLabelsClick)

        self.retranslateUi(MainForm)
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "DTM Analysis"))
        self.menuFile.setTitle(_translate("MainForm", "File"))
        self.menuAnalysis.setTitle(_translate("MainForm", "Analysis"))
        self.menuSettings.setTitle(_translate("MainForm", "Settings"))
        self.menuView.setTitle(_translate("MainForm", "View"))
        self.menuHelp.setTitle(_translate("MainForm", "Help"))
        self.toolBar.setWindowTitle(_translate("MainForm", "toolBar"))
        self.actionOpen.setText(_translate("MainForm", "Open..."))
        self.actionExit.setText(_translate("MainForm", "Exit"))
        self.actionCreate_DMT.setText(_translate("MainForm", "Create DMT"))
        self.actionCreate_lines.setText(_translate("MainForm", "Create lines"))
        self.actionAnalyze_aspect.setText(_translate("MainForm", "Analyze aspect"))
        self.actionAnalyze_slope.setText(_translate("MainForm", "Analyze slope"))
        self.actionContourSettings.setText(_translate("MainForm", "Contour settings..."))
        self.actionShowContourLabels.setText(_translate("MainForm", "Show contour labels"))
        self.actionClearContours.setText(_translate("MainForm", "Clear contour lines"))
        self.actionClearSlopeAspect.setText(_translate("MainForm", "Clear slope/aspect"))
        self.actionClear.setText(_translate("MainForm", "Clear all"))
        self.actionAbout.setText(_translate("MainForm", "About..."))

    def runDT(self):
        """Gets Delaunay triangulation from points"""
        points = self.Canvas.getPoints()
        if points == []:
            return
        #Run triangulation
        a = Algorithms()
        dt = a.createDT(points)

        #Set results
        self.Canvas.setDT(dt)
        self.Canvas.repaint()

    def runContourSettings(self):
        self.Canvas.setContourSettings()

    def runContourLines(self):
        """Analyzes contour lines from DEM
        z_min, z_max, dz
            na vstupu list hran - spustit DT, nebo získat delaunyho triangulaci - v praxi pořešit asi oboje
            spustíme vl metodu create contour lines - bude mít nějaké parametry - zmin, zmax, dz - return cl
            vrátit to třídy draw a vykreslit - set.coutourlines
            repaint()
        """
        a = Algorithms()
        dt = self.Canvas.getDT()
        if dt == []:
            return
        zmin = self.Canvas.getZMin()
        zmax = self.Canvas.getZMax()
        dz = self.Canvas.getDZ()
        contours, index_contours = a.createContourLines(dt, zmin, zmax, dz)
        if contours is None:
            return
        #set results to draw
        self.Canvas.setContours(contours, index_contours)
        self.Canvas.repaint()

    def runSlope(self):
        """Analyzes DEM slope"""
        dt = self.Canvas.getDT()
        if dt == []:
            return
        a = Algorithms()
        dtm = a.analyzeDTMSlope(dt)
        self.Canvas.switchSlopeAspect(0)
        self.Canvas.setSlope(dtm)
        self.Canvas.repaint()

    def runAspect(self):
        """Analyzes DEM aspect"""
        dt = self.Canvas.getDT()
        if dt == []:
            return
        a = Algorithms()
        dtm = a.analyzeDTMAspect(dt)
        self.Canvas.switchSlopeAspect(1)
        self.Canvas.setAspect(dtm)
        self.Canvas.repaint()

    def clearButton(self):
        """Clears canvas."""
        self.Canvas.clearCanvas()
        self.Canvas.repaint()

    def clearSlopeAspectClick(self):
        self.Canvas.clearSlopeAspect()
        self.Canvas.repaint()

    def clearContoursClick(self):
        self.Canvas.clearContourLines()
        self.Canvas.repaint()

    def showContourLabelsClick(self):
        self.Canvas.showContourLinesLabels()
        self.Canvas.repaint()

    def aboutClick(self):
        """Opens GitHub repository link."""
        url = QUrl("https://github.com/koziskoa/APK_2023/tree/master/DEM")
        QDesktopServices.openUrl(url)

    def exitClick(self):
        """Closes the application."""
        sys.exit()

    def openFile(self):
        """Opens CSV file."""
        filename, _ = QFileDialog.getOpenFileName(caption="Open File", directory="input_files/.",
                                                  filter="CSV file (*.csv)")
        # Return if no file has been opened
        if filename == "":
            return None
        # Return data from JSON
        with open(filename, 'r', encoding='utf-8-sig') as f:
            data = csv.reader(f, delimiter = ';')
            self.Canvas.loadData(data)

    def processFile(self):
        """Handles opening and loading the data."""
        # Open file
        data = self.openFile()
        # Return if no file has been opened
        if data == None:
            return
        # Clear canvas for new polygon layer
        self.Canvas.clearCanvas()
        # Try to load and process the data
        correct_data = self.Canvas.loadData(data)
        # Alert the user if JSON has incorrect formatting
        if correct_data == False:
            dlg = QtWidgets.QMessageBox()
            dlg.setWindowTitle("Error Message")
            dlg.setText("Invalid CSV file")
            dlg.exec()
            return

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainForm = QtWidgets.QMainWindow()
    ui = Ui_MainForm()
    ui.setupUi(MainForm)
    MainForm.show()
    sys.exit(app.exec())
