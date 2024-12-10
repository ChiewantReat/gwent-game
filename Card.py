import pygame
import sys
import random

class Card:
    def __init__(self, name, strength, row, ability=None, image_path=None):
        """
        Initialize a card with its properties.

        :param name: The name of the card (string).
        :param strength: The strength value of the card (integer).
        :param row: The row type ('close', 'ranged', or 'siege').
        :param ability: The special ability of the card, if any (string).
        :param image_path: Path to the card's image (string).
        """
        self.name = name
        self.strength = strength
        self.row = row  # 'close', 'ranged', or 'siege'
        self.ability = ability
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
            # Draw the card's image
            screen.blit(self.image, (x, y))
        else:
            # Fallback: Draw a blank card with text
            pygame.draw.rect(screen, (255, 255, 255), (x, y, 120, 180))  # Card background
            font = pygame.font.Font(None, 24)
            name_text = font.render(self.name, True, (0, 0, 0))
            strength_text = font.render(f"Strength: {self.strength}", True, (0, 0, 0))
            screen.blit(name_text, (x + 10, y + 10))
            screen.blit(strength_text, (x + 10, y + 50))


# Northern Realms Deck
northern_realms_deck = [
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
nilfgaardian_deck = [
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
neutral_deck = [
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
special_cards = [
    Card("Decoy", None, None, "decoy", "special", "special_decoy.jpg"),
    Card("Biting Frost", None, None, "frost", "weather", "weather_frost.jpg"),
    Card("Impenetrable Fog", None, None, "fog", "weather", "weather_fog.jpg"),
    Card("Torrential Rain", None, None, "rain", "weather", "weather_rain.jpg"),
    Card("Clear Weather", None, None, "clear", "weather", "weather_clear.jpg"),
    Card("Commander’s Horn", None, None, "horn", "special", "special_horn.jpg"),
    Card("Scorch", None, None, "scorch", "special", "special_scorch.jpg"),
]