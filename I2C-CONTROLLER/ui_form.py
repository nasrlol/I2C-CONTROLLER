# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLCDNumber, QMainWindow, QSizePolicy,
    QStatusBar, QWidget)

class Ui_GUI(object):
    def setupUi(self, GUI):
        if not GUI.objectName():
            GUI.setObjectName(u"GUI")
        GUI.resize(800, 800)
        icon = QIcon()
        icon.addFile(u"../assets/icons/LCD1602.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        GUI.setWindowIcon(icon)
        self.centralwidget = QWidget(GUI)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setAutoFillBackground(False)
        self.LCD1602EMULATION = QLCDNumber(self.centralwidget)
        self.LCD1602EMULATION.setObjectName(u"LCD1602EMULATION")
        self.LCD1602EMULATION.setGeometry(QRect(50, 570, 341, 191))
        GUI.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(GUI)
        self.statusbar.setObjectName(u"statusbar")
        GUI.setStatusBar(self.statusbar)

        self.retranslateUi(GUI)

        QMetaObject.connectSlotsByName(GUI)
    # setupUi

    def retranslateUi(self, GUI):
        GUI.setWindowTitle(QCoreApplication.translate("GUI", u"GUI", None))
    # retranslateUi

