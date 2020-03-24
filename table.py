'''table.py holds the game logic for the poker game.'''

import os
import pandas as pd

from poker_classes.player import Player
from poker_classes.dealer import Dealer
from poker_classes.game import Game
from poker_classes.cards import Cards

working_dir=os.getcwd()
app_dir=working_dir+'/poker_classes/'
player_dir=working_dir+'/existing_players/'

alba=Player(player_dir,name='John Alba',nickname='JohnAlba')
bornstein=Player(player_dir,name='Bill Murphy',nickname='Bornstein')
clyde=Player(player_dir,name='Bob Vincent',nickname='Clyde')

players=[alba,bornstein,clyde]

bornstein.add_funds(500)
clyde.add_funds(1000)

this_game=Game()
this_game.set_pic_a_wheel()
print(f'This game hands: {this_game.hands} ')
dealer=Dealer()

shuffled=dealer.deal_cards(players,this_game)
for p in players:
    print(p.p_nickname,p.bankroll,p.hands)

print(f"Common Cards: {dealer.common_cards}")
print(f"Cards remaining in deck {len(shuffled)}")

cards=Cards()
for h in dealer.common_cards:
    for c in h:
        this_card=cards.get_simple_u_card_p(c)
        print(c,this_card[0],this_card[1])

for h in alba.hands:
    for c in h:
        this_card=cards.get_simple_u_card_p(c)
        print(c,this_card[0],this_card[1])
