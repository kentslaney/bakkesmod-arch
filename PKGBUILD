# Maintainer: Kent Slaney <kent@slaney.org>
pkgname=bakkesmod-steam
pkgver=2.43
pkgrel=4
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

rlver=( 2 0 43 )
rlstr=$(IFS=. ; echo "${rlver[*]}")
rlesc=$(IFS=- ; echo "${rlver[*]}")
pkgesc=`echo "$pkgver" | sed 's%\.%-%g'`

source=(
    "dll-$rlesc.zip::https://github.com/bakkesmodorg/BakkesModInjectorCpp/releases/download/$rlstr/bakkesmod.zip"
    "src-$rlesc.zip::https://github.com/bakkesmodorg/BakkesModInjectorCpp/archive/refs/tags/$rlstr.zip"
    "loopback-$pkgesc-$pkgrel.zip::https://github.com/kentslaney/bakkesmod-arch/archive/refs/tags/$pkgver-$pkgrel-steam.zip"
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

# 4th line of config_info contains the selected proton launcher's path
proton_paths=$(cat <<'EOF'
    steamapps="$HOME/.steam/steam/steamapps"
    compat="$steamapps/compatdata/252950"
    if [ ! -f "$steamapps/compatdata/252950/config_info" ]; then
        echo "could not find steam's proton config for Rocket League" >&2
        exit 1
    fi
    proton=`sed -n 4p "$compat/config_info" | xargs -d '\n' dirname`
    bm_pfx="$compat/pfx/drive_c/users/steamuser/AppData/Roaming/bakkesmod"
EOF
)

remove_between() {
    echo -e "$(head -n "$(( $1 - 1 ))" "$3")\n$(tail -n +"$(( $2 + 1 ))" "$3")"
}

insert_lines_before() { # 1 indexed line numbers like grep
    echo -e "$(head -n "$(( $1 - 1 ))" "$3")\n$( cat "$2" )\n$(tail -n +"$(( $1 ))" "$3")"
}

build_version() {
    RL_version=`grep buildid "$1/appmanifest_252950.acf" | sed 's%[^0-9]%%g'`
    echo "$RL_version.$( cat "$srcdir/version.txt" ).$pkgver.$pkgrel"
}

package() {
    # used in this function and for running resulting exe files
    eval "$proton_paths"
    echo "build version string: $(build_version "$steamapps")"

    echo "$proton_paths" > "$srcdir/runner.sh"
    # supposedly this might need to be ESYNC in some cases but this works by default
    cat <<"    EOF" >> "$srcdir/runner.sh"
        dll=`[ "$PROMPTLESS" = 1 ] && echo "bakkesmod_promptless.dll" || echo "bakkesmod_official.dll"`
        ln -sf "$bm_pfx/bakkesmod/dll/$dll" "$bm_pfx/bakkesmod/dll/bakkesmod.dll"
        WINEFSYNC=1 WINEPREFIX="$compat/pfx/" "$proton/bin/wine64" "$@"
    EOF
    chmod a+x "$srcdir/runner.sh"
    mkdir -p "$bm_pfx"

    unzip -quo "dll-$rlesc.zip" -d "$bm_pfx/bakkesmod"
    # by default, starts with bakkesmod.dll and outputs bakkesmod_promptless.dll
    echo -n "shunted winuser calls for DLL patch: "
    dll_path="$bm_pfx/bakkesmod/dll"
    python "$srcdir/dll_patch.py" "$dll_path"
    mv "$dll_path/bakkesmod.dll" "$dll_path/bakkesmod_official.dll"
    ln -sf "$dll_path/bakkesmod_official.dll" "$dll_path/bakkesmod.dll"

    cp -f "$srcdir/inject.exe" "$bm_pfx"
    cp -f "$srcdir/runner.sh" "$srcdir/dll_patch.py" "$bm_pfx"

    echo "direct injection command:" "'$bm_pfx/runner.sh' '$bm_pfx/inject.exe'"

    cp -f "$srcdir/settings_252950_bakkes.py" "$proton/.."
    loader="$srcdir/bakkesmod-steam-user-settings.py"
    conf="$proton/../user_settings.py"
    sig=`sha256sum "$loader" | sed "s% *[^ ]*$%%"`
    touch "$conf"
    settings_version() {
        grep "^### \+$1 \+[0-9a-fA-F]\{64\}\( \|$\)" "$loader" | \
            sed 's%^\([^ ]\+ \+\)\{2\}\([^ ]\+\).*%\2%' | \
            xargs -I % grep -n '^### \+%' "$conf" || true
    }
    if [ ! -z "$( settings_version overlaps )" ]; then
        echo "found overlapping user_settings.py setup, aborting" >&2
        exit 1
    fi
    delimited="$srcdir/user_settings.py"
    echo "### $sig $( basename "$loader" )" > "$delimited"
    cat "$srcdir/bakkesmod-steam-user-settings.py" >> "$delimited"
    echo "### $sig EOF" >> "$delimited"
    updates=`settings_version replaces`
    if [ ! -z "${updates}" ]; then
        for (( pair=`echo "$updates" | wc -l`; pair>0; pair-=2 )); do
            start=`head -n "$(( pair - 1 ))" - <<< "$updates" | tail -1`
            end=`head -n "$(( pair ))" - <<< "$updates" | tail -1`
            if ! grep "EOF$" - <<< "$end" > /dev/null || grep "EOF$" - <<< "$start" > /dev/null; then
                echo "mismatched checksum delimitors" >&2
                exit 1
            fi
            start=`echo "$start" | cut -f1 -d:`
            end=`echo "$end" | cut -f1 -d:`
            remove_between "$start" "$end" "$conf" > "$conf"
        done
        ins=`echo "$updates" | head -1 | cut -f1 -d:`
        insert_lines_before "$ins" "$delimited" "$conf" > "$conf"
    elif ! grep "### \+$sig" "$conf" > /dev/null; then
        cp "$delimited" "$conf"
    fi
    echo "to finish installing, update your launch options by prepending \"BAKKES=1\" or by setting them to \"BAKKES=1 %command%\" if none have been set yet"
    echo "to inject the bakkesmod DLL without the message box about version verification, also prepend \"PROMPTLESS=1\""
    echo "the launch option is tied to the proton installation, so you will need to reinstall if you switch versions"
}

pre_remove() {
    if ! ( eval "$proton_paths" ); then return 0; fi
    eval "$proton_paths"
    rm -f "$proton/../settings_252950_bakkes.py"
    if ! ls "$proton/.." | grep "^settings_[0-9]\+\(_\|.py$\)" > /dev/null; then
        loader="$srcdir/bakkesmod-steam-user-settings.py"
        conf="$proton/../user_settings.py"
        sig=`sha256sum "$loader" | sed "s% *[^ ]*$%%"`
        echo "$loader $conf $sig"
        if start=`grep -n "^### $sig $( basename "$loader" )$" "$conf"`; then
            start=`echo "$start" | cut -d: -f1`
            end=`grep -n "^### $sig EOF$" "$conf" | cut -d: -f1`
            # only remove one
            start=`echo "$start" | head -1`
            end=`echo "$end" | awk "\$0 > $start" | head -1`
            remove_between "$start" "$end" "$conf" > "$conf"
        fi
        if [[ -z `cat "$conf" | tr -d "\n"` ]]; then rm "$conf"; fi
    fi
    rm -fr "$bm_pfx"
}

# unrelated: I recommend the -NoKeyboardUI option for desktop big picture mode
