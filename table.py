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
        print(''.join([str(this_card[0]),this_card[1]]),end=',')
    print('')

for h in alba.hands:
    for c in h:
        this_card=cards.get_simple_u_card_p(c)
        print(c,this_card[0],this_card[1])

start=dt.datetime.now()
a=[[3,2,5,4,2],[3,3,5,4,5],[3,3,4,3,5],[3,5,4,7,6],[3,3,5,3,5],[3,3,5,3,3],]
b=[[(3,'H'),(2,'C'),(5,'C'),(4,'D'),(2,'H')],[(3,'H'),(3,'C'),(5,'C'),(4,'D'),(5,'H')],
    [(3,'H'),(4,'H'),(3,'C'),(7,'H'),(3,'D')],
    [(3,'H'),(2,'H'),(8,'H'),(4,'H'),(9,'H')],[(3,'H'),(6,'C'),(5,'C'),(4,'D'),(7,'H')],
    [(3,'H'),(2,'H'),(3,'C'),(3,'D'),(2,'S')],[(3,'H'),(3,'C'),(5,'C'),(3,'D'),(3,'S')],
    [(3,'H'),(5,'H'),(4,'H'),(6,'H'),(2,'H')],[(3,'H'),(1,'H'),(4,'H'),(6,'S'),(2,'H')],
]
#for k in range(2000):
for c in b:
        rank=dealer.rank_hands(c)
        print(c,rank)
end=dt.datetime.now()

time_elapsed=end-start
print('time in seconds: ',time_elapsed.total_seconds())

c=[1,2,3,4,5,6,7,8,9,10,11]

print(len(list(combinations(c,4))))
print(len(list(combinations(c,3))))
print(len(list(combinations(c,2))))
print(len(list(combinations(c,1))))
