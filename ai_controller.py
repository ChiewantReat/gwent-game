import random

class AIController:
    def __init__(self, player, board):
        """
        Initialize the AIController.
        :param player: The AI player object (Player class instance).
        :param board: The game board (Board class instance).
        """
        self.player = player
        self.board = board

    def decide_action(self, opponent_score):
        """
        Decide whether the AI will play a card, pass, or activate a leader ability.
        :param opponent_score: The current score of the opponent.
        :return: The chosen action ('play_card', 'pass', or 'leader_ability').
        """
        # If AI has no cards left, it must pass
        if not self.player.hand:
            return "pass"

        # Weight-based decision-making
        if self.player.total_score >= opponent_score:
            # More likely to pass if ahead
            actions = ["play_card", "pass"]
            weights = [0.4, 0.6]
        else:
            # More likely to play a card if behind
            actions = ["play_card", "leader_ability"]
            weights = [0.7, 0.3]

        return random.choices(actions, weights)[0]

    def choose_card(self):
        """
        Choose a card to play from the AI's hand.
        :return: The selected card (Card object).
        """
        # Basic logic: prioritize high-strength cards
        highest_strength_card = max(
            (card for card in self.player.hand if card.strength is not None),
            key=lambda card: card.strength,
            default=None
        )
        return highest_strength_card or random.choice(self.player.hand)

    def activate_leader(self):
        """
        Activate the AI's leader ability if available.
        """
        if not self.player.leader_used and self.player.leader_card:
            print(f"AI activates leader ability: {self.player.leader_card.name}")
            self.player.activate_leader()
        else:
            print("AI cannot use leader ability.")

    def play_turn(self, opponent_score):
        """
        Execute the AI's turn based on its decision.
        :param opponent_score: The current score of the opponent.
        """
        action = self.decide_action(opponent_score)

        if action == "play_card":
            selected_card = self.choose_card()
            if selected_card:
                self.player.hand.remove(selected_card)
                self.board.place_card(selected_card, "ai")
                print(f"AI plays {selected_card.name} ({selected_card.strength if selected_card.strength else 'Special'})")

                # Handle special abilities
                if selected_card.ability:
                    self.handle_special_ability(selected_card, "ai")

        elif action == "leader_ability":
            self.activate_leader()

        elif action == "pass":
            self.player.pass_round()
            print("AI passes the round.")

    def handle_special_ability(self, card, player_type):
        """
        Handle special abilities of the played card.
        :param card: The card with a special ability.
        :param player_type: The player type ("player" or "ai").
        """
        opponent_type = "player" if player_type == "ai" else "ai"
        if card.ability == "Spy":
            print(f"{card.name}: Spy ability activated!")
            self.board.place_card(card, opponent_type)
            self.player.hand.extend(self.player.deck.draw(2))
        elif card.ability == "Scorch":
            print(f"{card.name}: Scorch ability activated!")
            self.board.scorch_highest_units()
        elif card.ability == "Medic":
            resurrected_card = self.player.resurrect_card()
            if resurrected_card:
                self.board.place_card(resurrected_card, player_type)
                print(f"AI resurrects {resurrected_card.name}")
            else:
                print("No cards available to resurrect.")
        elif card.ability in ["Frost", "Fog", "Rain"]:
            print(f"{card.name}: Weather ability activated ({card.ability})!")
            self.board.apply_effect_to_all_rows("weather", opponent_type)
        elif card.ability == "Horn":
            print(f"{card.name}: Commander's Horn activated!")
            self.board.apply_effect_to_all_rows("horn", player_type)
