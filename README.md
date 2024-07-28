# BakkesMod for Steam on Arch
[Hosted on AUR](https://aur.archlinux.org/packages/bakkesmod-steam): just
install and add `BAKKES=1` as a launch option for the official DLL or
`BAKKES=1 PROMPTLESS=1` for the patched version without the version detection
prompt. If you're unfamiliar with launch options, remember to add `%command%` at
the end.

The AUR package replaces the official updater with the system package manager,
so use
[bakkesmod-steam-git](https://aur.archlinux.org/packages/bakkesmod-steam-git)
instead if the main repo ends up out of date (relative to the latest
[BakkesModInjectorCpp](
https://github.com/bakkesmodorg/BakkesModInjectorCpp/releases/latest)
release).

## Promptless Injection
The `dll_patch.py` script, followed by the BakkesMod DLL path as a CLI argument,
will create a patched DLL version which will not prompt the user to verify
injection despite being unable to detect the version. This injector version can
be used via Proton by adding `PROMPTLESS=1` as a launch option. The patched
version should also get rid of the injection verification on Windows, provided
that the BakkesMod DLL is replaced rather than duplicated, which is the default.

