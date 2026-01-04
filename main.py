# main.py

import ctypes
from clipops.config import APP_NAME, APP_VERSION, ICON_FILE
from clipops.utils import ensure_icon_exists
from clipops.controller import ClipOpsController

def main():
    # 1. Fix Taskbar Icon for Windows
    try:
        myappid = f'collexa.{APP_NAME}.{APP_VERSION}.gui'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    # 2. Ensure resources exist
    ensure_icon_exists(ICON_FILE)

    # 3. Launch App using MVC
    app = ClipOpsController()
    app.run()

if __name__ == "__main__":
    main()