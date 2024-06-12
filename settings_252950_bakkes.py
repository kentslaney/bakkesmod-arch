import os, shlex
flag, user_settings = "BAKKES", {"PROTON_REMOTE_DEBUG_CMD": shlex.join((
    os.environ["STEAM_COMPAT_DATA_PATH"] +
    "/pfx/drive_c/users/steamuser/AppData/Roaming/bakkesmod/inject.exe",
    "launching"))}

