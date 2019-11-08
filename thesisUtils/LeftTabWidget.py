import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qtawesome
import os


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
        self.local_pdf_path_list, self.local_pdf_name_list = list(self.getLocalPDF())
        self.list_widget_of_local_pdf = QListWidget()
        self.list_widget_of_local_pdf.addItems(self.local_pdf_name_list)
        self.local_pdf_layout = QVBoxLayout(self.list_widget_of_local_pdf)

        # History PDF
        self.form2 = QWidget()
        self.formLayout2 = QHBoxLayout(self.form2)
        self.label2 = QLabel()
        self.label2.setText("History PDF")
        self.label2.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.label2.setAlignment(Qt.AlignCenter)
        self.formLayout2.addWidget(self.label2)

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
        self.stacked_widget.addWidget(self.form2)
        self.stacked_widget.addWidget(self.form3)

        # clicked event definition
        # for button
        self.local_pdf.clicked.connect(self.localPDFClicked)
        self.history_pdf.clicked.connect(self.historyPDFClicked)
        self.pushButton3.clicked.connect(self.on_pushButton3_clicked)
        self.hide_button.clicked.connect(self.hide_button_clicked)
        # for item
        self.list_widget_of_local_pdf.itemDoubleClicked.connect(self.listWidgetDBClicked)

    def listWidgetDBClicked(self, item):
        for path in self.local_pdf_path_list:
            if item.text() in path:
                self.pdfWrapper.changePDF(path)

    def hide_button_clicked(self):
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

    def getLocalPDF(self, roots='G:\\Let_the_boy_fly'):

        def _getFullPath():
            for root, dirs, files in os.walk(roots, topdown=True):
                for name in files:
                    if name.split('.')[1] == 'pdf':
                        full_path = os.path.join(root, name)
                        yield full_path

        def _getFullName():
            for root, dirs, files in os.walk(roots, topdown=True):
                for name in files:
                    if name.split('.')[1] == 'pdf':
                        yield name.split('.')[0]

        return list(_getFullPath()), list(_getFullName())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    left_tab_widget = LeftTabWidget()
    left_tab_widget.show()
    sys.exit(app.exec_())