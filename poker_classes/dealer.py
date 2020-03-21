import random as random

class Dealer():

    def __init__(self):
        self.new_deck=[(rank, suit) for rank in range(1,14) for suit in ['S','H','C','D']]
        self.dealer_position=0

    def shuffle_deck(self,deck):
        random.shuffle(deck)
        return deck

    def deal_card(self,deck):
        card=deck.pop(0)
        return card
