import sys
import os
from PyQt5.QtWidgets import QApplication

from home import Ui_HomeWindow

import logging

logging.basicConfig(filename="error.log", level=logging.ERROR)

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        home = Ui_HomeWindow()
        sys.exit(app.exec_())
    except Exception as e:
        logging.error(e)
        sys.exit(1)
