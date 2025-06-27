import tkinter as tk
from tkinter import messagebox
import math

def interpolate_color(value, min_val, max_val, color1, color2):
    """Interpolate between two colors based on a value."""
    ratio = (value - min_val) / (max_val - min_val)
    r = int(color1[0] + (color2[0] - color1[0]) * ratio)
    g = int(color1[1] + (color2[1] - color1[1]) * ratio)
    b = int(color1[2] + (color2[2] - color1[2]) * ratio)
    return f'#{r:02x}{g:02x}{b:02x}'

def get_color(percentage):
    """Determine the color based on percentage (0% red, 50% orange, 100% green)."""
    red = (255, 0, 0)
    orange = (255, 165, 0)
    green = (0, 255, 0)
    if percentage <= 50:
        return interpolate_color(percentage, 0, 50, red, orange)
    else:
        return interpolate_color(percentage, 50, 100, orange, green)

def draw_gauge(percentage):
    """Draw a circular gauge on the canvas based on the percentage."""
    canvas.delete("all")  # Clear previous drawing
    center_x, center_y = 150, 150
    radius = 100
    start_angle = 135  # Start at 135 degrees (left side)
    extent = 270       # Cover 270 degrees to 45 degrees
    
    # Draw background arc
    canvas.create_arc(center_x - radius, center_y - radius, center_x + radius, center_y + radius,
                      start=start_angle, extent=extent, style=tk.ARC, outline="grey", width=10)
    
    # Draw filled arc for percentage
    percentage_extent = (percentage / 100) * extent
    color = get_color(percentage)
    canvas.create_arc(center_x - radius, center_y - radius, center_x + radius, center_y + radius,
                      start=start_angle, extent=percentage_extent, style=tk.ARC, outline=color, width=10)
    
    # Draw needle
    angle = math.radians(start_angle + percentage_extent)
    needle_length = radius - 10
    end_x = center_x + needle_length * math.cos(angle)
    end_y = center_y - needle_length * math.sin(angle)
    canvas.create_line(center_x, center_y, end_x, end_y, fill="black", width=2)
    
    # Draw center dot
    canvas.create_oval(center_x - 5, center_y - 5, center_x + 5, center_y + 5, fill="black")

def submit():
    """Handle the submit button action."""
    label_text = label_entry.get("1.0", tk.END).strip()
    try:
        percentage = float(percentage_entry.get())
        if not 0 <= percentage <= 100:
            messagebox.showerror("Invalid Input", "Percentage must be between 0 and 100.")
            return
        
        # Update label
        display_label.config(text=label_text)
        
        # Update gauge
        draw_gauge(percentage)
        
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid percentage (e.g., 75.5).")

# Create the main window
root = tk.Tk()
root.title("Percentage Circular Gauge")
root.geometry("400x500")

# Label input (up to three lines)
tk.Label(root, text="Enter Label (up to 3 lines):").pack(pady=10)
label_entry = tk.Text(root, height=3, width=30)
label_entry.pack()

# Percentage input
tk.Label(root, text="Enter Percentage (0-100):").pack(pady=10)
percentage_entry = tk.Entry(root)
percentage_entry.pack()

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack(pady=10)

# Display label
display_label = tk.Label(root, text="", wraplength=350, justify="center")
display_label.pack(pady=20)

# Canvas for gauge
canvas = tk.Canvas(root, width=300, height=300)
canvas.pack(pady=20)

# Start the main loop
root.mainloop()