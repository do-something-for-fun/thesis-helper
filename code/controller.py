from PyQt5.QtCore import QObject, pyqtSignal
class Controller(QObject):
    clip_changed = pyqtSignal(str)
    closed = pyqtSignal()
con = Controller()