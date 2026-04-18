"""
solve.py — quantization_station
Reproduces the flag end-to-end. Run from the task folder:  python solve.py

Inventory (from np.load('quantization_station.npz')):
    stem.proj.weight_q              (8, 6)    int8    — plausible weights
    stem.proj.scale                 (8,)      float32 — plausible scales
    stem.proj.zero_point            (8,)      int32   — plausible zero-points
    encoder.block0.ffn.weight_q     (12, 8)   int8
    encoder.block0.ffn.scale        (12,)     float32
    encoder.block0.ffn.zero_point   (12,)     int32
    encoder.block1.ffn.weight_q     (10, 12)  int8
    encoder.block1.ffn.scale        (10,)     float32
    encoder.block1.ffn.zero_point   (10,)     int32
    bridge.out_proj.weight_q        (69, 1)   int8    — ALL 127
    bridge.out_proj.scale           (69,)     float32 — ALL 0.5
    bridge.out_proj.zero_point      (69,)     int32   — 69 varying values

The bridge layer is the outlier: constant weight (127) and constant scale (0.5),
with the only variation in zero_point. Length 69 matches a flag-sized string.
Dequantizing with the standard formula yields printable ASCII:
    x = scale * (weight_q - zero_point) = 0.5 * (127 - zp)
"""
import numpy as np

ARTIFACT = "quantization_station.npz"


def extract(data) -> str:
    w = data["bridge.out_proj.weight_q"].ravel().astype(np.int64)
    s = data["bridge.out_proj.scale"]
    zp = data["bridge.out_proj.zero_point"]
    vals = (s * (w - zp)).round().astype(np.uint8)
    return bytes(vals).decode("ascii")


def verify(flag: str) -> bool:
    return flag.startswith("CTF{") and flag.endswith("}") and flag.isascii()


def main():
    data = np.load(ARTIFACT)
    flag = extract(data)
    assert verify(flag), f"flag failed validation: {flag!r}"
    print(flag)


if __name__ == "__main__":
    main()
