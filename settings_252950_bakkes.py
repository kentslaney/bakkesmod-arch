import os, shlex
flag = "BAKKES"

def update(user_settings):
    dll = ("promptless",) if os.environ.get("PROMPTLESS", "0") == "1" else ()
    user_settings.update({"PROTON_REMOTE_DEBUG_CMD": shlex.join((
        os.environ["STEAM_COMPAT_DATA_PATH"] +
        "/pfx/drive_c/users/steamuser/AppData/Roaming/bakkesmod/inject.exe",
        "launching") + dll)})

