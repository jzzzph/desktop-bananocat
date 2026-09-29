from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"

IDLE_SHEET = ASSETS_DIR / "cat" / "idle.png"      # sprite sheet de la animación idle
TRAY_ICON = ASSETS_DIR / "cat" / "cat_icon.png"   # ícono de la bandeja del sistema
