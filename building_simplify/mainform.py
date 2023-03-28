from PyQt6 import QtCore, QtGui, QtWidgets
from algorithms import *
from draw import Draw

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
        self.actionMinimum_Area_Enclosing_Rectangle = QtGui.QAction(parent=MainForm)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/maer.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionMinimum_Area_Enclosing_Rectangle.setIcon(icon2)
        self.actionMinimum_Area_Enclosing_Rectangle.setObjectName("actionMinimum_Area_Enclosing_Rectangle")
        self.actionWall_Average = QtGui.QAction(parent=MainForm)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/wa.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionWall_Average.setIcon(icon3)
        self.actionWall_Average.setObjectName("actionWall_Average")
        self.actionClear = QtGui.QAction(parent=MainForm)
        self.actionAbout = QtGui.QAction(parent=MainForm)
        self.actionAbout.setObjectName("actionAbout")
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
        self.menuSimplify.addAction(self.actionMinimum_Area_Enclosing_Rectangle)
        self.menuSimplify.addAction(self.actionWall_Average)
        self.menuSimplify.addSeparator()
        self.menuSimplify.addAction(self.actionClear)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSimplify.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.setStyleSheet("QToolBar{spacing:4px;}")
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionMinimum_Area_Enclosing_Rectangle)
        self.toolBar.addAction(self.actionWall_Average)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClear)
        self.toolBar.addSeparator()

        # Toolbar settings
        self.buttonJarvis = QtWidgets.QRadioButton(text="Jarvis Scan", checkable=True)
        self.buttonJarvis.setChecked(True)
        self.buttonJarvis.setToolTip("Construct convex hull using Jarvis Scan algorithm")
        self.buttonGraham = QtWidgets.QRadioButton(text="Graham Scan", checkable=True)
        self.buttonGraham.setToolTip("Construct convex hull using Graham Scan algorithm")
        self.buttonCH = QtWidgets.QPushButton(text="Construct Convex Hull")
        self.buttonCH.setIcon(icon6)
        self.buttonJarvis.clicked.connect(self.switchToJarvis)
        self.buttonGraham.clicked.connect(self.switchToGraham)
        self.buttonCH.clicked.connect(self.constructCH)
        self.group = QtWidgets.QButtonGroup(exclusive=True)
        for button in (self.buttonCH, self.buttonJarvis, self.buttonGraham):
            self.toolBar.addWidget(button)
            self.group.addButton(button)

        #connect signals and slots
        self.actionMinimum_Area_Enclosing_Rectangle.triggered.connect(self.simplifyBuildingEnclosinRectangleClick)
        self.actionClear.triggered.connect(self.clearButtpn)
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
        self.actionMinimum_Area_Enclosing_Rectangle.setText(_translate("MainForm", "Minimum Area Enclosing Rectangle"))
        self.actionWall_Average.setText(_translate("MainForm", "Wall Average"))
        self.actionClear.setText(_translate("MainForm", "Clear"))
        self.actionAbout.setText(_translate("MainForm", "About..."))

    def switchToJarvis(self):
        Algorithms.ch_alg = Algorithms.jarvisScan

    def switchToGraham(self):
        Algorithms.ch_alg = Algorithms.grahamScan

    def constructCH(self):
        pol = self.Canvas.getPolygon()
        ch = Algorithms.ch_alg(pol)
        self.Canvas.setConvexHull(ch)
        self.Canvas.repaint()

    def simplifyBuildingEnclosinRectangleClick(self):
        # get polygon
        pol = self.Canvas.getPolygon()
        
        a = Algorithms()
        #convex hull
        #ch = a.ch_alg(pol)
        #self.Canvas.setConvexHull(ch)
        c_er =  a.minAreaEnclosingRectangle(pol) #minAreaEnclosingRectangle
        self.Canvas.setEnclosingRectangle(c_er)
        self.Canvas.repaint()
    
    def clearButtpn(self):
        self.Canvas.clearCanvas()
        self.Canvas.repaint()

    def exitClick(self):
        sys.exit()

    def aboutClick(self):
        """Opens GitHub repository link."""
        url = QUrl("https://github.com/koziskoa/APK_2023/tree/master/building_simplify")
        QDesktopServices.openUrl(url)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainForm = QtWidgets.QMainWindow()
    ui = Ui_MainForm()
    ui.setupUi(MainForm)
    MainForm.show()
    sys.exit(app.exec())