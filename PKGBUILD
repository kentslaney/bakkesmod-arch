# Maintainer: Kent Slaney <kent@slaney.org>
pkgname=bakkesmod-steam
rlver=( 2 0 63 )
pkgver="${rlver[0]}.${rlver[2]}"
pkgrel=1
pkgdesc="A mod aimed at making you better at Rocket League!"
arch=('x86_64')
url="https://bakkesmod.com/"
license=('GPL')
groups=()
depends=()
makedepends=('python')
optdepends=()

# versionless URLs and official repo backups
# "https://github.com/bakkesmodorg/BakkesModInjectorCpp/releases/latest/download/BakkesModSetup.exe"
# "https://github.com/bakkesmodorg/BakkesModInjectorCpp/releases/latest/download/BakkesModInjectorWin7.zip"
# "https://github.com/bakkesmodorg/BakkesModInjectorCpp/releases/latest/download/BakkesMod.zip"
# "https://api.github.com/repos/bakkesmodorg/BakkesModInjectorCpp/zipball/master"

rlstr=$(IFS=. ; echo "${rlver[*]}")
rlesc=$(IFS=- ; echo "${rlver[*]}")
pkgesc=`echo "$pkgver" | sed 's%\.%-%g'`

source=(
    "dll-$rlesc.zip::https://github.com/bakkesmodorg/BakkesModInjectorCpp/releases/download/$rlstr/bakkesmod.zip"
    "src-$rlesc.zip::https://github.com/bakkesmodorg/BakkesModInjectorCpp/archive/refs/tags/$rlstr.zip"
    "loopback-$pkgesc-$pkgrel.zip::https://github.com/kentslaney/bakkesmod-arch/archive/refs/tags/$pkgver-$pkgrel-steam.zip"
    "https://github.com/kentslaney/bakkesmod-arch/releases/download/c369f24-1/inject.exe"

    "https://github.com/kentslaney/bakkesmod-arch/releases/download/05ea332-1/powershell32.exe"
    "https://github.com/kentslaney/bakkesmod-arch/releases/download/05ea332-1/powershell64.exe"
    "https://github.com/PowerShell/PowerShell/releases/download/v7.4.1/PowerShell-7.4.1-win-x64.msi"
    "https://github.com/Maximus5/ConEmu/releases/download/v23.07.24/ConEmuPack.230724.7z"
    "https://www.7-zip.org/a/7z2501-x64.exe"
    "https://raw.githubusercontent.com/PietJankbal/powershell-wrapper-for-wine/master/profile.ps1"
)

sha256sums=(
    '6e14e7d09061569ad1f7c6003798ba0aabda26223d92f0ddfb5b637ef1eeddc0'
    '9d591139b20a5c4f2c8e38c92efc72b9a84d89f930d0c71a7e7c733b53e4d27f'
    'SKIP'
    '0e038a4f0a2799f6aaa34f6560f5d1d41fba0cf26f8814571cebc94f5bb67a6e'

    '196886b557e632547d32354f20834e88ba3726df29a486c85d6409900064f364'
    'e8dae4079a66d5a1564c577bd27caf8c890a1044d9c56948581591e196e4ac8c'
    '66c7c35ed9a46bd27e3d915dcf9a05e38b3f5ebb039883b92aa62ffea20fb187'
    '2a9b98ebecaede62665ef427b05b3a5ccdac7bd3202414fc0f4c10825b4f4ea2'
    '78afa2a1c773caf3cf7edf62f857d2a8a5da55fb0fff5da416074c0d28b2b55f'
    'b0fd5df54a2b281348ab03c2942b1e83278bee62c71e06d3d671724b49946593'
)

build() {
    # folder with official injector release (commit hash in name)
    ref=`find "$srcdir" -maxdepth 1 -name "*Cpp-$rlstr" -type d`
    # move loopback src to srcdir
    tmp=$(mktemp -d)
    unzip -qd "$tmp" "$srcdir/loopback-$pkgesc-$pkgrel.zip"
    mv "$tmp"/*/* "$srcdir"
    rm -fr "$tmp"/* "$tmp"
    rm -rf "$srcdir/7zr.exe" && cp "$srcdir"/7z*-x64.exe "$srcdir/7zr.exe"
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

# 3rd line of config_info contains the selected proton launcher's path
# https://github.com/ValveSoftware/Proton/blob/3a269ab9966409b968c8bc8f3e68bd0d2f42aadf/proton#L996-L1009
proton_paths=$(cat <<'EOF'
    steamapps="$HOME/.steam/steam/steamapps"
    compat="$steamapps/compatdata/252950"
    if [ ! -f "$steamapps/compatdata/252950/config_info" ]; then
        echo "could not find steam's proton config for Rocket League" >&2
        echo "if on SteamOS, re-run from the deck account" >&2
        exit 1
    fi
    proton=`sed -n 3p "$compat/config_info" | xargs -d '\n' dirname`
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

powershell_installer() {
    "$1" 'C:\windows\system32\WindowsPowerShell\v1.0\powershell.exe' -noni -c 'echo "powershell64_installed"'
    "$1" 'C:\windows\syswow64\WindowsPowerShell\v1.0\powershell.exe' -noni -c 'echo "powershell32_installed"'
}

powershell() {
    rm -f fsync
    python sandbox.py > fsync &
    sandbox_pid=$!
    trap "if kill -0 '$sandbox_pid' &> /dev/null; then kill '$sandbox_pid'; fi" EXIT
    echo -n "waiting for sandbox port "
    tail -f fsync | grep -m 1 "."

    pth32="$WINEPREFIX/drive_c/windows/system32/WindowsPowerShell/v1.0/powershell.exe"
    pth64="$WINEPREFIX/drive_c/windows/syswow64/WindowsPowerShell/v1.0/powershell.exe"

    cp -f powershell32_.exe "$pth32"; cp -f powershell64_.exe "$pth64";
    ( powershell_installer "$1" 2>pwsh.log ) || ( cat pwsh.log && false )
    cp -f powershell32.exe "$pth32"; cp -f powershell64.exe "$pth64";
    if kill -0 "$sandbox_pid" &> /dev/null; then kill "$sandbox_pid"; fi
    rm -f fsync
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

    dll_path="$bm_pfx/bakkesmod/dll"
    rm -f "$dll_path/bakkesmod.dll"
    unzip -quo "dll-$rlesc.zip" -d "$bm_pfx/bakkesmod"
    # by default, starts with bakkesmod.dll and outputs bakkesmod_promptless.dll
    echo -n "shunted winuser calls for DLL patch: "
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
    if [ -f "$compat/pfx/drive_c/Program Files/PowerShell/7/pwsh.exe" ]; then
        echo "skipping powershell installation in favor of existing pwsh.exe"
    else
        ( cd "$srcdir" && WINEPREFIX="$compat/pfx/" powershell "$proton/bin/wine64" )
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
