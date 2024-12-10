import pygame

def initialize_screen():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("GWENT - Card Game")
    return screen

def render_card(screen, card, x, y, font):
    pygame.draw.rect(screen, (255, 255, 255), (x, y, 120, 180))  # Card background
    name_text = font.render(card.name, True, (0, 0, 0))
    strength_text = font.render(f"Strength: {card.strength}", True, (0, 0, 0))
    screen.blit(name_text, (x + 10, y + 10))
    screen.blit(strength_text, (x + 10, y + 50))
