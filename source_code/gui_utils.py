from PyQt5.QtWidgets import QFrame, QFileDialog, QHBoxLayout, QGridLayout, QShortcut
from PyQt5 import QtWidgets, QtGui
from qfluentwidgets import (setTheme, qrouter, SubtitleLabel, setFont, PushButton, PlainTextEdit, TogglePushButton)
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QEventLoop
from DataProcessing import *
from BridgeSearching import *
from Routing import *
import matplotlib.pyplot as plt
import networkx as nx
from PyQt5.QtGui import QIcon, QKeySequence
import shutil 

"""
图片视窗基础类
"""
class ImageViewer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.selected_imgsPath = []
        self.current_image_index = 0
        self.gLayout = QGridLayout(self)
        self.initWindow()
        self.LayoutOption()
    
    def initWindow(self):
        self.resize(1100, 1000)
        self.setWindowIcon(QIcon('./logo/logo.ico'))
        self.setWindowTitle('展示当前文本有向图')
        
    def LayoutOption(self, stepbutton=False):
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setFixedSize(1100, 900)

        if stepbutton:
            self.next_image_button = PushButton('下一步', self)
            self.next_image_button.clicked.connect(self.showNextImage)
            self.next_image_button.setFixedSize(550, 35)
            self.prev_image_button = PushButton('上一步', self)
            self.prev_image_button.clicked.connect(self.showPrevImage)
            self.prev_image_button.setFixedSize(550, 35)
        
        self.gLayout.addWidget(self.label_3, 0, 0, 1, 2)
        if stepbutton:
            self.gLayout.addWidget(self.next_image_button, 1, 0)
            self.gLayout.addWidget(self.prev_image_button, 1, 1)
        self.gLayout.setSpacing(0)

    def openImage(self, filepath):
        self.selected_imgsPath = sorted([os.path.join(filepath, nm) for nm in os.listdir(filepath) if nm[-3:] in ['png']])
        if len(self.selected_imgsPath) == 0:
            self.empty_information()
            return
 
        img = QtGui.QPixmap(self.selected_imgsPath[0]).scaled(1100, 900)
        self.label_3.setPixmap(img)
        self.current_image_index = 0
        
    def showNextImage(self):
        if len(self.selected_imgsPath) == 0:
            return
 
        self.current_image_index += 1
        if self.current_image_index >= len(self.selected_imgsPath):
            self.current_image_index = 0
 
        img_path = self.selected_imgsPath[self.current_image_index]
        img = QtGui.QPixmap(img_path).scaled(1100, 900)
        self.label_3.setPixmap(img)
        
    def showPrevImage(self):
        if len(self.selected_imgsPath) == 0:
            return
 
        self.current_image_index -= 1
        if self.current_image_index < 0:
            self.current_image_index = len(self.selected_imgsPath) - 1
 
        img_path = self.selected_imgsPath[self.current_image_index]
        img = QtGui.QPixmap(img_path).scaled(1100, 900) 
        self.label_3.setPixmap(img)

