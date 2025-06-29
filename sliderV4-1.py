import asyncio
import platform
import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Donut Dial Percentage")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Font
font = pygame.font.SysFont("arial", 24)

# Input variables
label_lines = ["", "", ""]
current_line = 0
percentage = ""
input_active = True
input_type = "label"  # Switch between "label" and "percentage"

def interpolate_color(percentage):
    """Interpolate color from red (0%) to orange (50%) to green (100%)."""
    if percentage <= 50:
        # Red (255, 0, 0) to Orange (255, 165, 0)
        r = 255
        g = int(165 * (percentage / 50))
        b = 0
    else:
        # Orange (255, 165, 0) to Green (0, 255, 0)
        r = int(255 * (1 - (percentage - 50) / 50))
        g = 255
        b = 0
    return (r, g, b)

def draw_donut_dial(screen, percentage, color):
    """Draw a donut dial representing the percentage."""
    center = (WIDTH // 2, HEIGHT // 2 - 50)
    outer_radius = 100
    inner_radius = 60
    # Draw background circle
    pygame.draw.circle(screen, GRAY, center, outer_radius)
    pygame.draw.circle(screen, WHITE, center, inner_radius)
    # Draw percentage arc
    start_angle = -math.pi / 2  # Start at top
    end_angle = start_angle + (2 * math.pi * (percentage / 100))
    num_points = 100
    for i in range(num_points):
        angle = start_angle + (end_angle - start_angle) * (i / num_points)
        next_angle = start_angle + (end_angle - start_angle) * ((i + 1) / num_points)
        outer_points = [
            (center[0] + outer_radius * math.cos(angle), center[1] + outer_radius * math.sin(angle)),
            (center[0] + outer_radius * math.cos(next_angle), center[1] + outer_radius * math.sin(next_angle)),
        ]
        inner_points = [
            (center[0] + inner_radius * math.cos(next_angle), center[1] + inner_radius * math.sin(next_angle)),
            (center[0] + inner_radius * math.cos(angle), center[1] + inner_radius * math.sin(angle)),
        ]
        pygame.draw.polygon(screen, color, outer_points + inner_points)

def draw_text():
    """Draw the label and percentage text."""
    # Draw label (up to 3 lines)
    for i, line in enumerate(label_lines):
        text_surface = font.render(line, True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 100 + i * 30))
        screen.fill(WHITE, text_rect)  # Clear background for text
        screen.blit(text_surface, text_rect)
    # Draw percentage
    perc_text = f"{percentage}%" if percentage and percentage.replace(".", "").isdigit() else ""
    perc_surface = font.render(perc_text, True, BLACK)
    perc_rect = perc_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.fill(WHITE, perc_rect)  # Clear background for text
    screen.blit(perc_surface, perc_rect)
    # Draw input prompt
    if input_active:
        prompt = "Enter label line {}: ".format(current_line + 1) if input_type == "label" else "Enter percentage: "
        prompt_surface = font.render(prompt, True, BLACK)
        prompt_rect = prompt_surface.get_rect(center=(WIDTH // 2, HEIGHT - 160))
        screen.fill(WHITE, prompt_rect)  # Clear background for prompt
        screen.blit(prompt_surface, prompt_rect)

def setup():
    """Initialize the game state."""
    screen.fill(WHITE)

async def update_loop():
    """Main update loop for handling input and drawing."""
    global input_active, input_type, current_line, percentage, label_lines
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif input_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if input_type == "label" and label_lines[current_line]:
                        label_lines[current_line] = label_lines[current_line][:-1]
                    elif input_type == "percentage" and percentage:
                        percentage = percentage[:-1]
                elif event.key == pygame.K_RETURN:
                    if input_type == "label" and label_lines[current_line]:
                        current_line += 1
                        if current_line >= 3:
                            input_type = "percentage"
                            current_line = 0
                    elif input_type == "percentage" and percentage:
                        try:
                            perc = float(percentage)
                            if 0 <= perc <= 100:
                                input_active = False
                        except ValueError:
                            percentage = ""  # Reset invalid input
                elif event.unicode.isprintable():
                    if input_type == "label" and len(label_lines[current_line]) < 20:
                        label_lines[current_line] += event.unicode
                    elif input_type == "percentage" and len(percentage) < 6:
                        if event.unicode.isdigit() or event.unicode == ".":
                            percentage += event.unicode

        # Clear screen
        screen.fill(WHITE)

        # Draw visualization if percentage is entered
        if not input_active and percentage.replace(".", "").isdigit():
            perc = float(percentage)
            color = interpolate_color(perc)
            draw_donut_dial(screen, perc, color)

        # Draw text
        draw_text()

        # Update display
        pygame.display.flip()

        await asyncio.sleep(1.0 / 60)  # 60 FPS

if platform.system() == "Emscripten":
    asyncio.ensure_future(update_loop())
else:
    if __name__ == "__main__":
        asyncio.run(update_loop())