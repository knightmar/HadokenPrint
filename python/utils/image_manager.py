import pygame
from svgpathtools import svg2paths, Path, Line, CubicBezier, QuadraticBezier, Arc
import numpy as np


def extract_points_from_svg(file_path):
    # Read paths and attributes from the SVG file
    paths, attributes = svg2paths(file_path)

    all_points = []
    for path in paths:
        for segment in path:
            if isinstance(segment, Line):
                all_points.append((segment.start.real, segment.start.imag))
                all_points.append((segment.end.real, segment.end.imag))
            elif isinstance(segment, (CubicBezier, QuadraticBezier, Arc)):
                all_points.extend(approximate_curve(segment, 5))
    return all_points


def approximate_curve(segment, num_points=100):
    """Approximate a curve segment with a series of points."""
    points = []
    for i in range(num_points + 1):
        t = i / num_points
        point = segment.point(t)
        points.append((point.real, point.imag))
    return points


def display_points_in_pygame(points):
    # Initialize Pygame
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('SVG Points and Curves with Scale Slider')

    # Slider properties
    slider_rect = pygame.Rect(50, height - 50, width - 100, 10)
    slider_pos = slider_rect.x
    scale_factor = 1

    font = pygame.font.SysFont(None, 24)

    def draw_slider():
        pygame.draw.rect(screen, (150, 150, 150), slider_rect)
        handle_rect = pygame.Rect(slider_pos - 5, slider_rect.y - 5, 10, 20)
        pygame.draw.rect(screen, (0, 0, 0), handle_rect)

    def get_scale_factor():
        return (0.1 + (slider_pos - slider_rect.x) / slider_rect.width * 2.0)

    # Main loop
    running = True
    dragging = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if slider_rect.collidepoint(event.pos):
                    dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                slider_pos = max(slider_rect.x, min(event.pos[0], slider_rect.x + slider_rect.width))
                scale_factor = get_scale_factor()

        screen.fill((255, 255, 255))  # Fill the screen with white

        # Draw points
        for point in points:
            scaled_point = (int(point[0] * scale_factor), int(point[1] * scale_factor))
            pygame.draw.circle(screen, (0, 0, 0), scaled_point, 3)

        draw_slider()

        # Display scale factor
        scale_text = font.render(f'Scale: {scale_factor:.2f}', True, (0, 0, 0))
        screen.blit(scale_text, (50, 50))

        pygame.display.flip()

    pygame.quit()


# Example usage
svg_file_path = '/home/knightmar/Téléchargements/laser.svg'
points = extract_points_from_svg(svg_file_path)
display_points_in_pygame(points)
print(points)
