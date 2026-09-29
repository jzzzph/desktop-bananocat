import sys
from PySide6.QtWidgets import QApplication

from desktop_cat.pet_window import PetWindow
from desktop_cat.tray import TrayIcon


def main():
    app = QApplication(sys.argv)

    window = PetWindow()
    window.show()

    tray = TrayIcon()
    tray.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()