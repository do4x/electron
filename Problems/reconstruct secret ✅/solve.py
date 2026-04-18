"""
solve.py - Reconstruct the Secret
Run from the task folder:  python solve.py

Inventory of secret_net.pt (OrderedDict):
  _ns                  ()          int64        = 1337   (bait: "noise seed")
  layer1.weight        (64, 16)    float32      range ~ [-0.58, 0.96]
  layer1.bias          (64,)       float32
  layer2.weight        (128, 64)   float32      range ~ [-0.63, 0.80]
  layer2.bias          (128,)      float32
  layer3.weight        (64, 128)   float32      range ~ [-0.70, 0.80]
  layer3.bias          (64,)       float32
  layer4.weight        (32, 64)    float32      range ~ [-0.93, 0.98]
  layer4.bias          (32,)       float32
  output.weight        (2, 32)     float32
  output.bias          (2,)        float32
  ghost_layer.weight   (4, 32)     float32      int-valued in [0, 125]
                                                -> decodes to "CTF{not_in_weights}" (BAIT)

The real flag is encoded in the FIRST ROW of the weight matrix of each
of the four hidden layers. Each value is a flag byte scaled by 1/128:
    byte = round(weight * 128)
Only the leading positions of each row are flag bytes; the rest are
ordinary trained noise.

  layer1.weight[0][0:4]  -> "CTF{"
  layer2.weight[0][0:32] -> 32 hex chars
  layer3.weight[0][0:32] -> 32 hex chars
  layer4.weight[0][0:1]  -> "}"
"""

import numpy as np
import torch


ARTIFACT = "secret_net.pt"
CHUNKS = [("layer1", 4), ("layer2", 32), ("layer3", 32), ("layer4", 1)]


def load():
    return torch.load(ARTIFACT, map_location="cpu", weights_only=False)


def extract(sd) -> str:
    pieces = []
    for name, n in CHUNKS:
        row = sd[f"{name}.weight"].numpy()[0, :n]
        bytes_ = np.round(row * 128).astype(np.int64).clip(0, 255).astype(np.uint8)
        pieces.append(bytes(bytes_).decode("ascii"))
    return "".join(pieces)


def verify(flag: str) -> bool:
    return flag.startswith("CTF{") and flag.endswith("}") and flag.isascii()


def main():
    sd = load()
    flag = extract(sd)
    assert verify(flag), f"flag failed validation: {flag!r}"
    print(flag)


if __name__ == "__main__":
    main()
