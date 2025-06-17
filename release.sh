cd "$(dirname "$0")"

steam=`sh update.sh`
legendary=`sh update.sh legendary`

tmp_steam=`echo "$steam" | tail -2 | head -1`
ver_steam=`echo "$steam" | tail -1`

tmp_legendary=`echo "$legendary" | tail -2 | head -1`
ver_legendary=`echo "$legendary" | tail -1`

cd "$tmp_steam"
git commit -Am "$ver_steam"
git tag "$ver_steam-1-steam"
git remote set-url downstream ssh://aur@aur.archlinux.org/bakkesmod-steam.git

echo ""
echo "steam: $tmp_steam"
git diff HEAD~1
git log | head
git remote -v
echo ""

cd "$tmp_legendary"
git commit -Am "$ver_legendary"
git tag "$ver_legendary-1-legendary"
git remote set-url downstream ssh://aur@aur.archlinux.org/bakkesmod-legendary.git

echo ""
echo "legendary: $tmp_legendary"
git diff HEAD~1
git log | head
git remote -v
echo ""

printf 'Ok to push? [Yn] '
read answer

if [ "$answer" != "${answer#[Nn]}" ] ;then
    exit 1
fi

cd "$tmp_steam"
git push
git push --tags
git push downstream

cd "$tmp_legendary"
git push
git push --tags
git push downstream legendary:master

