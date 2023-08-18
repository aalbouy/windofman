from ewmh import EWMH

from confManager import ConfManager
from tools import get_character_name

class WindowManager():

    def __init__(self):

        self.ewmh = EWMH()
        self.windows = self.get_windows()
        self.current_window = self.windows[0] if self.windows else []
    
        self.__sort_windows()

    def get_windows(self):
        windows = []
        for window in self.ewmh.getClientList():
            if b'Dofus' in self.ewmh.getWmName(window):
                windows.append(window)
        return windows

    def print_windows_name(self):
        for window in self.windows:
            print(get_character_name(self.ewmh.getWmName(window)))

    def next(self):
       self.__switch(1)

    def previous(self):
        self.__switch(0)

    def __switch(self, forward : bool):
        step = 1 if forward else -1
        index = self.windows.index(self.current_window) + step

        if not index < len(self.windows):
            index = 0
        elif index < 0:
            index = len(self.windows)-1

        self.current_window = self.windows[index]

        self.__active_current_window()

    def __active_current_window(self):
        self.ewmh.setActiveWindow(self.current_window)
        self.ewmh.display.flush()

    def __sort_windows(self):
        initiative = ConfManager.get_initiative(self.windows,self.ewmh)
        self.windows = sorted(self.windows, key=lambda w : initiative[get_character_name(self.ewmh.getWmName(w))],reverse=True)
