import threading
import pyperclip
import time
from controller import con
from translate import get_translation

class WatchClip(threading.Thread):
    def __init__(self):
        super(WatchClip, self).__init__()
        self.name = ""

    def run(self):
        recent_text = pyperclip.paste()
        cur_text = ""
        while True:
            cur_text = pyperclip.paste()
            if cur_text == recent_text:
                time.sleep(0.1)
            else:
                recent_text = cur_text
                self.update(cur_text)

    def update(self, cur_text):
        con.clip_changed.emit(get_translation(cur_text))