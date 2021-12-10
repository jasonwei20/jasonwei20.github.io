# From the DeepMind Jax Basics tutorial
# Jax currently broken with python 3.8

import jax
import jax.numpy as jnp
import numpy as np

xs = np.random.normal(size=(100,))
noise = np.random.normal(scale=0.1, size=(100,))
ys = xs * 3 - 1 + noise

def model(theta, x):
	"""Computes wx + b on a batch of input x."""
	w, b = theta
	return w * x + b

def loss_fn(theta, x, y):
	prediction = model(theta, x)
	return jnp.mean((prediction-y)**2)

def update(theta, x, y, lr=0.1):
	loss, gradient = jax.value_and_grad(loss_fn)(theta, x, y)
	return theta - lr * gradient

theta = jnp.array([1., 1.])

for _ in range(1000):
  theta = update(theta, xs, ys)

w, b = theta
print(f"w: {w:<.2f}, b: {b:<.2f}")
