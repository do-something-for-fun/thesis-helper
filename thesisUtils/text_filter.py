import re
import os
import sys

class TextFilter():
    def __init__(self):
        self.english_dictionary = []
        self.english_dictionary_path = os.path.join(os.getcwd(), "dictionary", "words_alpha.txt")
        if sys.platform == "win32":
            self.english_dictionary_path = self.english_dictionary_path.replace('\\', '/')
        self.__loadDictFromTxt(self.english_dictionary_path)

    def __loadDictFromTxt(self,fn):
        with open(fn,'r') as f:
            for line in f:
                self.english_dictionary.append(line.strip('\n'))

    def removeDashLine(self,input_text):
        newstr = ''
        words = input_text.split()
        for wo in words:
            if '-' in wo:
                wor = wo.replace('-','')
                wor_split = re.split(" |\.|,|!|\?|\)|\(|\[|\]", wor)[0]
                if wor_split in self.english_dictionary:
                    newstr = newstr + wor + ' '
                else:
                    newstr = newstr + wo + ' '
                pass
            else:
                newstr = newstr + wo + ' '
        return newstr