"""
1. 选择文本并展示图 主页下的第一个选择
"""
class selectFile(QFrame):
    signal = pyqtSignal(list)
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.gLayout = QGridLayout(self)
        self.setObjectName(text.replace(' ', '-'))
       

        self.GRAPH = None
        self.NLIST = None
        self.WORDS = None
        self.POS = None

        self.btu1 = PushButton(FIF.FOLDER, '选择用于构图的英文txt文本', self)
        self.btu1.clicked.connect(self.Select_a_single_file)
        self.btu1.setFixedSize(246, 35)

        self.btu2 = PushButton(FIF.SAVE, '保存有向图', self)
        self.btu2.clicked.connect(self.Show_graph_by_click)
        self.btu2.setFixedSize(246, 35)

        self.pathshow = PlainTextEdit()
        self.pathshow.setFixedSize(500, 35)
        self.pathshow.setReadOnly(True)

        self.textshow = PlainTextEdit()
        self.textshow.setFixedSize(500, 200)
        self.textshow.setReadOnly(True)
        
        self.viewer = ImageViewer()

        self.gLayout.addWidget(self.btu1, 0, 0)
        self.gLayout.addWidget(self.btu2, 0, 1)
        self.gLayout.addWidget(self.pathshow, 1, 0, 1, 2)
        self.gLayout.addWidget(self.textshow, 2, 0, 1, 2)
        self.gLayout.setSpacing(0)


    def showDirectedGraph(self, G, path, seed, filename="origin"):
        plt.figure(figsize=(11, 9))
        pos = nx.spring_layout(G, k=25, iterations=20, seed=seed)
        self.POS = pos
        nx.draw(G, pos, alpha=0.5, node_size=700)
        node_labels = nx.get_node_attributes(G, 'name')
        nx.draw_networkx_labels(G, pos=pos, labels=node_labels, font_size=7)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        dir_path = os.path.join(path, "initGraph")
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        plt.savefig(os.path.join(dir_path, f"{filename}.png"))
        plt.cla()


    def Select_a_single_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "./data/raw", "txt英文文本文件 (*.txt)")
        if file_path:
            self.pathshow.setReadOnly(False)
            self.pathshow.setPlainText(file_path)
            self.pathshow.setReadOnly(True)
            f = open(file_path, "r", encoding="utf-8")
            file = f.read()
            f.close()
            self.textshow.setReadOnly(False)
            self.textshow.setPlainText(file)
            self.textshow.setReadOnly(True)
            
            self.GRAPH, self.WORDS, self.NLIST = text_to_graph(file_path)


    def Show_graph_by_click(self):
        if self.GRAPH is not None and self.WORDS is not None and self.NLIST is not None:
            self.showDirectedGraph(self.GRAPH, "./save_figure", seed=50, filename="init")
            self.viewer.show()
            self.viewer.openImage("./save_figure/initGraph")
            change_content = [self.GRAPH, self.WORDS, self.NLIST, self.POS]  # 返回信号构建
            self.signal.emit(change_content)

"""
桥接词显示类重写
"""
class BridgeViewer(ImageViewer):
    signal_b = pyqtSignal(bool)
    def __init__(self):
        super().__init__()

    def initWindow(self):
        self.resize(1100, 1000)
        self.setWindowIcon(QIcon('./logo/logo.ico'))
        self.setWindowTitle('展示桥接词')

    def closeEvent(self, event):
        self.signal_b.emit(True)

    def LayoutOption(self, stepbutton=True):
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setFixedSize(1100, 900)

        if stepbutton:
            self.next_image_button = PushButton(FIF.PAGE_RIGHT, '下一桥接词', self)
            self.next_image_button.clicked.connect(self.showNextImage)
            self.next_image_button.setFixedSize(550, 35)
            self.prev_image_button = PushButton(FIF.PAGE_LEFT, '上一桥接词', self)
            self.prev_image_button.clicked.connect(self.showPrevImage)
            self.prev_image_button.setFixedSize(550, 35)
        
        self.gLayout.addWidget(self.label_3, 0, 0, 1, 2)
        if stepbutton:
            self.gLayout.addWidget(self.prev_image_button, 1, 0)
            self.gLayout.addWidget(self.next_image_button, 1, 1)
        self.gLayout.setSpacing(0)

