import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

def get_valid_label():
    """Prompt user for a label (up to three lines) and validate input."""
    print("Enter a label (up to three lines, press Enter twice to finish):")
    lines = []
    for i in range(3):
        line = input(f"Line {i+1} (or press Enter to finish): ").strip()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines) if lines else "Default Label"

def get_valid_percentage():
    """Prompt user for a percentage and validate input."""
    while True:
        try:
            percentage = float(input("Enter percentage (0-100): "))
            if 0 <= percentage <= 100:
                return percentage
            else:
                print("Percentage must be between 0 and 100.")
        except ValueError:
            print("Please enter a valid number.")

def get_color(percentage):
    """Calculate color based on percentage (red at 0%, orange at 50%, green at 100%)."""
    if percentage < 50:
        # Transition from red (0%) to orange (50%)
        norm = percentage / 50
        color = mcolors.to_hex((1, norm, 0))  # Red to orange
    else:
        # Transition from orange (50%) to green (100%)
        norm = (percentage - 50) / 50
        color = mcolors.to_hex((1 - norm, 1, 0))  # Orange to green
    return color

def visualize_percentage_dial(label, percentage):
    """Create a dial (gauge) visualization of the percentage with a color-coded arc."""
    # Set seaborn style for consistency
    sns.set_style("whitegrid")
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw={'projection': 'polar'})
    
    # Convert percentage to angle (0% = 0°, 100% = 180°)
    angle = (percentage / 100) * np.pi  # Map 0-100% to 0-180 degrees
    
    # Get color based on percentage
    color = get_color(percentage)
    
    # Draw the gauge arc
    ax.barh(0, angle, color=color, height=0.4, alpha=0.8)
    
    # Draw the background arc (grey, for the unfilled portion)
    ax.barh(0, np.pi, color='lightgrey', height=0.4, alpha=0.3)
    
    # Customize the gauge
    ax.set_ylim(-0.5, 0.5)  # Control the thickness of the arc
    ax.set_yticks([])  # Remove radial ticks
    ax.set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])  # Ticks at 0%, 25%, 50%, 75%, 100%
    ax.set_xticklabels(['0%', '25%', '50%', '75%', '100%'], fontsize=10)
    
    # Add percentage text in the center
    ax.text(0, 0, f"{percentage:.1f}%", ha='center', va='center', fontsize=20, fontweight='bold')
    
    # Set title (label) above the gauge
    ax.set_title(label, pad=20, fontsize=12, wrap=True)
    
    # Remove spines for a cleaner look
    ax.set_frame_on(False)
    
    # Show plot
    plt.tight_layout()
    plt.show()

def main():
    """Main function to run the percentage dial visualizer."""
    label = get_valid_label()
    percentage = get_valid_percentage()
    visualize_percentage_dial(label, percentage)

if __name__ == "__main__":
    main()