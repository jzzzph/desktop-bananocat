import random

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QWidget, QLabel

from desktop_cat.animation import Animation, load_frames, mirror_frames
from desktop_cat.paths import IDLE_SHEET, SPRINT_SHEET

IDLE_FRAME_COUNT = 6
IDLE_FRAME_MS = 200   # 6 FPS

SPRINT_FRAME_COUNT = 4
SPRINT_FRAME_MS = 200    # 5 FPS
SPRINT_SPEED = 2         # píxeles que avanza en cada actualización

MOVE_INTERVAL_MS = 16    # ~60 actualizaciones por segundo

IDLE_DURATION_MS = (2000, 6000)     # (mínimo, máximo)
SPRINT_DURATION_MS = (3000, 8000)   # (mínimo, máximo)


class PetWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Animaciones
        self.idle = Animation(load_frames(IDLE_SHEET, IDLE_FRAME_COUNT), IDLE_FRAME_MS)
        sprint_frames = load_frames(SPRINT_SHEET, SPRINT_FRAME_COUNT)
        self.sprint_right = Animation(sprint_frames, SPRINT_FRAME_MS)
        self.sprint_left = Animation(mirror_frames(sprint_frames), SPRINT_FRAME_MS)

        self.direction = 1  # 1 = derecha, -1 = izquierda
        self.animation = self.idle

        # Label con el tamaño inicial
        self.label = QLabel(self)
        self._show_current_frame()
        frame_size = self.animation.current_frame().size()
        self.label.resize(frame_size)
        self.resize(frame_size)

        # Reloj de la animación
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self._next_frame)

        # Reloj del movimiento
        self.move_timer = QTimer(self)
        self.move_timer.setTimerType(Qt.TimerType.PreciseTimer)
        self.move_timer.timeout.connect(self._move_step)

        self._place_on_screen()
        self._enter_idle()

    # ---------- Estados ----------

    def _enter_idle(self):
        self.move_timer.stop()
        self._set_animation(self.idle)
        QTimer.singleShot(random.randint(*IDLE_DURATION_MS), self._enter_sprint)

    def _enter_sprint(self):
        self._set_animation(self._sprint_animation())
        self.move_timer.start(MOVE_INTERVAL_MS)
        QTimer.singleShot(random.randint(*SPRINT_DURATION_MS), self._enter_idle)

    # ---------- Animación ----------

    def _set_animation(self, animation):
        # Guardar el punto de anclaje: centro de los pies
        anchor_x = self.x() + self.width() // 2
        anchor_y = self.y() + self.height()

        self.animation = animation
        self._show_current_frame()

        new_size = animation.current_frame().size()
        self.label.resize(new_size)
        self.resize(new_size)

        # Recolocar la ventana para que el anclaje no se mueva
        self.move(anchor_x - self.width() // 2, anchor_y - self.height())

        self.anim_timer.start(animation.frame_ms)

    def _sprint_animation(self):
        return self.sprint_right if self.direction == 1 else self.sprint_left

    def _show_current_frame(self):
        self.label.setPixmap(self.animation.current_frame())

    def _next_frame(self):
        self.animation.advance()
        self._show_current_frame()

    # ---------- Movimiento ----------

    def _place_on_screen(self):
        area = QGuiApplication.primaryScreen().availableGeometry()

        x = area.x() + (area.width() - self.width()) // 2
        y = area.y() + area.height() - self.height()

        self.move(x, y)

    def _move_step(self):
        area = QGuiApplication.primaryScreen().availableGeometry()
        left_limit = area.x()
        right_limit = area.x() + area.width() - self.width()

        new_x = self.x() + SPRINT_SPEED * self.direction

        if new_x <= left_limit or new_x >= right_limit:
            new_x = max(left_limit, min(new_x, right_limit))
            self._turn_around()

        self.move(new_x, self.y())

    def _turn_around(self):
        self.direction *= -1
        self._set_animation(self._sprint_animation())