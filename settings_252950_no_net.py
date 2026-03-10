# BakkesMod --> BAKKES --> BAKKA --> BAGA --> 8494 (port #)
# BakkesMod specific in case rewriting requests is later needed
# Right now, though, the proxy server is just a dead end to disable the network
# Starting a server isn't even needed since a failed connection disables it too

import os, pathlib, subprocess, re, shutil

net_key = r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings"
net_port = 8494

def winepath(path):
    return "Z:" + str(pathlib.PureWindowsPath(pathlib.Path(path)))

def wine(*cmd):
    pfx = pathlib.Path(os.environ["STEAM_COMPAT_DATA_PATH"]) / "pfx"
    binary = pathlib.Path(__file__).parents[0] / "files" / "bin" / "wine64"
    subprocess.run([binary, *cmd], env={**os.environ, "WINEPREFIX": str(pfx)})

def update(user_settings):
    no_net = os.environ.get("NO_NET", os.environ.get("BAKKES", "0")) == "1"
    pfx = pathlib.Path(os.environ["STEAM_COMPAT_DATA_PATH"]) / "pfx"
    reg_src = pfx / "no_net.reg"
    reg_bak = pfx / "no_net.reg.bak"
    reg_dump = pfx / "no_net.reg.log"
    wine("regedit", "/E", winepath(reg_dump), net_key)
    with open(reg_dump, encoding='utf-16') as fp:
        reg_str = fp.read()
    preset = bool(re.search(f'\n"ProxyServer"="[^:"]+://[^:"]+:{net_port}"', reg_str))
    if no_net and not preset:
        shutil.copy(reg_dump, reg_bak)
        wine("regedit", winepath(reg_src))
    elif not no_net and preset:
        wine("regedit", winepath(reg_bak))
    os.remove(reg_dump)

