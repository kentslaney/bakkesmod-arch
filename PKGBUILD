# Maintainer: Kent Slaney <kent@slaney.org>
pkgname=bakkesmod-legendary
pkgver=2.43
pkgrel=2
pkgdesc="A mod aimed at making you better at Rocket League!"
arch=('x86_64')
url="https://bakkesmod.com/"
license=('GPL')
groups=()
depends=()
makedepends=('mingw-w64-binutils' 'mingw-w64-crt' 'mingw-w64-gcc' 'mingw-w64-headers' 'mingw-w64-winpthreads' 'python' 'jq')
optdepends=()

# versionless URLs and official repo backups
# "https://github.com/bakkesmodorg/BakkesModInjectorCpp/releases/latest/download/BakkesModSetup.exe"
# "https://github.com/bakkesmodorg/BakkesModInjectorCpp/releases/latest/download/BakkesModInjectorWin7.zip"
# "https://github.com/bakkesmodorg/BakkesModInjectorCpp/releases/latest/download/BakkesMod.zip"
# "https://api.github.com/repos/bakkesmodorg/BakkesModInjectorCpp/zipball/master"

rlver=( 2 0 43 )
rlstr=$(IFS=. ; echo "${rlver[*]}")
rlesc=$(IFS=- ; echo "${rlver[*]}")
pkgesc=`echo "$pkgver" | sed 's%\.%-%g'`

source=(
    "dll-$rlesc.zip::https://github.com/bakkesmodorg/BakkesModInjectorCpp/releases/download/$rlstr/bakkesmod.zip"
    "src-$rlesc.zip::https://github.com/bakkesmodorg/BakkesModInjectorCpp/archive/refs/tags/$rlstr.zip"
    "loopback-$pkgesc-$pkgrel.zip::https://github.com/kentslaney/bakkesmod-steam/archive/refs/tags/$pkgver-$pkgrel.zip"
)
sha256sums=(
    '3d39b07149872d891659330185ef9c4e02c580bfad67ed2df9979dbd72d4ae61'
    '2d9cb1534fbae77ba008b07be3291d30e98a872ebfb0f0b3e6bb0c638d98bef8'
    'SKIP'
)

