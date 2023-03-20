# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QStatusBar, QToolBar,
    QWidget)

from draw import Draw

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1106, 600)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        icon = QIcon()
        icon.addFile(u"icons/open_file.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOpen.setIcon(icon)
        self.actionClose = QAction(MainWindow)
        self.actionClose.setObjectName(u"actionClose")
        icon1 = QIcon()
        icon1.addFile(u"icons/exit.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionClose.setIcon(icon1)
        self.actionMinimum_Area_Enclosing_Rectangle = QAction(MainWindow)
        self.actionMinimum_Area_Enclosing_Rectangle.setObjectName(u"actionMinimum_Area_Enclosing_Rectangle")
        icon2 = QIcon()
        icon2.addFile(u"icons/maer.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionMinimum_Area_Enclosing_Rectangle.setIcon(icon2)
        self.actionWall_Average = QAction(MainWindow)
        self.actionWall_Average.setObjectName(u"actionWall_Average")
        icon3 = QIcon()
        icon3.addFile(u"icons/wa.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionWall_Average.setIcon(icon3)
        self.actionClear = QAction(MainWindow)
        self.actionClear.setObjectName(u"actionClear")
        icon4 = QIcon()
        icon4.addFile(u"icons/clear.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actionClear.setIcon(icon4)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.Canvas = Draw(self.centralwidget)
        self.Canvas.setObjectName(u"Canvas")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Canvas.sizePolicy().hasHeightForWidth())
        self.Canvas.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.Canvas)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1106, 26))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuSimplify = QMenu(self.menubar)
        self.menuSimplify.setObjectName(u"menuSimplify")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSimplify.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuSimplify.addAction(self.actionMinimum_Area_Enclosing_Rectangle)
        self.menuSimplify.addAction(self.actionWall_Average)
        self.menuSimplify.addSeparator()
        self.menuSimplify.addAction(self.actionClear)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionMinimum_Area_Enclosing_Rectangle)
        self.toolBar.addAction(self.actionWall_Average)
        self.toolBar.addAction(self.actionClear)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClose)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Building simplify", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(tooltip)
        self.actionOpen.setToolTip(QCoreApplication.translate("MainWindow", u"Open File", None))
#endif // QT_CONFIG(tooltip)
        self.actionClose.setText(QCoreApplication.translate("MainWindow", u"Close", None))
#if QT_CONFIG(tooltip)
        self.actionClose.setToolTip(QCoreApplication.translate("MainWindow", u"Close Aplication", None))
#endif // QT_CONFIG(tooltip)
        self.actionMinimum_Area_Enclosing_Rectangle.setText(QCoreApplication.translate("MainWindow", u"Minimum Area Enclosing Rectangle", None))
#if QT_CONFIG(tooltip)
        self.actionMinimum_Area_Enclosing_Rectangle.setToolTip(QCoreApplication.translate("MainWindow", u"Simplify Building using MAER", None))
#endif // QT_CONFIG(tooltip)
        self.actionWall_Average.setText(QCoreApplication.translate("MainWindow", u"Wall Average", None))
#if QT_CONFIG(tooltip)
        self.actionWall_Average.setToolTip(QCoreApplication.translate("MainWindow", u"Simplpify building using Wall Average", None))
#endif // QT_CONFIG(tooltip)
        self.actionClear.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
#if QT_CONFIG(tooltip)
        self.actionClear.setToolTip(QCoreApplication.translate("MainWindow", u"Clear results", None))
#endif // QT_CONFIG(tooltip)
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuSimplify.setTitle(QCoreApplication.translate("MainWindow", u"Simplify", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

