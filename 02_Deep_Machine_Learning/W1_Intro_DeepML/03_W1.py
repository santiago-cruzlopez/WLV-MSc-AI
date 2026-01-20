"""
   The following code computes and visualizes the sigmoid activation function and its derivative using TensorFlow's automatic differentiation capabilities like GradientTape.
   The objective is to illustrate how the gradient of the sigmoid function behaves across a range of input values from -10 to 10. Then , it plots both the sigmoid function and its derivative for comparison.
"""
   
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

# Generate input values
x = tf.linspace(-10.0, 10.0, 201)

# Compute sigmoid and gradient using GradientTape
with tf.GradientTape() as tape:
    tape.watch(x)  # Watch the input tensor
    y = tf.nn.sigmoid(x)  # Sigmoid function

dy_dx = tape.gradient(y, x)  # Computed derivative

# Analytical derivative for verification
analytical_dy_dx = y * (1 - y)

# Convert to NumPy for plotting
x_np = x.numpy()
y_np = y.numpy()
dy_dx_np = dy_dx.numpy()
analytical_np = analytical_dy_dx.numpy()

# Plot with improvements
plt.figure(figsize=(10, 6))
plt.plot(x_np, y_np, 'b-', label='y = sigmoid(x)')
plt.plot(x_np, dy_dx_np, 'r--', label='dy/dx (Computed)')
plt.plot(x_np, analytical_np, 'g-.', label='dy/dx (Analytical)')
plt.title('Sigmoid Function and Its Derivative')
plt.xlabel('x')
plt.ylabel('Value')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()