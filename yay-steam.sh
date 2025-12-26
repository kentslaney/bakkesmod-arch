sudo steamos-readonly disable
sudo pacman-key --init
sudo pacman-key --populate archlinux holo
sudo pacman --noconfirm -S git base-devel
[ ! -d yay-bin ] && git clone https://aur.archlinux.org/yay-bin.git
cd yay-bin
git pull
makepkg --noconfirm -si

# https://github.com/Jguer/yay/issues/2508#issuecomment-3657461690
linked_so='/lib/'`ldd "$(which yay)" | grep -o 'libalpm.\S* ' | head -1`
existing_so='/lib/libalpm.so'
[ ! -e "$linked_so" ] && [ -f "$existing_so" ] && sudo ln -s "$existing_so" "$linked_so"