build() {
    # folder with official injector release (commit hash in name)
    ref=`find "$srcdir" -maxdepth 1 -name "*Cpp-$rlstr" -type d`
    # move loopback src to srcdir
    tmp=$(mktemp -d)
    unzip -qd "$tmp" "$srcdir/loopback-$pkgesc-$pkgrel.zip"
    mv "$tmp"/*/* "$srcdir"
    rm -fr "$tmp"/* "$tmp"

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
            auto official = L"C:\\users\\steamuser\\AppData\\Roaming\\bakkesmod\\bakkesmod\\dll\\bakkesmod.dll";
            auto promptless = L"C:\\users\\steamuser\\AppData\\Roaming\\bakkesmod\\bakkesmod\\dll\\bakkesmod_promptless.dll";
            const wchar_t* launcher = official;
            DllInjector dllInjector;
            bool launching = false;
            for (int i = 1; i < argc; i++) {
                auto arg = std::wstring(argv[i]);
                if (arg == L"launching") {
                    launching = true;
                } else if (arg == L"promptless") {
                    launcher = promptless;
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
wine_bm_path="drive_c/users/steamuser/AppData/Roaming/bakkesmod"

installed_version() {
    jq -er .Sugar.version < "$1"
}

install_data() {
    local RL_version=""
    for fp in "${legendary_prefixes[@]}"; do
        installed="$fp/installed.json"
        if [ -f "$installed" ] && RL_version=`installed_version "$installed"`; then
            break
        fi
    done
    if (( "$RL_version" == "null" )); then
        echo "could not find a LEGENDARY_CONFIG_PATH with Rocket League installed" >&2
        exit 1
    fi
    echo "$installed"
}

wine_pfx() {
    pfx=`jq -er .Sugar.install_path < "$1"`
    echo "$(dirname "$pfx")/Prefixes/default/Rocket League"
}

package() {
    installed=`install_data`
    echo "build version string: $(installed_version "$installed")"

    pfx=`wine_pfx "$installed"`
    user=`grep '^"USERNAME"="' "$pfx/user.reg" | sed "s/^[^=]*=\"\|\"$//g"`
    # creates broken (ignored) symlink if $user == "steamuser"
    ( cd "$pfx/drive_c/users" && ln -sf "$user" "steamuser" )

    bm_pfx="$pfx/$wine_bm_path"
    mkdir -p "$bm_pfx"
    py=$(sed "s/^ \{8\}//" <<"    EOF"
        import os, configparser, pathlib, shlex
        f, pfx = (pathlib.Path(os.environ[i]) for i in ("FP", "PFX"))
        cfg = configparser.ConfigParser()
        cfg.read(f)
        if not cfg.has_section("Sugar"):
            cfg.add_section("Sugar")
        cmd = shlex.join(("sh", str(pfx / "runner.sh"), "promptless"))
        cfg["Sugar"]["pre_launch_command"] = cmd
        cfg["Sugar"]["pre_launch_wait"] = "true"
        with open(f, "w") as fp:
            cfg.write(fp)
    EOF
    )
    PFX="$bm_pfx" FP="$(dirname "$installed")/config.ini" python -c "$py"

    sed "s/^ \{8\}//" <<"    EOF" > "$bm_pfx/runner.py"
        import argparse, os

        with open("/proc/{}/cmdline".format(os.environ["PS"])) as fp:
            cmd = fp.read().rstrip("\x00").split("\x00")
        parser = argparse.ArgumentParser()
        parser.add_argument("--wine")
        print(parser.parse_known_args(cmd)[0].wine)
    EOF

    json_pfx=`jq -e .Sugar.install_path < "$installed"`
    echo "pfx=$json_pfx" > "$bm_pfx/runner.sh"
    cat <<"    EOF" >> "$bm_pfx/runner.sh"
        pfx="$(dirname "$pfx")/Prefixes/default/Rocket League"
        bm_pfx=`dirname "$0"`
        wine_bin=`PS="$PPID" python "$bm_pfx/runner.py"`
        WINEFSYNC=1 WINEPREFIX="$pfx" "$wine_bin" "$bm_pfx/inject.exe" launching "$@" &
    EOF

    unzip -quo "dll-$rlesc.zip" -d "$bm_pfx/bakkesmod"
    # by default, starts with bakkesmod.dll and outputs bakkesmod_promptless.dll
    echo -n "shunted winuser calls for DLL patch: "
    python "$srcdir/dll_patch.py" "$bm_pfx/bakkesmod/dll"

    cp -f "$srcdir/inject.exe" "$bm_pfx"
}

pre_remove() {
    installed=`install_data`
    pfx=`wine_pfx "$installed"`
    bm_pfx="$pfx/$wine_bm_path"

    py=$(sed "s/^ \{8\}//" <<"    EOF"
        import os, configparser, pathlib, shlex
        f, pfx = (pathlib.Path(os.environ[i]) for i in ("FP", "PFX"))
        cfg = configparser.ConfigParser()
        cfg.read(f)
        if not cfg.has_section("Sugar"):
            exit(0)
        cmd = shlex.join(("sh", str(pfx / "runner.sh"), "promptless"))
        if (
                cfg["Sugar"].get("pre_launch_command") == cmd and
                cfg["Sugar"].get("pre_launch_wait") == "true"):
            cfg.remove_option("Sugar", "pre_launch_command")
            cfg.remove_option("Sugar", "pre_launch_wait")
        if len(cfg.options("Sugar")) == 0:
            cfg.remove_section("Sugar")
        with open(str(f), "w") as fp:
            cfg.write(fp)
    EOF
    )
    PFX="$bm_pfx" FP="$(dirname "$installed")/config.ini" python -c "$py"
    return 0

    rm -fr "$bm_pfx"
    linked="$pfx/drive_c/users/steamuser"
    if [ -h "$linked" ]; then rm "$linked"
    elif [ -d "$linked" ] && [ -h "$linked/steamuser" ]; then rm "$linked/steamuser"
    fi
}

