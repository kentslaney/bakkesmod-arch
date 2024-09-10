import os, shlex, pathlib
flag = "BAKKES"

def update(user_settings):
    promptless = os.environ.get("PROMPTLESS", "0") == "1"
    dll = "bakkesmod_promptless.dll" if promptless else "bakkesmod_official.dll"
    pfx = pathlib.Path(os.environ["STEAM_COMPAT_DATA_PATH"]) / \
        pathlib.Path("pfx/drive_c/users/steamuser/AppData/Roaming/bakkesmod")
    print(pfx)
    return
    dll_path = pfx / "bakkesmod" / "dll"
    try:
        os.remove(dll_path / "bakkesmod.dll")
    finally:
        os.symlink(dll_path / dll, dll_path / "bakkesmod.dll")
    user_settings.update({"PROTON_REMOTE_DEBUG_CMD": shlex.join((
        str(pfx / "inject.exe"), "launching"))})
