lea64 = b'\x48\x8d'
call64 = b'\xFF'
little = lambda x: int.from_bytes(x, byteorder='little')

# iterate over matches for lea64
def leas(f, start=None, end=None, op=lea64):
    match = f.find(op, start, end)
    while match != -1:
        yield match
        match = f.find(op, match + 1, end)

# give the position and loaded virtual address for each lea match
def addr(f, start=None, end=None, op=lea64, reg=1):
    arg = len(op) + reg
    for i in leas(f, start, end, op):
        yield [i, i + arg + 4 + little(f[i + arg: i + arg + 4])]

# VA offsets for .text and .rdata
def offsets(f):
    # .text567_size_want
    off = (f.index(b".text"), f.index(b".rdata"))
    return [a - b for a, b in zip(
            [little(f[i + 0xc : i + 0x10]) for i in off],
            [little(f[i + 0x14 : i + 0x18]) for i in off],
        )]

targets = [
        b'Could not verify RL version',
        b'Dunno how the user got here',
        b'User wishes to inject anyway',
    ]

# gives storage locations of target phrases accounting for offsets
def rel32(f):
    text, rdata = offsets(f)
    return [f.index(i) + rdata - text for i in targets]

# gives positions of references to the target phrases
def refs(f, rel=None, it=None):
    default = rel is None and it is None
    rel, it = rel or rel32(f), it or addr(f)
    res = tuple(zip(*[(rel.index(x), i) for i, x in it if x in rel]))
    if default:
        assert res[0] == (0, 1, 2, 0, 1, 2)
        return (res[1][:3], res[1][3:])
    return res

jcc32 = [b'\x0F' + int.to_bytes(i, 1, 'little') for i in range(0x80, 0x90)]
jcc8 = list(bytes(range(0x70, 0x80)))

# gives "inject anyway" jmp RVAs
def branches(f, ref=None):
    ref = ref or refs(f)
    def inner(a, b):
        seq = f[a : b]
        op32 = [seq.index(i) for i in jcc32 if i in seq]
        op8 = [seq.index(i) for i in jcc8 if i in seq]
        loc32 = [a + i + 6 + little(seq[i + 2 : i + 6]) for i in op32]
        loc8 = [a + i + 2 + little(seq[i + 1 : i + 2]) for i in op8]
        return loc8 + loc32
    return [max(m for m in inner(i, j) if m <= k) for i, j, k in ref]

optionals = (
    (2, "Magic"),
    (1, "MajorLinkerVersion"),
    (1, "MinorLinkerVersion"),
    (4, "SizeOfCode"),
    (4, "SizeOfInitializedData"),
    (4, "SizeOfUninitializedData"),
    (4, "AddressOfEntryPoint"),
    (4, "BaseOfCode"),
    (8, "ImageBase"),
    (4, "SectionAlignment"),
    (4, "FileAlignment"),
    (2, "MajorOperatingSystemVersion"),
    (2, "MinorOperatingSystemVersion"),
    (2, "MajorImageVersion"),
    (2, "MinorImageVersion"),
    (2, "MajorSubsystemVersion"),
    (2, "MinorSubsystemVersion"),
    (4, "Win32VersionValue"),
    (4, "SizeOfImage"),
    (4, "SizeOfHeaders"),
    (4, "CheckSum"),
    (2, "Subsystem"),
    (2, "DllCharacteristics"),
    (8, "SizeOfStackReserve"),
    (8, "SizeOfStackCommit"),
    (8, "SizeOfHeapReserve"),
    (8, "SizeOfHeapCommit"),
    (4, "LoaderFlags"),
    (4, "NumberOfRvaAndSizes"),
)

def header(name, offset=0):
    for size, field in optionals:
        if field == name:
            return (offset, offset + size)
        offset += size
    raise Exception()

# gives offset and size of DLL directory
def idata(f, off=None):
    off = off or offsets(f)
    magic = f.index(b'\x0b\x02')
    iaddr = header("NumberOfRvaAndSizes", magic + 0xc)
    isize = header("NumberOfRvaAndSizes", magic + 0x10)
    return little(f[slice(*iaddr)]) - off[1], little(f[slice(*isize)])

ox = lambda x: tuple(map(hex, x))

# gives IAT start and end
def user32(f, dlls=None, size=None, off=None):
    off = off or offsets(f)
    dlls, size = idata(f, off) if dlls is None else (dlls, size)
    rows = [dlls + i for i in range(0, size, 20)]
    rvas = [little(f[i + 0xc  : i + 0x10]) for i in rows]
    tabs = [little(f[i + 0x10 : i + 0x14]) for i in rows]
    matching = b'USER32.dll'
    substr = lambda i: f[i - off[1] : i - off[1] + len(matching)]
    ptrs = [n for n, i in enumerate(rvas) if i != 0 and substr(i) == matching]
    assert len(ptrs) == 1
    ptr = ptrs[0]
    end = min(i for i in tabs if i > tabs[ptr])
    return tabs[ptr] - off[1], end - off[1]

# gives start of 8 byte IAT line as a .text RVA
def fns(f, iat=None, end=None, off=None):
    off = off or offsets(f)
    iat, end = user32(f, off=off) if iat is None else (dlls, size)
    rvas = [little(f[i : i + 4]) for i in range(iat, end, 8)]
    vas = [i - off[1] for i in rvas if i != 0]
    hints = [f[i : i + 2] for i in vas]
    names = [f[i + 2 : f.index(b'\x00', i + 2)] for i in vas]
    return iat + names.index(b'MessageBoxA') * 8 + off[1] - off[0]

def shunts(f, dbg=True):
    loads, msg = refs(f), fns(f)
    calls = [refs(f, (msg,), addr(f, *ref[:2], call64))[1][0] for ref in loads]
    skips = branches(f, loads)
    paired = tuple(zip(calls, skips))
    if dbg:
        print(tuple(map(ox, paired)))
    return paired

jmp = lambda x: b'\xE9' + int.to_bytes(x, 4, "little")

def mask(f, space=6):
    prev, out = 0, b''
    for pos, end in shunts(f):
        update = jmp(end - pos - 5)
        assert len(update) == 5
        out += f[prev:pos] + update + b'\x90' * (space - len(update))
        prev = pos + space
    out += f[prev:]
    assert len(f) == len(out)
    return out

def dll(path, dest=None):
    global Path
    from pathlib import Path
    path = Path(path)
    path = path if path.is_file() else path / "bakkesmod.dll"
    with open(path, "rb") as fp:
        f = fp.read()
    f = mask(f)
    dest = path.parents[0] if dest is None else dest
    dest = dest if dest.is_file() else dest / "bakkesmod_promptless.dll"
    with open(dest, "wb") as fp:
        fp.write(f)

if __name__ == "__main__":
    import sys
    dll(*sys.argv[1:])