"""
2. 桥接词模块 主页下的第二个选择
"""
class bridgeSearch(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.gLayout = QGridLayout(self)
        self.setObjectName(text.replace(' ', '-'))
       
        self.GRAPH = None
        self.NLIST = None
        self.WORDS = None
        self.POS = None
        self.printlog = False
        self.generate_mode = 0

        self.btu1 = PushButton(FIF.ACCEPT, '确认', self)
        self.btu1.clicked.connect(self.confirmInput)
        self.btu1.setFixedSize(81, 35)
        shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Return), self)
        shortcut.activated.connect(self.confirmInput)
        shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Enter), self)
        shortcut.activated.connect(self.confirmInput)

        self.btu2 = PushButton(FIF.BRUSH, '清屏', self)
        self.btu2.clicked.connect(self.clearConsole)
        self.btu2.setFixedSize(81, 35)

        self.btu3 = TogglePushButton(FIF.SYNC, '生成模式', self)
        self.btu3.clicked.connect(self.enableSelect)
        self.btu3.setFixedSize(164, 35)
        
        self.btu4 = PushButton(FIF.DOCUMENT, '选择待处理txt', self)
        self.btu4.clicked.connect(self.selectSentence)
        self.btu4.setEnabled(False)
        self.btu4.setFixedSize(164, 35)

        self.inputedit = PlainTextEdit()
        self.inputedit.setFixedSize(500, 70)
        self.inputedit.setEnabled(False)

        self.console = PlainTextEdit()
        self.console.setFixedSize(500, 200)
        self.console.setReadOnly(True)
        
        self.viewer = BridgeViewer()
        self.viewer.signal_b.connect(self.enableInput_aftershow)

        self.gLayout.addWidget(self.console, 0, 0, 1, 6)
        self.gLayout.addWidget(self.inputedit, 1, 0, 1, 6)
        self.gLayout.addWidget(self.btu1, 2, 0)
        self.gLayout.addWidget(self.btu2, 2, 1)
        self.gLayout.addWidget(self.btu3, 2, 2, 1, 2)
        self.gLayout.addWidget(self.btu4, 2, 4, 1, 2)
        self.gLayout.setSpacing(0)

        self.clearConsole()

    def enableInput_aftershow(self, ifenable):
        self.inputedit.setEnabled(True)

    def enableSelect(self):
        if self.btu3.isChecked():
            self.btu4.setEnabled(True)
            self.generate_mode = 1
        else:
            self.btu4.setEnabled(False)
            self.generate_mode = 0

    def clearConsole(self):
        self.console.clear()
        if self.WORDS is not None:
            welcome = "                  🚀欢迎使用桥接词功能模块🚀包含两项功能:\n1. 查询模式---在输入框键入两个单词并确认，查询桥接词信息\n2. 生成模式---点选“生成模式”, 可直接输入或选择txt, 根据图为其插入桥接词\n以下为当前图的词表:\n"
            self.console.setPlainText(welcome)
            wordlist = ""
            num = len(self.WORDS)
            for i in range(num):
                wordlist = wordlist + self.WORDS[i]
                if i != num-1:
                    wordlist = wordlist + ', '
            self.console.appendPlainText(wordlist+'\n')
        else:
            tips = "                                 🚀欢迎使用桥接词功能模块🚀\n              请先在侧栏“图搭建”中选择待处理的英文文本并保存"
            self.console.setPlainText(tips)
    
    def selectSentence(self):
        if self.WORDS is not None and self.GRAPH is not None and self.NLIST is not None:
            file_path, _ = QFileDialog.getOpenFileName(self, "选择句子文件", "./data/bridge_word_insert/input", "txt英文文本文件 (*.txt)")
            if file_path:
                f = open(file_path, "r", encoding="utf-8")
                file = f.read()
                f.close()
                self.inputedit.clear()
                self.inputedit.setPlainText(file)
    
    def consolePrint(self, log, printlog=True):
        if printlog:
            self.console.appendPlainText(log)
            bar = self.console.verticalScrollBar()
            bar.setSliderPosition(bar.maximum())

    def queryBridgeWords(self, word1, word2):
        bridge = []
        if word1 not in self.WORDS and word2 not in self.WORDS:
            self.consolePrint(f"<GraphDealer> 查询失败: No \"{word1}\" and \"{word2}\" in the graph!", self.printlog)
            return bridge
        elif word1 not in self.WORDS:
            self.consolePrint(f"<GraphDealer> 查询失败: No \"{word1}\" in the graph!", self.printlog)
            return bridge
        elif word2 not in self.WORDS:
            self.consolePrint(f"<GraphDealer> 查询失败: No \"{word2}\" in the graph!", self.printlog)
            return bridge
        index1 = self.WORDS.index(word1)
        index2 = self.WORDS.index(word2)
        nodelist = self.NLIST
        node1 = nodelist[index1]
        node2 = nodelist[index2]
        bridge = set(node1.after.keys()).intersection(set(node2.before.keys()))
        bridge = list(bridge)
        bridge = [self.WORDS[p] for p in bridge]
        if len(bridge) == 0:
            self.consolePrint(f"<GraphDealer> 查询成功: No bridge word from \"{word1}\" to \"{word2}\"!", self.printlog)
        elif len(bridge) == 1:
            self.consolePrint(f"<GraphDealer> 查询成功: The bridge word from \"{word1}\" to \"{word2}\" is: {bridge[0]}.", self.printlog)
        else:
            word_string = ""
            for i in range(0, len(bridge)-1):
                word_string = word_string + bridge[i] + ", "
            word_string = word_string[:-2] + " and " + bridge[len(bridge)-1]
            self.consolePrint(f"<GraphDealer> 查询成功: The bridge words from \"{word1}\" to \"{word2}\" are: {word_string}.", self.printlog)
        return bridge

    def saveBridgeOnGraph(self, G, pos, path, k1, k2, bridge):
        dir_path = os.path.join(path, "BridgeQuery")
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        for word in bridge:
            plt.rcParams['figure.figsize'] = (12, 15)
            nx.draw(G, pos, alpha=0.5, node_size=700)
            node_labels = nx.get_node_attributes(G, 'name')
            nx.draw_networkx_labels(G, pos=pos, labels=node_labels, font_size=7)

            edge_pairs_bridge = [(k1, word), (word, k2)]
            nx.draw_networkx_edges(G, pos, edgelist=edge_pairs_bridge, edge_color='m', width=4)
            labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

            plt.savefig(os.path.join(dir_path, f"bridge_temp_{word}.png"))
            plt.cla()
    
    def generateNewText(self, sentence):
        sentence = sentence.lower()
        sentence = re.sub(PATTERN, " ", sentence)
        word_list = sentence.split()
        if len(word_list) == 0:
            sentence_new = ''
            return sentence_new
        i = 0
        while i < len(word_list)-1:
            word_1 = word_list[i]
            word_2 = word_list[i+1]
            self.printlog = False
            bridge = self.queryBridgeWords(word_1, word_2)
            if len(bridge) > 0:
                index = random.randint(0, len(bridge)-1)
                word_insert = bridge[index]
                word_list.insert(i+1, word_insert)
                i += 2
            else:
                i += 1
        word_list[0] = word_list[0].capitalize()
        sentence_new = " ".join(word_list)
        return sentence_new

    def confirmInput(self):
        if self.WORDS is not None and self.GRAPH is not None and self.NLIST is not None:
            if not self.generate_mode:  # 查询模式
                input = self.inputedit.toPlainText()
                self.inputedit.clear()
                self.inputedit.setEnabled(False)

                prompt = input.split()
                if len(prompt) == 2:
                    token1, token2 = prompt[0].lower(), prompt[1].lower()
                else:
                    self.consolePrint("<GraphDealer> 查询失败: 输入格式有误！请重新输入！")
                    self.inputedit.setEnabled(True)
                    return
                
                self.printlog = True
                bridge = self.queryBridgeWords(token1, token2)
                if len(bridge):
                    shutil.rmtree('./save_figure/BridgeQuery')  
                    os.mkdir('./save_figure/BridgeQuery')
                    self.saveBridgeOnGraph(self.GRAPH, self.POS, "./save_figure", token1, token2, bridge)
                    self.viewer.show()
                    self.viewer.openImage("./save_figure/BridgeQuery")
                else:
                    self.inputedit.setEnabled(True)
                return
            elif self.generate_mode:  # 生成模式
                input = self.inputedit.toPlainText()
                self.inputedit.clear()
                self.inputedit.setEnabled(False)

                sentence_new = self.generateNewText(input)
                self.consolePrint(f"<GraphDealer> 生成成功: {sentence_new}")
                self.inputedit.setEnabled(True)
                return
            else:
                return
        else:
            return

