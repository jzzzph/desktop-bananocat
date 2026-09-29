from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QWidget, QLabel

from desktop_cat.animation import load_frames
from desktop_cat.paths import IDLE_SHEET

IDLE_FRAME_COUNT = 4
IDLE_FRAME_MS = 167  # 6 FPS


class PetWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Ventana sin bordes, siempre encima y fuera de la barra de tareas
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Frames de la animación y frame actual
        self.frames = load_frames(IDLE_SHEET, IDLE_FRAME_COUNT)
        self.current_frame = 0

        # Label que muestra el frame actual
        self.label = QLabel(self)
        self._show_current_frame()
        self.label.resize(self.frames[0].size())
        self.resize(self.frames[0].size())

        # Temporizador que avanza la animación
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._next_frame)
        self.timer.start(IDLE_FRAME_MS)

        self._place_on_screen()

    def _place_on_screen(self):
        screen = QGuiApplication.primaryScreen()
        area = screen.availableGeometry()

        x = area.x() + (area.width() - self.width()) // 2
        y = area.y() + area.height() - self.height()

        self.move(x, y)

    def _show_current_frame(self):
        self.label.setPixmap(self.frames[self.current_frame])

    def _next_frame(self):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self._show_current_frame()