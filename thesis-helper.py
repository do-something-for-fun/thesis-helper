#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019年11月4日16:56:33
# @Author  : 穆华岭
# @Software: 毕业论文小助手
# @github    ：https://github.com/muhualing/
import os
import sys
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl,pyqtSignal,QEvent,Qt
import platform
sysstr = platform.system()
is_win = is_linux = is_mac = False

if sysstr == "Windows":

    is_win = True
elif sysstr == "Linux":
    is_linux = True
elif sysstr == "Mac":
    is_mac = True


print('System: %s' % sysstr)
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QMainWindow,
    QGroupBox,QApplication, QLabel, QPlainTextEdit,
    QComboBox
)

from thesisUtils.controller import con
from thesisUtils.watch_clip import WatchClip
from thesisUtils.text_filter import TextFilter


MAX_CHARACTERS = 5000

class WebView(QWebEngineView):
    def __init__(self):
        print('init webView')
        super(WebView, self).__init__()
        self._glwidget = None
        self.pdf_js_path = "file:///" + os.path.join(os.getcwd(), "pdfjs", "web", "viewer.html")
        pdf_path = "file:///" + os.path.join(os.getcwd(), "sample", "sample_2.pdf")        
        if sys.platform == "win32":
            self.pdf_js_path = self.pdf_js_path.replace('\\', '/')
            pdf_path = pdf_path.replace('\\', '/')
        self.changePDF(pdf_path)
        self.setAcceptDrops(True)
        self.installEventFilter(self)

    def dragEnterEvent(self,e):
        """
        Detect mouse drag something into the view

        :param e: Mouse event
        :return: None
        """
        if is_linux or is_mac:
            if e.mimeData().hasFormat('text/plain') and e.mimeData().text()[-6:-2] == ".pdf":
                e.accept()
            else:
                e.ignore()
        elif is_win:
            if e.mimeData().text()[-4:] == ".pdf":
                e.accept()
            else:
                e.ignore()

            # QMessageBox.about(self, "提示", "所选文件不是pdf格式的文件") 这行会卡死 不知道为啥
    def dropEvent(self,e):
        """
        Detect mouse release event the view and state before release is dragging

        :param e: Mouse event
        :return: None
        """
        self.changePDF(e.mimeData().text())

    def event(self, e):
        """
        Detect child add event, as QWebEngineView do not capture mouse event directly,
        the child layer _glwidget is implicitly added to QWebEngineView and we track mouse event through the glwidget

        :param e: QEvent
        :return: super().event(e)
        """
        if self._glwidget is None:
            if e.type() == QEvent.ChildAdded and e.child().isWidgetType():
                    print('child add')

                    self._glwidget = e.child()
                    self._glwidget.installEventFilter(self)
        # if(e.type() == QEvent.ChildRemoved and e.child().isWidgetType()):
        #     # print('child removed')
        #     if(self._glwidget is not None):
        #         self._glwidget.removeEventFilter(self)
        # if(e.type() == QEvent.Close):
        #     # print('close webView')
        #     self.removeEventFilter(self)
        return super().event(e)

    def eventFilter(self, source, event):
        if (event.type() == QEvent.MouseButtonRelease and source is self._glwidget):
            con.pdfViewMouseRelease.emit()
        return super().eventFilter(source, event)
    def changePDF(self,pdf_path ):
        self.load(QUrl.fromUserInput('%s?file=%s' % (self.pdf_js_path, pdf_path)))


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.thread_my = WatchClip()
        self.thread_my.start()

        self.setWindowTitle("毕业论文小助手")

        self.translate_ori = QPlainTextEdit()
        # self.translate_ori.setTextBackgroundColor(QColor(127, 127, 127, 60))
        # self.translate_ori.setTextColor(QColor(0, 0, 0, 0))

        self.translate_ori.setStyleSheet("font: 12pt Roboto")

        self.translate_res = QPlainTextEdit()
        self.translate_res.setStyleSheet("font: 12pt Roboto")

        self.selectable_text_size = ['8','9','10','11','12','13','14','15',]

        self.text_size_combobox_ori = QComboBox()
        self.text_size_combobox_ori.addItems(self.selectable_text_size)
        self.text_size_combobox_ori.setCurrentIndex(4)

        self.text_size_combobox_res = QComboBox()
        self.text_size_combobox_res.addItems(self.selectable_text_size)
        self.text_size_combobox_res.setCurrentIndex(4)


        label1 = QLabel('字体大小:')
        label1.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        label2 = QLabel('字体大小:')
        label2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        oriHboxLayout = QHBoxLayout()
        oriHboxLayout.addWidget(QLabel('原文'))
        oriHboxLayout.addWidget(label1)
        oriHboxLayout.addWidget(self.text_size_combobox_ori)
        oriHboxLayout.setStretch(0,6)
        oriHboxLayout.setStretch(1,3)
        oriHboxLayout.setStretch(2,3)
        oriWidget = QWidget()
        oriWidget.setLayout(oriHboxLayout)

        resHboxLayout = QHBoxLayout()
        resHboxLayout.addWidget(QLabel('译文'))
        resHboxLayout.addWidget(label2)
        resHboxLayout.addWidget(self.text_size_combobox_res)
        resHboxLayout.setStretch(0,6)
        resHboxLayout.setStretch(1,3)
        resHboxLayout.setStretch(2,3)
        resWidget = QWidget()
        resWidget.setLayout(resHboxLayout)

        self.filter = TextFilter()
        vbox = QVBoxLayout()
        vbox.addWidget(oriWidget)
        vbox.addWidget(self.translate_ori)
        vbox.addWidget(resWidget)
        vbox.addWidget(self.translate_res)

        gbox = QGroupBox()
        gbox.setStyleSheet("font: 12pt Roboto")
        gbox.setLayout(vbox)

        self.pdfWrapper = WebView()
        hBoxLayout = QHBoxLayout()
        hBoxLayout.addWidget(self.pdfWrapper)
        hBoxLayout.addWidget(gbox)
        hBoxLayout.setStretch(0, 9)
        hBoxLayout.setStretch(1, 3)

        widget = QWidget()
        widget.setLayout(hBoxLayout)
        self.setCentralWidget(widget)
        self.recent_text = ""
        self.showMaximized()

    def updateTranslation(self, cur_text):
        self.translate_res.clear()
        self.translate_res.setPlainText(cur_text)

    def updateByMouseRelease(self):
        # print('no seletion to translate')
        if self.pdfWrapper.hasSelection():

            to_translate_text = self.pdfWrapper.selectedText()
            if len(to_translate_text) > MAX_CHARACTERS:
                hint_str = '请选择少于%d个英文字符' % MAX_CHARACTERS
                # print(hint_str)
                self.translate_ori.setText(hint_str)

                return
            else:
                if self.recent_text == to_translate_text:
                    # print('same as before, not new translate')
                    return
                else:
                    hint_str = '正在翻译...'
                    filtered = self.filter.removeDashLine(to_translate_text)
                    # print(filtered)
                    self.recent_text = to_translate_text
                    self.translate_ori.setPlainText(filtered)
                    self.translate_res.setPlainText(hint_str)
                    # self.thread_my.setTranslateText(filtered)

    def updateByTextEdit(self):
        # print('TextEdited')
        self.thread_my.setTranslateText(self.translate_ori.toPlainText())

    def updateOriTextSizeByIndexChanged(self, index):
        self.translate_ori.setStyleSheet("font: {0}pt Roboto".format(self.selectable_text_size[index]))

    def updateResTextSizeByIndexChanged(self, index):
        self.translate_res.setStyleSheet("font: {0}pt Roboto".format(self.selectable_text_size[index]))

    def closeEvent(self, event):
        self.thread_my.expired()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    con.translationChanged.connect(mainWindow.updateTranslation)
    con.pdfViewMouseRelease.connect(mainWindow.updateByMouseRelease)
    mainWindow.translate_ori.textChanged.connect(mainWindow.updateByTextEdit)
    mainWindow.text_size_combobox_ori.currentIndexChanged.connect(mainWindow.updateOriTextSizeByIndexChanged)
    mainWindow.text_size_combobox_res.currentIndexChanged.connect(mainWindow.updateResTextSizeByIndexChanged)
    sys.exit(app.exec_())
    