"""
图寻路显示类重写
"""
class RouteViewer(QtWidgets.QWidget):
    signal_r = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.mark_path = []
        self.selected_dirPath = []
        self.selected_imgsPath = []
        self.current_dir_index = 0
        self.current_image_index = 0
        self.gLayout = QGridLayout(self)
        self.initWindow()
        self.LayoutOption()
    
    def closeEvent(self, event):
        self.signal_r.emit(True)

    def initWindow(self):
        self.resize(1100, 1000)
        self.setWindowIcon(QIcon('./logo/logo.ico'))
        self.setWindowTitle('展示最短路')
        
    def LayoutOption(self, stepbutton=True):
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setFixedSize(1100, 900)

        if stepbutton:
            self.next_image_button = PushButton(FIF.PAGE_RIGHT, '下一步', self)
            self.next_image_button.clicked.connect(self.showNextImage)
            self.next_image_button.setFixedSize(183, 35)
            self.prev_image_button = PushButton(FIF.PAGE_LEFT, '上一步', self)
            self.prev_image_button.clicked.connect(self.showPrevImage)
            self.prev_image_button.setFixedSize(183, 35)
            self.next_dir_button = PushButton(FIF.RIGHT_ARROW, '查看下一条最短路', self)
            self.next_dir_button.clicked.connect(self.showNextDir)
            self.next_dir_button.setFixedSize(366, 35)
            self.mark_button = PushButton(FIF.LEAF, '展示所有最短路', self)
            self.mark_button.clicked.connect(self.showAll)
            self.mark_button.setFixedSize(366, 35)
        
        self.gLayout.addWidget(self.label_3, 0, 0, 1, 6)
        if stepbutton:
            self.gLayout.addWidget(self.prev_image_button, 1, 0)
            self.gLayout.addWidget(self.next_image_button, 1, 1)
            self.gLayout.addWidget(self.next_dir_button, 1, 2, 1, 2)
            self.gLayout.addWidget(self.mark_button, 1, 4, 1, 2)
        self.gLayout.setSpacing(0)

    def openImage(self, filepath, markpath):
        self.mark_path = [os.path.join(markpath, i) for i in sorted(os.listdir(markpath))]
        self.selected_dirPath = [os.path.join(filepath, i) for i in sorted(os.listdir(filepath))]
        if len(self.selected_dirPath) == 0:
            self.empty_information()
            print("某文件夹下图为空")
            return
        dirpath = self.selected_dirPath[0]
        self.selected_imgsPath = sorted([os.path.join(dirpath, nm) for nm in os.listdir(dirpath) if nm[-3:] in ['png']])
        if len(self.selected_imgsPath) == 0:
            self.empty_information()
            return
 
        img = QtGui.QPixmap(self.selected_imgsPath[0]).scaled(1100, 900)
        self.label_3.setPixmap(img)
        self.current_image_index = 0
        self.current_dir_index = 0
        
    def showNextImage(self):
        if len(self.selected_imgsPath) == 0:
            return
 
        self.current_image_index += 1
        if self.current_image_index >= len(self.selected_imgsPath):
            self.current_image_index = 0
 
        img_path = self.selected_imgsPath[self.current_image_index]
        img = QtGui.QPixmap(img_path).scaled(1100, 900)
        self.label_3.setPixmap(img)
        
    def showPrevImage(self):
        if len(self.selected_imgsPath) == 0:
            return
 
        self.current_image_index -= 1
        if self.current_image_index < 0:
            self.current_image_index = len(self.selected_imgsPath) - 1
 
        img_path = self.selected_imgsPath[self.current_image_index]
        img = QtGui.QPixmap(img_path).scaled(1100, 900) 
        self.label_3.setPixmap(img)
    
    def showNextDir(self):
        if len(self.selected_dirPath) == 0:
            self.empty_information()
            return
        
        self.current_dir_index += 1
        if self.current_dir_index >= len(self.selected_dirPath):
            self.current_dir_index = 0

        dirpath = self.selected_dirPath[self.current_dir_index]
        self.selected_imgsPath = sorted([os.path.join(dirpath, nm) for nm in os.listdir(dirpath) if nm[-3:] in ['png']])
        if len(self.selected_imgsPath) == 0:
            self.empty_information()
            print("某文件夹下图为空")
            return
        img = QtGui.QPixmap(self.selected_imgsPath[0]).scaled(1100, 900)
        self.label_3.setPixmap(img)
        self.current_image_index = 0
    
    def showAll(self):
        if len(self.mark_path) == 0:
            self.empty_information()
            return
        img = QtGui.QPixmap(self.mark_path[0]).scaled(1100, 900)
        self.label_3.setPixmap(img)

