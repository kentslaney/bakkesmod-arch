# BakkesMod for Legendary on Arch
[Hosted on AUR](https://aur.archlinux.org/packages/bakkesmod-legendary)

The AUR package replaces the official updater with the system package manager,
upstream is [BakkesModInjectorCpp](
https://github.com/bakkesmodorg/BakkesModInjectorCpp/releases/latest).

## Promptless Injection
The `dll_patch.py` script, followed by the BakkesMod DLL path as a CLI argument,
will create a patched DLL version which will not prompt the user to verify
injection despite being unable to detect the version. This injector version can
be used via Proton by adding `PROMPTLESS=1` as a launch option. The patched
version should also get rid of the injection verification on Windows, provided
that the BakkesMod DLL is replaced rather than duplicated, which is the default.

