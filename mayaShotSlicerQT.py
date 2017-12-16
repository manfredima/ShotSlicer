#coding: utf-8

from pymel.core import ui, sceneName, system, mel
from PySide.QtGui import *
from PySide.QtCore import *

from .mayaShotSlicer import getShots, launch
# from .standalone import standaloneStart
from .widgets import shotSlicer_UIs
from collections import OrderedDict
import os


shot_list = []
qMaya = ui.PyUI('MayaWindow').asQtObject() # Maya как QT-объект
#style = os.path.join(os.path.dirname(__file__), 'style.css')


class shotSlicerClass(QMainWindow, shotSlicer_UIs.Ui_cgf_shotSlicer):
    def __init__(self):
        super(shotSlicerClass, self).__init__(qMaya) # Maya как парент
        self.setupUi(self)  # подключение widgets/shotSlicer_UIs.py

        #self.setStyleSheet(open(style).read())

        self.mayapy_pro = QProcess()
        self.shot_list_d = dict()
        self.shots_mute = getShots()[1]
        self.shots_mute_dict = dict()
        self.shot_selected = set()
        self.mode = 'by Sequenser Order'

        self.getStartData()
        self.fillList()

        # self.pushButton.setStyleSheet("color: white; background-color: green;")

        # connects
        self.pushButton.clicked.connect(self.confirmSelected)
        self.cbx_allmuted.stateChanged.connect(self.addAllMuted)
        #self.gbx.toggled.connect(self.radioButtons)
        self.rb_byorder.clicked.connect(self.radioButtons)
        self.rb_byname.clicked.connect(self.radioButtons)


    def checkMuted(self, value):
        obj = self.sender()  # отправитель
        # print obj.text(), value

        # коррекция списка-множества шотов
        if value == 2:
            self.shot_selected.add(obj.text())
            obj.setStyleSheet("color: c8c8c8ff;")

        if value == 0:
            self.shot_selected.remove(obj.text())
            obj.setStyleSheet("color: grey;")

        if obj.text() in self.shots_mute:
            obj.setStyleSheet("background: #993333;")

        # print 'CHANGE SHOT SELECTED', self.shot_selected
        self.textSelected()


    def addAllMuted(self, value):
        for snm in self.shots_mute:
            obj = self.shots_mute_dict[snm]

            if value:
                obj.setChecked(True)
            else:
                obj.setChecked(False)

        print 'QT ADD MUTED SELECTED:', self.shot_selected
        print 'QT MODE 2:', self.mode


    def textSelected(self):
        if len(self.shot_selected) == len(shot_list):
            select_text = "selected ALL from " + str(len(shot_list)) + " "
            self.selected_lb.setStyleSheet("font: bold;")

        else:
            select_text = "selected " + str(len(self.shot_selected)) + " from " + str(len(shot_list)) + " "
            self.selected_lb.setStyleSheet("font: normal;")

        self.selected_lb.setText(QApplication.translate("cgf_shotSlicer", select_text, None, QApplication.UnicodeUTF8))


    def radioButtons(self): # saving options
        obj = self.sender()  # отправитель
        self.mode = obj.text()

        print 'QT MODE 1:', self.mode


    def fillList(self):
        self.rb_byorder.setChecked(True)
        self.textSelected()

        # таблица
        self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.setRowCount(0)
        # self.tableWidget.setColumnWidth(1, 90)
        # self.tableWidget.setColumnWidth(2, 60)

        # строки
        l = len(self.shot_list_d)
        self.tableWidget.setRowCount(l)

        # print 'SHOT LIST D:', self.shot_list_d

        for i, sn in enumerate(self.shot_list_d):
            sht_number = ''.join(list(sn)[-3:])

            # print 'SHOTS MUTE:', self.shots_mute, '\nNUMBER:', sht_number

            if sn in self.shots_mute:
                muted = 'YES'
            else:
                muted = 'NO'

            item = QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(i, item)
            self.tableWidget.verticalHeaderItem(i).setText(
                QApplication.translate("cgf_shotSlicer", str(i+1), None, QApplication.UnicodeUTF8))

            # установка виджетов в ячейки
            font = QFont()
            font.setPointSize(10)

            cbx = QCheckBox()
            cbx.setText(sn)
            cbx.setFont(font)
            if muted == 'YES':
                cbx.setCheckState(Qt.Unchecked)
                self.shots_mute_dict[sn] = cbx
            else:
                cbx.setCheckState(Qt.Checked)
            # connect
            cbx.stateChanged.connect(self.checkMuted)

            tr = QLabel()
            tr.setText(sht_number)
            tr.setFont(font)
            tr.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            if muted == 'YES':
                cbx.setStyleSheet("color: grey; background: #993333;")
                tr.setStyleSheet("color: grey; background: #993333;")

            mu = QLabel()
            mu.setText(muted)
            mu.setFont(font)
            mu.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            if muted == 'NO':
                mu.setStyleSheet("color: grey")
            else:
                mu.setStyleSheet("background: #993333;")

            self.tableWidget.setCellWidget(i, 0, cbx)
            self.tableWidget.setCellWidget(i, 1, tr)
            self.tableWidget.setCellWidget(i, 2, mu)

            # self.tableWidget.cellWidget(i, 1).setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            # self.tableWidget.cellWidget(i, 2).setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.pushButton.setMinimumSize(QSize(160, 30))
        self.pushButton.setMaximumSize(QSize(160, 30))
        self.pushButton.setText('CONFIRM + CUTTING')

        self.plainTextEdit.setStyleSheet("color: grey;")


    def confirmList(self):
        self.shot_selected = set()

        for i in xrange(self.tableWidget.rowCount()):
            if self.tableWidget.cellWidget(i, 0).checkState():
                self.shot_selected.add(self.tableWidget.cellWidget(i, 0).text())

        print self.shot_selected


    def getStartData(self):
        global shot_list
        shot_list = getShots()[0]

        from .mayaShotSlicer import shot_list_dict
        self.shot_list_d = shot_list_dict

        if not self.shot_selected:
            shots = set(shot_list)
            self.shot_selected = shots.difference(self.shots_mute)


    # старт обработки
    def confirmSelected(self):
        self.confirmList()
        self.pushButton.setText(u'»»» RUN »»»')
        self.pushButton.setStyleSheet("color: black; background-color: #CC9933;")

        print 'QT LAUNCH SELECTED:', self.shot_selected

        if self.shot_selected:
            if self.cbx_standalone.isChecked():
                self.startBackground(self.shot_selected, self.mode)
            else:
                launch(self.shot_selected, self.mode) # с передачей режима радиокнопок
                self.close()
        else:
            print 'Nothing selected. You must to select shots.'


    def startBackground(self, shot_selected, mode):
        mayapy = 'H:/Autodesk/Maya2016/bin/mayapy.exe'
        #mayapy = '/opt/maya2016/bin/mayapy'
        scene = os.path.normpath(sceneName())
        pyfile = os.path.normpath(os.path.join(os.path.dirname(__file__), 'mayaShotSlicer.py'))

        # cmd = [mayapy, pyfile, scene, mode] + shot_selected
        # subprocess.Popen(cmd)

        # коннекты
        self.mayapy_pro.finished.connect(self.finish)
        self.mayapy_pro.readyRead.connect(self.readOut)

        args = [pyfile, scene, shot_selected, mode]
        print 'ARGS:\nSCENE:', scene, '\nPYFILE:', pyfile, '\nSHOT SELECTED:', shot_selected, '\nMODE:', mode
        self.mayapy_pro.start(mayapy, args)

    def finish(self):
        print 'Background finished'

    def readOut(self):
        out = str(self.mayapy_pro.readAll()).strip()
        print 'OUT:', out


def run():
    shot_list = getShots()[0]
    #shot_list = shot_list_dict.keys()

    if shot_list:
        w = shotSlicerClass()
        w.show()