"""
3. 图寻路模块 主页下的第三个选择
"""
class graphRouting(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.gLayout = QGridLayout(self)
        self.setObjectName(text.replace(' ', '-'))
       
        self.GRAPH = None
        self.NLIST = None
        self.WORDS = None
        self.POS = None

        self.btu1 = PushButton(FIF.ACCEPT, '确认输入', self)
        self.btu1.clicked.connect(self.confirmInput)
        self.btu1.setFixedSize(247, 35)
        shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Return), self)
        shortcut.activated.connect(self.confirmInput)
        shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Enter), self)
        shortcut.activated.connect(self.confirmInput)

        self.btu2 = PushButton(FIF.BRUSH, '清空屏幕', self)
        self.btu2.clicked.connect(self.clearConsole)
        self.btu2.setFixedSize(247, 35)

        self.inputedit = PlainTextEdit()
        self.inputedit.setFixedSize(500, 70)
        self.inputedit.setEnabled(False)

        self.console = PlainTextEdit()
        self.console.setFixedSize(500, 200)
        self.console.setReadOnly(True)
        
        self.viewer = RouteViewer()
        self.viewer.signal_r.connect(self.enableInput_aftershow)

        self.gLayout.addWidget(self.console, 0, 0, 1, 2)
        self.gLayout.addWidget(self.inputedit, 1, 0, 1, 2)
        self.gLayout.addWidget(self.btu1, 2, 0)
        self.gLayout.addWidget(self.btu2, 2, 1)
        self.gLayout.setSpacing(0)

        self.clearConsole()
        
    def enableInput_aftershow(self, ifenable):
        self.inputedit.setEnabled(True)

    def clearConsole(self):
        self.console.clear()
        if self.WORDS is not None:
            welcome = "                  🚀欢迎使用图寻路功能模块🚀包含两项功能:\n1. 一对一寻路：输入一对单词，确认后将输出其所有的最短路情况\n2. 一对多寻路：输入一个单词，确认后输出其到图中其他节点的最短路情况\n以下为当前图的词表:\n"
            self.console.setPlainText(welcome)
            wordlist = ""
            num = len(self.WORDS)
            for i in range(num):
                wordlist = wordlist + self.WORDS[i]
                if i != num-1:
                    wordlist = wordlist + ', '
            self.console.appendPlainText(wordlist+'\n')
        else:
            tips = "                                 🚀欢迎使用图寻路功能模块🚀\n              请先在侧栏“图搭建”中选择待处理的英文文本并保存"
            self.console.setPlainText(tips)

    def consolePrint(self, log, printlog=True):
        if printlog:
            self.console.appendPlainText(log)
            bar = self.console.verticalScrollBar()
            bar.setSliderPosition(bar.maximum())

    def showRouteOnGraph(self, G, pos, path, elist, i):
        dir_path = os.path.join(path, f"{i}")
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        for j in range(len(elist)):
            edge = elist[j]
            plt.rcParams['figure.figsize'] = (12, 15)
            nx.draw(G, pos, alpha=0.5, node_size=700)
            node_labels = nx.get_node_attributes(G, 'name')
            nx.draw_networkx_labels(G, pos=pos, labels=node_labels, font_size=7)

            edge_pairs_bridge = [edge]
            nx.draw_networkx_edges(G, pos, edgelist=edge_pairs_bridge, edge_color='m', width=4)
            labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
            plt.savefig(os.path.join(dir_path, f"{j}.png"))
            plt.cla()

    def markAllRoute(self, G, pos, path, elist):
        edge_color = ['r', 'g', 'b', 'y', 'k']
        
        plt.rcParams['figure.figsize'] = (12, 15)
        nx.draw(G, pos, alpha=0.5, node_size=700)
        node_labels = nx.get_node_attributes(G, 'name')
        nx.draw_networkx_labels(G, pos=pos, labels=node_labels, font_size=7)

        for i in range(len(elist)):
            oneway = elist[i]
            edges = []
            for j in range(len(oneway)-1):
                node_1, node_2 = self.WORDS[oneway[j]], self.WORDS[oneway[j+1]]
                one_edge = (node_1, node_2)
                edges.append(one_edge)
            nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=edge_color[i], width=4)
        
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.savefig(os.path.join(path, f"colorMark.png"))
        plt.cla()

    def calcShortestPath(self, token1, token2):
        if token1 == token2:
            self.consolePrint(f"<GraphDealer> 特例: 输入词相同，不进行最短路查询")
            self.inputedit.setEnabled(True)
            return
        if token1 not in self.WORDS or token2 not in self.WORDS:
            self.consolePrint(f"<GraphDealer> 计算失败: 输入词不合法，请输入词表中的词")
            self.inputedit.setEnabled(True)
            return
        seq_1 = self.WORDS.index(token1)
        seq_2 = self.WORDS.index(token2)
        graph_route = Nodes_to_Graph(self.NLIST)
        distances, paths = graph_route.Dijkstra(seq_1)
        if paths[seq_2][0] is None:
            self.consolePrint(f"<GraphDealer> 计算成功: {token1} 到 {token2}不可达")
            self.inputedit.setEnabled(True)
        else:
            route_result = graph_route.getPaths(seq_1, seq_2, paths)
            self.consolePrint(f"<GraphDealer> 计算成功: {token1} 到 {token2}的最短路长度 {distances[seq_2]}")
            self.consolePrint(f"   以下是所有长度为 {distances[seq_2]} 的路径：")
            for i in range(0, len(route_result)):
                string = '->'.join([self.WORDS[i] for i in route_result[i]])
                self.consolePrint(f"    序号{i+1}:  {string}")
            self.consolePrint('')
            
            shutil.rmtree('./save_figure/Routing')  
            os.mkdir('./save_figure/Routing')
            shutil.rmtree('./save_figure/Routing_all')  
            os.mkdir('./save_figure/Routing_all')
            for i in range(len(route_result)):
                oneway = route_result[i]
                edges = []
                for j in range(len(oneway)-1):
                    node_1, node_2 = self.WORDS[oneway[j]], self.WORDS[oneway[j+1]]
                    one_edge = (node_1, node_2)
                    edges.append(one_edge)
                self.showRouteOnGraph(self.GRAPH, self.POS, "./save_figure/Routing", edges, i)
            self.markAllRoute(self.GRAPH, self.POS, "./save_figure/Routing_all", route_result)
            self.viewer.show()
            self.viewer.openImage("./save_figure/Routing", "./save_figure/Routing_all")

    def confirmInput(self):
        if self.WORDS is not None and self.GRAPH is not None and self.NLIST is not None:
            input = self.inputedit.toPlainText()
            self.inputedit.clear()
            self.inputedit.setEnabled(False)

            prompt = input.split()
            if len(prompt) == 2:
                token1, token2 = prompt[0].lower(), prompt[1].lower()
                self.calcShortestPath(token1, token2)

            elif len(prompt) == 1:
                token1 = prompt[0].lower()
                if token1 not in self.WORDS:
                    self.consolePrint(f"<GraphDealer> 计算失败: 输入词不合法，请输入词表中的词")
                    self.inputedit.setEnabled(True)
                    return
                seq_query = self.WORDS.index(token1)
                graph_route = Nodes_to_Graph(self.NLIST)
                distances, paths = graph_route.Dijkstra(seq_query)
                for i in range(len(distances)):
                    word = self.WORDS[i]
                    if paths[i][0] is None:
                        if word != token1:
                            self.consolePrint(f"<GraphDealer> 计算成功: {token1} 到 {word}不可达")
                            self.consolePrint('')
                    else:
                        route_results = graph_route.getAllPath(seq_query, paths)
                        self.consolePrint(f"<GraphDealer> 计算成功: {token1} 到 {word}的最短路长为 {distances[i]}")
                        self.consolePrint(f"   其中途经节点最少的一条是：")
                        string = '->'.join([self.WORDS[j] for j in route_results[i]])
                        self.consolePrint(f"    {string}")
                        self.consolePrint('')
                self.inputedit.setEnabled(True)
            
            else:
                self.consolePrint("<GraphDealer> 计算失败: 输入词不合法，请输入词表中的词")
                self.inputedit.setEnabled(True)
            return
        else:
            return

