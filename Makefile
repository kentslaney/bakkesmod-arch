all: inject sandbox

inject:
	mkdir -p build/include dist;\
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
        "main.cpp" -o "dist/inject.exe"

sandbox:
	mkdir -p build dist;\
	[ ! -d build/powershell-wrapper-for-wine ] && git clone https://github.com/PietJankbal/powershell-wrapper-for-wine.git build/powershell-wrapper-for-wine;\
	git apply -q --directory=build/powershell-wrapper-for-wine sandbox.patch;\
	x86_64-w64-mingw32-gcc -O1 -fno-ident -fno-stack-protector -fomit-frame-pointer -fno-unwind-tables -fno-asynchronous-unwind-tables -falign-functions=1 -falign-jumps=1 -falign-loops=1 -fwhole-program \
		-mconsole -municode -mno-stack-arg-probe -Xlinker --stack=0x200000,0x200000 -nostdlib  -Wall -Wextra -ffreestanding build/powershell-wrapper-for-wine/main.c -lurlmon -lkernel32 -lucrtbase -nostdlib -lshell32 -lshlwapi -s -o dist/powershell64.exe;\
	i686-w64-mingw32-gcc   -O1 -fno-ident -fno-stack-protector -fomit-frame-pointer -fno-unwind-tables -fno-asynchronous-unwind-tables -falign-functions=1 -falign-jumps=1 -falign-loops=1 -fwhole-program \
		-mconsole -municode -mno-stack-arg-probe -Xlinker --stack=0x200000,0x200000 -nostdlib  -Wall -Wextra -ffreestanding build/powershell-wrapper-for-wine/main.c -lurlmon -lkernel32 -lucrtbase -nostdlib -lshell32 -lshlwapi -s -o dist/powershell32.exe

clean:
	rm -rf build dist
