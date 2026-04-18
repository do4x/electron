#!/usr/bin/env python3
"""Custom model architecture for the Reconstruct the Secret challenge."""

from __future__ import annotations

import math

import torch
from torch import nn
from torch.nn import functional as F


MAGIC = 0xDEAD_C0DE


class SoftplusShifted(nn.Module):
    """Softplus shifted so that f(0) == 0."""

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return F.softplus(x) - math.log(2.0)


class SecretNet(nn.Module):
    """Neural network whose layers will later carry hidden flag fragments."""

    MAGIC = MAGIC

    def __init__(self, noise_seed: int = 0) -> None:
        super().__init__()
        self.noise_seed = noise_seed
        self.register_buffer("_ns", torch.tensor(int(noise_seed), dtype=torch.int64))

        self.layer1 = nn.Linear(16, 64)
        self.act1 = SoftplusShifted()
        self.layer2 = nn.Linear(64, 128)
        self.act2 = nn.Tanh()
        self.layer3 = nn.Linear(128, 64)
        self.act3 = nn.ReLU()
        self.layer4 = nn.Linear(64, 32)
        self.act4 = nn.Sigmoid()
        self.output = nn.Linear(32, 2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.layer1(x)
        x = self.act1(x)
        x = self.layer2(x)
        x = self.act2(x)
        x = self.layer3(x)
        x = self.act3(x)
        x = self.layer4(x)
        x = self.act4(x)
        x = self.output(x)
        return x

    def get_layer_names(self) -> list[str]:
        return ["layer1", "layer2", "layer3", "layer4", "output"]


def count_trainable_parameters(model: nn.Module) -> int:
    return sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad)


if __name__ == "__main__":
    model = SecretNet()
    sample_input = torch.randn(1, 16)
    sample_output = model(sample_input)

    print(f"Output shape: {tuple(sample_output.shape)}")
    print(f"Trainable parameters: {count_trainable_parameters(model)}")
