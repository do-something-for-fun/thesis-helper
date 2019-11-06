from PyQt5.QtCore import QObject, pyqtSignal
class Controller(QObject):
    translationChanged = pyqtSignal(str)
    closed = pyqtSignal()
    pdfViewMouseRelease = pyqtSignal()
con = Controller()