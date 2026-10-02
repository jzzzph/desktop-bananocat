from PySide6.QtGui import QPixmap, QTransform

def load_frames(sheet_path, frame_count):
    sheet = QPixmap(str(sheet_path))

    if sheet.isNull():
        raise FileNotFoundError(f"No se pudo cargar la sprite sheet: {sheet_path}")

    if sheet.width() % frame_count != 0:
        raise ValueError(
            f"El ancho de la sprite sheet ({sheet.width()}) "
            f"no se puede dividir en {frame_count} frames iguales"
        )

    frame_width = sheet.width() // frame_count
    frame_height = sheet.height()

    frames = []
    for i in range(frame_count):
        x = i * frame_width
        frame = sheet.copy(x, 0, frame_width, frame_height)
        frames.append(frame)

    return frames

def mirror_frames(frames):
    flip = QTransform().scale(-1, 1)
    return [frame.transformed(flip) for frame in frames]

class Animation:
    def __init__(self, frames, frame_ms):
        self.frames = frames
        self.frame_ms = frame_ms
        self.current_index = 0

    def current_frame(self):
        return self.frames[self.current_index]

    def advance(self):
        self.current_index = (self.current_index + 1) % len(self.frames)