"""
4. 图游走模块 主页下的第四个选择
"""
class graphWalking(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.gLayout = QGridLayout(self)
        self.setObjectName(text.replace(' ', '-'))
       
        self.GRAPH = None
        self.NLIST = None
        self.WORDS = None
        self.POS = None

        self.goflag = True

        self.btu1 = PushButton(FIF.ACCEPT, '确认输入', self)
        self.btu1.clicked.connect(self.randomWalk)
        self.btu1.setFixedSize(124, 35)
        shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Return), self)
        shortcut.activated.connect(self.randomWalk)
        shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Enter), self)
        shortcut.activated.connect(self.randomWalk)

        self.btu2 = PushButton(FIF.BRUSH, '清空屏幕', self)
        self.btu2.clicked.connect(self.clearConsole)
        self.btu2.setFixedSize(124, 35)

        self.btu3 = PushButton(FIF.SAVE, '中止游走并提前保存结果', self)
        self.btu3.clicked.connect(self.interuptSave)
        self.btu3.setFixedSize(248, 35)
        self.btu3.setEnabled(False)
        
        self.inputedit = PlainTextEdit()
        self.inputedit.setFixedSize(500, 70)
        self.inputedit.setEnabled(False)

        self.console = PlainTextEdit()
        self.console.setFixedSize(500, 200)
        self.console.setReadOnly(True)
        
        self.gLayout.addWidget(self.console, 0, 0, 1, 4)
        self.gLayout.addWidget(self.inputedit, 1, 0, 1, 4)
        self.gLayout.addWidget(self.btu1, 2, 0)
        self.gLayout.addWidget(self.btu2, 2, 1)
        self.gLayout.addWidget(self.btu3, 2, 2, 1, 2)
        self.gLayout.setSpacing(0)

        self.clearConsole()

    def pause(self, seconds):
        loop = QEventLoop()
        QTimer.singleShot(seconds * 1000, loop.quit)
        loop.exec_()

    def consolePrint(self, log, printlog=True):
        if printlog:
            self.console.appendPlainText(log)
            bar = self.console.verticalScrollBar()
            bar.setSliderPosition(bar.maximum())

    def clearConsole(self):
        self.console.clear()
        if self.WORDS is not None:
            welcome = "                  🚀欢迎使用图游走功能模块🚀包含一项功能:\n随机游走: 输入起点词，将沿出边随机遍历直到边重复、无出边或人为中止\n以下为当前图的词表:\n"
            self.console.setPlainText(welcome)
            wordlist = ""
            num = len(self.WORDS)
            for i in range(num):
                wordlist = wordlist + self.WORDS[i]
                if i != num-1:
                    wordlist = wordlist + ', '
            self.console.appendPlainText(wordlist+'\n')
        else:
            tips = "                                 🚀欢迎使用图游走功能模块🚀\n              请先在侧栏“图搭建”中选择待处理的英文文本并保存"
            self.console.setPlainText(tips)

    def interuptSave(self):
        self.goflag = False
        self.btu3.setEnabled(False)

    def Random_Walk_ui(self, node_list, start_seq, save_path):
        file = open(save_path, "w", encoding="utf-8")
        word_list = []
        line = str()
        seq = start_seq
        self.btu3.setEnabled(True)
        while len(node_list[seq].after.keys()) >= 0 and self.goflag :
            word = node_list[seq].name
            word_list.append(word)
            self.consolePrint(f"<GraphDealer> 游走提示: 当前所在节点: {word}")

            addr_list = search_word(word, word_list)
            if len(addr_list) > 1:
                quit_flag = if_quit_by_repeated_edge(word_list, addr_list)
                if quit_flag:
                    break

            next_words = list(node_list[seq].after.keys())
            if len(next_words) == 0:
                break
            else:
                rand = random.randint(0, len(next_words) - 1)
                seq = next_words[rand]
            
            self.pause(1.5)

        self.consolePrint(f"<GraphDealer> 游走完成: 以下结果将被保存到文件:")
        self.goflag = True
        self.btu3.setEnabled(False)
        for word_i in word_list:
            line += (word_i + " ")
        
        self.consolePrint(f"  {line}")
        file.write(line)


    def randomWalk(self):
        if self.WORDS is not None and self.GRAPH is not None and self.NLIST is not None:
            input = self.inputedit.toPlainText()
            self.inputedit.clear()
            self.inputedit.setEnabled(False)
        
            prompt = input.split()
            if len(prompt) == 0:
                n = random.randint(0, len(self.WORDS)-1)
                prompt = [self.WORDS[n]]
            if len(prompt) == 1 and prompt[0] in self.WORDS:
                seq = self.WORDS.index(prompt[0])
                self.consolePrint(f"<GraphDealer> 游走开始，起点: {prompt[0]}")
                self.Random_Walk_ui(self.NLIST, seq, "./data/random_walk/result.txt")
                self.inputedit.setEnabled(True)
                return
            else:
                self.consolePrint(f"<GraphDealer> 游走失败: 输入词不合法，请输入词表中的词")
                self.inputedit.setEnabled(True)
                return
        else:
            return

        