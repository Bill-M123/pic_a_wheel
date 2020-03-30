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
print('Funds added')

shuffled=dealer.deal_cards(players,this_game)
print('Player cards dealt.')
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

#for h in alba.hands:
#    for c in h:
#        this_card=cards.get_simple_u_card_p(c)
#        print('Alba hand: ',c,this_card[0],this_card[1])

#for c in alba.common_cards:
#    this_card=cards.get_simple_u_card_p(c)
#    print('Alba common: ',c,this_card[0],this_card[1])


# Betting Rounds:
for bet_rnd in range(this_game.betting_rounds):
    print(f'Round{bet_rnd}: Betting on:')

    #Reset round variables
    dealer.who_opened='No one'
    dealer.last_raise='No one'
    dealer.round_complete=False

    # Show flipped common cards
    for com_flip in range(len(dealer.common_cards)):
        if dealer.common_cards_flipped[com_flip]:
            print(dealer.common_cards[com_flip])
        else:
            print(['X' for x in dealer.common_cards[com_flip]])
    if bet_rnd<this_game.betting_rounds-1:
        dealer.common_cards_flipped[bet_rnd]=True

    times_around=0 #Set flag to assure at least one trip around table

    # Check for completely folded hands:
    dealer.check_which_players_are_folded(players)
    remaining_players=[x for x in players if x.in_hand]
    print(f"Remaining Players: {[p.p_name for p in remaining_players]}\n")

    while (dealer.round_complete==False):

        for p in remaining_players:
            print(f'Action to: {p.p_nickname}, last raise: {dealer.last_raise}')

            if (dealer.who_opened=='No one')|(p.this_round_per_side<dealer.bet_per_side):

                p.fold_decisions()  # Fold decisions for player
                p.open_bet_decisions(p,dealer,this_game) #All actions for player this round
                #print(f"{p.p_nickname} has {p.in_pot} in the pot.")


        dealer.check_which_players_are_folded(players)
        remaining_players=[x for x in players if x.in_hand]
        all_bets=[b.this_round_per_side for b in remaining_players]

        bet_check=len(list(set(all_bets)))
        if bet_check==1:
            #print('found bet_check')
            dealer.round_complete=True
        else:
            dealer.round_complete=False
            #print('bets not equal')

        times_around+=1

        print(f"Times around {times_around}, remaining: {[x.p_nickname for x in remaining_players]}")
        print(f"bets: {all_bets}, round complete: {dealer.round_complete}")
        print(f'Different bets{len(set(all_bets))}\n\n')

    print(f"\n\nAfter round {bet_rnd} of betting, the following hands remain:")
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
