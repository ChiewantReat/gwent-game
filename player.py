from deck import Deck
from card import Card


class Player:
    def __init__(self, name, faction, deck, leader_card=None):
        """
        Initialize a Player object.
        
        :param name: Player's name (string).
        :param faction: Faction name (string).
        :param deck: The player's deck (Deck object).
        :param leader_card: The leader card (Card object).
        """
        self.name = name
        self.faction = faction
        self.deck = deck
        self.hand = []  # Cards currently in hand
        self.graveyard = []  # Discarded cards
        self.leader_card = leader_card
        self.leader_used = False
        self.health = 2  # Number of lives (rounds)
        self.passed = False
        self.total_score = 0

    def draw_initial_hand(self):
        """
        Draw the initial 10 cards for the player.
        """
        self.hand = self.deck.draw(10)

    def play_card(self, card):
        """
        Play a card from the player's hand.
        
        :param card: The card to play (Card object).
        :return: The played card.
        """
        if card in self.hand:
            self.hand.remove(card)
            return card
        raise ValueError("Card not found in hand.")

    def pass_round(self):
        """
        Pass the current round.
        """
        self.passed = True

    def activate_leader(self):
        """
        Activate the leader card's ability.
        """
        if self.leader_card and not self.leader_used:
            print(f"{self.name} activates leader ability: {self.leader_card.name}")
            # Implement specific leader abilities here
            self.leader_used = True
        else:
            print("Leader ability already used or not available.")

    def update_score(self, points):
        """
        Update the player's total score for the round.
        
        :param points: Points to add (positive or negative).
        """
        self.total_score += points

    def reset_round(self):
        """
        Reset the player's state for a new round.
        """
        self.passed = False
        self.total_score = 0

    def add_to_graveyard(self, card):
        """
        Add a card to the player's graveyard.
        
        :param card: The card to add (Card object).
        """
        self.graveyard.append(card)

    def resurrect_card(self):
        """
        Resurrect the most recently discarded card from the graveyard.
        
        :return: The resurrected card, or None if the graveyard is empty.
        """
        return self.graveyard.pop() if self.graveyard else None

