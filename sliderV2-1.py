import tkinter as tk
from tkinter import messagebox
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

def get_color(percentage):
    """Calculate color based on percentage (0% red, 50% orange, 100% green)."""
    if percentage <= 50:
        # Interpolate from red (0%) to orange (50%)
        r = 1.0
        g = (percentage / 50) * 0.647  # Orange has RGB (1, 0.647, 0)
        b = 0.0
    else:
        # Interpolate from orange (50%) to green (100%)
        r = ((100 - percentage) / 50) * 1.0  # Orange to green, reduce red
        g = 1.0  # Green component increases
        b = 0.0
    return (r, g, b)

def create_visualization():
    """Create the visualization based on user input."""
    label = label_text.get("1.0", tk.END).strip()
    try:
        percentage = float(percentage_entry.get())
        if not 0 <= percentage <= 100:
            messagebox.showerror("Invalid Input", "Percentage must be between 0 and 100.")
            return
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid percentage.")
        return

    # Close the input window
    root.destroy()

    # Set up Seaborn style
    sns.set_style("whitegrid")

    # Create a figure
    fig, ax = plt.subplots(figsize=(10, 4))

    # Create custom colormap for the slider
    colors = [(1, 0, 0), (1, 0.647, 0), (0, 1, 0)]  # Red, Orange, Green
    cmap = LinearSegmentedColormap.from_list("custom", colors)

    # Plot the slider (bar)
    ax.barh(0, percentage, color=get_color(percentage), height=0.4)
    ax.set_xlim(0, 100)
    ax.set_yticks([])
    ax.set_xticks(np.arange(0, 101, 10))
    ax.set_xlabel("Percentage (%)")

    # Add the label as title (split into lines if necessary)
    ax.set_title(label, pad=20, wrap=True)

    # Show the plot
    plt.tight_layout()
    plt.show()

# Create the Tkinter GUI
root = tk.Tk()
root.title("Percentage Slider Input")
root.geometry("400x300")

# Label input (up to three lines)
tk.Label(root, text="Enter Label (up to 3 lines):").pack(pady=10)
label_text = tk.Text(root, height=3, width=30)
label_text.pack(pady=5)

# Percentage input
tk.Label(root, text="Enter Percentage (0-100):").pack(pady=10)
percentage_entry = tk.Entry(root)
percentage_entry.pack(pady=5)

# Submit button
tk.Button(root, text="Create Visualization", command=create_visualization).pack(pady=20)

# Start the Tkinter main loop
root.mainloop()