# -*- coding: utf-8 -*-
"""works.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nDKE4-R0RxsTEdDEWdMMR67eKaBA5M6A
"""

import torch
import math
import matplotlib.pyplot as plt

dtype = torch.float
device = "cuda" if torch.cuda.is_available() else "cpu"

x = torch.linspace(-3, 3, 2000, device=device, dtype=dtype)
y = torch.sin(x)

a=torch.randn((), device=device, dtype=dtype)
b=torch.randn((), device=device, dtype=dtype)
c=torch.randn((), device=device, dtype=dtype)
d=torch.randn((), device=device, dtype=dtype)
e=torch.randn((), device=device, dtype=dtype)

import torch

iterations = 400
learning_rate = 1e-7
min_learning_rate = 1e-11
free = [1]  # Initialize with a high value to ensure the first comparison is valid

# Initialize parameters with smaller values
a = torch.randn((), device=device, dtype=dtype) * 0.01
b = torch.randn((), device=device, dtype=dtype) * 0.01
c = torch.randn((), device=device, dtype=dtype) * 0.01
d = torch.randn((), device=device, dtype=dtype) * 0.01
e = torch.randn((), device=device, dtype=dtype) * 0.01

# Define a flag to control the outer loop
stop_training = False

while learning_rate >= min_learning_rate and not stop_training:
    for t in range(iterations):
        # Forward pass
        y_pred = a + b * x + c * x**2 + d * x**3 + e * x.abs()**(1/2)

        # Compute loss
        loss = (y_pred - y).pow(2).sum()
        # Check for NaN in loss or predictions
        if torch.isnan(loss) or torch.isnan(y_pred).any():
            print(f"NaN detected. Loss: {loss}, y_pred: {y_pred}")
            learning_rate /= 2
            print(f"Reducing learning rate to {learning_rate}")
            stop_training = True
            break

        if t % 200 == 199:
            print(f"Iteration {t}, Loss: {loss.item()}")

        # Compute gradients
        grad_y_pred = 2.0 * (y_pred - y)
        grad_a = grad_y_pred.sum()
        grad_b = (grad_y_pred * x).sum()
        grad_c = (grad_y_pred * x**2).sum()
        grad_d = (grad_y_pred * x**3).sum()
        grad_e = (grad_y_pred * x.abs()**(1/2)).sum()

        # Print gradients
        if t % 200 == 199:
          if abs(free[0] - loss.item()) < 1e-4:
            print(f"Early stopping triggered at iteration {t}. Loss change is minimal: {loss.item()}")
            stop_training = True
            break
          else:
            free[0] = loss.item()
            print(f"Gradients: grad_a = {grad_a.item()}, grad_b = {grad_b.item()}, grad_c = {grad_c.item()}, grad_d = {grad_d.item()}, grad_e = {grad_e.item()}")

        # Apply gradient clipping
        max_grad_norm = 1.0
        torch.nn.utils.clip_grad_norm_([a, b, c, d, e], max_grad_norm)

        # Update parameters
        a -= learning_rate * grad_a
        b -= learning_rate * grad_b
        c -= learning_rate * grad_c
        d -= learning_rate * grad_d
        e -= learning_rate * grad_e

    # Check if learning rate is too small and break the outer loop
    if learning_rate < min_learning_rate:
        print("Learning rate too small. Stopping training.")
        stop_training = True

print(f"Result: y = {a.item()} + {b.item()}x + {c.item()}x^2 + {d.item()}x^3 + {e.item()}x^1/2")

a.item(), b.item(), c.item(), d.item(), e.item()

plt.plot(a.item() + b.item() * x + c.item() * x**2 + d.item() * x**3 + e.item() * x.abs()**(1/2))
plt.plot(y)
plt.show()