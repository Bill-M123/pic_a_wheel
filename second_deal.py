from flask import Flask
from flask import render_template

#########################
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

cards=Cards()
this_game=Game()
this_game.set_pic_a_wheel()

dealer=Dealer()

alba=Player(player_dir,name='John Alba',nickname='JohnAlba')
bornstein=Player(player_dir,name='Bill Murphy',nickname='Bornstein')
clyde=Player(player_dir,name='Bob Vincent',nickname='Clyde')
brian=Player(player_dir,name='Brian Mercer',nickname='Mercer')
ed=Player(player_dir,name='Ed Mulhern',nickname='Ed')

players=[alba,bornstein,clyde,brian,ed]
for p in players:
    p.add_funds(500)
print('Funds added')
player_dict={}

shuffled=dealer.deal_cards(players,this_game)
for i,p in enumerate(players):
    print(p.p_nickname,p.hands[0],p.common_cards,p.hands[1])
    player_dict=dealer.add_to_display_dict(player_dict,i,p,cards)


#########################
app=Flask(__name__)

@app.route('/')
def index():
    return '<h1>Home page for second deal</h1>'

@app.route('/base_table')
def raw_table():
    return render_template('base_table.html',players=player_dict)

@app.route('/new_deal')
def new_deal():
    display_dict={}
    shuffled=dealer.deal_cards(players,this_game)
    for i,p in enumerate(players):
        #high_hand_ranks=[]
        #low_hand_ranks=[]
        p.high_hands=[]
        p.low_hands=[]
        for hand in p.hands:
            high_hand_ranks=[]
            low_hand_ranks=[]
            tmp_hand=hand+p.common_cards
            flat_list = [item for sublist in dealer.common_cards for item in sublist]
            combos=dealer.get_possible_hands(tmp_hand,flat_list)
            for c in combos:
                tmp_high,tmp_low=dealer.rank_hands((c))

                sorting_dict={1:'01',2:'02',3:'03',4:'04',5:'05',
                        6:'06',7:'07',8:'08',9:'09',10:'10',
                        11:'11',12:'12',13:'13',14:'14',15:'15'}

                
                tmp_high_c=[sorting_dict[x] for x in tmp_high[2]]
                tmp_low_c=[sorting_dict[x] for x in tmp_low[2]]
                tmp_high=(tmp_high[0],tmp_high[1],tmp_high_c,tmp_high[3])
                tmp_low=(tmp_low[0],tmp_low[1],tmp_low_c,tmp_low[3])

                high_hand_ranks.append(tmp_high)
                low_hand_ranks.append(tmp_low)
            #print('High/Low',high_hand_ranks[0],low_hand_ranks[0])
            high_hand_ranks.sort(key=lambda tup: tup[0])

            low_hand_ranks.sort(key=lambda tup: (tup[0],tup[2]),reverse=True)
            #print(low_hand_ranks[0],low_hand_ranks[-1])
            high_hand=high_hand_ranks[0]
            low_hand=low_hand_ranks[-1]
            p.high_hands.append(high_hand)
            p.low_hands.append(high_hand)

            print(f"{p.p_nickname} \nhigh: {high_hand[1]} {high_hand[2]} \nlow: {low_hand[1]} {low_hand[2]}")
            #print('Low_hands','\n',low_hand_ranks[:3],'\n',low_hand_ranks[-3:],'\n')



        display_dict=dealer.add_to_display_dict(display_dict,i,p,cards)
    #print(dealer.common_cards)
    common_dict=dealer.make_common_display_dict(dealer.common_cards,cards)

    return render_template('base_table.html',players=display_dict,
    common=common_dict)


@app.route('/da_var')
def some_func():
    my_var={'name':'Barry Bornstein',
            'favorite_bet':'20 cents'}
    return render_template('test_var.html',my_variable=my_var)


if __name__=='__main__':
    app.run(debug=True)
