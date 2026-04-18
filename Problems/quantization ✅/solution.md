# quantization — Quantization Station

## The Puzzle
We are handed `quantization_station.npz`, a tiny NumPy archive styled like a per-channel quantized neural network: each "layer" has a `weight_q` (int8), a `scale` (float32), and a `zero_point` (int32). The task hints that **one layer is not like the others** and asks for a `CTF{...}` flag. Nothing about this is real inference — the archive is a costume, and one of the four layers is wearing it badly.

## What I Found in the File
A one-pass inventory tells the whole story:

| key prefix | weight_q shape | weight range | scale range | zero_point range |
| --- | --- | --- | --- | --- |
| `stem.proj` | (8, 6) | [-22, 21] | [0.035, 0.134] | [-12, 9] |
| `encoder.block0.ffn` | (12, 8) | [-18, 23] | [0.087, 0.140] | [-11, 12] |
| `encoder.block1.ffn` | (10, 12) | [-29, 40] | [0.030, 0.131] | [-11, 12] |
| **`bridge.out_proj`** | **(69, 1)** | **[127, 127]** | **[0.5, 0.5]** | **[-123, 31]** |

Three of the four layers look like normal quantized weights: varied int8 values, tiny positive scales, small zero-points. The `bridge.out_proj` block is the outlier on every axis:

- **Weight** is constant `127` across all 69 entries — no information lives there.
- **Scale** is constant `0.5` — also carrying nothing.
- **Zero-point** is the only tensor that varies, and it has exactly **69** entries, suspiciously close to a flag length.

Every other layer stored its signal in `weight_q`. This one moved the signal into `zero_point`.

## Why That Was the Flag
The standard dequantization formula for affine quantization is `x = scale * (weight_q - zero_point)`. With `weight_q = 127` and `scale = 0.5` held constant, that collapses to:

```
x = 0.5 * (127 - zero_point)
```

So the author built a layer whose "dequantized" output is a deterministic linear function of the one tensor they varied. Plugging in the first four zero-points:

- `0.5 * (127 - (-7))  = 67  → 'C'`
- `0.5 * (127 - (-41)) = 84  → 'T'`
- `0.5 * (127 - (-13)) = 70  → 'F'`
- `0.5 * (127 - (-119)) = 123 → '{'`

The bait is the *name* `zero_point` — a parameter that in a real quantized model is a small integer you barely look at. The lesson of the challenge is exactly what the manual warned about: a tensor named `zero_point` is not a contract, and a "layer" that produces ASCII when you run its own dequant formula is the flag layer.

## How to Pull It Out
```python
import numpy as np
d = np.load("quantization_station.npz")
w  = d["bridge.out_proj.weight_q"].ravel().astype(np.int64)  # all 127
s  = d["bridge.out_proj.scale"]                              # all 0.5
zp = d["bridge.out_proj.zero_point"]                         # the 69 varying ints
flag = bytes((s * (w - zp)).round().astype(np.uint8)).decode()
```

The punchline is the single expression `s * (w - zp)` — the model's own dequantization rule, applied honestly, prints the flag.

## The Flag
`CTF{b1a59cab118d90b0a1de12f129f926707017a67957d335f2dcd382b0856e91d3}`

## Run It Yourself
```bash
cd quantization && python solve.py
```
