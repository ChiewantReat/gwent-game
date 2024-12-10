class Row:
    def __init__(self, name):
        """
        Initialize a single row on the board.

        :param name: The name of the row (e.g., "close", "ranged", "siege").
        """
        self.name = name
        self.cards = []
        self.effects = []  # Active effects like "weather", "horn"

    def add_card(self, card):
        """
        Add a card to the row.
        :param card: The card to add.
        """
        self.cards.append(card)

    def apply_effect(self, effect):
        """
        Apply an effect to the row (e.g., weather).
        :param effect: The effect to apply.
        """
        if effect not in self.effects:
            self.effects.append(effect)

    def remove_effect(self, effect):
        """
        Remove an effect from the row.
        :param effect: The effect to remove.
        """
        if effect in self.effects:
            self.effects.remove(effect)

    def calculate_score(self):
        """
        Calculate the total score of the row, considering active effects.
        :return: Total score of the row.
        """
        total_score = 0
        for card in self.cards:
            card_strength = card.strength or 0

            # Apply effects (e.g., weather reduces strength to 1)
            if "weather" in self.effects:
                card_strength = 1 if card.strength is not None else 0

            total_score += card_strength
        return total_score


class Board:
    def __init__(self):
        """
        Initialize the game board with rows for both players.
        """
        self.player_rows = {
            "close": Row("close"),
            "ranged": Row("ranged"),
            "siege": Row("siege"),
        }
        self.ai_rows = {
            "close": Row("close"),
            "ranged": Row("ranged"),
            "siege": Row("siege"),
        }

    def place_card(self, card, player_type):
        """
        Place a card on the board.
        :param card: The card to place.
        :param player_type: "player" or "ai" to indicate whose row to place the card on.
        """
        target_rows = self.player_rows if player_type == "player" else self.ai_rows
        target_row = target_rows.get(card.row)

        if target_row:
            target_row.add_card(card)

    def calculate_total_score(self, player_type):
        """
        Calculate the total score for the specified player.
        :param player_type: "player" or "ai".
        :return: Total score for the player.
        """
        target_rows = self.player_rows if player_type == "player" else self.ai_rows
        return sum(row.calculate_score() for row in target_rows.values())

    def apply_effect_to_all_rows(self, effect, player_type):
        """
        Apply an effect (e.g., weather) to all rows for the specified player.
        :param effect: The effect to apply.
        :param player_type: "player" or "ai".
        """
        target_rows = self.player_rows if player_type == "player" else self.ai_rows
        for row in target_rows.values():
            row.apply_effect(effect)

    def clear_effects(self, player_type):
        """
        Clear all effects from the rows for the specified player.
        :param player_type: "player" or "ai".
        """
        target_rows = self.player_rows if player_type == "player" else self.ai_rows
        for row in target_rows.values():
            row.effects = []

    def scorch_highest_units(self):
        """
        Scorch the highest-strength units on the board for both players.
        """
        for player_type in ["player", "ai"]:
            target_rows = self.player_rows if player_type == "player" else self.ai_rows
            max_strength = max(
                (card.strength for row in target_rows.values() for card in row.cards if card.strength), default=0
            )
            for row in target_rows.values():
                row.cards = [card for card in row.cards if card.strength != max_strength]    