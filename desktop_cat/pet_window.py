from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QGuiApplication
from PySide6.QtWidgets import QWidget, QLabel
from desktop_cat.paths import CAT_IMAGE


class PetWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint # quita la barra de título y bordes
            | Qt.WindowType.WindowStaysOnTopHint # mantiene encima de las demás ventanas
            | Qt.WindowType.Tool # evita que aparezca en la barra de tareas
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # permite que el fondo sea transparente

        pixmap = QPixmap(str(CAT_IMAGE))

        if pixmap.isNull():
            raise FileNotFoundError(f"No se pudo cargar la imagen: {CAT_IMAGE}")

        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.size())
        self.resize(pixmap.size())

        self._place_on_screen()

    def _place_on_screen(self):
        screen = QGuiApplication.primaryScreen()
        area = screen.availableGeometry()

        x = area.x() + (area.width() - self.width()) // 2
        y = area.y() + area.height() - self.height()

        self.move(x, y)
        print(area)