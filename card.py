import pygame
import sys
import random

class Card:
    def __init__(self, name, strength, row, ability=None, deck_type="faction", image_path=None):
        """
        Base class for all cards.

        :param name: The name of the card (string).
        :param strength: The strength value of the card (integer or None for special cards).
        :param row: The row type ('close', 'ranged', 'siege', 'agile', or None for special cards).
        :param ability: The special ability of the card (string).
        :param deck_type: The deck type ('faction', 'neutral', 'special', 'weather').
        :param image_path: Path to the card's image (string).
        """
        self.name = name
        self.strength = strength
        self.row = row
        self.ability = ability
        self.deck_type = deck_type
        self.image_path = image_path
        self.image = None

        # Load the card image if an image path is provided
        if self.image_path:
            self.image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(self.image, (120, 180))  # Resize to standard card dimensions

    def render(self, screen, x, y):
        """
        Render the card at the specified position on the screen.

        :param screen: The Pygame display surface.
        :param x: The x-coordinate of the card's position.
        :param y: The y-coordinate of the card's position.
        """
        if self.image:
            screen.blit(self.image, (x, y))  # Draw the card image
        else:
            pygame.draw.rect(screen, (255, 255, 255), (x, y, 120, 180))  # Placeholder rectangle
            font = pygame.font.Font(None, 24)
            name_text = font.render(self.name, True, (0, 0, 0))
            if self.strength is not None:
                strength_text = font.render(f"Strength: {self.strength}", True, (0, 0, 0))
                screen.blit(strength_text, (x + 10, y + 50))
            screen.blit(name_text, (x + 10, y + 10))

    def activate_ability(self, board, player_type, opponent_type):
        """
        Activate the card's ability on the board.
        :param board: The game board (Board object).
        :param player_type: The player who played the card ("player" or "ai").
        :param opponent_type: The opponent ("player" or "ai").
        """
        if self.ability == "Spy":
            print(f"{self.name}: Spy ability activated!")
            board.place_card(self, opponent_type)  # Play on the opponent's side
            return "draw_two"  # Player draws two cards
        elif self.ability == "Scorch":
            print(f"{self.name}: Scorch ability activated!")
            return "scorch"  # Signal to scorch logic
        elif self.ability == "Medic":
            print(f"{self.name}: Medic ability activated!")
            return "resurrect"  # Signal to resurrect logic
        elif self.ability in ["Frost", "Fog", "Rain"]:
            print(f"{self.name}: Weather ability activated ({self.ability})!")
            board.apply_effect_to_all_rows("weather", player_type)
        elif self.ability == "Horn":
            print(f"{self.name}: Commander's Horn activated!")
            board.apply_effect_to_all_rows("horn", player_type)
        else:
            print(f"{self.name}: No special ability.")


# Specialized Card Classes
class HeroCard(Card):
    def __init__(self, name, strength, row, image_path=None):
        super().__init__(name, strength, row, "Hero", "faction", image_path)


class WeatherCard(Card):
    def __init__(self, name, ability, image_path=None):
        super().__init__(name, None, None, ability, "weather", image_path)


class SpecialCard(Card):
    def __init__(self, name, ability, image_path=None):
        super().__init__(name, None, None, ability, "special", image_path)


# Deck Initialization
def create_card(data):
    """Create a card from a dictionary of attributes."""
    if data["type"] == "Hero":
        return HeroCard(data["name"], data["strength"], data["row"], data["image_path"])
    elif data["type"] == "Weather":
        return WeatherCard(data["name"], data["ability"], data["image_path"])
    elif data["type"] == "Special":
        return SpecialCard(data["name"], data["ability"], data["image_path"])
    else:
        return Card(data["name"], data["strength"], data["row"], data["ability"], data["image_path"])


def initialize_deck(deck_data):
    """
    Initialize a deck from a list of card dictionaries or pre-created Card objects.
    :param deck_data: List of card data (dictionary or Card objects).
    :return: List of Card objects.
    """
    # If items are dictionaries, convert them to Card objects
    if isinstance(deck_data[0], dict):
        return [create_card(card_data) for card_data in deck_data]
    # If items are already Card objects, return as is
    return deck_data

# Northern Realms Deck
northern_realms_data = [
    Card("Blue Stripes Commando", 4, "close", "Tight Bond", "realms_blue_stripes.jpg"),
    Card("Poor Fucking Infantry", 1, "close", "Tight Bond", "realms_poor_infantry.jpg"),
    Card("Siegfried of Denesle", 5, "close", None, "realms_siegfried.jpg"),
    Card("Ves", 5, "close", None, "realms_ves.jpg"),
    Card("Yarpen Zigrin", 2, "close", None, "realms_yarpen.jpg"),
    Card("Crinfrid Reavers Dragon Hunter", 5, "ranged", "Tight Bond", "realms_crinfrid.jpg"),
    Card("Keira Metz", 5, "ranged", None, "realms_keira.jpg"),
    Card("Sabrina Glevissig", 4, "ranged", None, "realms_sabrina.jpg"), # to be further implemented 
    Card("Sheldon Skaggs", 4, "ranged", None, "realms_sheldon.jpg"),
    Card("Síle de Tansarville", 5, "ranged", None, "realms_sheala.jpg"),
    Card("Ballista", 6, "siege", None, "realms_ballista.jpg"),
    Card("Catapult", 8, "siege", "Tight Bond", "realms_catapult_1.jpg"),
    Card("Trebuchet", 6, "siege", None, "realms_trebuchet.jpg"),
    Card("Siege Tower", 6, "siege", None, "realms_siege_tower.jpg"),
    Card("Kaedweni Siege Expert", 1, "siege", "Morale Boost", "realms_kaedwen_siege.jpg"),
    Card("Esterad Thyssen", 10, "close", "Hero", "realms_esterad.jpg"),
    Card("John Natalis", 10, "close", "Hero", "realms_natalis.jpg"),
    Card("Philippa Eilhart", 10, "ranged", "Hero", "realms_philippa.jpg"),
    Card("Vernon Roche", 10, "close", "Hero", "realms_vernon.jpg"),
    Card("Dun Banner Medic", 5, "siege", "Medic", "realms_banner_nurse.jpg"),
    Card("Prince Stennis", 5, "close", "Spy", "realms_stennis.jpg"),
    Card("Sigismund Dijkstra", 4, "close", "Spy", "realms_dijkstra.jpg"),
    Card("Thaler", 1, "close", "Spy", "realms_thaler.jpg")
]

