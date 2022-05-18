import numpy as np
import matplotlib.pyplot as plt


omega = 0.5 * np.pi
noise = 0.05
sigma = 0.05


def my_signal(X):
    # Base signal
    f = np.sin(omega * X)**2

    # Noise
    f += np.random.normal(noise, sigma, len(X))

    return f


X_range = (0., 4.)

X = np.linspace(*X_range, 1000)
y = my_signal(X)

# Plot
fig, ax = plt.subplots()

ax.plot(X, y)

ax.set_xlim(*X_range)
ax.set_ylim(0., 1.)

plt.show()
