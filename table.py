import os
import pandas as pd

from poker_classes.player import Player
from poker_classes.dealer import Dealer

working_dir=os.getcwd()
app_dir=working_dir+'/poker_classes/'
player_dir=working_dir+'/existing_players/'

alba=Player(player_dir,name='John Alba',nickname='JohnAlba')
bornstein=Player(player_dir,name='Bill Murphy',nickname='Bornstein')
clyde=Player(player_dir,name='Bob Vincent',nickname='Clyde')

players=[alba,bornstein,clyde]

bornstein.add_funds(500)
clyde.add_funds(1000)

dealer=Dealer()
deck=dealer.new_deck.copy()
shuffled=dealer.shuffle_deck(deck)


num_hands=2

for card in range(2):
    for p in players:
        for hand in range(num_hands):

            p.hands[hand].append(dealer.deal_card(shuffled))


for p in players:
    print(p.p_nickname,p.bankroll,p.hands)
print(f"Cards remaining in deck {len(shuffled)}")
