# gguf graveyard

## The Puzzle

A single `graveyard.gguf` file, 3028 bytes, masquerading as a TinyLlama checkpoint.
The `task.md` is empty on purpose -- the puzzle is to discover that the file has
no tensors (`tensor_count = 0`) and that its metadata table has been seeded with
decoys and bodies. The challenge name calls the file a *graveyard*: every grave
is a key-value pair, and one of them holds a fake flag while others hold the
real one in pieces.

## What I Found in the File

The header parses as normal GGUF v2 (`magic = "GGUF"`, `version = 2`), but the
value-type enum is shifted from the standard spec:

| type | meaning in this file |
|-----:|----------------------|
|   0  | U32                  |
|   2  | ARRAY                |
|   3  | F32                  |
|   7  | STRING               |
|   9  | BOOL                 |
|  11  | INT64                |

Array headers are `(element_type:u32, array_n:u32)` -- u32 for the length, not
u64 as the current spec says. That custom shape is why the stock `gguf` Python
reader crashes with an `IndexError` on this file.

With a custom parser the 38 KV entries come out clean. 31 of them are ordinary
model metadata (`general.architecture = "llama"`, `llama.context_length = 2048`,
tokenizer and training fields, etc). The interesting ones are:

```
[00] general.signature              ARRAY<INT64>[69]  "CTF{509aab1a@a19d8e08&f7252f7@225@9d66627b29&7ce1e6@80805@cd662f@85@}"
[02] 3e265995-436f-854f-a8ed-814052e3c697  ARRAY<INT64>[16]  "aab1a4a19d8e083f"
[03] 8d35a957-ee4f-bce7-438f-ba5bf9cfed60  ARRAY<INT64>[2]   "66"
[04] 769f6669-a010-d290-a35c-4f283fbff16b  ARRAY<INT64>[4]   "2549"
[20] cdbe4262-deb3-8661-e789-e5b4355c22e9  ARRAY<INT64>[30]  "27b2937ce1e64808054cd662f4854}"
[21] 1b02ad77-50cb-c17a-2c20-7c37d6df61f0  ARRAY<INT64>[7]   "CTF{509"
[25] 4d7dd5de-4589-ce5f-3293-a4593359f09e  ARRAY<INT64>[8]   "7252f742"
[27] 79e73759-326b-f2c0-564b-6d270ec25a2d  ARRAY<INT64>[2]   "d6"
```

Every other layer had a sensible name; these seven had UUIDs, which no standard
GGUF field ever uses. Their values are INT64 arrays, but every element lives in
`[32, 126]` -- printable ASCII smuggled through a 64-bit integer channel.

## Why That Was the Flag

`general.signature` is the grave marker with the headstone. It has the right
shape (starts with `CTF{`, ends with `}`, length 69) and is the first key in the
file, so a scanner that prints the "obvious" key walks away with it. But its
content contains `@` and `&`, which are not valid hex -- and the rest of the
file is heavy on hex-looking chunks. Those non-hex characters are the
fingerprint of a decoy: the author wanted a string that *looks* like the flag
but couldn't be a real hex digest.

The seven UUID keys are the actual bodies. None of them mean anything to a
GGUF loader (llama.cpp will just ignore unknown metadata), so they are free
storage. Concatenating them in the order the file lists them gives nonsense --
the fragments are laid down in a scrambled order on purpose. Sorting the UUIDs
by their first 8-hex-digit segment (ascending) puts them back in flag order:

```
1b02ad77  'CTF{509'
3e265995  'aab1a4a19d8e083f'
4d7dd5de  '7252f742'
769f6669  '2549'
79e73759  'd6'
8d35a957  '66'
cdbe4262  '27b2937ce1e64808054cd662f4854}'
```

Concatenated: `CTF{509aab1a4a19d8e083f7252f7422549d66627b2937ce1e64808054cd662f4854}`.

Exactly 64 hex characters between the braces -- a 256-bit value, the sort of
thing a real CTF flag wraps. That is the punchline: the "signature" was a
plausible-but-malformed imitation; the real signature is a SHA-256-sized hex
string reassembled from seven gravestones whose ordering key is the UUID's
first segment.

## How to Pull It Out

```python
import re, struct

UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")

# parse(data) returns [(key, value), ...] using the custom type enum
entries = parse(open("graveyard.gguf", "rb").read())

frags = [(k, "".join(chr(c) for c in v)) for k, v in entries if UUID_RE.match(k)]
frags.sort(key=lambda kv: int(kv[0][:8], 16))
flag = "".join(s for _, s in frags)
```

The punchline line is `frags.sort(key=lambda kv: int(kv[0][:8], 16))` -- the
graveyard is unordered until you read the names on the stones.

## The Flag

`CTF{509aab1a4a19d8e083f7252f7422549d66627b2937ce1e64808054cd662f4854}`

## Run It Yourself

```bash
cd "Problems/gguf graveyard" && python solve.py
```
