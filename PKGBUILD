# Maintainer: Kent Slaney <kent@slaney.org>
pkgname=bakkesmod-steam
pkgver=2.40
pkgrel=1
pkgdesc="A mod aimed at making you better at Rocket League!"
arch=('x86_64')
url="https://bakkesmod.com/"
license=('GPL')
groups=('mingw-w64')
depends=()
makedepends=()
optdepends=()
source=(
    "https://github.com/bakkesmodorg/BakkesModInjectorCpp/releases/latest/download/BakkesModSetup.exe"
    "https://github.com/bakkesmodorg/BakkesModInjectorCpp/releases/latest/download/BakkesModInjectorWin7.zip"
    "https://api.github.com/repos/bakkesmodorg/BakkesModInjectorCpp/zipball/master"
)
sha256sums=('SKIP' 'SKIP' 'SKIP')
build() {
    ref="$srcdir/$( ls | grep org )"
    patches="$srcdir/include"
    mkdir -p "$patches"
    ln -sf /usr/x86_64-w64-mingw32/include/windows.h "$patches/Windows.h"
    ln -sf /usr/x86_64-w64-mingw32/include/sdkddkver.h "$patches/SDKDDKVer.h"
    ln -sf "$ref/BakkesModWPF/Resource.h" "$patches/resource.h"
    CXX_FLAGS=( "-std=c++20" "-static-libgcc" "-static-libstdc++" "-static" "-municode" )
    CXX_version=`ls /usr/lib/gcc/x86_64-w64-mingw32/ | sort --version-sort | tail -1`
    CXX_LD=(
        "-I$patches"
        "-I/usr/lib/gcc/x86_64-w64-mingw32/$CXX_version"
        "-I/usr/x86_64-w64-mingw32/include"
        "-I/usr/x86_64-w64-mingw32/lib"
        "-I$ref/BakkesModInjectorC++"
    )

    cat <<"    EOF" > "$srcdir/main.cpp"
        #include "DllInjector.h"

        int wmain(int argc, wchar_t* argv[]) {
            DllInjector dllInjector;
            std::wstring ps = L"RocketLeague.exe";
            std::filesystem::path ws =
                "C:\\users\\steamuser\\Application Data\\bakkesmod\\bakkesmod\\dll\\bakkesmod.dll";
            dllInjector.InjectDLL(ps, ws);
            return 0;
        }
    EOF

    includes="#include <algorithm>"
    getter="WindowsUtils::GetMyDocumentsFolder()"
    docs='C:\\\\users\\\\steamuser\\\\Documents'
    sed "s@pragma once@pragma once\n$includes@" \
        "$ref/BakkesModInjectorC++/WindowsUtils.h" > "$patches/WindowsUtils.h"
    sed -z "s@$getter[^{]*{@$getter { return \"$docs\";@" \
        "$ref/BakkesModInjectorC++/WindowsUtils.cpp" > "$patches/WindowsUtils.cpp"

    if [ -f "$srcdir/inject.exe" ]; then
        echo "reusing existing inject.exe"
    else
        x86_64-w64-mingw32-c++ "${CXX_FLAGS[@]}" "${CXX_LD[@]}" \
            "$patches/WindowsUtils.cpp" \
            "$ref/BakkesModWPF/BakkesModWPF.cpp" \
            "$ref/BakkesModInjectorC++/DllInjector.cpp" \
            "$srcdir/main.cpp" -o "$srcdir/inject.exe"
    fi

    chmod a+x "$srcdir/BakkesMod.exe"
}

package() {
    paths=$(cat <<"    EOF"
        compat="$HOME/.steam/steam/steamapps/compatdata/252950"
        proton=`sed -n 4p "$compat/config_info" | xargs -d '\n' dirname`
        bm_pfx="$compat/pfx/drive_c/users/steamuser/AppData/Roaming/bakkesmod"
    EOF
    )
    eval "$paths"

    if [ -d "$bm_pfx" ]; then
        echo "$bm_pfx already exists; skipping BakkesModSetup.exe"
    else
        WINEPREFIX="$compat/pfx/" "$proton/bin/wine64" "$srcdir/BakkesModSetup.exe"
    fi

    cp -f "$srcdir/BakkesMod.exe" "$srcdir/inject.exe" "$bm_pfx"
    echo "$paths" > "$bm_pfx/runner.sh"
    chmod a+x "$bm_pfx/runner.sh"
    cat <<"    EOF" >> "$bm_pfx/runner.sh"
        WINEFSYNC=1 WINEPREFIX="$compat/pfx/" "$proton/bin/wine64" "$@"
    EOF
    echo "run BakkesMod executable:" "$bm_pfx/runner.sh $bm_pfx/BakkesMod.exe"
    echo "direct injection command:" "$bm_pfx/runner.sh $bm_pfx/inject.exe"
    # echo "$bm_pfx/runner.sh $bm_pfx/BakkesMod.exe" > "$bm_pfx/launch.sh"
    # setup=`find "$HOME/.steam/steam/userdata" -name "localconfig.vdf"`
    # setup=`grep 252950 -A 10 "$setup" | grep LaunchOptions | sed 's@^\([^"]*"\)\{3\}@@'`
    # echo "set launch options to: \"$bm_pfx/launch.sh & $setup"
    # I recommend the -NoKeyboardUI option
}

