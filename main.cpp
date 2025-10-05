#include "DllInjector.h"
#include <iostream>

int wmain(int argc, wchar_t* argv[]) {
    std::wstring ps = L"RocketLeague.exe";
    const wchar_t* launcher = L"C:\\users\\steamuser\\AppData\\Roaming\\bakkesmod\\bakkesmod\\dll\\bakkesmod.dll";
    DllInjector dllInjector;
    bool launching = false;
    for (int i = 1; i < argc; i++) {
        auto arg = std::wstring(argv[i]);
        if (arg == L"launching") {
            launching = true;
        }
    }
    if (launching) {
        std::cout << "Injector waiting for launch" << std::endl;
        while (dllInjector.GetProcessID64(ps) == 0) {
            Sleep(1000);
        }
        std::cout << "Found PID, attempting injection" << std::endl;
    }
    dllInjector.InjectDLL(ps, launcher);
    return 0;
}
