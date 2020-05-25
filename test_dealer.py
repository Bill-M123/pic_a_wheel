import pytest
import os
import random
import copy
import pandas as pd
import pickle


from poker_classes.cards import Cards
from poker_classes.dealer import Dealer
from poker_classes.game import Game
from poker_classes.player import Player

working_dir = os.getcwd()
app_dir = working_dir + '/poker_classes/'
player_dir = working_dir + '/existing_players/'

@pytest.fixture
def dealer():
    da_dealer=Dealer()
    return da_dealer

@pytest.fixture
def players():
    alba = Player(player_dir, name='John Alba', nickname='JohnAlba')
    brian = Player(player_dir, name='Brian Mercer', nickname='Brian')
    clyde = Player(player_dir, name='Bob Vincent', nickname='Clyde')
    degroot = Player(player_dir, name='Henry DeGroot', nickname='DeGroot')
    ed = Player(player_dir, name='Ed Mulhern', nickname='Mr.Pink')
    players=[alba,brian,clyde,degroot,ed]
    return players

@pytest.fixture
def game():
    this_game=Game()
    this_game.set_pic_a_wheel()
    return this_game

@pytest.fixture
def cards():
    cards=Cards()
    return cards

@pytest.fixture
def new_deck():
    new_deck=[(rank, suit) for rank in range(1, 14) for suit in ['S', 'H', 'C', 'D']]
    return new_deck



def test_create_player(players):
    a=players[0]
    assert a.p_nickname == 'JohnAlba'

def test_bankroll(players,dealer):
    a=players[0]
    a.bankroll += dealer.initial_player_funds
    assert a.bankroll == 500

def test_rotate_players(players,dealer):
    tmp=players.copy()
    next_dealer=tmp[0]
    new_tmp=dealer.rotate_deal(tmp)
    new_dealer=new_tmp[-1]
    assert next_dealer.p_nickname == new_dealer.p_nickname

def test_insert_new_player(players,dealer):
    tmp=players.copy()
    player_list=[]
    dealer.insert_new_player(player_list,tmp[0])
    tmp2=player_list[0]
    assert tmp2.p_nickname == 'JohnAlba'
    dealer.insert_new_player(player_list,tmp[0])
    tmp3=player_list[0]
    assert player_list == [tmp3,tmp2]

def test_shuffle(dealer,new_deck):
    aseed=27
    test_deck=new_deck.copy()
    random.seed(aseed)
    random.shuffle(test_deck)
    deck=dealer.new_deck.copy()
    deck=dealer.shuffle_deck(deck,aseed)
    assert deck==test_deck

def test_deal_card(dealer):
    deck=dealer.new_deck.copy()
    card,new_deck=dealer.deal_card(deck)
    assert card == (1,'S')

def test_deal_cards(players, game, dealer, aseed=27):
    common_cards_ref=[[(4, 'C'), (13, 'D'), (1, 'H')], [(10, 'D'), (4, 'H'),
    (7, 'S')], [(7, 'D'), (2, 'H')]]

    dealer.deal_cards(players,game,aseed=27)
    assert dealer.common_cards == common_cards_ref

def test_check_which_players_are_folded(dealer,players):
    for i,p in enumerate(players):
        if p.p_nickname=='JohnAlba':
            p.hands =['folded','folded']
            players[i]=p
    dealer.check_which_players_are_folded(players)
    assert dealer.folded_players_list == ['JohnAlba']

def test_calc_hi_low_pots(dealer):
    dealer.pot=155
    dealer.calc_hi_low_pots()
    assert dealer.high_pot == 80
    assert dealer.low_pot == 75

def test_get_possible_hands(dealer):
    this_hand=[(1,'S'),(2,'C'),(3,'D')]
    com_cards=[(5,'S'),(6,'C'),(7,'D'),(8,'S'),(9,'C'),(10,'D'),
        (11,'S'),(12,'C'),(13,'D')]
    combos = [(1, 'S'), (5, 'S'), (6, 'C'), (7, 'D'), (8, 'S')]
    assert dealer.get_possible_hands(this_hand, com_cards, omaha=False)[0] == combos
    combos=[(1, 'S'), (2, 'C'), (3, 'D'), (12, 'C'), (13, 'D')]
    assert dealer.get_possible_hands(this_hand, com_cards, omaha=False)[-1] == combos

def test_rank_single_hand(dealer):
    this_hand=[(1,'S'),(2,'D'),(3,'H'),(4,'C'),(6,'S')]
    best_high,best_low=dealer.rank_single_hand(this_hand)
    check_best = (9, 'High card', [14, 6, 4, 3, 2], [(1, 'S'), (2, 'D'), (3, 'H'), (4, 'C'), (6, 'S')])
    assert best_high == check_best
    check_best= (1, 'High card', [6, 4, 3, 2, 1], [(1, 'S'), (2, 'D'), (3, 'H'), (4, 'C'), (6, 'S')])
    assert best_low == check_best

    this_hand=[(1,'S'),(2,'S'),(3,'S'),(4,'S'),(6,'S')]
    best_high,best_low=dealer.rank_single_hand(this_hand)
    check_best = (4, 'Flush', [14, 6, 4, 3, 2], [(1, 'S'), (2, 'S'), (3, 'S'), (4, 'S'), (6, 'S')])
    assert best_high == check_best
    check_best = (6, 'Flush', [6, 4, 3, 2, 1], [(1, 'S'), (2, 'S'), (3, 'S'), (4, 'S'), (6, 'S')])
    assert best_low == check_best

