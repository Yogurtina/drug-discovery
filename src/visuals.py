import matplotlib.pyplot as plt
import numpy as np

# Data
substances = [3, 5, 10, 20, 30, 40, 50, 100]
solve_time = [0.0, 0.0, 0.1, 4.7, 19.5, 134.1, 1125.7, None]

# Filter out None values and get the maximum solve time
filtered_solve_time = [t for t in solve_time if t is not None]
max_solve_time = max(filtered_solve_time)

# Set a large value relative to the maximum solve time
large_value = max_solve_time * 10 if max_solve_time is not None else 1.0

# Replace None values with the large value for plotting
solve_time = [t if t is not None else large_value for t in solve_time]

# Plotting
plt.plot(substances, solve_time, marker='o')
plt.xlabel('Number of Substances')
plt.ylabel('Solve Time (s)')
plt.title('Solve Time vs Number of Substances')
plt.grid(True)

# Scale y-axis using log scale if large values are present
if large_value > max(solve_time):
    plt.yscale('log')

# Show or save the plot
plt.show()

e_values = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
objective_values = [-0.1, 14.1985, 28.9004, 43.6076, 58.3148, 73.022, 87.7292, 102.4364, 117.1436, 131.8508, 146.558]

plt.plot(e_values, objective_values, marker='o')
plt.xlabel('e values')
plt.ylabel('Objective')
plt.title('Objective vs e values')
plt.grid(True)

plt.show()
