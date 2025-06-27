import tkinter as tk
from tkinter import messagebox

def interpolate_color(value, min_val, max_val, color1, color2):
    """Interpolate between two colors based on a value."""
    ratio = (value - min_val) / (max_val - min_val)
    r = int(color1[0] + (color2[0] - color1[0]) * ratio)
    g = int(color1[1] + (color2[1] - color1[1]) * ratio)
    b = int(color1[2] + (color2[2] - color1[2]) * ratio)
    return f'#{r:02x}{g:02x}{b:02x}'

def get_color(percentage):
    """Determine the color based on percentage (0% red, 50% orange, 100% green)."""
    red = (255, 0, 0)      # RGB for red
    orange = (255, 165, 0)  # RGB for orange
    green = (0, 255, 0)     # RGB for green
    
    if percentage <= 50:
        # Interpolate between red and orange
        return interpolate_color(percentage, 0, 50, red, orange)
    else:
        # Interpolate between orange and green
        return interpolate_color(percentage, 50, 100, orange, green)

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
        
        # Update slider
        slider.set(percentage)
        
        # Update slider color
        color = get_color(percentage)
        slider.config(troughcolor=color, background=color)
        
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid percentage (e.g., 75.5).")



# Create the main window
root = tk.Tk()
root.title("Percentage Slider")
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

# Slider
slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, length=300, showvalue=True)
slider.pack(pady=20)

# Start the main loop
root.mainloop()