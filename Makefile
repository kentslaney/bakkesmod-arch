all:
	mkdir -p build/include;\
	[ ! -d build/BakkesModInjectorCpp ] && git clone https://github.com/bakkesmodorg/BakkesModInjectorCpp.git build/BakkesModInjectorCpp;\
	git apply -q --directory=build/BakkesModInjectorCpp mingw.patch;\
	ln -sf /usr/x86_64-w64-mingw32/include/windows.h "build/include/Windows.h";\
	ln -sf /usr/x86_64-w64-mingw32/include/sdkddkver.h "build/include/SDKDDKVer.h";\
	ln -sf /usr/x86_64-w64-mingw32/include/shlobj.h "build/include/shlobj_core.h";\
	ln -sf "../BakkesModInjectorCpp/BakkesModWPF/Resource.h" "build/include/resource.h";\
	ln -sf "../BakkesModInjectorCpp/BakkesModInjectorC++/WindowsUtils.h" "build/include/windowsutils.h";\
    x86_64-w64-mingw32-g++ -std=c++17 -static-libgcc -static-libstdc++ -static -municode -mconsole -lpsapi -w -Ibuild/include -I/usr/x86_64-w64-mingw32/include -Ibuild/BakkesModInjectorCpp/BakkesModInjectorC++ \
        "build/BakkesModInjectorCpp/BakkesModInjectorC++/WindowsUtils.cpp" \
        "build/BakkesModInjectorCpp/BakkesModWPF/BakkesModWPF.cpp" \
        "build/BakkesModInjectorCpp/BakkesModInjectorC++/DllInjector.cpp" \
        "main.cpp" -o "build/inject.exe"

clean:
	rm -rf build
