import random
from player import Player
from board import Board
from ai_controller import AIController
from gui import GUI

class Game:
    def __init__(self, player, ai, screen):
        """
        Initialize the Game object.

        :param player: The human player (Player object).
        :param ai: The AI opponent (Player object).
        :param screen: Pygame screen object for rendering.
        """
        self.player = player
        self.ai = ai
        self.screen = screen
        self.board = Board()
        self.gui = GUI(screen)  # Initialize GUI
        self.ai_controller = AIController(ai, self.board)
        self.rounds_played = 0
        self.current_turn = None  # 'player' or 'ai'

    def coin_toss(self):
        """
        Perform a coin toss to determine who goes first.
        """
        self.current_turn = random.choice(['player', 'ai'])
        self.gui.show_notification(f"Coin toss result: {self.current_turn.capitalize()} goes first!")

    def redraw_phase(self):
        """
        Allow both players to redraw up to 2 cards from their initial hand.
        """
        self.gui.show_notification("Redraw phase: Replace up to 2 cards.")

        # Player redraw logic
        player_replacements = []
        while len(player_replacements) < 2:
            self.gui.draw_hand(self.player.hand)
            self.gui.update_screen()
            print("Your hand:")
            for idx, card in enumerate(self.player.hand):
                print(f"{idx + 1}. {card.name} ({card.strength if card.strength else 'Special'})")
            choice = input("Enter card number to replace (or press Enter to finish): ")
            if not choice:
                break
            try:
                choice = int(choice) - 1
                if 0 <= choice < len(self.player.hand):
                    player_replacements.append(self.player.hand[choice])
            except ValueError:
                print("Invalid input. Try again.")

        for card in player_replacements:
            self.player.hand.remove(card)
            self.player.hand.append(self.player.deck.draw(1)[0])

        # AI redraw logic
        self.ai_controller.play_turn(None)  # AI will perform a redraw as part of its logic

    def start_round(self):
        """
        Initialize a new round.
        """
        self.rounds_played += 1
        self.player.reset_round()
        self.ai.reset_round()
        self.gui.show_notification(f"Starting round {self.rounds_played}!")

    def end_round(self):
        """
        End the current round, determine the winner, and update health.
        """
        player_score = self.board.calculate_total_score("player")
        ai_score = self.board.calculate_total_score("ai")

        self.gui.show_notification(f"End of round {self.rounds_played}!")
        self.gui.show_notification(f"Player Score: {player_score}, AI Score: {ai_score}")

        if player_score > ai_score:
            self.ai.health -= 1
            self.gui.show_notification("You win the round!")
        elif ai_score > player_score:
            self.player.health -= 1
            self.gui.show_notification("AI wins the round!")
        else:
            self.gui.show_notification("Round is a tie!")

        self.board = Board()  # Reset the board for the next round

    def is_game_over(self):
        """
        Check if the game is over.
        :return: True if the game is over, False otherwise.
        """
        return self.player.health == 0 or self.ai.health == 0

    def play_turn(self):
        """
        Handle a single turn of the game.
        """
        if self.current_turn == "player":
            self.gui.show_notification("Your turn!")
            selected_card = None
            while not selected_card:
                self.gui.draw_board(self.board, self.player.total_score, self.ai.total_score)
                self.gui.draw_hand(self.player.hand)
                self.gui.update_screen()

                # Prompt player to choose a card
                print("Your hand:")
                for idx, card in enumerate(self.player.hand):
                    print(f"{idx + 1}. {card.name} ({card.strength if card.strength else 'Special'})")
                choice = input("Choose a card to play (Enter card number): ")
                try:
                    choice = int(choice) - 1
                    if 0 <= choice < len(self.player.hand):
                        selected_card = self.player.hand.pop(choice)
                        self.board.place_card(selected_card, "player")
                        self.gui.show_notification(f"You played: {selected_card.name}")
                        if selected_card.ability:
                            self.handle_special_ability(selected_card, "player")
                except ValueError:
                    print("Invalid input. Try again.")

            self.current_turn = "ai"

        elif self.current_turn == "ai":
            self.gui.show_notification("AI's turn!")
            self.ai_controller.play_turn(self.board.calculate_total_score("player"))
            self.current_turn = "player"

    def handle_special_ability(self, card, player_type):
        """
        Handle special abilities of the played card.
        :param card: The card with a special ability.
        :param player_type: The player type ("player" or "ai").
        """
        opponent_type = "player" if player_type == "ai" else "ai"
        if card.ability == "Spy":
            self.board.place_card(card, opponent_type)
            self.player.hand.extend(self.player.deck.draw(2))
            self.gui.show_notification(f"{card.name}: Spy activated!")
        elif card.ability == "Scorch":
            self.board.scorch_highest_units()
            self.gui.show_notification(f"{card.name}: Scorch activated!")
        elif card.ability == "Medic":
            resurrected_card = self.player.resurrect_card()
            if resurrected_card:
                self.board.place_card(resurrected_card, player_type)
                self.gui.show_notification(f"{player_type} resurrects {resurrected_card.name}")
            else:
                self.gui.show_notification("No cards available to resurrect.")
        elif card.ability in ["Frost", "Fog", "Rain"]:
            self.board.apply_effect_to_all_rows("weather", opponent_type)
            self.gui.show_notification(f"{card.name}: Weather ({card.ability}) activated!")
        elif card.ability == "Horn":
            self.board.apply_effect_to_all_rows("horn", player_type)
            self.gui.show_notification(f"{card.name}: Commander's Horn activated!")

    def run(self):
        """
        Main game loop.
        """
        self.gui.show_notification("Starting the game!")
        self.coin_toss()

        # Redraw phase
        self.redraw_phase()

        # Main game loop
        while not self.is_game_over():
            self.start_round()

            # Round loop
            while not (self.player.passed and self.ai.passed):
                self.play_turn()

            self.end_round()

        # Determine winner
        if self.player.health > self.ai.health:
            self.gui.show_notification("Congratulations! You win the game!")
        else:
            self.gui.show_notification("The AI wins. Better luck next time!")
