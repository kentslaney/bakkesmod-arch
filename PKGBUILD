# Maintainer: Kent Slaney <kent@slaney.org>
pkgname=bakkesmod-legendary
rlver=( 2 0 54 )
pkgver="${rlver[0]}.${rlver[2]}"
pkgrel=4
pkgdesc="A mod aimed at making you better at Rocket League!"
arch=('x86_64')
url="https://bakkesmod.com/"
license=('GPL')
groups=()
depends=()
makedepends=('python' 'jq')
optdepends=()

# versionless URLs and official repo backups
# "https://github.com/bakkesmodorg/BakkesModInjectorCpp/releases/latest/download/BakkesModSetup.exe"
# "https://github.com/bakkesmodorg/BakkesModInjectorCpp/releases/latest/download/BakkesModInjectorWin7.zip"
# "https://github.com/bakkesmodorg/BakkesModInjectorCpp/releases/latest/download/BakkesMod.zip"
# "https://api.github.com/repos/bakkesmodorg/BakkesModInjectorCpp/zipball/master"

rlstr=$(IFS=. ; echo "${rlver[*]}")
rlesc=$(IFS=- ; echo "${rlver[*]}")
pkgesc=`echo "$pkgver" | sed 's%\.%-%g'`
pwsh_sum='05ea332209f52b796a78246a89757a291f254fb6'

source=(
    "dll-$rlesc.zip::https://github.com/bakkesmodorg/BakkesModInjectorCpp/releases/download/$rlstr/bakkesmod.zip"
    "src-$rlesc.zip::https://github.com/bakkesmodorg/BakkesModInjectorCpp/archive/refs/tags/$rlstr.zip"
    "loopback-$pkgesc-$pkgrel.zip::https://github.com/kentslaney/bakkesmod-arch/archive/refs/tags/$pkgver-$pkgrel-legendary.zip"
    "https://github.com/kentslaney/bakkesmod-arch/releases/download/c369f24-1/inject.exe"
    "pwshwrapper-${pwsh_sum:0:7}.zip::https://github.com/PietJankbal/powershell-wrapper-for-wine/archive/$pwsh_sum.zip"
)
sha256sums=(
    '725e86dbd275fd798d550536739a97a642a0b0979ed948f714a40f1980eb11c4'
    '7dbb2ec5b02d90745764561c508f74fa5d4e028fa7d8331a7102cff87490eaba'
    'SKIP'
    '0e038a4f0a2799f6aaa34f6560f5d1d41fba0cf26f8814571cebc94f5bb67a6e'
    '79ac12ff72dad9c0f79f5658fa4fed7c4d92476c6eea77427aa2bc84964fcf94'
)

