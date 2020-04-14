'''test_ranking.py holds the game logic for the poker game.'''

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


start=dt.datetime.now()

b=[[(3,'H'),(2,'C'),(5,'C'),(4,'D'),(2,'H')],[(3,'H'),(3,'C'),(5,'C'),(4,'D'),(5,'H')],
    [(3,'H'),(4,'H'),(3,'C'),(7,'H'),(3,'D')],
    [(3,'H'),(2,'H'),(8,'H'),(4,'H'),(9,'H')],[(3,'H'),(6,'C'),(5,'C'),(4,'D'),(7,'H')],
    [(3,'H'),(2,'H'),(3,'C'),(3,'D'),(2,'S')],[(3,'H'),(3,'C'),(5,'C'),(3,'D'),(3,'S')],
    [(3,'H'),(5,'H'),(4,'H'),(6,'H'),(2,'H')],[(3,'H'),(1,'H'),(4,'H'),(6,'S'),(2,'H')],
]

test_loops=10000
for k in range(test_loops):
    for c in b:
            rank=dealer.rank_single_hand(c)

end=dt.datetime.now()

time_elapsed=end-start
print(f'Evaluated {test_loops*len(b)} hands, time in seconds: {time_elapsed.total_seconds()}')