# Nilfgaardian Empire Deck
nilfgaardian_data = [
    Card("Impera Brigade Guard", 3, "close", "Tight Bond", "nilfgaard_imperal_brigade.jpg"),
    Card("Nausicaa Cavalry Rider", 2, "close", "Tight Bond", "nilfgaard_nauzicaa_2.jpg"),
    Card("Black Infantry Archer", 10, "close", None, "nilfgaard_black_archer.jpg"),
    Card("Renuald aep Matsen", 5, "close", None, "nilfgaard_renuald.jpg"),
    Card("Sweers", 2, "close", None, "nilfgaard_sweers.jpg"),
    Card("Albrich", 2, "ranged", None, "nilfgaard_albrich.jpg"),
    Card("Assire var Anahid", 6, "ranged", None, "nilfgaard_assire.jpg"),
    Card("Cynthia", 4, "ranged", None, "nilfgaard_cynthia.jpg"),
    Card("Fringilla Vigo", 6, "ranged", None, "nilfgaard_fringilla.jpg"),
    Card("Vanhemar", 4, "ranged", None, "nilfgaard_vanhemar.jpg"),
    Card("Heavy Zerrikanian Fire Scorpion", 10, "siege", None, "nilfgaard_heavy_zerri.jpg"),
    Card("Siege Engineer", 6, "siege", None, "nilfgaard_siege_engineer.jpg"),
    Card("Siege Technician", 0, "siege", "Medic", "nilfgaard_siege_support.jpg"),
    Card("Etolian Auxiliary Archers", 1, "siege", "Medic", "nilfgaard_archer_support.jpg"),
    Card("Rotten Mangonel", 3, "siege", None, "nilfgaard_rotten.jpg"),
    Card("Letho of Gulet", 10, "close", "Hero", "nilfgaard_letho.jpg"),
    Card("Menno Coehoorn", 10, "close", "Hero", "nilfgaard_menno.jpg"),
    Card("Morvran Voorhis", 10, "close", "Hero", "nilfgaard_moorvran.jpg"),
    Card("Tibor Eggebracht", 10, "ranged", "Hero", "nilfgaard_tibor.jpg"),
    Card("Shilard Fitz-Oesterlen", 7, "close", "Spy", "nilfgaard_shilard.jpg"),
    Card("Vattier de Rideaux", 4, "close", "Spy", "nilfgaard_vattier.jpg"),
    Card("Stephan Skellen", 9, "close", "Spy", "nilfgaard_stefan.jpg")
]

# Neutral Deck
neutral_data = [
    Card("Geralt of Rivia", 15, "close", "Hero", "neutral_geralt (1).jpg"),
    Card("Cirilla Fiona Elen Riannon", 15, "close", "Hero", "neutral_ciri (1).jpg"),
    Card("Yennefer of Vengerberg", 7, "ranged", "Hero Medic", "neutral_yennefer.jpg"),
    Card("Triss Merigold", 7, "close", "Hero", "neutral_triss.jpg"),
    Card("Villentretenmerth", 7, "close", "Scorch Close", "neutral_villen.jpg"),
    Card("Dandelion", 2, "close", "Commander Horn", "neutral_dandelion.jpg"),
    Card("Zoltan Chivay", 5, "close", None, "neutral_zoltan.jpg"),
    Card("Vesemir", 6, "close", None, "neutral_vesemir.jpg"),
    Card("Emiel Regis Rohellec Terzieff", 5, "close", None, "neutral_emiel.jpg"),
    Card("Olgierd von Everec", 6, "agile", "Morale Boost", "neutral_olgierd.jpg"),
]

# Special Cards Initialization
special_cards_data = [
    Card("Decoy", None, None, "decoy", "special", "special_decoy.jpg"),
    Card("Biting Frost", None, None, "frost", "weather", "weather_frost.jpg"),
    Card("Impenetrable Fog", None, None, "fog", "weather", "weather_fog.jpg"),
    Card("Torrential Rain", None, None, "rain", "weather", "weather_rain.jpg"),
    Card("Clear Weather", None, None, "clear", "weather", "weather_clear.jpg"),
    Card("Commander’s Horn", None, None, "horn", "special", "special_horn.jpg"),
    Card("Scorch", None, None, "scorch", "special", "special_scorch.jpg"),
]

northern_realms_deck = initialize_deck(northern_realms_data)
nilfgaardian_deck = initialize_deck(nilfgaardian_data)
neutral_deck = initialize_deck(neutral_data)
special_cards = initialize_deck(special_cards_data)

__all__ = ["northern_realms_deck", "nilfgaardian_deck", "neutral_deck", "special_cards"]
