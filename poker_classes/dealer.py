import random as random

class Dealer():
    '''The dealer class is responsible for moving the cards, and holding the
    common cards.'''

    def __init__(self):
        self.new_deck=[(rank, suit) for rank in range(1,14) for suit in ['S','H','C','D']]
        self.dealer_position=0
        self.common_cards=[]

    def shuffle_deck(self,deck):
        random.shuffle(deck)
        return deck

    def deal_card(self,deck):
        card=deck.pop(0)
        return card,deck

    def deal_cards(self,players,game):

        new_deck=self.new_deck.copy()
        shuffled=self.shuffle_deck(new_deck)

        #deal
        for p in players:
            p.hands=game.hands

        for p in players:
            card_count=0
            p.hands=[[] for x in game.hands_count]
            for i,c in enumerate(game.hands_count):
                for h in range(c):

                    if card_count<c:
                        card,shuffled=self.deal_card(shuffled)
                        p.hands[i].append(card)

                    else:
                        pass
            card_count+=1

        self.common_cards=[[] for x in range(len(game.common_cards))]
        for i,flip in enumerate(game.common_cards):
            for f in range(flip):
                card,shuffled=self.deal_card(shuffled)
                self.common_cards[i].append(card)

        return shuffled
