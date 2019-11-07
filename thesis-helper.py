#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019年11月4日16:56:33
# @Author  : 穆华岭
# @Software: 毕业论文小助手
# @github    ：https://github.com/muhualing/
import os
import sys
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl,pyqtSignal,QEvent
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QWidget,
    QHBoxLayout, QVBoxLayout, QMainWindow, QTextEdit, QGroupBox,QApplication, QLabel, QTextBrowser)

from thesisUtils.controller import con
from thesisUtils.watch_clip import WatchClip
from thesisUtils.text_filter import TextFilter


MAX_CHARACTERS = 5000

class WebView(QWebEngineView):
    def __init__(self):
        super(WebView, self).__init__()
        self.pdf_js_path = "file:///" + os.path.join(os.getcwd(), "pdfjs", "web", "viewer.html")
        pdf_path = "file:///" + os.path.join(os.getcwd(), "sample", "sample_2.pdf")        
        if sys.platform == "win32":
            self.pdf_js_path = self.pdf_js_path.replace('\\', '/')
            pdf_path = pdf_path.replace('\\', '/')
        self.changePDF(pdf_path)
        self.setAcceptDrops(True)
        self.installEventFilter(self)
    def dragEnterEvent(self,e):
        print('drag')
        e.accept()

    def dropEvent(self,e):
        print('drop')
        self.changePDF(e.mimeData().text())

    def event(self, e):
        if(e.type() == QEvent.ChildAdded and e.child().isWidgetType()):
            # print('child add')
            self._glwidget = e.child()
            self._glwidget.installEventFilter(self)

        if(e.type() == QEvent.ChildRemoved and e.child.isWidgetType()):
            # print('child removed')
            if(self._glwidget is not None):
                self._glwidget.removeEventFilter(self)
        if(e.type() == QEvent.Close):
            # print('close webView')
            self.removeEventFilter(self)
        return super().event(e)

    def eventFilter(self, source, event):
        if (event.type() == QEvent.MouseButtonRelease and source is self._glwidget):
            con.pdfViewMouseRelease.emit()
        return super().eventFilter(source, event)
    def changePDF(self,pdf_path ):
        self.load(QUrl.fromUserInput('%s?file=%s' % (self.pdf_js_path, pdf_path)))

    # def



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.thread_my = WatchClip()
        self.thread_my.start()

        self.setWindowTitle("毕业论文小助手")

        self.translate_ori = QTextEdit()
        self.translate_ori.setTextBackgroundColor(QColor(127, 127, 127, 60))
        self.translate_ori.setStyleSheet("font: 12pt Roboto")

        self.translate_res = QTextEdit()
        self.translate_res.setStyleSheet("font: 12pt Roboto")

        self.label = QLabel('翻译原文')

        self.filter = TextFilter()
        vbox = QVBoxLayout()
        vbox.addWidget(self.translate_res)
        vbox.addWidget(self.label)
        vbox.addWidget(self.translate_ori)

        gbox = QGroupBox("中文翻译结果")
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
        self.translate_res.setText(cur_text)

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
                    self.translate_ori.setText(filtered)
                    self.translate_res.setText(hint_str)
                    # self.thread_my.setTranslateText(filtered)

    def updateByTextEdit(self):
        # print('TextEdited')
        self.thread_my.setTranslateText(self.translate_ori.toPlainText())

    def closeEvent(self, event):
        self.thread_my.expired()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    con.translationChanged.connect(mainWindow.updateTranslation)
    con.pdfViewMouseRelease.connect(mainWindow.updateByMouseRelease)
    mainWindow.translate_ori.textChanged.connect(mainWindow.updateByTextEdit)
    sys.exit(app.exec_())
    