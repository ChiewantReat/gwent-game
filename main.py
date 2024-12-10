from  card import northern_realms_deck, nilfgaardian_deck, neutral_deck, special_cards
from deck import Deck
from player import Player
import pygame


def initialize_screen():
    """
    Initialize the Pygame screen and window.
    """
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Gwent: The Card Game")
    return screen


def main(): 
    # Initialize GUI
    screen = initialize_screen()
    font = pygame.font.Font(None, 36)

    # Set up factions
    print("Choose your faction:")
    print("1. Northern Realms")
    print("2. Nilfgaardian Empire")
    choice = input("Enter the number of your choice: ")

    if choice == "1":
        player_faction = "Northern Realms"
        player_deck = Deck(
            faction_name=player_faction,
            faction_cards=northern_realms_deck,
            neutral_cards=neutral_deck[:5],
            special_cards=special_cards[:3]
        )
        ai_faction = "Nilfgaardian Empire"
        ai_deck = Deck(
            faction_name=ai_faction,
            faction_cards=nilfgaardian_deck,
            neutral_cards=neutral_deck[5:10],
            special_cards=special_cards[3:6]
        )
    elif choice == "2":
        player_faction = "Nilfgaardian Empire"
        player_deck = Deck(
            faction_name=player_faction,
            faction_cards=nilfgaardian_deck,
            neutral_cards=neutral_deck[:5],
            special_cards=special_cards[:3]
        )
        ai_faction = "Northern Realms"
        ai_deck = Deck(
            faction_name=ai_faction,
            faction_cards=northern_realms_deck,
            neutral_cards=neutral_deck[5:10],
            special_cards=special_cards[3:6]
        )
    else:
        print("Invalid choice. Defaulting to Northern Realms.")
        player_faction = "Northern Realms"
        player_deck = Deck(
            faction_name=player_faction,
            faction_cards=northern_realms_deck,
            neutral_cards=neutral_deck[:5],
            special_cards=special_cards[:3]
        )
        ai_faction = "Nilfgaardian Empire"
        ai_deck = Deck(
            faction_name=ai_faction,
            faction_cards=nilfgaardian_deck,
            neutral_cards=neutral_deck[5:10],
            special_cards=special_cards[3:6]
        )

    # Initialize Player and AI
    player = Player(name="Player", faction=player_faction, deck=player_deck)
    ai = Player(name="AI Opponent", faction=ai_faction, deck=ai_deck)

    # Draw initial hands
    player.draw_initial_hand()
    ai.draw_initial_hand()

    # Display initial player hand
    print("Your Hand:")
    for card in player.hand:
        print(f"- {card.name} ({card.strength if card.strength else 'Special'})")

    # Game loop (placeholder for now)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Render screen
        screen.fill((0, 128, 0))  # Green background
        y_offset = 50

        # Render player hand
        for i, card in enumerate(player.hand):
            card.render(screen, 50 + i * 140, 500)

        # Render AI placeholder
        for i, card in enumerate(ai.hand):
            pygame.draw.rect(screen, (255, 0, 0), (50 + i * 140, 50, 120, 180))  # Placeholder

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
