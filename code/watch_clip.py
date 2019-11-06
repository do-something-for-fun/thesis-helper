import threading
import pyperclip
import time
from controller import con
from translate import get_translation, get_translation_by_google
from text_filter import TextFilter

class WatchClip(threading.Thread):
    def __init__(self):
        super(WatchClip, self).__init__()
        self.name = ""
        self.expire = False
        self.filter = TextFilter()

    def run(self):
        con.closed.connect(self.expired)
        recent_text = pyperclip.paste()
        cur_text = ""
        while True and not self.expire:
            cur_text = pyperclip.paste()
            if cur_text == recent_text:
                time.sleep(0.1)
            else:
                recent_text = cur_text
                self.update(cur_text)

    def update(self, cur_text):
        # con.clip_changed.emit(get_translation(cur_text))
        cur_text = self.filter.removeDashLine(cur_text)
        con.clip_changed.emit(get_translation_by_google(cur_text))

    def expired(self):
        self.expire = True