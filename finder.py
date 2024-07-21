import threading
import time
from pathlib import Path
from blinker import Signal
from confManager import ConfManager

import pyautogui
from os import listdir
from os.path import isfile, join

found_char_turn = Signal()


class Finder(threading.Thread):
    @staticmethod
    def __remove_suffix__(word, suffix):
        if word.endswith(suffix):
            return word[:-len(suffix)]
        return word

    def __init__(self):
        super().__init__()
        self.is_running = False
        self.img_path = join(Path(__file__).parent.absolute(), 'finder')
        files = [f for f in listdir(self.img_path) if isfile(join(self.img_path, f))]
        self.chars = []
        for file in files:
            if file.endswith('.png'):
                self.chars.append(self.__remove_suffix__(file, '.png'))

        self.killed = False

    def run(self):
        while True:
            if self.is_running:
                for char in self.chars:
                    file = join(self.img_path, f'{char}.png')
                    try:
                        pyautogui.locateOnScreen(file, confidence=0.9, region=ConfManager.get_finder_zone())
                        found_char_turn.send(self, char=char)
                    except pyautogui.ImageNotFoundException:
                        pass

            if self.killed:
                break
            time.sleep(0.2)

    def set_running(self, is_running):
        self.is_running = is_running

    def end_thread(self):
        self.killed = True
