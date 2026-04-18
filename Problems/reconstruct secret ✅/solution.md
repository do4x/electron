# reconstruct secret — Reconstruct the Secret

## The Puzzle
We are given a PyTorch checkpoint `secret_net.pt` for a 5-layer feedforward
network (`SecretNet`). The task description says the real flag is "split across
the four hidden layers" and warns that any parameter you can spot at a glance
is probably bait. Our job is to find a `CTF{...}` string hidden in the
weights themselves.

## What I Found in the File

Opening `secret_net.pt` with `torch.load` yields an `OrderedDict` with the
expected `layer1..layer4` and `output` weights/biases, plus two extras that
don't belong to the architecture defined in `model.py`:

| key                  | shape     | dtype   | notes |
| -------------------- | --------- | ------- | ----- |
| `_ns`                | `()`      | int64   | value `1337` |
| `ghost_layer.weight` | `(4, 32)` | float32 | every value is an integer in `[0, 125]` |

The four hidden layers themselves fingerprint like ordinary trained weights —
floats spread across `[-1, 1]`, no obvious ASCII when scaled, no sparse
diff vs. a seeded init.

But inspecting weight rows revealed an anomaly: **the first row** of each
hidden layer's weight matrix contained leading values that were not
kaiming-init-like at all. For `layer1.weight[0]`, the first four values were
`0.5234`, `0.6562`, `0.5469`, `0.9609`. Kaiming init for
`Linear(16, 64)` is bounded by `1/sqrt(16) = 0.25`, so values near `0.96` in
row 0 are wildly out of distribution.

Multiplying those four values by 128 gives exactly `67, 84, 70, 123` — i.e.
`"CTF{"`. The rest of each row was ordinary noise, but the leading entries
of rows 0 in layers 2, 3, and 4 decoded the same way to produce
two 32-character hex blocks and the closing `}`.

## Why That Was the Flag

The challenge explicitly flagged two decoys:

1. **`ghost_layer.weight`** — a `(4, 32)` tensor of printable byte values
   that decodes to the string `CTF{not_in_weights}`. It's not referenced
   in the `SecretNet` architecture, so the loader silently ignores it
   during inference; it exists purely to catch anyone who runs a byte-scan
   and stops at the first `CTF{...}` they find.
2. **`_ns = 1337`** — a "noise seed" buffer that strongly suggests a
   `torch.manual_seed(1337)` reconstruction attack: seed, re-initialize
   the network, subtract to find the training delta. But the checkpoint
   was actually trained (80 epochs of Adam per `TECH_NOTES.txf`), so the
   diff against a seeded init is just noisy training-path gradients with
   no ASCII signal.

The real trick is subtle: after training, the author overwrote a small
leading slice of the **first row** of each hidden layer's weight matrix
with `byte / 128` floats. The task hint — "split across the four hidden
layers" — describes exactly this: CTF{ in layer 1, a 32-hex block in
layer 2, another 32-hex block in layer 3, and } in layer 4.

Why `/128`? It keeps the injected values inside the weight matrix's
natural float range so nothing jumps out on a quick `min/max` inventory.
`0.523` and `0.961` look like perfectly plausible trained weights until
you realize the layer's init bound was `0.25`.

## How to Pull It Out

```python
sd = torch.load("secret_net.pt", map_location="cpu", weights_only=False)
chunks = [("layer1", 4), ("layer2", 32), ("layer3", 32), ("layer4", 1)]

flag = ""
for name, n in chunks:
    row = sd[f"{name}.weight"].numpy()[0, :n]
    flag += bytes(np.round(row * 128).astype(np.uint8)).decode("ascii")
```

The punchline is the single line `np.round(row * 128).astype(np.uint8)` —
everything else is just slicing the right number of bytes out of each
layer.

## The Flag

`CTF{ea47d8c6afbe1c6b442b2ae180f8b48eec7b3569b932f3c48b470acf1162dcf4}`

This is the intended solution: the hint "split across the four hidden
layers" maps one-to-one onto the four weight rows, and the `/128` scaling
matches the standard "smuggle bytes inside a plausible weight range"
trick that the `ghost_layer` bait was designed to distract from.

## Run It Yourself

```bash
cd "Problems/reconstruct secret" && python solve.py
```
