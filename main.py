"""
main.py — Punto de entrada de la aplicación.
"""

import sys
import os
import ctypes

def attach_to_default_desktop() -> None:
    if sys.platform == "win32":
        try:
            user32 = ctypes.windll.user32
            hdesk = user32.OpenDesktopW("Default", 0, False, 0x10000000)
            if hdesk:
                user32.SetThreadDesktop(hdesk)
        except Exception:
            pass

attach_to_default_desktop()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from views.main_window import MainWindow


def main() -> None:
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
