Receptive Leak
Description
A convolutional network can remember more than its predictions.

You are given a single PyTorch checkpoint:

cnn_secure_stego.pt

It still behaves like a normal CNN digit classifier, but the checkpoint was also used as a storage medium for a second message.

There are no passwords, no sidecar secrets, and no external oracle. Everything needed to recover the flag is already inside the checkpoint.

If you want the flag, it would be wise to not look at the logits (at least not only at them).

Flag format:

CTF{...}