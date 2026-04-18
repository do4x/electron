#!/usr/bin/env python3
"""model.py — beta-VAE architecture for the VAE Latent Secret challenge."""

import torch
import torch.nn as nn


class VAEEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Sequential(
            # block 1: 3x64x64 -> 32x32x32
            nn.Conv2d(3, 32, 4, stride=2, padding=1),
            nn.BatchNorm2d(32),
            nn.LeakyReLU(0.2),
            # block 2: 32x32x32 -> 64x16x16
            nn.Conv2d(32, 64, 4, stride=2, padding=1),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(0.2),
            # block 3: 64x16x16 -> 128x8x8
            nn.Conv2d(64, 128, 4, stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2),
            # block 4: 128x8x8 -> 256x4x4
            nn.Conv2d(128, 256, 4, stride=2, padding=1),
            nn.BatchNorm2d(256),
            nn.LeakyReLU(0.2),
        )
        self.fc_hidden = nn.Sequential(
            nn.Linear(256 * 4 * 4, 1024),
            nn.LeakyReLU(0.2),
        )
        self.fc_mu      = nn.Linear(1024, 512)
        self.fc_log_var = nn.Linear(1024, 512)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        h = self.conv(x)
        h = h.view(h.size(0), -1)
        h = self.fc_hidden(h)
        return self.fc_mu(h), self.fc_log_var(h)


class VAEDecoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(512, 1024),
            nn.ReLU(),
            nn.Linear(1024, 256 * 4 * 4),
            nn.ReLU(),
        )
        self.deconv = nn.Sequential(
            # block 1: 256x4x4 -> 128x8x8
            nn.ConvTranspose2d(256, 128, 4, stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            # block 2: 128x8x8 -> 64x16x16
            nn.ConvTranspose2d(128, 64, 4, stride=2, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            # block 3: 64x16x16 -> 32x32x32
            nn.ConvTranspose2d(64, 32, 4, stride=2, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            # block 4: 32x32x32 -> 3x64x64
            nn.ConvTranspose2d(32, 3, 4, stride=2, padding=1),
            nn.Sigmoid(),
        )

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        h = self.fc(z)
        h = h.view(h.size(0), 256, 4, 4)
        return self.deconv(h)


class BetaVAE(nn.Module):
    LATENT_DIM   = 512
    DEFAULT_BETA = 4.0

    def __init__(self, latent_dim: int = 512, beta: float = 4.0):
        super().__init__()
        self.latent_dim = latent_dim
        self.beta       = beta
        self.encoder    = VAEEncoder()
        self.decoder    = VAEDecoder()

    def reparameterize(self, mu: torch.Tensor, log_var: torch.Tensor) -> torch.Tensor:
        std = torch.exp(0.5 * log_var)
        eps = torch.randn_like(std)
        return mu + eps * std

    def forward(
        self, x: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        mu, log_var = self.encoder(x)
        z           = self.reparameterize(mu, log_var)
        recon       = self.decoder(z)
        return recon, mu, log_var, z

    def encode(self, x: torch.Tensor) -> torch.Tensor:
        mu, _ = self.encoder(x)
        return mu

    def decode(self, z: torch.Tensor) -> torch.Tensor:
        return self.decoder(z)


def vae_loss(
    recon: torch.Tensor,
    x: torch.Tensor,
    mu: torch.Tensor,
    log_var: torch.Tensor,
    beta: float,
) -> dict[str, torch.Tensor]:
    recon_loss = nn.functional.mse_loss(recon, x, reduction="mean") * (64 * 64 * 3)
    kl_loss    = -0.5 * torch.sum(1 + log_var - mu.pow(2) - log_var.exp(), dim=1)
    kl_loss    = kl_loss.mean()
    total      = recon_loss + beta * kl_loss
    return {"total": total, "recon": recon_loss, "kl": kl_loss}


if __name__ == "__main__":
    model = BetaVAE()
    x     = torch.randn(2, 3, 64, 64)

    recon, mu, log_var, z = model(x)
    losses = vae_loss(recon, x, mu, log_var, model.beta)

    print(f"Input shape:      {tuple(x.shape)}")
    print(f"Recon shape:      {tuple(recon.shape)}")
    print(f"mu shape:         {tuple(mu.shape)}")
    print(f"log_var shape:    {tuple(log_var.shape)}")
    print(f"z shape:          {tuple(z.shape)}")
    print(f"Loss total:       {losses['total'].item():.4f}")
    print(f"Loss recon:       {losses['recon'].item():.4f}")
    print(f"Loss kl:          {losses['kl'].item():.4f}")
    n_params = sum(p.numel() for p in model.parameters())
    print(f"Parameter count:  {n_params:,}")
