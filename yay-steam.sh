sudo steamos-readonly disable
sudo pacman-key --init
sudo pacman-key --populate archlinux holo
sudo pacman -S git base-devel
[ ! -d yay-bin ] && git clone https://aur.archlinux.org/yay-bin.git
cd yay-bin
git pull
makepkg -si
