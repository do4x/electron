"""
solve.py - gguf graveyard
Reproduces the flag end-to-end. Run from the task folder:  python solve.py

Inventory of graveyard.gguf (version=2, tensor_count=0, kv_count=38):
  - A near-standard GGUF header, BUT with a custom type enum:
        0 = U32, 2 = ARRAY, 3 = F32, 7 = STRING, 9 = BOOL, 11 = INT64
    Array header is (element_type:u32, array_n:u32) -- u32 length, not u64.
  - 31 normal metadata keys (general.*, llama.*, tokenizer.*, training.*).
  - `general.signature` is a 69-char array claiming to be the flag; it
    contains `@` and `&` in place of hex digits -> obvious bait.
  - 7 metadata keys named like UUIDs, each an INT64 array whose values are
    ASCII codepoints. Concatenating their contents in the order given by the
    UUID's first hex segment yields the real flag.

    1b02ad77-...  'CTF{509'
    3e265995-...  'aab1a4a19d8e083f'
    4d7dd5de-...  '7252f742'
    769f6669-...  '2549'
    79e73759-...  'd6'
    8d35a957-...  '66'
    cdbe4262-...  '27b2937ce1e64808054cd662f4854}'
"""
import re
import struct

ARTIFACT = "graveyard.gguf"

UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")

SCALAR = {
    0:  ("<I", 4),
    3:  ("<f", 4),
    9:  ("<B", 1),
    11: ("<q", 8),
}


def load():
    with open(ARTIFACT, "rb") as f:
        return f.read()


def read_str(data, off):
    ln = struct.unpack("<Q", data[off:off + 8])[0]
    return data[off + 8:off + 8 + ln].decode("utf-8", "replace"), off + 8 + ln


def read_value(data, off, vt):
    if vt == 7:
        return read_str(data, off)
    if vt == 2:
        et = struct.unpack("<I", data[off:off + 4])[0]
        n  = struct.unpack("<I", data[off + 4:off + 8])[0]
        off += 8
        if et == 7:
            arr = []
            for _ in range(n):
                s, off = read_str(data, off)
                arr.append(s)
            return arr, off
        fmt, sz = SCALAR[et]
        arr = [struct.unpack(fmt, data[off + i * sz:off + (i + 1) * sz])[0] for i in range(n)]
        return arr, off + n * sz
    fmt, sz = SCALAR[vt]
    return struct.unpack(fmt, data[off:off + sz])[0], off + sz


def parse(data):
    assert data[:4] == b"GGUF"
    kv_count = struct.unpack("<Q", data[16:24])[0]
    off = 24
    entries = []
    for _ in range(kv_count):
        klen = struct.unpack("<Q", data[off:off + 8])[0]; off += 8
        key = data[off:off + klen].decode(); off += klen
        vt = struct.unpack("<I", data[off:off + 4])[0]; off += 4
        val, off = read_value(data, off, vt)
        entries.append((key, val))
    return entries


def extract(entries):
    frags = [(k, "".join(chr(c) for c in v)) for k, v in entries if UUID_RE.match(k)]
    frags.sort(key=lambda kv: int(kv[0][:8], 16))
    return "".join(s for _, s in frags)


def verify(flag: str) -> bool:
    return flag.startswith("CTF{") and flag.endswith("}") and flag.isascii()


def main():
    entries = parse(load())
    flag = extract(entries)
    assert verify(flag), f"flag failed validation: {flag!r}"
    print(flag)


if __name__ == "__main__":
    main()
