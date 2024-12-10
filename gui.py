import pygame
from pygame.locals import *

class GUI:
    def __init__(self, screen):
        """
        Initialize the GUI.
        :param screen: Pygame screen object for rendering.
        """
        self.screen = screen
        self.font = pygame.font.Font(None, 36)

    def draw_board(self, board, player_score, ai_score):
        """
        Render the game board with rows, scores, and effects.
        :param board: The Board object containing row data.
        :param player_score: Player's current total score.
        :param ai_score: AI's current total score.
        """
        self.screen.fill((0, 128, 0))  # Green background

        # Draw AI rows
        y_offset = 50
        for row_name, row in board.ai_rows.items():
            self.draw_row(row, y_offset, row_name, "AI")
            y_offset += 150

        # Draw Player rows
        y_offset = 450
        for row_name, row in board.player_rows.items():
            self.draw_row(row, y_offset, row_name, "Player")
            y_offset += 150

        # Display scores
        self.draw_text(f"Player Score: {player_score}", 50, 650)
        self.draw_text(f"AI Score: {ai_score}", 50, 20)

    def draw_row(self, row, y_offset, row_name, owner):
        """
        Render a single row on the board.
        :param row: The Row object to render.
        :param y_offset: Vertical offset for the row.
        :param row_name: The name of the row (e.g., "close").
        :param owner: The owner of the row ("Player" or "AI").
        """
        # Row label
        self.draw_text(f"{owner} {row_name.capitalize()} Row", 50, y_offset - 30)

        # Draw cards in the row
        x_offset = 50
        for card in row.cards:
            self.draw_card(card, x_offset, y_offset)
            x_offset += 140

        # Draw effects
        effect_text = ", ".join(row.effects) if row.effects else "No Effects"
        self.draw_text(f"Effects: {effect_text}", 50, y_offset + 100)

    def draw_card(self, card, x, y):
        """
        Render a single card.
        :param card: The Card object to render.
        :param x: Horizontal position.
        :param y: Vertical position.
        """
        if card.image:
            self.screen.blit(card.image, (x, y))
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), (x, y, 120, 180))
            self.draw_text(card.name, x + 10, y + 10)

    def draw_hand(self, hand, selected_index=None):
        """
        Render the player's hand.
        :param hand: List of Card objects in the player's hand.
        :param selected_index: Highlight the selected card if applicable.
        """
        x_offset = 50
        y_offset = 700
        for index, card in enumerate(hand):
            if index == selected_index:
                pygame.draw.rect(self.screen, (255, 255, 0), (x_offset - 5, y_offset - 5, 130, 190), 5)  # Highlight
            self.draw_card(card, x_offset, y_offset)
            x_offset += 140

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        """
        Render text on the screen.
        :param text: Text to render.
        :param x: Horizontal position.
        :param y: Vertical position.
        :param color: Color of the text.
        """
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def update_screen(self):
        """
        Refresh the screen.
        """
        pygame.display.flip()

    def show_notification(self, message):
        """
        Display a notification or turn message.
        :param message: Notification message to display.
        """
        self.draw_text(message, 600, 360, color=(255, 0, 0))  # Centered notification
        self.update_screen()
        pygame.time.wait(2000)  # Display for 2 seconds
