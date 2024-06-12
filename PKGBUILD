# Maintainer: Kent Slaney <kent@slaney.org>
pkgname=bakkesmod-steam
pkgver=2.40
pkgrel=6
pkgdesc="A mod aimed at making you better at Rocket League!"
arch=('x86_64')
url="https://bakkesmod.com/"
license=('GPL')
groups=()
depends=()
makedepends=('mingw-w64-binutils' 'mingw-w64-crt' 'mingw-w64-gcc' 'mingw-w64-headers' 'mingw-w64-winpthreads' 'python')
optdepends=()

# versionless URLs and official repo backups
# "https://github.com/bakkesmodorg/BakkesModInjectorCpp/releases/latest/download/BakkesModSetup.exe"
# "https://github.com/bakkesmodorg/BakkesModInjectorCpp/releases/latest/download/BakkesModInjectorWin7.zip"
# "https://github.com/bakkesmodorg/BakkesModInjectorCpp/releases/latest/download/BakkesMod.zip"
# "https://api.github.com/repos/bakkesmodorg/BakkesModInjectorCpp/zipball/master"

source=(
    "https://github.com/bakkesmodorg/BakkesModInjectorCpp/releases/download/2.0.40/bakkesmod.zip" # manually save dll
    "https://github.com/bakkesmodorg/BakkesModInjectorCpp/archive/refs/tags/2.0.40.zip" # manually build source
    "loopback::https://api.github.com/repos/kentslaney/bakkesmod-steam/zipball/master" # promptless injector
)
sha256sums=(
    'b117958fad739ae2ab8bbf76f25024141e72eeba880e45a0c30ae6a956489712'
    'dce175011c8df9bb5cfed576fd9efff8fdb2383d182fab99afde91d619aab4a4'
    'SKIP'
)

build() {
    # folder with official injector release (commit hash in name)
    ref=`find "$srcdir" -maxdepth 1 -name "*Cpp*" -type d`
    # move loopback src to srcdir
    find `find "$srcdir" -maxdepth 1 -name "*-steam*" -type d` -type f | xargs -I % mv -f % "$srcdir"

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
            DllInjector dllInjector;
            if (argc > 1 && std::wstring(argv[1]) == L"launching") {
                std::cout << "Injector waiting for launch" << std::endl;
                while (dllInjector.GetProcessID64(ps) == 0) {
                    Sleep(1000);
                }
                std::cout << "Found PID, attempting injection" << std::endl;
            }
            std::filesystem::path ws =
                "C:\\users\\steamuser\\AppData\\Roaming\\"
                "bakkesmod\\bakkesmod\\dll\\bakkesmod_promptless.dll";
            dllInjector.InjectDLL(ps, ws);
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

    # wstring memory issues
    ws='C:\\\\users\\\\steamuser\\\\Application Data\\\\bakkesmod\\\\bakkesmod/dll\\\\bakkesmod_promptless.dll';
    sed "s%path.wstring().c_str()%L\"$ws\"%" \
        "$ref/BakkesModInjectorC++/DllInjector.cpp" > "$patches/DllInjector.cpp"

    if [ -f "$srcdir/inject.exe" ]; then
        echo "reusing existing inject.exe"
    else
        x86_64-w64-mingw32-g++ "${CXX_FLAGS[@]}" "${CXX_LD[@]}" \
            "$patches/WindowsUtils.cpp" \
            "$ref/BakkesModWPF/BakkesModWPF.cpp" \
            "$patches/DllInjector.cpp" \
            "$srcdir/main.cpp" -o "$srcdir/inject.exe"
    fi

    # make bakkesmod folder to expand release into and output RL version
    cat <<"    EOF" > "$srcdir/status.cpp"
        #include "BakkesModInstallation.h"
        #include <iostream>

        int wmain(int argc, wchar_t* argv[]) {
            BakkesModInstallation installer;
            installer.CreateAppDataFolderIfDoesntExist();
            std::cout << installer.GetSteamVersion();
            return 0;
        }
    EOF

    if [ -f "$srcdir/status.exe" ]; then
        echo "reusing existing status.exe"
    else
        # too many finicky changes to patch robustly
        patch -p0 -N -d "$ref" < "$srcdir/installer.diff" || true
        # -luser32 for FOLDERID and -lole for CoTaskMemFree
        x86_64-w64-mingw32-g++ "${CXX_FLAGS[@]}" "${CXX_LD[@]}" \
            "$patches/WindowsUtils.cpp" \
            "$ref/BakkesModInjectorC++/SettingsManager.cpp" \
            "$ref/BakkesModInjectorC++/BakkesModInstallation.cpp" \
            -luser32 -lole32 "$srcdir/status.cpp" -o "$srcdir/status.exe"
    fi
}

package() {
    # 4th line of config_info contains the selected proton launcher's path
    paths=$(cat <<"    EOF"
        compat="$HOME/.steam/steam/steamapps/compatdata/252950"
        proton=`sed -n 4p "$compat/config_info" | xargs -d '\n' dirname`
        bm_pfx="$compat/pfx/drive_c/users/steamuser/AppData/Roaming/bakkesmod"
    EOF
    )
    # used in this function and for running resulting exe files
    eval "$paths"
    echo "$paths" > "$srcdir/runner.sh"

    # supposedly this might need to be ESYNC in some cases but this works by default
    cat <<"    EOF" >> "$srcdir/runner.sh"
        WINEFSYNC=1 WINEPREFIX="$compat/pfx/" "$proton/bin/wine64" "$@"
    EOF
    chmod a+x "$srcdir/runner.sh"
    RL_version=`"$srcdir/runner.sh" "$srcdir/status.exe" 2>/dev/null`
    echo "build version string: $RL_version-$( cat "$srcdir/version.txt" )-$pkgver-$pkgrel"

    # expand and patch dll (capitalization changes between latest and explicit version)
    compressed=`find "$srcdir" -name "[bB]akkes[Mm]od.zip"`
    unzip -oq "$compressed" -d "$bm_pfx/bakkesmod"
    # by default, starts with bakkesmod.dll and outputs bakkesmod_promptless.dll
    #echo -n "shunted file addresses for DLL patch: "
    python "$srcdir/dll_patch.py" "$bm_pfx/bakkesmod/dll" > /dev/null

    cp -f "$srcdir/inject.exe" "$srcdir/status.exe" "$bm_pfx"
    cp -f "$srcdir/runner.sh" "$srcdir/dll_patch.py" "$bm_pfx"

    #echo "direct injection command:" "$bm_pfx/runner.sh $bm_pfx/inject.exe"

    cp -f "$srcdir/settings_252950_bakkes.py" "$proton/.."
    loader="$srcdir/bakkesmod-steam-user-settings.py"
    conf="$proton/../user_settings.py"
    sig=`sha256sum "$loader" | sed "s% *[^ ]*$%%"`
    if ! grep "$sig" "$conf" > /dev/null; then
        echo "### $sig $( basename "$loader" )" >> "$conf"
        cat "$srcdir/bakkesmod-steam-user-settings.py" >> "$conf"
        echo "### $sig EOF" >> "$conf"
    fi
    echo "to finish install, set BAKKES=1 in your launch options, or \"BAKKES=1 %command%\" if you don't have any yet"
    echo "the launch option is tied to the proton installation, so you will need to reinstall if you switch versions"
}
# unrelated: I recommend the -NoKeyboardUI option for desktop big picture mode; thanks for reading!

