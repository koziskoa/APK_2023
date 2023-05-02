from PyQt6 import QtCore, QtGui, QtWidgets
from algorithms import *
from draw import Draw
import json

class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(1000, 880)
        self.centralwidget = QtWidgets.QWidget(parent=MainForm)
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
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1107, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSimplify = QtWidgets.QMenu(parent=self.menubar)
        self.menuSimplify.setObjectName("menuSimplify")
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
        self.actionMAER = QtGui.QAction(parent=MainForm)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/maer.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionMAER.setIcon(icon2)
        self.actionMAER.setObjectName("actionMAER")
        self.actionWallAverage = QtGui.QAction(parent=MainForm)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/wa.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionWallAverage.setIcon(icon3)
        self.actionWallAverage.setObjectName("actionWallAverage")
        self.actionLongestEdge = QtGui.QAction(parent=MainForm)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("icons/longestedge.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionLongestEdge.setIcon(icon7)
        self.actionLongestEdge.setObjectName("actionLongestEdge")
        self.actionClear = QtGui.QAction(parent=MainForm)
        self.actionAbout = QtGui.QAction(parent=MainForm)
        self.actionAbout.setObjectName("actionAbout")
        self.actionWeightedBisector = QtGui.QAction(parent=MainForm)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("icons/weightedbisector.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionWeightedBisector.setIcon(icon8)
        self.actionWeightedBisector.setObjectName("actionWeightedBisector")
        self.actionClearEnclosingRects = QtGui.QAction(parent=MainForm)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("icons/clear_er.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClearEnclosingRects.setIcon(icon9)
        self.actionClearEnclosingRects.setObjectName("actionClearEnclosingRects")
        self.actionClearConvexHulls = QtGui.QAction(parent=MainForm)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("icons/clear_ch.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClearConvexHulls.setIcon(icon10)
        self.actionClearConvexHulls.setObjectName("actionClearConvexHulls")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/clear.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClear.setIcon(icon4)
        self.actionClear.setObjectName("actionClear")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/about.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionAbout.setIcon(icon5)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icons/ch.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuSimplify.addAction(self.actionMAER)
        self.menuSimplify.addAction(self.actionWallAverage)
        self.menuSimplify.addAction(self.actionLongestEdge)
        self.menuSimplify.addAction(self.actionWeightedBisector)
        self.menuSimplify.addSeparator()
        self.menuSimplify.addAction(self.actionClearEnclosingRects)
        self.menuSimplify.addAction(self.actionClearConvexHulls)
        self.menuSimplify.addAction(self.actionClear)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSimplify.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.setStyleSheet("QToolBar{spacing:4px;}")
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionMAER)
        self.toolBar.addAction(self.actionWallAverage)
        self.toolBar.addAction(self.actionLongestEdge)
        self.toolBar.addAction(self.actionWeightedBisector)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClearEnclosingRects)
        self.toolBar.addAction(self.actionClearConvexHulls)
        self.toolBar.addAction(self.actionClear)
        self.toolBar.addSeparator()

        # Toolbar settings
        self.buttonJarvis = QtWidgets.QRadioButton(text="Jarvis Scan", checkable=True)
        self.buttonJarvis.setChecked(True)
        self.buttonJarvis.setToolTip("Construct convex hull using Jarvis Scan algorithm")
        self.buttonGraham = QtWidgets.QRadioButton(text="Graham Scan", checkable=True)
        self.buttonGraham.setToolTip("Construct convex hull using Graham Scan algorithm")
        self.buttonCH = QtWidgets.QPushButton(text="Show Convex Hull")
        self.buttonCH.setIcon(icon6)
        self.buttonJarvis.clicked.connect(self.switchToJarvis)
        self.buttonGraham.clicked.connect(self.switchToGraham)
        self.buttonCH.clicked.connect(self.constructCH)
        self.group = QtWidgets.QButtonGroup(exclusive=True)
        for button in (self.buttonCH, self.buttonJarvis, self.buttonGraham):
            self.toolBar.addWidget(button)
            self.group.addButton(button)

        #connect signals and slots
        self.actionOpen.triggered.connect(self.processFile)
        self.actionMAER.triggered.connect(self.simplifyMAERClick)
        self.actionWallAverage.triggered.connect(self.simplifyWallAverageClick)
        self.actionLongestEdge.triggered.connect(self.simplifyLongestEdgeClick)
        self.actionWeightedBisector.triggered.connect(self.simplifyWeightedBisectorClick)
        self.actionClearEnclosingRects.triggered.connect(self.clearERButton)
        self.actionClearConvexHulls.triggered.connect(self.clearCHButton)
        self.actionClear.triggered.connect(self.clearButton)
        self.actionExit.triggered.connect(self.exitClick)
        self.actionAbout.triggered.connect(self.aboutClick)

        self.retranslateUi(MainForm)
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "Building Simplifier"))
        self.menuFile.setTitle(_translate("MainForm", "File"))
        self.menuSimplify.setTitle(_translate("MainForm", "Simplify"))
        self.menuHelp.setTitle(_translate("MainForm", "Help"))
        self.toolBar.setWindowTitle(_translate("MainForm", "toolBar"))
        self.actionOpen.setText(_translate("MainForm", "Open..."))
        self.actionOpen.setToolTip(_translate("MainForm", "Open file"))
        self.actionExit.setText(_translate("MainForm", "Exit"))
        self.actionExit.setToolTip(_translate("MainForm", "Exit application"))
        self.actionMAER.setText(_translate("MainForm", "Minimum Area Enclosing Rectangle"))
        self.actionWallAverage.setText(_translate("MainForm", "Wall Average"))
        self.actionLongestEdge.setText(_translate("MainForm", "Longest Edge"))
        self.actionWeightedBisector.setText(_translate("MainForm", "Weighted Bisector"))
        self.actionClear.setText(_translate("MainForm", "Clear All"))
        self.actionClearConvexHulls.setText(_translate("MainForm", "Clear Convex Hulls"))
        self.actionClearEnclosingRects.setText(_translate("MainForm", "Clear Enclosing Rectangles"))
        self.actionAbout.setText(_translate("MainForm", "About..."))

    def switchToJarvis(self):
        """Switches to Jarvis Scan algorithm to construct convex hulls."""
        Algorithms.ch_alg = Algorithms.jarvisScan

    def switchToGraham(self):
        """Switches to Graham Scan algorithm to construct convex hulls."""
        Algorithms.ch_alg = Algorithms.grahamScan

    def constructCH(self):
        """Constructs convex hulls using selected algorithm."""
        pol_list = self.Canvas.getPolygonList()
        ch_list = []
        for pol in pol_list:
            ch = Algorithms.ch_alg(pol)
            # If convex hull can't be created, proceed to next polygon
            if ch == False:
                continue
            ch_list.append(ch)
        self.Canvas.setConvexHulls(ch_list)
        self.Canvas.repaint()

    def simplifyMAERClick(self):
        """Simplifies input polygons using Minimum Area Enclosing Rectangle algorithm."""
        pol_list = self.Canvas.getPolygonList()
        er_list = []
        for pol in pol_list:
            enclosing_rect = Algorithms.minAreaEnclosingRectangle(pol)
            # If ER can't be created, proceed to next polygon
            if enclosing_rect == False:
                continue
            er_list.append(enclosing_rect)
        self.Canvas.setEnclosingRectangles(er_list)
        self.Canvas.repaint()

    def simplifyWallAverageClick(self):
        """Simplifies input polygons using Wall Average algorithm."""
        pol_list = self.Canvas.getPolygonList()
        er_list = []
        for pol in pol_list:
            enclosing_rect = Algorithms.wallAverage(pol)
            # If ER can't be created, proceed to next polygon
            if enclosing_rect == False:
                continue
            er_list.append(enclosing_rect)
        self.Canvas.setEnclosingRectangles(er_list)
        self.Canvas.repaint()

    def simplifyLongestEdgeClick(self):
        """Simplifies input polygons using Longest Edge algorithm."""
        pol_list = self.Canvas.getPolygonList()
        er_list = []
        for pol in pol_list:
            enclosing_rect = Algorithms.longestEdge(pol)
            # If ER can't be created, proceed to next polygon
            if enclosing_rect == False:
                continue
            er_list.append(enclosing_rect)
        self.Canvas.setEnclosingRectangles(er_list)
        self.Canvas.repaint()

    def simplifyWeightedBisectorClick(self):
        """Simplifies input polygons using Weighted Bisector algorithm."""
        pol_list = self.Canvas.getPolygonList()
        er_list = []
        for pol in pol_list:
            enclosing_rect = Algorithms.weightedBisector(pol)
            # If ER can't be created, proceed to next polygon
            if enclosing_rect == False:
                continue
            er_list.append(enclosing_rect)
        self.Canvas.setEnclosingRectangles(er_list)
        self.Canvas.repaint()
    
    def clearButton(self):
        """Clears canvas."""
        self.Canvas.clearCanvas()
        self.Canvas.repaint()

    def clearERButton(self):
        """Clears enclosing rectangles."""
        self.Canvas.clearERs()
        self.Canvas.repaint()

    def clearCHButton(self):
        """Clears convex hulls."""
        self.Canvas.clearCHs()
        self.Canvas.repaint()

    def exitClick(self):
        """Closes the application."""
        sys.exit()

    def aboutClick(self):
        """Opens GitHub repository link."""
        url = QUrl("https://github.com/koziskoa/APK_2023/tree/master/building_simplify")
        QDesktopServices.openUrl(url)

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
            dlg.setText("Invalid JSON file")
            dlg.exec()
            return

    def openFile(self):
        """Opens JSON/GEOJSON files."""
        filename, _ = QFileDialog.getOpenFileName(caption="Open File", directory="input_files/.", filter="JSON file (*.json; *.geojson)")
        # Return if no file has been opened
        if filename == "":
            return None
        # Return data from JSON
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return(data)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainForm = QtWidgets.QMainWindow()
    ui = Ui_MainForm()
    ui.setupUi(MainForm)
    MainForm.show()
    sys.exit(app.exec())