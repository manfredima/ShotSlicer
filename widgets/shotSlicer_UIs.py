# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/users/d.liubimov/sandbox/toolbox/pipeline/maya_common/cgf_scripts/scripts/shotSlicer/widgets/shotSlicer.ui'
#
# Created: Fri Dec 15 11:43:48 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_cgf_shotSlicer(object):
    def setupUi(self, cgf_shotSlicer):
        cgf_shotSlicer.setObjectName("cgf_shotSlicer")
        cgf_shotSlicer.resize(338, 513)
        self.centralwidget = QtGui.QWidget(cgf_shotSlicer)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gbx = QtGui.QGroupBox(self.centralwidget)
        self.gbx.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.gbx.setObjectName("gbx")
        self.horizontalLayout = QtGui.QHBoxLayout(self.gbx)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(153, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.rb_byname = QtGui.QRadioButton(self.gbx)
        self.rb_byname.setMinimumSize(QtCore.QSize(166, 30))
        self.rb_byname.setMaximumSize(QtCore.QSize(180, 30))
        self.rb_byname.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.rb_byname.setObjectName("rb_byname")
        self.verticalLayout.addWidget(self.rb_byname)
        self.rb_byorder = QtGui.QRadioButton(self.gbx)
        self.rb_byorder.setMinimumSize(QtCore.QSize(166, 30))
        self.rb_byorder.setMaximumSize(QtCore.QSize(180, 30))
        self.rb_byorder.setChecked(True)
        self.rb_byorder.setObjectName("rb_byorder")
        self.verticalLayout.addWidget(self.rb_byorder)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addWidget(self.gbx)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.cbx_allmuted = QtGui.QCheckBox(self.centralwidget)
        self.cbx_allmuted.setMinimumSize(QtCore.QSize(120, 0))
        self.cbx_allmuted.setMaximumSize(QtCore.QSize(200, 16777215))
        self.cbx_allmuted.setObjectName("cbx_allmuted")
        self.horizontalLayout_3.addWidget(self.cbx_allmuted)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.cbx_standalone = QtGui.QCheckBox(self.centralwidget)
        self.cbx_standalone.setObjectName("cbx_standalone")
        self.horizontalLayout_3.addWidget(self.cbx_standalone)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.selected_lb = QtGui.QLabel(self.centralwidget)
        self.selected_lb.setMinimumSize(QtCore.QSize(240, 20))
        self.selected_lb.setMaximumSize(QtCore.QSize(600, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.selected_lb.setFont(font)
        self.selected_lb.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.selected_lb.setObjectName("selected_lb")
        self.verticalLayout_2.addWidget(self.selected_lb)
        self.tableWidget = QtGui.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 20, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setMinimumSize(QtCore.QSize(120, 30))
        self.pushButton.setMaximumSize(QtCore.QSize(140, 30))
        self.pushButton.setStyleSheet("background-color: rgb(102, 141, 60);\n"
"color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.plainTextEdit = QtGui.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setEnabled(False)
        self.plainTextEdit.setMinimumSize(QtCore.QSize(0, 80))
        self.plainTextEdit.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout_2.addWidget(self.plainTextEdit)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        cgf_shotSlicer.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(cgf_shotSlicer)
        self.statusbar.setObjectName("statusbar")
        cgf_shotSlicer.setStatusBar(self.statusbar)

        self.retranslateUi(cgf_shotSlicer)
        QtCore.QMetaObject.connectSlotsByName(cgf_shotSlicer)

    def retranslateUi(self, cgf_shotSlicer):
        cgf_shotSlicer.setWindowTitle(QtGui.QApplication.translate("cgf_shotSlicer", "Shot Slicer select dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.gbx.setTitle(QtGui.QApplication.translate("cgf_shotSlicer", "Shots list sorting", None, QtGui.QApplication.UnicodeUTF8))
        self.rb_byname.setText(QtGui.QApplication.translate("cgf_shotSlicer", "by Name", None, QtGui.QApplication.UnicodeUTF8))
        self.rb_byorder.setText(QtGui.QApplication.translate("cgf_shotSlicer", "by Sequenser Order      ", None, QtGui.QApplication.UnicodeUTF8))
        self.cbx_allmuted.setText(QtGui.QApplication.translate("cgf_shotSlicer", "add All Muted", None, QtGui.QApplication.UnicodeUTF8))
        self.cbx_standalone.setText(QtGui.QApplication.translate("cgf_shotSlicer", "run in Background", None, QtGui.QApplication.UnicodeUTF8))
        self.selected_lb.setText(QtGui.QApplication.translate("cgf_shotSlicer", "Selected ... shots from ...", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("cgf_shotSlicer", "Shot Name", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("cgf_shotSlicer", "Shot Number", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("cgf_shotSlicer", "Mute", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("cgf_shotSlicer", "CONFIRM + START", None, QtGui.QApplication.UnicodeUTF8))
        self.plainTextEdit.setPlainText(QtGui.QApplication.translate("cgf_shotSlicer", "The plugin does not affect the original scene. It only creates new Maya and movie files. The sort order affects only  the names of the new files.", None, QtGui.QApplication.UnicodeUTF8))

