### replaces b5a430e9cf5078843d1a39f08ae95456891d4067872ad3512b04cb84f9a094c0

import sys, os, pathlib, importlib.util

user_settings = globals().get("user_settings", {})
matching = ("settings_{}.py", "settings_{}_*.py")
game_id = os.environ.get("SteamGameId")
base = pathlib.Path(__file__).parents[0]
check = lambda flag: os.environ.get(flag, "0") == "1"
cond = lambda flag, fn: fn(user_settings) if check(flag) else None

for pattern in matching:
    for file in base.glob(pattern.format(game_id)):
        spec = importlib.util.spec_from_file_location(file.stem, str(file))
        mod = importlib.util.module_from_spec(spec)
        sys.modules[file.stem] = mod
        spec.loader.exec_module(mod)

        if hasattr(mod, "flag"):
            if hasattr(mod, "update"):
                cond(mod.flag, mod.update)
            elif hasattr(mod, "user_settings") and check(mod.flag):
                user_settings.update(mod.user_settings)
        elif hasattr(mod, "update"):
            mod.update(user_settings)
        elif not hasattr(mod, "flags") and hasattr(mod, "user_settings"):
                user_settings.update(mod.user_settings)
        if hasattr(mod, "flags"):
            for flag, handler in mod.flags.items():
                if isinstance(type(handler), dict):
                    handler = lambda x: x.update(handler)
                cond(flag, handler)

print('user_settings', user_settings)

