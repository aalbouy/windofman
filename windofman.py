#!/usr/bin/env -S sh -c '"`dirname $0`/venv/bin/python3" "$0" "$@"'
from keyboardManager import KeyboardManager
from windowConfig import WindowConfig
from windowManager import WindowManager
from finder import Finder


def main():
    finder = Finder()
    finder.start()
    wm = WindowManager()
    wc = WindowConfig(wm, finder)
    KeyboardManager(wm)
    wc.start()


if __name__ == '__main__':
    main()
