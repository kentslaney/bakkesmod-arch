api="https://api.github.com/repos/bakkesmodorg/BakkesModInjectorCpp/releases/latest"
dll="https://github.com/bakkesmodorg/BakkesModInjectorCpp/releases/latest/download/BakkesMod.zip"
loopback="https://github.com/kentslaney/bakkesmod-arch.git"

cd `mktemp -d`
curl -LO "$api"
rlstr=`jq -r .tag_name latest`
src="https://github.com/bakkesmodorg/BakkesModInjectorCpp/archive/refs/tags/$rlstr.zip"

curl -LO "$dll"
curl -LO "$src"
git clone "$loopback"

rlver=`echo "$rlstr" | sed "s%\.% %g"`
pkgver=`echo "$rlstr" | sed "s%\..*\.%.%g"`
dll_sum=`sha256sum BakkesMod.zip | sed "s% *[^ ]*$%%"`
src_sum=`sha256sum "$rlstr.zip" | sed "s% *[^ ]*$%%"`

cd bakkesmod-arch
git checkout "${1:-master}"
git remote set-url origin git@github.com:kentslaney/bakkesmod-arch.git
eval `grep -Pzo "source=\([^)]*\)" PKGBUILD | xargs --null echo`
start=`grep -n "sha256sums=" PKGBUILD | cut -d':' -f1`
for i in $(seq 0 "${#source[@]}"); do
    if echo "${source[$i]}" | grep "^dll" > /dev/null; then
        dll_idx=$((start + i + 1))
    elif echo "${source[$i]}" | grep "^src" > /dev/null; then
        src_idx=$((start + i + 1))
    fi
done

sed -i "${dll_idx}s/\( *\)'[^']*'/\1'$dll_sum'/" PKGBUILD
sed -i "${src_idx}s/\( *\)'[^']*'/\1'$src_sum'/" PKGBUILD
sed -i "s/rlver=( .* )/rlver=( $rlver )/" PKGBUILD
sed -i "s/pkgrel=.*/pkgrel=1/" PKGBUILD
makepkg --printsrcinfo > .SRCINFO
pwd
echo "$pkgver"

