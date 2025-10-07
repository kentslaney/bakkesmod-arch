cd "$(dirname "$0")"

steam=`sh update.sh`
legendary=`sh update.sh legendary`

tmp_steam=`echo "$steam" | tail -2 | head -1`
ver_steam=`echo "$steam" | tail -1`

tmp_legendary=`echo "$legendary" | tail -2 | head -1`
ver_legendary=`echo "$legendary" | tail -1`

cd "$tmp_steam"
git commit -am "$ver_steam"
git tag "$ver_steam-steam"
git remote add downstream ssh://aur@aur.archlinux.org/bakkesmod-steam.git

echo ""
echo "steam: $tmp_steam"
git --no-pager diff HEAD~1
git log --decorate | head
git remote -v
echo ""

cd "$tmp_legendary"
git commit -am "$ver_legendary"
git tag "$ver_legendary-legendary"
git remote add downstream ssh://aur@aur.archlinux.org/bakkesmod-legendary.git

echo ""
echo "legendary: $tmp_legendary"
git --no-pager diff HEAD~1
git log --decorate | head
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

