import sys
import os
from PyQt5.QtWidgets import QApplication
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'message'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'youtube'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ui'))
from ui.download2 import DownloadView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    home = DownloadView()
    sys.exit(app.exec_())
