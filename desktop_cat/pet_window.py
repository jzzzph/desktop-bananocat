from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QWidget, QLabel

from desktop_cat.animation import Animation, load_frames
from desktop_cat.paths import IDLE_SHEET

IDLE_FRAME_COUNT = 6
IDLE_FRAME_MS = 200  # 6 FPS


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

        # Animación que se está reproduciendo
        self.animation = Animation(
            load_frames(IDLE_SHEET, IDLE_FRAME_COUNT),
            IDLE_FRAME_MS,
        )

        # Label que muestra el frame actual
        self.label = QLabel(self)
        self._show_current_frame()
        frame_size = self.animation.current_frame().size()
        self.label.resize(frame_size)
        self.resize(frame_size)

        # Temporizador que avanza la animación
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._next_frame)
        self.timer.start(self.animation.frame_ms)

        self._place_on_screen()

    def _place_on_screen(self):
        screen = QGuiApplication.primaryScreen()
        area = screen.availableGeometry()

        x = area.x() + (area.width() - self.width()) // 2
        y = area.y() + area.height() - self.height()

        self.move(x, y)

    def _show_current_frame(self):
        self.label.setPixmap(self.animation.current_frame())

    def _next_frame(self):
        self.animation.advance()
        self._show_current_frame()