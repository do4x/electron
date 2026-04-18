# Reconstruct the Secret - Challenge Handoff

## Overview
This is a Machine Learning / PyTorch-based CTF challenge called "Reconstruct the Secret". 
The goal is to find the hidden flag formatted as `CTF{...}`.

## Files
- `model.py`: Contains the model architecture (`SecretNet`), a 5-layer feedforward neural network (4 hidden layers, 1 output layer).
- `secret_net.pt`: The trained model weights checkpoint.
- `TECH_NOTES.txt` / `TECH_NOTES.txf`: Training metadata (appears empty or unavailable).

## Findings So Far
1. **The Bait**: The `secret_net.pt` file contained an extra layer not defined in the architecture called `ghost_layer.weight`. When converted from ASCII, its values spell out `CTF{not_in_weights}`. This matches the challenge description's mention of "deliberate bait for anyone who only scans obvious parameters."
2. **The Seed**: The checkpoint contains a persistent buffer `_ns` (noise seed) which has been set to the value `1337`.
3. **The Clue**: The challenge description states, *"The real flag is split across the four hidden layers."*

## Strategy for the Next Agent
Since the flag is not directly encoded in the literal weights (as confirmed by the bait), it is highly likely hidden in the **differences** between the loaded weights and the initial random weights.

**Suggested approach:**
1. Initialize a new `SecretNet` model instance.
2. Before initialization, set the random seed to the noise seed found in the checkpoint: `torch.manual_seed(1337)`.
3. Load the checkpoint weights (`secret_net.pt`).
4. Calculate the difference (delta) between the initialized weights/biases (using seed 1337) and the loaded weights/biases for `layer1`, `layer2`, `layer3`, and `layer4`.
5. Convert the non-zero differences into ASCII characters to reconstruct the real flag.

## Environment
- A virtual environment is already set up at `c:\Electron\venv_win` with PyTorch installed (`.\venv_win\Scripts\python.exe`).
