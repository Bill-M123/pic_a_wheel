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
    return '<h1>Home page for first deal</h1>'

@app.route('/base_table')
def raw_table():
    return render_template('base_table.html',players=player_dict)

@app.route('/new_deal')
def new_deal():
    display_dict={}
    shuffled=dealer.deal_cards(players,this_game)
    for i,p in enumerate(players):
        display_dict=dealer.add_to_display_dict(display_dict,i,p,cards)
    print(dealer.common_cards)
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