build() {
    # folder with official injector release (commit hash in name)
    ref=`find "$srcdir" -maxdepth 1 -name "*Cpp-$rlstr" -type d`
    # move loopback src to srcdir
    tmp=$(mktemp -d)
    unzip -qd "$tmp" "$srcdir/loopback-$pkgesc-$pkgrel.zip"
    mv "$tmp"/*/* "$srcdir"
    rm -fr "$tmp"/* "$tmp"
}

compile() {
    # MinGW and VS header disagreement
    patches="$srcdir/include"
    mkdir -p "$patches"
    ln -sf /usr/x86_64-w64-mingw32/include/windows.h "$patches/Windows.h"
    ln -sf /usr/x86_64-w64-mingw32/include/sdkddkver.h "$patches/SDKDDKVer.h"
    ln -sf /usr/x86_64-w64-mingw32/include/shlobj.h "$patches/shlobj_core.h"
    ln -sf "$ref/BakkesModWPF/Resource.h" "$patches/resource.h"

    # has to be below C++20 which removes ofstream functionality
    CXX_FLAGS=( "-std=c++17" "-static-libgcc" "-static-libstdc++" "-static" "-municode" "-mconsole" "-lpsapi" "-w" )
    CXX_LD=( "-I$patches" "-I/usr/x86_64-w64-mingw32/include" "-I$ref/BakkesModInjectorC++" )

    # call injector with patched dll
    cat <<"    EOF" > "$srcdir/main.cpp"
        #include "DllInjector.h"
        #include <iostream>

        int wmain(int argc, wchar_t* argv[]) {
            std::wstring ps = L"RocketLeague.exe";
            const wchar_t* launcher = L"C:\\users\\steamuser\\AppData\\Roaming\\bakkesmod\\bakkesmod\\dll\\bakkesmod.dll";
            DllInjector dllInjector;
            bool launching = false;
            for (int i = 1; i < argc; i++) {
                auto arg = std::wstring(argv[i]);
                if (arg == L"launching") {
                    launching = true;
                }
            }
            if (launching) {
                std::cout << "Injector waiting for launch" << std::endl;
                while (dllInjector.GetProcessID64(ps) == 0) {
                    Sleep(1000);
                }
                std::cout << "Found PID, attempting injection" << std::endl;
            }
            dllInjector.InjectDLL(ps, launcher);
            return 0;
        }
    EOF

    # std::search is defined in std::algorithm
    includes="#include <algorithm>"
    sed "s%pragma once%pragma once\n$includes%" \
        "$ref/BakkesModInjectorC++/WindowsUtils.h" > "$patches/WindowsUtils.h"
    ln -sf "$patches/WindowsUtils.h" "$patches/windowsutils.h"

    # unused, faster and easier to short circuit
    getter="WindowsUtils::GetMyDocumentsFolder()"
    docs='C:\\\\users\\\\steamuser\\\\Documents'
    sed -z "s%$getter[^{]*{%$getter { return \"$docs\";%" \
        "$ref/BakkesModInjectorC++/WindowsUtils.cpp" > "$patches/WindowsUtils.cpp"

    wpath="s%std::filesystem::path path%const wchar_t* path%g"
    sed "s%path.wstring().c_str()%path%" \
        "$ref/BakkesModInjectorC++/DllInjector.cpp" > "$patches/DllInjector.cpp"
    sed -i "$wpath" "$patches/DllInjector.cpp"
    sed "$wpath" "$ref/BakkesModInjectorC++/DllInjector.h" > "$patches/DllInjector.h"
    x86_64-w64-mingw32-g++ "${CXX_FLAGS[@]}" "${CXX_LD[@]}" \
        "$patches/WindowsUtils.cpp" \
        "$ref/BakkesModWPF/BakkesModWPF.cpp" \
        "$patches/DllInjector.cpp" \
        "$srcdir/main.cpp" -o "$srcdir/inject.exe"
}

legendary_prefixes=(
    "$LEGENDARY_CONFIG_PATH"
    "$HOME/.config/legendary"
    "$HOME/.var/app/com.heroicgameslauncher.hgl/config/legendary"
    "$HOME/.config/heroic/legendaryConfig/legendary"
    "$HOME/.var/app/com.heroicgameslauncher.hgl/config/heroic/legendaryConfig/legendary"
)
heroic_prefixes=(
    "$HOME/.config/heroic/GamesConfig/Sugar.json"
    "$HOME/.var/app/com.heroicgameslauncher.hgl/config/heroic/GamesConfig/Sugar.json"
)
heroic_global=(
    "$HOME/.config/heroic/config.json"
    "$HOME/.var/app/com.heroicgameslauncher.hgl/config/heroic/config.json"
)
wine_bm_path="drive_c/users/steamuser/AppData/Roaming/bakkesmod"

installed_version() {
    jq -er .Sugar.version < "$1"
}

install_data() {
    for fp in "${legendary_prefixes[@]}"; do
        installed="$fp/installed.json"
        if [ -f "$installed" ] && ( installed_version "$installed" > /dev/null ); then
            echo "$installed"
            return 0
        fi
    done
    echo "could not find a LEGENDARY_CONFIG_PATH with Rocket League installed" >&2
    exit 1
}

wine_pfx() {
    pfx=`jq -er .Sugar.install_path < "$1"`
    echo "$(dirname "$pfx")/Prefixes/default/Rocket League"
}

heroic_env() {
    for fp in "${heroic_prefixes[@]}"; do
        if [ -f "$fp" ]; then
            echo "$fp"
            return 0
        fi
    done
}

heroic_config() {
    for fp in "${heroic_global[@]}"; do
        if [ -f "$fp" ]; then
            jq -er .defaultSettings.defaultSteamPath < "$fp"
            return 0
        fi
    done
}

build_version() {
    RL_version="$(installed_version "$1")"
    echo "$RL_version.$( cat "$srcdir/version.txt" ).$pkgver.$pkgrel"
}

powershell() {
    cp -rf powershell64.exe "$WINEPREFIX/drive_c/windows/system32/WindowsPowerShell/v1.0/powershell.exe"
    cp -rf powershell32.exe "$WINEPREFIX/drive_c/windows/syswow64/WindowsPowerShell/v1.0/powershell.exe"
    eval "$1 'C:\windows\system32\WindowsPowerShell\v1.0\powershell.exe' -noni -c 'echo \"powershell64_installed\"'"
    eval "$1 'C:\windows\syswow64\WindowsPowerShell\v1.0\powershell.exe' -noni -c 'echo \"powershell32_installed\"'"
}

package() {
    installed=`install_data`
    echo "build version string: $(build_version "$installed")"

    pfx=`wine_pfx "$installed"`
    pfx0="$pfx"
    if ! [ -a "$pfx/user.reg" ]; then pfx="$pfx/pfx"; fi # proton specific (?)
    user=`grep '^"USERNAME"="' "$pfx/user.reg" | sed "s/^[^=]*=\"\|\"$//g"`
    # creates broken (ignored) symlink if $user == "steamuser"
    ( cd "$pfx/drive_c/users" && ln -sf "$user" "steamuser" )

    bm_pfx="$pfx/$wine_bm_path"
    mkdir -p "$bm_pfx"
    py=$(sed "s/^ \{8\}//" <<"    EOF"
        import os, pathlib, sys
        f, pfx, env = (pathlib.Path(os.environ[i]) for i in ("FP", "PFX", "SUGAR_ENV"))

        # legendary launch command
        import configparser, shlex
        cfg = configparser.ConfigParser()
        cfg.read(f)
        if not cfg.has_section("Sugar"):
            cfg.add_section("Sugar")
        cmd = shlex.join(("sh", str(pfx / "runner.sh")))
        cfg["Sugar"]["pre_launch_command"] = cmd
        cfg["Sugar"]["pre_launch_wait"] = "true"
        with open(f, "w") as fp:
            cfg.write(fp)

        # heroic env variables
        import json
        if not env.is_file():
            print("wine")
            exit(0)
        with open(env) as fp:
            opt = json.load(fp)
        environ = opt.get("Sugar", {}).get("enviromentOptions", [])
        opt["Sugar"] = {**opt.get("Sugar", {}), "enviromentOptions": environ}
        preset = [i["key"] for i in environ]
        changed = False
        for var in ("BAKKES", "PROMPTLESS"):
            if var not in preset:
                changed = True
                environ.append({"key": var, "value": "1"})
            else:
                last = len(preset) - 1 - list(reversed(preset)).index(var)
                initial = environ[last]["value"]
                if initial != "1":
                    print(f"warning: Heroic flag {var} is set to {initial}", file=sys.stderr)
        if changed:
            with open(env, "w") as fp:
                json.dump(opt, fp, indent=2)
        try:
            cmd = [opt["Sugar"]["wineVersion"]["bin"]]
            if opt["Sugar"]["wineVersion"]["type"] == "proton":
                cmd.append("run")
            print(shlex.join(cmd))
        except:
            print("wine")
    EOF
    )
    cfg="$(dirname "$installed")/config.ini"
    wine_bin=`PFX="$bm_pfx" FP="$cfg" SUGAR_ENV="$(heroic_env)" python -c "$py"`

    sed "s/^ \{8\}//" <<"    EOF" > "$bm_pfx/runner.py"
        import argparse, os, shlex, pathlib

        with open("/proc/{}/cmdline".format(os.environ["PS"])) as fp:
            cmd = fp.read().rstrip("\x00").split("\x00")
        parser = argparse.ArgumentParser()
        parser.add_argument("--wine", action="append", default=[])
        parser.add_argument("--wrapper", default=[])
        flags, _ = parser.parse_known_args(cmd)
        flags.wrapper = flags.wrapper and shlex.split(flags.wrapper)
        pfx = pathlib.Path(__file__).parents[0]

        def wrap(wrapper):
            proton = os.environ.get("PROTONPATH", "")
            if len(flags.wrapper) < 2 or not proton:
                return wrapper
            relative = pathlib.Path(flags.wrapper[0]).relative_to(pathlib.Path(proton))
            if relative != pathlib.Path('proton'):
                return wrapper
            return [str(proton / pathlib.Path("files/bin/wine64"))]

        print(shlex.join(wrap(flags.wrapper) + flags.wine + [str(pfx / "inject.exe")]))
    EOF

    json_pfx=`jq -e .Sugar.install_path < "$installed"`
    echo "pfx=$json_pfx" > "$bm_pfx/runner.sh"
    cat <<"    EOF" >> "$bm_pfx/runner.sh"
        pfx="$(dirname "$pfx")/Prefixes/default/Rocket League"
        bm_pfx=`dirname "$0"`
        wine_bin=`PS="$PPID" python "$bm_pfx/runner.py"`
        if [ "$BAKKES" != 1 ]; then exit 0; fi
        dll=`[ "$PROMPTLESS" = 1 ] && echo "bakkesmod_promptless.dll" || echo "bakkesmod_official.dll"`
        ln -sf "$bm_pfx/bakkesmod/dll/$dll" "$bm_pfx/bakkesmod/dll/bakkesmod.dll"
        WINEFSYNC=1 WINEPREFIX="$pfx" eval "$wine_bin launching &"
    EOF

    dll_path="$bm_pfx/bakkesmod/dll"
    rm -f "$dll_path/bakkesmod.dll"
    unzip -quo "dll-$rlesc.zip" -d "$bm_pfx/bakkesmod"
    # by default, starts with bakkesmod.dll and outputs bakkesmod_promptless.dll
    echo -n "shunted winuser calls for DLL patch: "
    python "$srcdir/dll_patch.py" "$dll_path"
    mv "$dll_path/bakkesmod.dll" "$dll_path/bakkesmod_official.dll"
    ln -sf "$dll_path/bakkesmod_official.dll" "$dll_path/bakkesmod.dll"

    cp -f "$srcdir/inject.exe" "$bm_pfx"
    if [ -f "$pfx/drive_c/Program Files/PowerShell/7/pwsh.exe" ]; then
        echo "skipping powershell installation in favor of existing pwsh.exe"
    else
        # somewhere upstream has a non-checksumed file version
        #(
            cd "$srcdir/powershell-wrapper-for-wine-$pwsh_sum" &&
            LD_PRELOAD= WINEPREFIX="$pfx" STEAM_COMPAT_DATA_PATH="$pfx0" STEAM_COMPAT_CLIENT_INSTALL_PATH="$(heroic_config)" powershell "$wine_bin"
        #) 2> >(grep --color=NEVER mismatch >&2)
    fi
}

pre_remove() {
    installed=`install_data`
    pfx=`wine_pfx "$installed"`
    bm_pfx="$pfx/$wine_bm_path"

    py=$(sed "s/^ \{8\}//" <<"    EOF"
        import os, pathlib
        f, pfx, env = (pathlib.Path(os.environ[i]) for i in ("FP", "PFX", "SUGAR_ENV"))

        # legendary launch command
        import configparser, shlex
        cfg = configparser.ConfigParser()
        cfg.read(f)
        if cfg.has_section("Sugar"):
            cmd = shlex.join(("sh", str(pfx / "runner.sh")))
            if (
                    cfg["Sugar"].get("pre_launch_command").startswith(cmd) and
                    cfg["Sugar"].get("pre_launch_wait") == "true"):
                cfg.remove_option("Sugar", "pre_launch_command")
                cfg.remove_option("Sugar", "pre_launch_wait")
            if len(cfg.options("Sugar")) == 0:
                cfg.remove_section("Sugar")
            with open(f, "w") as fp:
                cfg.write(fp)

        # heroic env variables
        import json
        if env.is_file():
            with open(env) as fp:
                opt = json.load(fp)
            environ = opt["Sugar"]["enviromentOptions"]
            preset = [i["key"] for i in environ]
            changed = False
            for var in ("BAKKES", "PROMPTLESS"):
                if var in preset:
                    last = len(preset) - 1 - list(reversed(preset)).index(var)
                    if environ[last]["value"] == "1":
                        changed = True
                        environ.pop(last)
                        preset.pop(last)
            if changed:
                with open(env, "w") as fp:
                    json.dump(opt, fp, indent=2)
    EOF
    )
    cfg="$(dirname "$installed")/config.ini"
    PFX="$bm_pfx" FP="$cfg" SUGAR_ENV="$(heroic_env)" python -c "$py"

    rm -fr "$bm_pfx"
    linked="$pfx/drive_c/users/steamuser"
    if [ -h "$linked" ]; then rm "$linked"
    elif [ -d "$linked" ] && [ -h "$linked/steamuser" ]; then rm "$linked/steamuser"
    fi
}

