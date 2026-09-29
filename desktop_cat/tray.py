from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from desktop_cat.paths import TRAY_ICON


class TrayIcon(QSystemTrayIcon):
    def __init__(self):
        super().__init__()

        self.setIcon(QIcon(str(TRAY_ICON)))
        self.setToolTip("Bananocat")

        self.menu = QMenu()
        quit_action = self.menu.addAction("Salir")
        quit_action.triggered.connect(QApplication.quit)

        self.setContextMenu(self.menu)