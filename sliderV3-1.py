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

def visualize_percentage(label, percentage):
    """Create a visualization of the percentage with a color-coded bar."""
    # Set seaborn style
    sns.set_style("whitegrid")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Get color based on percentage
    color = get_color(percentage)
    
    # Create bar plot
    sns.barplot(x=[percentage], y=[0], color=color, ax=ax)
    
    # Customize plot
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.5, 0.5)
    ax.set_xlabel("Percentage (%)")
    ax.set_yticks([])
    ax.set_title(label, pad=20, fontsize=12, wrap=True)
    
    # Add percentage text on the bar
    ax.text(percentage, 0, f"{percentage:.1f}%", 
            ha='right' if percentage > 90 else 'left', 
            va='center', color='white', fontsize=12, fontweight='bold')
    
    # Remove top and right spines
    sns.despine(left=True, bottom=False)
    
    # Show plot
    plt.tight_layout()
    plt.show()

def main():
    """Main function to run the percentage visualizer."""
    label = get_valid_label()
    percentage = get_valid_percentage()
    visualize_percentage(label, percentage)

if __name__ == "__main__":
    main()