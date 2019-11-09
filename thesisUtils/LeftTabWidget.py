import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qtawesome
import os
from thesisUtils.configure import config

class LeftTabWidget(QWidget):
    def __init__(self, pdfWrapper):
        super().__init__()
        self.pdfWrapper = pdfWrapper
        self.setWindowTitle('LTB')

        # main window
        self.main_layout = QHBoxLayout(self)

        # buttons on the left
        self.left_widget = QWidget()
        self.main_layout.addWidget(self.left_widget)
        self.button_layout = QVBoxLayout(self.left_widget)

        self.hide_button = QPushButton(qtawesome.icon('fa.circle', color='red'), '')
        self.button_layout.addWidget(self.hide_button)

        self.update_button = QPushButton(qtawesome.icon('fa.cloud', color='red'), '')
        self.button_layout.addWidget(self.update_button)

        self.local_pdf = QPushButton(qtawesome.icon('fa.home', color='red'), '')
        self.button_layout.addWidget(self.local_pdf)

        self.history_pdf = QPushButton(qtawesome.icon('fa.heart', color='red'), '')
        self.button_layout.addWidget(self.history_pdf)

        self.pushButton3 = QPushButton(qtawesome.icon('fa.question', color='red'), '')
        self.button_layout.addWidget(self.pushButton3)

        # stacked_widget as the right widget
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)
        # resize the stacked_widget
        self.stacked_widget.setMinimumWidth(250)

        # Local PDF
        self.local_pdf_path_list, self.local_pdf_name_list = list(self.getLocalPDF(config['local_pdf']['roots']))
        self.list_widget_of_local_pdf = QListWidget()
        self.list_widget_of_local_pdf.addItems(self.local_pdf_name_list)
        self.local_pdf_layout = QVBoxLayout(self.list_widget_of_local_pdf)

        # History PDF
        self.history_pdf_path_list, self.history_pdf_name_list = self.getHistoryPDF()
        self.list_widget_of_history_pdf = QListWidget()
        self.list_widget_of_history_pdf.addItems(self.history_pdf_name_list)
        self.history_pdf_layout = QVBoxLayout(self.list_widget_of_history_pdf)

        # TODO
        self.form3 = QWidget()
        self.formLayout3 = QHBoxLayout(self.form3)
        self.label3 = QLabel()
        self.label3.setText("TODO")
        self.label3.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.label3.setAlignment(Qt.AlignCenter)
        # self.label3.setFont(QFont("Roman times", 50, QFont.Bold))
        self.formLayout3.addWidget(self.label3)

        # add widgets to stacked_widget
        self.stacked_widget.addWidget(self.list_widget_of_local_pdf)
        self.stacked_widget.addWidget(self.list_widget_of_history_pdf)
        self.stacked_widget.addWidget(self.form3)

        # clicked event definition
        # for button
        self.update_button.clicked.connect(self.updateButtonClicked)
        self.local_pdf.clicked.connect(self.localPDFClicked)
        self.history_pdf.clicked.connect(self.historyPDFClicked)
        self.pushButton3.clicked.connect(self.on_pushButton3_clicked)
        self.hide_button.clicked.connect(self.hideButtonClicked)
        # for item
        self.list_widget_of_local_pdf.itemDoubleClicked.connect(self.localListWidgetDBClicked)
        self.list_widget_of_history_pdf.itemDoubleClicked.connect(self.historyListWidgetDBClicked)

    def updateButtonClicked(self):
        self._updateHistory()

    def historyListWidgetDBClicked(self, item):
        for path in self.history_pdf_path_list:
            if item.text() in path.lower():
                self.pdfWrapper.changePDF(path)

    def localListWidgetDBClicked(self, item):
        for path in self.local_pdf_path_list:
            if item.text() in path:
                self.pdfWrapper.changePDF(path)

    def hideButtonClicked(self):
        self.stacked_widget.setHidden(not self.stacked_widget.isHidden())
        self.local_pdf.setEnabled(not self.stacked_widget.isHidden())
        self.history_pdf.setEnabled(not self.stacked_widget.isHidden())
        self.pushButton3.setEnabled(not self.stacked_widget.isHidden())

    def localPDFClicked(self):
        self.stacked_widget.setCurrentIndex(0)

    def historyPDFClicked(self):
        self.stacked_widget.setCurrentIndex(1)

    def on_pushButton3_clicked(self):
        self.stacked_widget.setCurrentIndex(2)

    def getLocalPDF(self, roots=''):
        """
        :param roots: should be absolute path
        :return: pdf path and pdf name
        """
        if roots == 'none':
            return [], []

        def _getFullPath():
            for root, dirs, files in os.walk(roots, topdown=True):
                for name in files:
                    if name.split('.')[1] == 'pdf':
                        full_path = os.path.join(root, name)
                        yield full_path.replace('\\', '/')

        def _getFullName():
            for root, dirs, files in os.walk(roots, topdown=True):
                for name in files:
                    if name.split('.')[1] == 'pdf':
                        yield name.split('.')[0]

        return list(_getFullPath()), list(_getFullName())

    def getHistoryPDF(self):
        tp = config.items('history_pdf')
        name_list = []
        path_list = []
        for item in tp:
            name_list.append(item[0])
            path_list.append(item[1])
        return path_list, name_list

    def _updateHistory(self):
        self.history_pdf_path_list, self.history_pdf_name_list = self.getHistoryPDF()
        self.list_widget_of_history_pdf.clear()
        self.list_widget_of_history_pdf.addItems(self.history_pdf_name_list)

    def updateLocal(self):
        self.local_pdf_path_list, self.local_pdf_name_list = list(self.getLocalPDF(config['local_pdf']['roots']))
        self.list_widget_of_local_pdf.clear()
        self.list_widget_of_local_pdf.addItems(self.local_pdf_name_list)


if __name__ == "__main__":
    print(config["local_pdf"]["roots"])