# coding:utf-8
import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import (NavigationItemPosition, MessageBox, MSFluentWindow,
                            qrouter, setFont)
from gui_utils import selectFile, bridgeSearch, graphRouting, graphWalking



class Window(MSFluentWindow):
    def __init__(self):
        super().__init__()

        # create sub interface
        self.homeInterface = selectFile('选择文件并展示图结构', self)
        self.Interface1 = bridgeSearch('查询桥接词或插入桥接词到新文本', self)
        self.Interface2 = graphRouting('最短路径处理', self)
        self.Interface3 = graphWalking('随机游走处理', self)

        self.globals = None

        self.homeInterface.signal.connect(self.updateGlobal)
        self.initNavigation()
        self.initWindow()

    def updateGlobal(self, signal_list):
        self.globals = signal_list
        self.activateInter1(signal_list)
        self.activateInter2(signal_list)
        self.activateInter3(signal_list)

    def activateInter1(self, slist):
        self.Interface1.GRAPH, self.Interface1.WORDS, self.Interface1.NLIST, self.Interface1.POS = slist
        self.Interface1.clearConsole()
        self.Interface1.inputedit.setEnabled(True)

    def activateInter2(self, slist):
        self.Interface2.GRAPH, self.Interface2.WORDS, self.Interface2.NLIST, self.Interface2.POS = slist
        self.Interface2.clearConsole()
        self.Interface2.inputedit.setEnabled(True)

    def activateInter3(self, slist):
        self.Interface3.GRAPH, self.Interface3.WORDS, self.Interface3.NLIST, self.Interface3.POS = slist
        self.Interface3.clearConsole()
        self.Interface3.inputedit.setEnabled(True)
        
    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, '图搭建', FIF.HOME_FILL)
        self.addSubInterface(self.Interface1, FIF.APPLICATION, '桥接词')
        self.addSubInterface(self.Interface2, FIF.APPLICATION, '图寻路')
        self.addSubInterface(self.Interface3, FIF.APPLICATION, '图游走')

        
        self.navigationInterface.addItem(
            routeKey='Help',
            icon=FIF.HELP,
            text='关于开发',
            onClick=self.showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.setCurrentItem(self.homeInterface.objectName())

    def initWindow(self):
        self.resize(580, 400)
        self.setWindowIcon(QIcon('./logo/logo.ico'))
        self.setWindowTitle('有向图处理')
        self.setFixedSize(580, 400)


        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def showMessageBox(self):
        w = MessageBox(
            '软件工程实验1: 结对编程',
            '开发者: HIT王梓健, HIT苗梓萌',
            self
        )
        w.yesButton.setText('返回')
        w.cancelButton.setText('退出程序')

        if w.exec():
            pass
        else:
            exit(0)

            


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Window()
    w.show()

    app.exec_()

