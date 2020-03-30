'''table.py holds the game logic for the poker game.'''

import os
import pandas as pd
import datetime as dt
from itertools import combinations

from poker_classes.player import Player
from poker_classes.dealer import Dealer
from poker_classes.game import Game
from poker_classes.cards import Cards

working_dir=os.getcwd()
app_dir=working_dir+'/poker_classes/'
player_dir=working_dir+'/existing_players/'

this_game=Game()
this_game.set_pic_a_wheel()

dealer=Dealer()

alba=Player(player_dir,name='John Alba',nickname='JohnAlba')
bornstein=Player(player_dir,name='Bill Murphy',nickname='Bornstein')
clyde=Player(player_dir,name='Bob Vincent',nickname='Clyde')

players=[alba,bornstein,clyde]

alba.add_funds(500)
bornstein.add_funds(500)
clyde.add_funds(500)



shuffled=dealer.deal_cards(players,this_game)
for p in players:
    print(p.p_nickname,p.bankroll,p.hands,p.common_cards)

print(f"Common Cards: {dealer.common_cards}")
print(f"Cards remaining in deck {len(shuffled)}")

cards=Cards()
for h in dealer.common_cards:
    for c in h:
        this_card=cards.get_simple_u_card_p(c)
        print(''.join([str(this_card[0]),this_card[1]]),end=',')
    print('')

for h in alba.hands:
    for c in h:
        this_card=cards.get_simple_u_card_p(c)
        print('Alba hand: ',c,this_card[0],this_card[1])

for c in alba.common_cards:
    this_card=cards.get_simple_u_card_p(c)
    print('Alba common: ',c,this_card[0],this_card[1])


# Deal Round:
for bet_rnd in range(this_game.betting_rounds):
    print(f'Round{bet_rnd}: Betting on:')
    for com_flip in range(len(dealer.common_cards)):
        if dealer.common_cards_flipped[com_flip]:
            print(dealer.common_cards[com_flip])
        else:
            print(['X' for x in dealer.common_cards[com_flip]])
    if bet_rnd<this_game.betting_rounds-1:
        dealer.common_cards_flipped[bet_rnd]=True


    for p in players:
        print(p.p_nickname,p.hands,p.common_cards)

        # Fold decisions for player
        p.fold_decisions()
        p.open_bet_decisions(dealer,this_game)

    print(f"After round {bet_rnd} of betting, the following hands remain:")
    for p in players:
        for h in p.hands:
            if h!='folded':
                print(p.p_nickname,h,p.common_cards)



alba.add_funds(50)
bornstein.add_funds(75)
clyde.add_funds(100)
alba.save_player_data()
bornstein.save_player_data()
clyde.save_player_data()
