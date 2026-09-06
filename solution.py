
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution
from scipy.spatial import cKDTree


# Load the supplied data
data = pd.read_csv("xy_data.csv")
given_points = data[["x", "y"]].values


# Generate the parametric curve
def generate_curve(params, n_points=3000):

    theta_deg, M, X = params
    theta = np.radians(theta_deg)

    t = np.linspace(6, 60, n_points)

    x_curve = (
        t * np.cos(theta)
        - np.exp(M * np.abs(t))
        * np.sin(0.3 * t)
        * np.sin(theta)
        + X
    )

    y_curve = (
        42
        + t * np.sin(theta)
        + np.exp(M * np.abs(t))
        * np.sin(0.3 * t)
        * np.cos(theta)
    )

    return np.column_stack((x_curve, y_curve))


# Calculate L1 distance
def calculate_l1_error(params):

    predicted_points = generate_curve(params)

    tree = cKDTree(predicted_points)

    _, nearest_indices = tree.query(given_points)

    nearest_points = predicted_points[nearest_indices]

    return np.sum(np.abs(given_points - nearest_points))


# Parameter limits
parameter_bounds = [
    (0, 50),
    (-0.05, 0.05),
    (0, 100)
]


# Find best parameters
result = differential_evolution(
    calculate_l1_error,
    parameter_bounds,
    seed=42,
    maxiter=100,
    popsize=10,
    tol=1e-8,
    polish=True
)


# Print results
theta_final = result.x[0]
M_final = result.x[1]
X_final = result.x[2]

print("=" * 60)
print("FLAMAI R&D ASSIGNMENT - FINAL RESULT")
print("=" * 60)

print(f"Theta (degrees): {theta_final:.6f}")
print(f"M              : {M_final:.6f}")
print(f"X              : {X_final:.6f}")
print(f"L1 Distance    : {result.fun:.6f}")

print("=" * 60)


# Generate final fitted curve
final_curve = generate_curve(result.x)

x_final = final_curve[:, 0]
y_final = final_curve[:, 1]


# Plot validation
plt.figure(figsize=(10, 6))

plt.scatter(
    given_points[:, 0],
    given_points[:, 1],
    s=5,
    label="Given data"
)

plt.plot(
    x_final,
    y_final,
    linewidth=2,
    label="Optimized curve"
)

plt.xlabel("X")
plt.ylabel("Y")
plt.title("Final Curve Fit")
plt.legend()
plt.grid(True)

plt.savefig(
    "curve_fit.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
