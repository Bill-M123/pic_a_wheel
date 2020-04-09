
############################################
# Imports for logic and basic table displays
############################################
import os
import pandas as pd
import datetime as dt
from itertools import combinations

from poker_classes.player import Player
from poker_classes.dealer import Dealer
from poker_classes.game import Game
from poker_classes.cards import Cards

from flask import Flask
from flask import render_template

#######Additional imports from clyde

from flask import flash
from flask import request, session, redirect, url_for
from flask_login import LoginManager
from flask_socketio import SocketIO, emit

#########################
from flask_login import login_required,current_user



working_dir=os.getcwd()
app_dir=working_dir+'/poker_classes/'
player_dir=working_dir+'/existing_players/'

cards=Cards()
this_game=Game()
this_game.set_pic_a_wheel()

dealer=Dealer()

login_manager=LoginManager() # Sets up player views


############################################
# Player Initialization
############################################
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

# Initial Deal, display cards on console
shuffled=dealer.deal_cards(players,this_game)
for i,p in enumerate(players):
    print(p.p_nickname,p.hands[0],p.common_cards,p.hands[1])
    player_dict=dealer.add_to_display_dict(player_dict,i,p,cards)


#########################
app=Flask(__name__)

# App config from Clyde
app.config["SECRET_KEY"] = "yousecntuch"
app.debug = True
socketio = SocketIO(app)
login_manager=login_manager.init_app(app)

@app.route('/')
def index():
    return '<h1>Home page for third_deal.py</h1>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    print(request.method)
    if request.method == 'POST':
        session['username'] = request.form['username']
        print(session['username'])
        valid_ids=[p.p_nickname for p in players]

        if session['username'] in valid_ids:
            return f"You are logged in as {session['username']}"
        else:
            return f"Invalid Login.  I don't know you.  I don't want to know you.  Go away."
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/base_table_w_player')
def raw_table():
    '''Render this page for testing.  Assumes viewer not logged in as player.'''
    print('current_user',current_user.is_authenticated)


    display_dict={}
    for i,p in enumerate(players):
            display_dict=dealer.add_to_display_dict(display_dict,i,p,cards)
            print(p.p_nickname,p.hands)

    for p in players:
            if session['username']==p.p_nickname:
                this_player=p

    common_dict=dealer.make_common_display_dict(dealer.common_cards,cards)

    return render_template('base_table_w_player.html',players=display_dict,
            common=common_dict,this_player=this_player)



@app.route('/new_deal')
def new_deal():
    display_dict={}
    shuffled=dealer.deal_cards(players,this_game)

    high_hand_list=[]
    low_hand_list=[]

    for i,p in enumerate(players):
        #high_hand_ranks=[]
        #low_hand_ranks=[]
        p.high_hands=[]
        p.low_hands=[]
        #print(p.p_nickname,p.hands,p.c)
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
                tmp_high=[tmp_high[0],tmp_high[1],tmp_high_c,tmp_high[3]]
                tmp_low=[tmp_low[0],tmp_low[1],tmp_low_c,tmp_low[3]]

                high_hand_ranks.append(tmp_high)
                low_hand_ranks.append(tmp_low)

            df_data_h=high_hand_ranks
            df_data_l=low_hand_ranks

            high_df=pd.DataFrame(columns=['Rank','Hand','Card_Values','Cards'],data=df_data_h)
            high_df.drop('Cards',axis=1,inplace=True)

            low_df=pd.DataFrame(columns=['Rank','Hand','Card_Values','Cards'],data=df_data_l)
            low_df.drop('Cards',axis=1,inplace=True)

            high_df['Card_Values']=high_df.Card_Values.apply(lambda x: '-'.join([str(y) for y in x]))
            high_df=high_df.drop_duplicates(keep="first")
            high_df=high_df.sort_values(['Rank','Card_Values'],ascending=[True,False]).reset_index(drop=True)

            low_df['Card_Values']=low_df.Card_Values.apply(lambda x: '-'.join([str(y) for y in x]))
            low_df=low_df.drop_duplicates(keep="first")
            low_df=low_df.sort_values(['Rank','Card_Values'],ascending=[False,False]).reset_index(drop=True)

            print(f"{p.p_nickname} rank: {high_df['Rank'][0]} high_new: {high_df['Hand'][0]} {high_df['Card_Values'][0]}")
            print(f"{p.p_nickname} rank: {high_df['Rank'][len(low_df)-1]} low_new: {low_df['Hand'][len(low_df)-1]} {low_df['Card_Values'][len(low_df)-1]}\n")

            high_hand_list.append([p.p_nickname,high_df['Rank'][0],high_df['Hand'][0],high_df['Card_Values'][0]])
            low_hand_list.append([p.p_nickname,low_df['Rank'][len(low_df)-1],low_df['Hand'][len(low_df)-1],low_df['Card_Values'][len(low_df)-1]])

        display_dict=dealer.add_to_display_dict(display_dict,i,p,cards)

    high_hand_df=pd.DataFrame(columns=['Name','Rank','Hand','Card_Values'],data=high_hand_list)
    low_hand_df=pd.DataFrame(columns=['Name','Rank','Hand','Card_Values'],data=low_hand_list)
    print('Best High Hands:\n',high_hand_df.sort_values(['Rank','Card_Values'],ascending=[True,False]).head(3))
    print('Best Low Hands:\n',low_hand_df.sort_values(['Rank','Card_Values'],ascending=[False,True]).head(3))


    #print(dealer.common_cards)
    common_dict=dealer.make_common_display_dict(dealer.common_cards,cards)
    print('Common_Dict: ',common_dict)

    return render_template('base_table.html',players=display_dict,
    common=common_dict)


@app.route('/da_var')
def some_func():
    my_var={'name':'Barry Bornstein',
            'favorite_bet':'20 cents'}
    return render_template('test_var.html',my_variable=my_var)


if __name__=='__main__':
    app.run(debug=True)
