class Player:
    def __init__(self, name, deck):
        self.name = name
        self.deck = deck
        self.hand = []
        self.graveyard = []

    def draw_hand(self, draw_function, count=10):
        self.hand, self.deck = draw_function(self.deck, count)

    def play_card(self, card):
        if card in self.hand:
            self.hand.remove(card)
            return card
        return None
