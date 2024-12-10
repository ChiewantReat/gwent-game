from Card import shuffle_deck, draw_cards, northern_realms_deck, nilfgaardian_deck, neutral_deck, special_cards
from Player import Player
from Gui import initialize_screen, render_card
import random
import pygame

def combine_with_neutral_and_special(faction_deck, neutral_deck, special_deck, num_neutral_cards=5, num_special_cards=3):
    """
    Combine a faction deck with neutral and special cards.

    :param faction_deck: The faction-specific deck.
    :param neutral_deck: The neutral deck.
    :param special_deck: The special deck.
    :param num_neutral_cards: Number of neutral cards to include.
    :param num_special_cards: Number of special cards to include.
    :return: The combined deck.
    """
    selected_neutral = random.sample(neutral_deck, min(num_neutral_cards, len(neutral_deck)))
    selected_special = random.sample(special_deck, min(num_special_cards, len(special_deck)))
    return faction_deck + selected_neutral + selected_special

def main():
    # Initialize the screen
    screen = initialize_screen()
    font = pygame.font.Font(None, 36)

    # Choose factions
    print("Choose your faction:")
    print("1. Northern Realms")
    print("2. Nilfgaardian Empire")
    choice = input("Enter the number of your choice: ")
    if choice == "1":
        player_faction = "Northern Realms"
        player_deck = northern_realms_deck
        opponent_faction = "Nilfgaardian Empire"
        opponent_deck = nilfgaardian_deck
    elif choice == "2":
        player_faction = "Nilfgaardian Empire"
        player_deck = nilfgaardian_deck
        opponent_faction = "Northern Realms"
        opponent_deck = northern_realms_deck
    else:
        print("Invalid choice. Defaulting to Northern Realms.")
        player_faction = "Northern Realms"
        player_deck = northern_realms_deck
        opponent_faction = "Nilfgaardian Empire"
        opponent_deck = nilfgaardian_deck

    # Add neutral and special cards to both decks
    player_deck = combine_with_neutral_and_special(player_deck, neutral_deck, special_cards, num_neutral_cards=5, num_special_cards=3)
    opponent_deck = combine_with_neutral_and_special(opponent_deck, neutral_deck, special_cards, num_neutral_cards=5, num_special_cards=3)

    # Shuffle decks
    shuffle_deck(player_deck)
    shuffle_deck(opponent_deck)

    # Initialize players
    player = Player("Player", player_deck)
    opponent = Player("Opponent", opponent_deck)

    # Draw 10 cards for each player
    player.draw_hand(draw_cards, count=10)
    opponent.draw_hand(draw_cards, count=10)

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw background
        screen.fill((0, 128, 0))  # Green background

        # Render player's cards
        for i, card in enumerate(player.hand):
            render_card(screen, card, 50 + i * 140, 400, font)

        # Render opponent's cards
        for i, card in enumerate(opponent.hand):
            render_card(screen, card, 50 + i * 140, 50, font)

        pygame.display.flip()

    pygame.quit()
