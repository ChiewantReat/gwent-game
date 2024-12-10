import random
from card import Card, HeroCard, WeatherCard, SpecialCard

class Deck:
    def __init__(self, faction_name, faction_cards, neutral_cards, special_cards, leader_card=None):
        """
        Initialize a deck with faction, neutral, and special cards.

        :param faction_name: The name of the faction (e.g., "Northern Realms").
        :param faction_cards: List of cards specific to the faction.
        :param neutral_cards: List of neutral cards available to all factions.
        :param special_cards: List of special cards (weather, decoy, etc.).
        :param leader_card: The assigned leader card for the deck.
        """
        self.faction_name = faction_name
        self.cards = faction_cards + neutral_cards + special_cards
        self.leader_card = leader_card
        self.graveyard = []
        self.shuffle()

    def shuffle(self):
        """Shuffle the deck randomly."""
        random.shuffle(self.cards)

    def draw(self, count=1):
        """
        Draw cards from the deck.
        :param count: Number of cards to draw.
        :return: List of drawn cards.
        """
        drawn = self.cards[:count]
        self.cards = self.cards[count:]
        return drawn

    def add_to_graveyard(self, card):
        """
        Add a card to the graveyard.
        :param card: The card to add.
        """
        self.graveyard.append(card)

    def resurrect_from_graveyard(self):
        """
        Resurrect the most recently discarded card.
        :return: The resurrected card, or None if the graveyard is empty.
        """
        return self.graveyard.pop() if self.graveyard else None

    def validate(self, min_units=22, max_specials=10):
        """
        Validate the deck according to Gwent rules.
        :param min_units: Minimum number of unit cards required.
        :param max_specials: Maximum number of special cards allowed.
        :return: True if the deck is valid, False otherwise.
        """
        unit_cards = [card for card in self.cards if card.strength is not None]
        special_cards = [card for card in self.cards if card.ability and card.deck_type == "special"]

        if len(unit_cards) < min_units:
            print(f"Invalid Deck: Needs at least {min_units} unit cards.")
            return False
        if len(special_cards) > max_specials:
            print(f"Invalid Deck: Can only have up to {max_specials} special cards.")
            return False
        return True

    def __len__(self):
        """Return the number of cards remaining in the deck."""
        return len(self.cards)

# Example Usage
if __name__ == "__main__":
    # Load decks from Card.py
    from card import northern_realms_deck, nilfgaardian_deck, neutral_deck, special_cards

    # Example: Initialize a Northern Realms deck
    my_deck = Deck(
        faction_name="Northern Realms",
        faction_cards=northern_realms_deck,
        neutral_cards=neutral_deck[:5],  # Use the first 5 neutral cards
        special_cards=special_cards[:3],  # Use the first 3 special cards
        leader_card=HeroCard("Foltest, King of Temeria", 0, None, "leader_foltest.jpg")
    )

    # Shuffle and draw cards
    my_deck.shuffle()
    hand = my_deck.draw(10)

    # Print drawn cards
    print("Your Hand:")
    for card in hand:
        print(f"- {card.name} ({card.strength if card.strength else 'Special'})")

    # Validate the deck
    is_valid = my_deck.validate()
    print("Deck Valid:", is_valid)