def test_rank_all_hands(players,game,dealer):
    dealer.deal_cards(players,game,aseed=27)
    high_df,low_df=dealer.evaluate_all_hands(players)
    high_check=pd.read_csv(working_dir+'/static/test_files/high_df.csv',index_col=0)
    low_check=pd.read_csv(working_dir+'/static/test_files/low_df.csv',index_col=0)
    assert high_df.equals(high_check)
    assert low_df.equals(low_check)

def test_calc_winnings(dealer):
    high_df=pd.read_csv(working_dir+'/static/test_files/high_df.csv',index_col=0)
    low_df=pd.read_csv(working_dir+'/static/test_files/low_df.csv',index_col=0)
    pot=135
    high_win_df=dealer.calc_winnings(high_df,pot)
    low_win_df=dealer.calc_winnings(low_df,pot)

    high_win_ref_df=pd.read_csv(working_dir+'/static/test_files/high_win_ref_df.csv',index_col=0)
    low_win_ref_df=pd.read_csv(working_dir+'/static/test_files/low_win_ref_df.csv',index_col=0)
    assert  high_win_df.equals(high_win_ref_df)
    assert  low_win_df.equals(low_win_ref_df)

def test_get_high_low_hands(dealer,game,players):
    dealer.deal_cards(players,game,aseed=27)

    #Set test choices
    choices=[['high','low'],['low','high',],['folded','low'],['high','folded'],['folded','folded']]
    for i,p in enumerate(players):
        p.hands_hi_lo=choices[i]
        players[i]=p

    players_high,players_low = dealer.get_high_low_hands(players)

    declare_h = []
    for p in players_high:
        declare_h.append(p.hands_hi_lo)

    declare_l = []
    for p in players_low:
        declare_l.append(p.hands_hi_lo)

    players_high_ref = pickle.load( open( working_dir+'/static/test_files/players_high_ref.p', "rb" ))
    declare_ref_h = []
    for p in players_high_ref:
        declare_ref_h.append(p.hands_hi_lo)

    players_low_ref = pickle.load( open( working_dir+'/static/test_files/players_low_ref.p', "rb" ))
    declare_ref_l = []
    for p in players_low_ref:
        declare_ref_l.append(p.hands_hi_lo)

    assert declare_h == declare_ref_h
    assert declare_l == declare_ref_l

def test_add_to_display_dict(players,game,dealer,cards):
    p_dict={}
    dealer.deal_cards(players,game,aseed=27)
    for i,p in enumerate(players):
        p_dict=dealer.add_to_display_dict(p_dict, i, p, cards)

    p_dict_ref=pickle.load( open( working_dir+'/static/test_files/p_dict.p', "rb" ))

    assert p_dict_ref == p_dict

def make_player_cards_no_options(players, dealer, cards):
    dealer.deal_cards(players,game,aseed=27)

    this_player=make_player_cards_no_options(self, players, 'Mercer', cards)
    this_player_ref = pickle.load( open( working_dir+'/static/test_files/this_player_ref_M.p', "rb" ))
    assert this_player.hands_pr == this_player_ref

    this_player=make_player_cards_no_options(self, players, 'DeGroot', cards)
    this_player_ref = pickle.load( open( working_dir+'/static/test_files/this_player_ref_D.p', "rb" ))
    assert this_player.common_cards_pr == this_player_ref

def test_convert_value_card_to_display(dealer):
    c=(1,'S')
    test_c=dealer.convert_value_card_to_display(c)
    assert test_c== ('A', '♠')

    c='folded'
    test_c=dealer.convert_value_card_to_display(c)
    assert test_c== 'folded'

def test_convert_value_hand_to_display(dealer):
    h=[(13,'D'),(2,'C')]
    test_h=dealer.convert_value_hand_to_display(h)
    assert test_h == [('K', '♦'), (2, '♣')]

    h=['folded']
    test_h=dealer.convert_value_hand_to_display(h)
    assert test_h == ['folded']

def test_make_your_hand_display_cards(players,dealer,game,cards):

    dealer.deal_cards(players,game,aseed=27)
    this_player=dealer.make_player_cards_no_options(players, 'JohnAlba', cards)

    this_player=dealer.make_your_hand_display_cards(this_player)

    test_hands_ref=this_player.hands_pr
    hands_ref = pickle.load( open( working_dir+'/static/test_files/hands_ref_J.p', "rb" ))
    assert test_hands_ref == hands_ref

    test_common_hands_ref=this_player.hands_pr
    hands_c_ref = pickle.load( open( working_dir+'/static/test_files/hands_com_ref_J.p', "rb" ))
    assert hands_c_ref == test_common_hands_ref
'''
def test_analyze_action(dealer, players):

    #set test player to Mr.Pink
    for p in players:
        if p.p_nickname == 'Mr.Pink':
            test_p = p

    dealer.deal_cards(players,game,aseed=27)

    dealer.last_raise == 'Bornstein'
    action='Check'
    action_amount = 0
    dealer.analyze_action(self, action, action_amount, players, test_p)'''
