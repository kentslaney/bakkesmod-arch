# BakkesMod for (Arch) Linux and Steam Deck
> [!WARNING]
> EGS support is currently broken. Tracked in [issue #5](https://github.com/kentslaney/bakkesmod-arch/issues/5).

TL;DR: [AUR for steam](https://aur.archlinux.org/packages/bakkesmod-steam), [AUR for Heroic/Legendary](https://aur.archlinux.org/packages/bakkesmod-legendary)
## Supported Environments
There are two versions of the Rocket League: Steam and Epic Games Store (EGS). The EGS version is the only one available going forwards and support for that version is primarily built around the [Heroic Launcher](https://heroicgameslauncher.com/) ([GitHub](https://github.com/Heroic-Games-Launcher)). Heroic Launcher supports EGS games through a CLI tool called [Legendary](https://github.com/derrod/legendary) (which is why the AUR is called `bakkesmod-legendary`), but Heroic Launcher's settings will be updated as well if it's installed.

This guide is built for Arch or its derivative SteamOS, which runs on the Steam Deck. SteamOS requires some additional steps to enable modifying the game files, which will be covered below. If you already have an Arch Linux setup with `yay`, you can skip to the [Platforms Section](#platforms). This repo currently relies on Arch Linux's `makepkg`, but most of the installation logic is portable, so it's possible that other distros will be added in the future. In the meantime, you can find cross-platform instructions at [CrumblyLiquid/BakkesLinux](https://github.com/CrumblyLiquid/BakkesLinux/blob/master/README.md), or read the [Bakkesmod issues thread for Linux](https://github.com/bakkesmodorg/BakkesMod2-Plugins/issues/2).
## Steam Deck Prep
The SteamOS file system is read-only by default and is re-imaged on SteamOS upgrade. This means that you will have to repeat this process when Rocket League (and therefore BakkesMod) updates, if there has been a system update since you last installed it. Steam system updates will not affect the existing BakkesMod installation. There is an alternative method for the Steam Deck without some of these problems in the [cross-platform instructions](https://github.com/CrumblyLiquid/BakkesLinux/blob/master/README.md).

Switch to [Desktop mode](https://help.steampowered.com/en/faqs/view/671A-4453-E8D2-323C) then open [Konsole](https://en.wikipedia.org/wiki/Konsole).
![The Konsole application on SteamOS desktop mode](/../docs/konsole.png)
Don't do anything in this app with untrusted sources. [tinyurl.com/yay-steam](https://tinyurl.com/yay-steam) links to [`yay-steam.sh`](https://raw.githubusercontent.com/kentslaney/bakkesmod-arch/refs/heads/master/yay-steam.sh) in this repo. TinyURLs are changable, so this is still bad practice. Enter and run the following:
```bash
curl -L tinyurl.com/yay-steam | sh
```
## Platforms
In order to disable BakkesMod, set the `BAKKES` enviornment variable to `0`. If you have the EGS version, continue reading. Otherwise, skip to the [Steam section](#steam).
## EGS (Heroic/Legendary)
> [!WARNING]
> EGS support is currently broken. Tracked in [issue #5](https://github.com/kentslaney/bakkesmod-arch/issues/5).

Install the package with
```bash
yay -S bakkesmod-legendary
```
Launching the game should now also launch BakkesMod, but to find the enviornment variable mentioned above, go to the settings icon on the upper right side of Rocket League's game page:

![The Rocket League game page on Heroic](/../docs/heroic-settings.png)

go to the advanced tab

![The advanced tab](/../docs/advanced.png)

and scroll down to the `Environment Variables` section

![The environment variables section](/../docs/env.png)
## Steam
Install the package with
```bash
yay -S bakkesmod-steam
```
Then navigate to the Rocket League game's launch page

![The Rocket League game page on Steam](/../docs/header.png)

and select the gear icon > Properties

![The Properties menu option](/../docs/menu.png)

The setting that needs to be modified is `Launch Options`

![The settings window containing Launch Options](/../docs/options.png)

The recommended `Launch Options` are
```bash
BAKKES=1 PROMPTLESS=1 %command%
```
My personal `Launch Options` on desktop are
```bash
BAKKES=1 PROMPTLESS=1 PROTON_LOG=1 WINEDEBUG=trace-unwind,warn+seh gamemoderun %command% -NoKeyboardUI
```
