# BakkesMod for Steam on Arch
[Hosted on AUR](https://aur.archlinux.org/packages/bakkesmod-steam): just
install and add `BAKKES=1` as a launch option.

## Promptless Injection
The `dll_patch.py` script, followed by the BakkesMod DLL path as a CLI argument
will create a patched DLL version which will not prompt the user to verify
injection despite being unable to detect the version. This injector version can
be used via Proton by adding `PROMPTLESS=1` as a launch option in addition to
the `BAKKES=1` flag mentioned above.

While this process happens automatically using `PKGBUILD` on linux, the patched
version should also get rid of the injection verification on Windows, provided
that the BakkesMod DLL is replaced rather than duplicated.

## TODO
- stop resetting the user's config on install
- rebase and publish the `rolling` branch as `bakkesmod-steam-git`

