# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from draw import Draw
from algorithms import *
import sys
class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(800, 600)
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
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuDraw = QtWidgets.QMenu(parent=self.menubar)
        self.menuDraw.setObjectName("menuDraw")
        self.menuAnalyze = QtWidgets.QMenu(parent=self.menubar)
        self.menuAnalyze.setObjectName("menuAnalyze")
        MainForm.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainForm)
        self.statusbar.setObjectName("statusbar")
        MainForm.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(parent=MainForm)
        self.toolBar.setObjectName("toolBar")
        MainForm.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.actionPoint_Polygon = QtGui.QAction(parent=MainForm)
        self.actionPoint_Polygon.setCheckable(True)
        self.actionPoint_Polygon.setObjectName("actionPoint_Polygon")
        self.actionClear = QtGui.QAction(parent=MainForm)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/clear.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClear.setIcon(icon)
        self.actionClear.setObjectName("actionClear")
        self.actionPoint_and_polygon_position = QtGui.QAction(parent=MainForm)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/polygon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionPoint_and_polygon_position.setIcon(icon1)
        self.actionPoint_and_polygon_position.setObjectName("actionPoint_and_polygon_position")
        self.actionOpen = QtGui.QAction(parent=MainForm)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/open_file.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionOpen.setIcon(icon2)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExit = QtGui.QAction(parent=MainForm)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/exit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionExit.setIcon(icon3)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExit)
        self.menuDraw.addAction(self.actionPoint_Polygon)
        self.menuDraw.addAction(self.actionClear)
        self.menuAnalyze.addAction(self.actionPoint_and_polygon_position)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDraw.menuAction())
        self.menubar.addAction(self.menuAnalyze.menuAction())
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPoint_and_polygon_position)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClear)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionExit)

        self.retranslateUi(MainForm)
        QtCore.QMetaObject.connectSlotsByName(MainForm)
        self.actionPoint_Polygon.triggered.connect(self.switchSourceClick)
        self.actionPoint_and_polygon_position.triggered.connect(self.analyzeClick)
        self.actionOpen.triggered.connect(self.openFileClick)
        self.actionExit.triggered.connect(self.exitClick)

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "MainWindow"))
        self.menuFile.setTitle(_translate("MainForm", "File"))
        self.menuDraw.setTitle(_translate("MainForm", "Draw"))
        self.menuAnalyze.setTitle(_translate("MainForm", "Analyze"))
        self.toolBar.setWindowTitle(_translate("MainForm", "toolBar"))
        self.actionPoint_Polygon.setText(_translate("MainForm", "Point/Polygon"))
        self.actionClear.setText(_translate("MainForm", "Clear"))
        self.actionPoint_and_polygon_position.setText(_translate("MainForm", "Point and polygon position"))
        self.actionPoint_and_polygon_position.setShortcut(_translate("MainForm", "Ctrl+A"))
        self.actionOpen.setText(_translate("MainForm", "Open"))
        self.actionExit.setText(_translate("MainForm", "Exit"))

    def switchSourceClick(self):
        self.Canvas.switchSource()

    def analyzeClick(self):
        #dialog = QtWidgets.QMessageBox()
        #dialog.setWindowTitle("result of analysis")
        # get point and polygon
        q = self.Canvas.getPoint()
        pol_list = self.Canvas.getPolygonList()

        #analyze pozition
        a = Algorithms()
        for i in range(len(pol_list)):
            res = a.getPointPolygonPositionR(q, pol_list[i])

            if res:
                self.Canvas.is_highlighted[i] = True
                self.Canvas.repaint()
                #dialog.setText(f"In polygon numero{i}")
        #Print results


        # if res == 1:
        #     dialog.setText("In polygon numero")
        # else:
        #     dialog.setText("Outside")
        # dialog.exec()

    def openFileClick(self):
        # dialog = QFileDialog()
        # dialog.setFileMode(QFileDialog.AnyFile)
        # fname = QFileDialog.getOpenFileName(self, 'Open File', )
        # dialog.setFilter("JSON files (*.json, *.geojson)")
        # filenames = QStringList()
        #
        # if dialog.exec():
        #     filenames = dialog.selectedFiles()
        #
        # a = Algorithms()
        # polygons = a.openJson()
        print("Zdravic")
        data = self.openDialogBox()
        self.Canvas.iterate_coords(data)

    def openDialogBox(self):
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        print(path)

        with open(path, "r", encoding="utf-8") as f:
            data =json.load(f)
        return(data)

    def exitClick(self):
        sys.exit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainForm = QtWidgets.QMainWindow()
    ui = Ui_MainForm()
    ui.setupUi(MainForm)
    MainForm.show()
    sys.exit(app.exec())
