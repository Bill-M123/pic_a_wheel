import json
import random as random
import datetime as dt
from pytz import timezone
from collections import Counter
from itertools import combinations

import pandas as pd
import matplotlib.pyplot as plt

import base64
from io import BytesIO
from matplotlib.figure import Figure

import numpy as np
import os
import copy

from poker_classes.cards import Cards


class Dealer():
    '''The dealer class is responsible for moving the cards, and holding the
    common cards.'''

    def __init__(self):
        # General Table variables
        self.game_number = 0
        self.perform_reset = False
        self.new_deck = [(rank, suit) for rank in range(1, 14) for suit in ['S', 'H', 'C', 'D']]
        self.first_deal = True
        self.deal_complete = False
        self.dealer_position = 0
        self.hand_number = 0
        self.original_dealer = 'Not defined yet'

        # Card Variables
        self.common_cards = []  # Will have separate lists for each flip
        self.common_cards_pr = []
        self.common_cards_flipped = [False, False, False]  # True/False for each flip
        self.cards = Cards()
        self.display_suits_dict = {'S': '\u2660', 'C': '\u2663', 'H': '\u2665', 'D': '\u2666', }
        self.display_rank_dict = {1: 'A', 11: 'J', 12: 'Q', 13: 'K', 2: 2, 3: 3, 4: 4, 5: 5, 6: 6,
                                  7: 7, 8: 8, 9: 9, 10: 10}
        self.showdown_rank_dict = {'01': 'A', '11': 'J', '12': 'Q', '13': 'K', '02': '2',
                                   '03': '3', '04': '4', '05': '5', '06': '6',
                                  '07': '7', '08': '8', '09': '9', '10': '10','14':'A',
                                   'You should have stayed':'You should have stayed'}

        # Controls Added for betting rounds
        self.betting_round_number = 0
        self.betting_rounds = [False, False, False, False, False]
        self.new_betting_order = []
        self.betting_complete = False
        self.made_round_summary = False
        self.new_bet = False
        self.check_count = 0
        self.num_raises = 0
        self.who_opened = 'No one'
        self.last_raise = 'No one'
        self.active_player = 'No One'

        # Money variables
        self.initial_player_funds = 500
        self.total_funds_check = False
        self.ante_taken = False

        self.total_player_bankroll = 0
        self.bet_per_side = 0
        self.pot = 0
        self.high_pot = 0
        self.low_pot = 0

        # Added for declare
        self.declare_open = False
        self.declare_done = False
        self.players_not_declared = []

        # House keeping
        self.showdown = False
        self.players_waiting_to_enter = []
        self.hand_in_progress = False
        self.waiting_names=[]
        self.folded_players_list = []
        self.dead_guys = []
        self.players_w_two_hands = 0
        self.players_w_one_hand = 0
        self.players_folded = 0
        self.calc_highs_lows = True
        self.high_hands = 0
        self.low_hands = 0
        self.show_winnings = False
        self.flips_complete = 0
        self.round_chart_location = ''
        self.pandl_chart_location = ''
        self.pandl_df = pd.DataFrame()
        self.pandl_df_made = False
        self.done_scoring = False
        self.low_hand_df = pd.DataFrame()
        self.low_hand_df_dis = pd.DataFrame()
        self.high_hand_df = pd.DataFrame()
        self.high_hand_df_dis = pd.DataFrame()
        self.cumm_pandl_df = pd.DataFrame()
        self.rolling_df = pd.DataFrame()
        self.summaries_made = False

        return

    def reset_table(self, players, this_game):
        '''Resets all table related values for players and dealer.'''

        # General Table variables
        self.perform_reset = False
        self.new_deck = [(rank, suit) for rank in range(1, 14) for suit in ['S', 'H', 'C', 'D']]
        self.first_deal = True
        self.deal_complete = False
        self.dealer_position = 0
        self.hand_number += 1


        # Card Variables
        self.common_cards = []  # Will have separate lists for each flip
        self.common_cards_pr = []
        self.common_cards_flipped = [False, False, False]  # True/False for each flip
        self.cards = Cards()
        self.display_suits_dict = {'S': '\u2660', 'C': '\u2663', 'H': '\u2665', 'D': '\u2666', }
        self.display_rank_dict = {1: 'A', 11: 'J', 12: 'Q', 13: 'K', 2: 2, 3: 3, 4: 4, 5: 5, 6: 6,
                                  7: 7, 8: 8, 9: 9, 10: 10}

        # Controls Added for betting rounds
        self.betting_round_number = 0
        self.betting_rounds = [False, False, False, False, False]
        self.new_betting_order = []
        self.betting_complete = False
        self.made_round_summary = False
        self.new_bet = False
        self.check_count = 0
        self.num_raises = 0
        self.who_opened = 'No one'
        self.last_raise = 'No one'
        self.active_player = 'No One'

        # Money variables
        self.ante_taken = False
        self.bet_per_side = 0
        self.pot = 0
        self.high_pot = 0
        self.low_pot = 0

        # Added for declare
        self.declare_open = False
        self.declare_done = False
        self.players_not_declared = []

        # House keeping
        self.showdown = False
        self.dead_guys = []
        self.folded_players_list = []
        self.players_w_two_hands = 0
        self.players_w_one_hand = 0
        self.players_folded = 0
        self.calc_highs_lows = True
        self.high_hands = 0
        self.low_hands = 0
        self.show_winnings = False
        self.flips_complete = 0
        self.round_chart_location = ''
        self.pandl_chart_location = ''
        self.pandl_df = pd.DataFrame()
        self.pandl_df_made = False
        self.done_scoring = False
        self.low_hand_df = pd.DataFrame()
        self.low_hand_df_dis = pd.DataFrame()
        self.high_hand_df = pd.DataFrame()
        self.high_hand_df_dis = pd.DataFrame()
        self.hand_in_progress = False
        self.rolling_df = pd.DataFrame()
        self.summaries_made = False

        return

    # Current option. Changing
    def assign_new_dealer(self, players):
        '''Get next dealer position'''
        print(f'Old dealer position: {self.dealer_position}', end=' ')
        num_players = len(players)
        if self.first_deal == True:
            self.first_deal = False
            print(f'New dealer position: {self.dealer_position}, first deal.')
            return
        else:
            self.dealer_position += 1
            if self.dealer_position == num_players:
                self.dealer_position = 0
            print(f'New dealer position: {self.dealer_position}')
            return

    def rotate_deal(self, last_order):
        dealer = last_order.pop(0)
        last_order.append(dealer)
        return last_order

    def insert_new_player(self, last_order, new_player):
        ''' Insert new player from waiting list, verify original dealer '''

        if last_order == []:
            last_order.append(new_player)
            self.original_dealer = new_player
            return

        where_orig_dealer = last_order.index(self.original_dealer)
        print(where_orig_dealer)
        if where_orig_dealer == 0:
            last_order.append(new_player)
        else:
            #last_order.insert(where_orig_dealer, 9)
            last_order.insert(where_orig_dealer, new_player)
        return

    '''l1=[1,2,3,4,5,6,7,8]
l1=[1]

original_dealer=l1[-1]
original_dealer

def rotate_deal(last_order):
    dealer=last_order.pop(-1)
    last_order.insert(0,dealer)
    return last_order

l1=rotate_deal(l1)
l1

def insert_new_player(last_order,new_player):
    where_orig_dealer=last_order.index(original_dealer)
    if where_orig_dealer==0:
        last_order.insert(-1,new_player)
    else:
        last_order.insert(where_orig_dealer,9)
    return last_order

new_player=9
l1=insert_new_player(l1,new_player)
l1'''

    def take_ante(self, dealing_player, ante=50):
        '''Takes ante from player, deposits in live pot'''
        dealing_player.bankroll -= ante
        self.pot += ante
        return

    def shuffle_deck(self, deck,aseed=False):
        '''Shuffles card in deck, returns decl'''
        #random.seed(dt.datetime.now().microsecond)
        if aseed:
            random.seed(aseed)
        random.shuffle(deck)
        return deck

    def deal_card(self, deck):
        '''Return single card, and adjusted deck'''
        card = deck.pop(0)
        return card, deck

    def deal_cards(self, players, game, aseed=False):

        new_deck = self.new_deck.copy()
        shuffled = self.shuffle_deck(new_deck,aseed=aseed)

        # deal
        for p in players:
            p.hands = game.hands

        for p in players:
            card_count = 0
            p.hands = [[] for x in game.hands_count]
            for i, c in enumerate(game.hands_count):
                for h in range(c):

                    if card_count < c:
                        card, shuffled = self.deal_card(shuffled)
                        p.hands[i].append(card)

                    else:
                        pass
            card_count += 1

            p.common_cards = []
            for c in range(game.p_common):
                card, shuffled = self.deal_card(shuffled)
                p.common_cards.append(card)

        self.common_cards = [[] for x in range(len(game.common_cards))]
        for i, flip in enumerate(game.common_cards):
            for f in range(flip):
                card, shuffled = self.deal_card(shuffled)
                self.common_cards[i].append(card)

            if f<game.max_flip:
                blanks=max_flip-f
                for i in range(blanks):
                    self.common_cards[i].append('blank_card')

        for i,flip in game.common_cards:
            print(f"Common cards for flip # {i} are {self.common_cards[i]}")


        self.common_cards_flipped = []
        for flip in self.common_cards:
            self.common_cards_flipped.append(False)

        return shuffled

    def check_which_players_are_folded(self, players):
        '''Accepts a list of player objects, compares remaining hands
        to a completely folded hand and sets self.folded_players_list=[] to list of folded players'''
        self.folded_players_list = []
        for p in players:
            if all(x == 'folded' for x in p.hands):
                self.folded_players_list.append(p.p_nickname)
        # print(f"Folded players: {self.folded_players_list}")
        return

    def calc_hi_low_pots(self):
        '''divide pot into high and low portions'''
        num_nicks = int(self.pot) / 5
        self.high_pot = int(num_nicks / 2) * 5
        self.low_pot = self.high_pot
        if num_nicks % 2 == 1:
            self.high_pot += 5
        self.high_pot = int(self.high_pot)
        self.low_pot = int(self.low_pot)
        return

    def get_possible_hands(self, this_hand, common, omaha=False):
        '''return a list of all possible hands based on hand and common cards.
        Sets omaha flag which drives to two cards from hand'''

        cards_from_hand = list(range(1, len(this_hand) + 1))

        if omaha:
            cards_from_hand = [2]
        possibles = []
        for hand_cards in cards_from_hand:
            for h in combinations(this_hand, hand_cards):
                for com in combinations(common, 5 - hand_cards):
                    possibles += [list(h) + list(com)]
        return possibles

    def rank_single_hand(self,hand):
        '''accept list of 5 cards, return hand rank
        If Ace, run calculations twice, returns a list of best hand(s).'''

        # trap for folded hand
        if hand == 'folded':
            folded_hand = (100, f"Folded", ['folded'], 'folded')
            return folded_hand, folded_hand

        # Separate cards into ranks and suits
        rank_list = [x[0] for x in hand]
        suits_list = [x[1] for x in hand]

        # Find two most common combinations, allows id of all hands including fh
        cnt_rnk = Counter(rank_list)
        mc_1 = cnt_rnk.most_common()[0]
        mc_2 = cnt_rnk.most_common()[1]

        # Set flush flag
        flush_flag = False
        if len(list(set(suits_list))) == 1:
            flush_flag = True

        # set ace_flag and hand combinations to try

        hand_options = [rank_list.copy()]
        ace_flag = False
        if 1 in rank_list:
            ace_flag = True
            a_h_list = [x if x != 1 else 14 for x in rank_list]
            a_l_list = rank_list
            hand_options = [a_h_list, a_l_list]

        print(f"hand_options: {hand_options}")
        high_hands = []
        low_hands = []

        for tmp in hand_options:

            # Find two most common combinations, allows id of all hands including fh
            cnt_rnk = Counter(tmp)
            mc_1 = cnt_rnk.most_common()[0]
            mc_2 = cnt_rnk.most_common()[1]

            hand_decision = False

            if not flush_flag:

                if (mc_1[1] == 2) & (mc_2[1] == 1) & (hand_decision == False):

                    show = [x for x in tmp if x == mc_1[0]] + \
                           sorted([x for x in tmp if x != mc_1[0]], reverse=True)

                    show_low = [x for x in tmp if x == mc_1[0]] + \
                               sorted([x for x in tmp if x != mc_1[0]])

                    high_hands.append((8, f"Pair", show, hand))
                    low_hands.append((2, f"Pair", show_low, hand))

                elif (mc_1[1] == 2) & (mc_2[1] == 2) & (hand_decision == False):

                    if mc_1[0] > mc_2[0]:
                        a = mc_1[0]
                        b = mc_2[0]
                    else:
                        a = mc_2[0]
                        b = mc_1[0]
                    show = [x for x in tmp if x == a] + \
                           [x for x in tmp if x == b] + \
                           sorted([x for x in tmp if (x != mc_1[0]) & (x != mc_2[0])],
                                  reverse=True)

                    show_low = [x for x in tmp if x == a] + \
                               [x for x in tmp if x == b] + \
                               sorted([x for x in tmp if (x != mc_1[0]) & (x != mc_2[0])])

                    high_hands.append((7, f"Two Pair", show, hand))
                    low_hands.append((3, f"Two Pair", show_low, hand))

                elif (mc_1[1] == 3) & (mc_2[1] == 1) & (hand_decision == False):

                    show = [x for x in tmp if x == mc_1[0]] + \
                           sorted([x for x in tmp if x != mc_1[0]], reverse=True)
                    show_low = [x for x in tmp if x == mc_1[0]] + \
                               sorted([x for x in tmp if x != mc_1[0]])

                    high_hands.append((6, f"Three of a Kind", show, hand))
                    low_hands.append((4, f"Three of a Kind", show_low, hand))

                elif (max(rank_list) - min(rank_list) == 4) & \
                        (len(set(rank_list)) == 5) & (hand_decision == False):
                    # best_hands.append((5,'Straight '+str(sorted(rank_list,reverse=True))))
                    high_hands.append((5, 'Straight', sorted(rank_list, reverse=True), hand))
                    low_hands.append((5, 'Straight', sorted(rank_list, reverse=True), hand))

                elif (mc_1[1] == 3) & (mc_2[1] == 2) & (hand_decision == False):

                    show = [x for x in tmp if x == mc_1[0]] + \
                           sorted([x for x in tmp if x != mc_1[0]], reverse=True)

                    high_hands.append((3, f"Full House", show, hand))
                    low_hands.append((7, f"Full House", show, hand))

                elif (mc_1[1] == 4) & (mc_2[1] == 1) & (hand_decision == False):
                    show = [x for x in tmp if x == mc_1[0]] + \
                           sorted([x for x in tmp if x != mc_1[0]], reverse=True)
                    high_hands.append((2, f'Four of a Kind', show, hand))
                    low_hands.append((8, f'Four of a Kind', show, hand))

                else:
                    high_hands.append((9, 'High card', sorted(tmp, reverse=True), hand))
                    low_hands.append((1, 'High card', sorted(tmp, reverse=True), hand))

            elif flush_flag:

                if (max(tmp) - min(tmp) == 4) & (len(set(tmp)) == 5) & \
                        (hand_decision == False):
                    high_hands.append((1, f"Straight Flush", sorted(tmp, reverse=True), hand))
                    low_hands.append((9, f"Straight Flush", sorted(tmp), hand))
                else:
                    high_hands.append((4, f"Flush", sorted(tmp, reverse=True), hand))
                    low_hands.append((6, f"Flush", sorted(tmp, reverse=True), hand))
            else:
                high_hands.append('Unknown: ' + str(hand))
                low_hands.append('Unknown: ' + str(hand))
        #return max(high_hands), min(low_hands)
        # New high eval
        def adjust_for_sorting(high_low_hand):
            '''Bandaid for sorting problem requires two uses of high_ranks dict'''
            high_ranks={1:9,2:8,3:7,4:6,5:5,6:4,7:3,8:2,9:1}
            new_hands=[]
            for x in high_low_hand:
                new_hands.append((high_ranks[x[0]],x[1],x[2],x[3]))
            best_hand = sorted(new_hands, key=lambda x: (x[0], x[2]))[-1]
            print("da_best_hand",best_hand)
            best_hand=(((high_ranks[best_hand[0]],best_hand[1],best_hand[2],best_hand[3])))
            return best_hand
        best_high=adjust_for_sorting(high_hands)
        return best_high, min(low_hands)#adjust_for_sorting(low_hands)#

    def evaluate_all_hands(self, players):
        '''Evaluate winning hands from remaining players'''
        high_hand_list = []
        low_hand_list = []

        for i, p in enumerate(players):

            p.high_hands = []
            p.low_hands = []

            for hand in p.hands:
                high_hand_ranks = []
                low_hand_ranks = []

                if hand != 'folded':
                    tmp_hand = hand + p.common_cards
                    flat_list = [item for sublist in self.common_cards for item in sublist]
                    combos = self.get_possible_hands(tmp_hand, flat_list)
                    for c in combos:
                        tmp_high, tmp_low = self.rank_single_hand((c))

                        sorting_dict = {1: '01', 2: '02', 3: '03', 4: '04', 5: '05',
                                        6: '06', 7: '07', 8: '08', 9: '09', 10: '10',
                                        11: '11', 12: '12', 13: '13', 14: '14', 15: '15'}

                        tmp_high_c = [sorting_dict[x] for x in tmp_high[2]]
                        tmp_low_c = [sorting_dict[x] for x in tmp_low[2]]
                        tmp_high = [tmp_high[0], tmp_high[1], tmp_high_c, tmp_high[3]]
                        tmp_low = [tmp_low[0], tmp_low[1], tmp_low_c, tmp_low[3]]

                        high_hand_ranks.append(tmp_high)
                        low_hand_ranks.append(tmp_low)

                    df_data_h = high_hand_ranks
                    df_data_l = low_hand_ranks

                    high_df = pd.DataFrame(columns=['Rank', 'Hand', 'Card_Values', 'Cards'], data=df_data_h)
                    high_df.drop('Cards', axis=1, inplace=True)

                    low_df = pd.DataFrame(columns=['Rank', 'Hand', 'Card_Values', 'Cards'], data=df_data_l)
                    low_df.drop('Cards', axis=1, inplace=True)

                    high_df['Card_Values'] = high_df.Card_Values.apply(lambda x: '-'.join([str(y) for y in x]))
                    high_df = high_df.sort_values(['Rank', 'Card_Values'], ascending=[True, False])
                    high_df = high_df.drop_duplicates(keep="first")
                    high_df.reset_index(drop=True, inplace=True)

                    low_df['Card_Values'] = low_df.Card_Values.apply(lambda x: '-'.join([str(y) for y in x]))
                    low_df = low_df.sort_values(['Rank', 'Card_Values'], ascending=[False, False])
                    low_df = low_df.drop_duplicates(keep="first")
                    low_df.reset_index(drop=True, inplace=True)

                    # print(
                    #   f"{p.p_nickname} rank: {high_df['Rank'][0]} high_new: {high_df['Hand'][0]} {high_df['Card_Values'][0]}")
                    # print(
                    # f"{p.p_nickname} rank: {high_df['Rank'][len(low_df) - 1]} low_new: {low_df['Hand'][len(low_df) - 1]} {low_df['Card_Values'][len(low_df) - 1]}\n")

                    high_hand_list.append(
                        [p.p_nickname, high_df['Rank'][0], high_df['Hand'][0], high_df['Card_Values'][0]])
                    low_hand_list.append(
                        [p.p_nickname, low_df['Rank'][len(low_df) - 1], low_df['Hand'][len(low_df) - 1],
                         low_df['Card_Values'][len(low_df) - 1]])

        high_hand_df = pd.DataFrame(columns=['Name', 'Rank', 'Hand', 'Card_Values'], data=high_hand_list)
        low_hand_df = pd.DataFrame(columns=['Name', 'Rank', 'Hand', 'Card_Values'], data=low_hand_list)

        high_hand_df = high_hand_df.sort_values(['Rank', 'Card_Values'], ascending=[True, False])
        low_hand_df = low_hand_df.sort_values(['Rank', 'Card_Values'], ascending=[False, True])

        return high_hand_df, low_hand_df

    def calc_winnings(self, hand_df, pot):
        '''Accept dorted df, allocate winnings'''
        tmp_df = hand_df.copy()
        tmp_df.reset_index(drop=True, inplace=True)
        try:
            winning_rank = tmp_df['Rank'][0]
            winning_card_values = tmp_df['Card_Values'][0]
        except:
            fail_df = pd.DataFrame(columns=['Name', 'Rank', 'Hand', 'Card_Values', 'sh_pot', 'Winnings'],
                                   data=[['No One', 100, 'None', 'You should have stayed', 0, 0]])
            print("Returning failing_df")
            return fail_df

        tmp_df['sh_pot'] = 0
        tmp_df['Winnings'] = 0
        tmp_df.loc[(tmp_df.Rank == winning_rank) & (tmp_df.Card_Values == winning_card_values), 'sh_pot'] = 1
        num_winning_shares = tmp_df['sh_pot'].sum()

        if pot % num_winning_shares == 0:
            winning_share = int(pot / num_winning_shares)
            tmp_df.loc[tmp_df.sh_pot == 1, 'Winnings'] = winning_share
        else:
            num_winning_shares = tmp_df['sh_pot'].sum()

            num_nickels = int(pot / 5)
            base_winning_share = int(num_nickels / num_winning_shares) * 5
            tmp_df['Winnings'] = 0
            tmp_df.loc[tmp_df.sh_pot == 1, 'Winnings'] = base_winning_share

            extra_shares = num_nickels % num_winning_shares
            winning_names = tmp_df.loc[tmp_df.sh_pot == 1, 'Name'].values
            random.shuffle(winning_names)
            winning_names = winning_names[0:extra_shares]

            tmp_df.loc[tmp_df.Name.isin(winning_names), 'Winnings'] = tmp_df.loc[tmp_df.Name.isin(
                winning_names), 'Winnings'] + 5

        # print("calc_winnings: Winnings\n", tmp_df, "\n")
        return tmp_df

    def get_high_low_hands(self, players):
        '''Used post declare to set evaluate groups.'''
        players_high = []
        players_low = []
        for p in players:
            tmp_high = copy.deepcopy(p)
            tmp_low = copy.deepcopy(p)
            add_low = 0
            add_high = 0

            Add_flag = 0
            for k in [0, 1]:
                if p.hands_hi_lo[k] == 'high':
                    add_high = 1
                else:
                    tmp_high.hands[k] = 'folded'
            for k in [0, 1]:
                if p.hands_hi_lo[k] == 'low':
                    add_low = 1
                else:
                    tmp_low.hands[k] = 'folded'

            if add_high == 1:
                players_high.append(tmp_high)
            if add_low == 1:
                players_low.append(tmp_low)

        return players_high, players_low

    def add_to_display_dict(self, player_dict, i, p, Cards):

        player_dict[i] = {'name': p.p_nickname,

                          'hand_1': [(self.display_rank_dict[Cards.get_simple_u_card_p(p.hands[0][0])[0]],
                                      Cards.get_simple_u_card_p(p.hands[0][0])[1]),
                                     (self.display_rank_dict[Cards.get_simple_u_card_p(p.hands[0][1])[0]],
                                      Cards.get_simple_u_card_p(p.hands[0][1])[1])],

                          'common': [(self.display_rank_dict[Cards.get_simple_u_card_p(p.common_cards[0])[0]],
                                      Cards.get_simple_u_card_p(p.common_cards[0])[1])],
                          'hand_2': [(self.display_rank_dict[Cards.get_simple_u_card_p(p.hands[1][0])[0]],
                                      Cards.get_simple_u_card_p(p.hands[1][0])[1]),
                                     (self.display_rank_dict[Cards.get_simple_u_card_p(p.hands[1][1])[0]],
                                      Cards.get_simple_u_card_p(p.hands[1][1])[1])]}

        return player_dict

    def make_common_display_dict(self, common, Cards):
        common_dict = {}
        max_rows = max([len(x) for x in common])

        for i, flip in enumerate(common):
            tmp = []
            for crd in flip:
                ranker = self.display_dict[Cards.get_simple_u_card_p(crd)[0]]
                suit = Cards.get_simple_u_card_p(crd)[1]
                tmp.append((ranker, suit))

            short_cards = max_rows - len(flip)
            for k in range(short_cards):
                tmp.append(' ')

            common_dict[i] = tmp

        return common_dict

    def make_player_cards_no_options(self, players, session_name, cards):
        '''Organize cards visible to player'''

        this_player = False
        for p in players:
            if session_name == p.p_nickname:
                this_player = p
        try:
            tmp = []
            for i, h in enumerate(this_player.hands):
                tmp_hand = []
                if h != "folded":
                    tmp_hand.append([cards.get_simple_u_card_p(h[0]), cards.get_simple_u_card_p(h[1])])
                    tmp.append(tmp_hand[0])
                else:
                    tmp.append(['folded'])
            this_player.hands_pr = tmp

            if this_player.common_cards == []:
                this_player.common_cards = []
                this_player.common_cards_pr = []
            else:
                this_player.common_cards_pr = [cards.get_simple_u_card_p(this_player.common_cards[0])]

        except:
            print('Failed card string to hex')
            pass
        return this_player

    def convert_value_card_to_display(self, c):

        if isinstance(c, str):
            print(f"Card: {c} is a really a string.  Returning {c}")
            return c

        if c == 'folded' or c == ['folded']:
            print(f"{session['username']} common passed to convert_value_card: {c}")
            return c

        if c[1] in self.display_suits_dict.values():
            return (self.display_rank_dict[c[0]], [c[1]])

        return (self.display_rank_dict[c[0]], self.display_suits_dict[c[1]])

    def convert_value_hand_to_display(self, hand):
        if hand == ['folded']:
            # print(f"Hand folded.  Returning: {hand}")
            return hand
        if hand == 'folded':
            # print(f"Hand folded.  Returning: {hand}")
            return hand
        new_hand = []
        for c in hand:
            new_hand.append(self.convert_value_card_to_display(c))
        return new_hand

    def make_your_hand_display_cards(self, this_player: object) -> object:
        '''Make your hands and common cards display cards'''
        # convert for display#
        new_hands = []
        for h in this_player.hands:
            new_hands.append(self.convert_value_hand_to_display(h))
        this_player.hands_pr = new_hands

        if this_player.common_cards_pr == []:
            pass

        elif set([str(x) for x in this_player.hands]) == {'folded'}:
            this_player.common_cards_pr = []

        else:

            this_player.common_cards_pr = [(self.convert_value_card_to_display(this_player.common_cards[0]))]

        new_common = []
        for f in self.common_cards:
            tmp_h = self.convert_value_hand_to_display(f)
            new_common.append(tmp_h)

        self.common_cards_pr = new_common

        return this_player

    def analyze_action(self, action, action_amount, players, player):

        print("Analyzing action: ", player.p_nickname, action, action_amount)

        # check for end of round
        if (self.last_raise == self.new_betting_order[0].p_nickname) and (self.check_count > 0):
            print(f"Got around to {self.last_raise}, this round betting ends")
            self.new_bet == False
            self.betting_complete = True
            self.calc_hi_low_pots()
            return player

        # check for no action
        if action == 'None':
            print('No action')
            self.calc_hi_low_pots()
            return player

        self.this_action = self.new_betting_order.pop(0)

        new_betting_order = self.new_betting_order.copy()
        max_bet = max([x.this_round_per_side for x in players])

        # call

        if (action == 'check') and (player.this_round_per_side < max_bet):
            action = 'call'

        if action == 'fold':
            pass

        elif action == 'check':

            self.new_betting_order = new_betting_order.copy()
            self.new_betting_order.append(self.this_action)

            # Addresses Clyde's first bug.

            self.check_count += 1
            if self.check_count == 1:
                self.last_raise = player.p_nickname
                self.new_bet = True

        elif action == 'call':
            action_price = max_bet - player.this_round_per_side

            self.new_betting_order = new_betting_order.copy()
            self.new_betting_order.append(self.this_action)
            self.pot += action_price * player.num_hands
            self.new_bet = False
            # self.first_check = False
            self.check_count += 1
            player.bankroll -= (action_price * player.num_hands)
            player.this_round_per_side += (action_price)
            player.in_pot += (action_price) * player.num_hands
            player.in_pot_this_round += (action_price) * player.num_hands
            player.evening_bets.append(action_price * player.num_hands)



        else:
            action_price = max_bet - player.this_round_per_side
            da_raise = action_amount

            self.num_raises += 1
            self.new_betting_order = new_betting_order.copy()
            self.new_betting_order.append(self.this_action)
            self.pot = self.pot + (action_price + da_raise) * player.num_hands
            self.last_raise = player.p_nickname
            self.new_bet = True

            if self.who_opened == 'No one':
                self.who_opened = player.p_nickname

            player.bankroll = player.bankroll - (action_price + da_raise) * player.num_hands
            player.this_round_per_side = player.this_round_per_side + (action_price + da_raise)
            player.in_pot += (action_price + da_raise) * player.num_hands
            player.in_pot_this_round += (action_price + da_raise) * player.num_hands
            player.evening_bets.append((action_price + da_raise) * player.num_hands)

        # check for end of round
        if (self.last_raise == self.new_betting_order[0].p_nickname) and (self.check_count > 0):
            print(f"Got around to {self.last_raise}, this round betting ends")
            self.new_bet == False
            self.betting_complete = True

        self.calc_hi_low_pots()
        return player

    def get_betting_order(self, player_list):
        """Accept a  list of player objects in order, slice out players that have folded, set the in_hand flag to False for
        the folded players.  Sets new betting order in dealer object and returns a new player list with updated flags"""

        new_player_list = []
        for p in player_list:
            p.get_number_hands()
            if p.num_hands > 0:
                p.in_hand = True
                self.new_betting_order.append(p)
            else:
                p.in_hand = False
            new_player_list.append(p)

        return new_player_list

    def force_fold_player(self,p_name,players):
        '''Accept a player name, set both hands and hands_pr to folded,
        set common and common_pr to ['folded']
        set new betting new_order
        set new active player.'''
        if p_name != self.active_player:
            print(f"Can not fold {p_name} since he is not active.")
            return

        for i,p in enumerate(players):
            if p.p_nickname == p_name:
                p.hands[0]='folded'
                p.hands[1]='folded'
                p.hands_pr[0]='folded'
                p.hands_pr[1]='folded'
                p.common_cards = ['folded']
                p.common_cards_pr = ['folded']
                p.in_hand = False
                players[i]=p

                # Check that folding player did not make last raise, and if yes, adjust last bet to next player
                if self.last_raise == p.p_nickname:
                    if p.p_nickname == self.new_betting_order[-1]:
                        self.last_raise = self.new_betting_order[0]
                    else:
                        self.last_raise = self.new_betting_order[self.new_betting_order.index(p.p_nickname)+1]
                    print(f"Changed last_bet to {self.last_raise}")

                self.new_betting_order = [x for x in self.new_betting_order if x.p_nickname != p_name]
                print("New Betting Order in dealer.force_fold_player:")
                print(f"{self.new_betting_order}")
        tmp=self.new_betting_order[0]
        self.active_player = tmp.p_nickname

        # Check for last bet and adjust:
        if self.last_raise == p_name:
            for p in self.new_betting_order:
                max_in_pot = max([x.this_round_per_side for x in self.new_betting_order])
                max_bets=[x.p_nickname for x in self.new_betting_order if x.this_round_per_side == max_in_pot ]
                self.last_raise = max_bets[0]

        return


    def make_hand_plot(self, players):
        '''Make betting round summary plot - Who is committed'''
        tmp = []
        for g, guy in enumerate(players):
            for h, hand in enumerate(guy.in_pot_by_round):
                tmp.append([guy.p_nickname, h, hand, guy.hands_by_round[h]])
        guys_df = pd.DataFrame(columns=['Name', 'rnd', 'rnd_pot', 'num_hnds'],
                               data=tmp)
        print("guys_df\n", guys_df)
        guys_df['rnd_ttl'] = guys_df['rnd_pot']
        guys_df['cum_bet'] = guys_df.groupby("Name")["rnd_ttl"].cumsum().fillna(0)
        tls = guys_df.pivot_table(index='Name', values='rnd_ttl', \
                                  aggfunc='sum').reset_index(drop=False).rename(columns={'rnd_ttl': 'ttl'})
        guys_df = pd.merge(guys_df, tls, on='Name')
        guys_df.sort_values(["ttl", "rnd"], ascending=[False, True], inplace=True)

        colors_dict = {0: 'red', 1: 'yellow', 2: 'darkgreen'}

        plt.figure(figsize=(5, 3), dpi=100)
        for r in sorted(list(guys_df.rnd.unique())):
            tmp = guys_df.loc[guys_df.rnd == r, :]

            if r == 0:
                bottoms = tmp.rnd
            else:
                tmp2 = guys_df.loc[guys_df.rnd == r - 1, :]
                bottoms = tmp2.cum_bet
            xs = list(tmp.Name)
            colors = [colors_dict[x] for x in tmp.num_hnds.values]
            plt.bar(range(len(xs)), tmp.rnd_ttl, bottom=bottoms, color=colors, edgecolor='gray')

        legend_x_base = len(xs) + 1
        x_txt = 0.5
        legend_y_base = guys_df.ttl.max()
        y_rect = 5

        plt.title("How committed are they? (g=2h,y=1h,r=Folded)")
        plt.xticks(np.arange(len(xs)), labels=xs, rotation=15)
        plt.tight_layout()
        pwd = os.getcwd()
        print(f'pwd: {pwd}')
        self.round_chart_location = '/static/images/betting_rounds_sum_table_hand' + \
                                    str(self.hand_number) + '_round_' + str(self.betting_round_number) + '.png'
        plt.savefig(pwd + self.round_chart_location)

        return

    def make_hand_plot_no_pyplot(self, players):
        '''Make betting round summary plot - Who is committed'''
        tmp = []
        for g, guy in enumerate(players):
            for h, hand in enumerate(guy.in_pot_by_round):
                tmp.append([guy.p_nickname, h, hand, guy.hands_by_round[h]])
        guys_df = pd.DataFrame(columns=['Name', 'rnd', 'rnd_pot', 'num_hnds'],
                               data=tmp)
        print("guys_df\n", guys_df)
        guys_df['rnd_ttl'] = guys_df['rnd_pot']
        guys_df['cum_bet'] = guys_df.groupby("Name")["rnd_ttl"].cumsum().fillna(0)
        tls = guys_df.pivot_table(index='Name', values='rnd_ttl', \
                                  aggfunc='sum').reset_index(drop=False).rename(columns={'rnd_ttl': 'ttl'})
        guys_df = pd.merge(guys_df, tls, on='Name')
        guys_df.sort_values(["ttl", "rnd"], ascending=[False, True], inplace=True)

        colors_dict = {0: 'red', 1: 'yellow', 2: 'darkgreen'}

        fig = Figure(figsize=(5, 3), dpi=100)
        ax1 = fig.add_subplot(1,1,1)

        for r in sorted(list(guys_df.rnd.unique())):
            tmp = guys_df.loc[guys_df.rnd == r, :]

            if r == 0:
                bottoms = tmp.rnd
            else:
                tmp2 = guys_df.loc[guys_df.rnd == r - 1, :]
                bottoms = tmp2.cum_bet
            xs = list(tmp.Name)
            colors = [colors_dict[x] for x in tmp.num_hnds.values]
            ax1.bar(range(len(xs)), tmp.rnd_ttl, bottom=bottoms, color=colors, edgecolor='gray')

        legend_x_base = len(xs) + 1
        x_txt = 0.5
        legend_y_base = guys_df.ttl.max()
        y_rect = 5

        ax1.set_title("How committed are they? (g=2h,y=1h,r=Folded)")

        ax1.set_xticks(np.arange(len(xs)))
        ax1.set_xticklabels(xs,rotation=15)
        fig.tight_layout()
        pwd = os.getcwd()
        print(f'pwd: {pwd}')
        self.round_chart_location = '/static/images/betting_rounds_sum_table_hand' + \
                                    str(self.hand_number) + '_round_' + str(self.betting_round_number) + '.png'
        fig.savefig(pwd + self.round_chart_location)

        return

    def make_pandl_df(self, players, high_hand_df, low_hand_df):
        '''Accept list of player objects, adjust bankrolls for winnings,
        convert df to userful df for score summary'''

        #added to prevent multiple calculations of round winnings
        if self.pandl_df_made:
            return

        pl = []
        for i, p in enumerate(players):
            winnings_h = 0
            winnings_l = 0
            print(f"{p.p_nickname} hnd:{self.hand_number}")

            try:
                print(high_hand_df.loc[high_hand_df.Name == p.p_nickname, :])
                print('winnings_h',high_hand_df.loc[high_hand_df.Name == p.p_nickname, "Winnings"].values[0])
                winnings_h = high_hand_df.loc[high_hand_df.Name == p.p_nickname, "Winnings"].values[0]
            except:
                print(f"{p.p_nickname} failed high_hand_df.  winnings_h remains 0\n", high_hand_df)
                winnings_h = 0

            try:
                print(low_hand_df.loc[low_hand_df.Name == p.p_nickname, :])
                print('winnings_l', low_hand_df.loc[low_hand_df.Name == p.p_nickname, "Winnings"].values[0])
                winnings_l = low_hand_df.loc[low_hand_df.Name == p.p_nickname, "Winnings"].values[0]
            except:
                print(f"{p.p_nickname} failed low_hand_df.  winnings_l remains 0\n", low_hand_df)
                winnings_l = 0

            winnings_t = winnings_h + winnings_l
            print(f"{p.p_nickname} hnd:{self.hand_number} {winnings_t}")

            # Assign winnings:
            p.evening_winnings.append(winnings_t)
            p.p_and_l = winnings_t - p.in_pot
            print(f"{p.p_nickname} Evening_bets {p.evening_bets} Evening_winnings {p.evening_winnings}")

            pl.append([p.p_nickname, p.bankroll, p.in_pot, winnings_t, p.p_and_l])
            players[i] = p

        self.pandl_df = pd.DataFrame(columns=["Name", "Stake", "in_hnd", "winnings", "p_and_l"],
                                     data=pl)
        self.pandl_df_made = True
        return

    def adjust_hi_lo_show_down_displays(self):
        '''Make copy of self.high_hand_df and self.low_hand_df, adjust for display'''
        self.high_hand_df_dis=self.high_hand_df.copy()
        self.low_hand_df_dis=self.low_hand_df.copy()

        def make_adjust(x):
            tmp=x.split('-')
            tmp=[self.showdown_rank_dict[x] for x in tmp]
            return '-'.join(tmp)

        self.high_hand_df_dis['Card_Values'] =\
            self.high_hand_df_dis['Card_Values'].apply(make_adjust)
        self.low_hand_df_dis['Card_Values'] =\
            self.low_hand_df_dis['Card_Values'].apply(make_adjust)

        return



#    def add_winnings_to_bankroll(self, players):
#        for i, p in enumerate(players):
#            try:
#                winnings = self.pandl_df.loc[self.pandl_df['Name'] == p.p_nickname, 'winnings'].values[0].sum()
#                print(f"{p.p_nickname} winnings: {winnings}")
#            except:
#                print(f"{p.p_nickname} Failed to add winnings: {p.p_nickname}")
#                winnings = 0
#
#            p.bankroll += winnings
#            players[i] = p
#        return

    def make_summary_plots(self, players):
        '''Accept list of player objects, combine with dealer object (pandl_df)
        generate round and nightly score plots'''

        if not self.done_scoring:
        ###################################

            df = self.pandl_df.copy()

            self.cumm_pandl_df.append(df)
            print("PandL columns:\n", self.cumm_pandl_df.columns)
            print("PandL:\n", self.cumm_pandl_df)

            df['colors'] = df.winnings.apply(lambda x: 'red' if x < 0 else 'navy')
            df.sort_values(['winnings', 'in_hnd'], ascending=[False, False], inplace=True)

            shft_wid = 0.25
            bar_width = 0.5
            inv_width = 0.75
            xs = list(range(1, len(df.Name) + 1))

            plt.subplots(1, 2, figsize=(10, 3), dpi=100)
            plt.subplot(1, 2, 1)
            plt.bar(xs, df.winnings, width=inv_width, color='navy', label="Winnings")
            plt.bar(xs, df.in_hnd, width=bar_width, color='red', label="Bets")

            plt.title('Last Hand Hall of Fame (Shame?)')
            plt.xticks(xs, df.Name.values)
            plt.legend(loc="best")

            ##################################
            plt.subplot(1, 2, 2)
            #####
            # Changed 5/16/2010 to reflect dealer_cumm_info
            # df = self.pandl_df.copy()
            # df['winnings'] = df.Stake - 500
            ######

            # Test removal 5_21
            #df = self.cumm_pandl_df.copy()
            #df = df.pivot_table(index='Name', values="p_and_l", aggfunc='sum').reset_index(drop=False)

            self.calculate_bankrolls(players)
            df = self.player_funds_df.copy()

            df['colors'] = df.p_and_l.apply(lambda x: 'red' if x < 0 else 'navy')
            df.sort_values('p_and_l', ascending=False, inplace=True)
            print("df before plotting p&l, plotting p_and_l column:\n", df)

            plt.bar(df.Name, df.p_and_l, color=df.colors)
            plt.title("Tonight's P&L")
            plt.tight_layout()

            pwd = os.getcwd()
            print(f'pwd: {pwd}')
            self.pandl_chart_location = '/static/images/pandl_post_hand_' + \
                                        str(self.hand_number) + '_round_' + str(self.betting_round_number) + '.png'
            plt.savefig(pwd + self.pandl_chart_location)
            plt.close('all')

        return

    def make_summary_plots_no_pyplot(self, players):
        '''Accept list of player objects, combine with dealer object (pandl_df)
        generate round and nightly score plots -without using pyplot'''

        if not self.done_scoring:
        ###################################

            df = self.pandl_df.copy()

            self.cumm_pandl_df.append(df)
            print("PandL columns:\n", self.cumm_pandl_df.columns)
            print("PandL:\n", self.cumm_pandl_df)

            df['colors'] = df.winnings.apply(lambda x: 'red' if x < 0 else 'navy')
            df.sort_values(['winnings', 'in_hnd'], ascending=[False, False], inplace=True)

            shft_wid = 0.25
            bar_width = 0.5
            inv_width = 0.75
            xs = np.arange(len(df.Name))

            fig = Figure(figsize=(10, 3), dpi=100)

            ax1 = fig.add_subplot(1, 2, 1)
            ax1.bar(xs, df.winnings, width=inv_width, color='navy', label="Winnings")
            ax1.bar(xs, df.in_hnd, width=bar_width, color='red', label="Bets")

            ax1.set_title('Last Hand Hall of Fame (Shame?)')
            ax1.set_xticks(xs)
            ax1.set_xticklabels(df.Name.values,rotation=15)
            ax1.legend(loc="best")

            ##################################
            ax2 = fig.add_subplot(1, 2, 2)

            self.calculate_bankrolls(players)
            df = self.player_funds_df.copy()

            df['colors'] = df.p_and_l.apply(lambda x: 'red' if x < 0 else 'navy')
            df.sort_values('p_and_l', ascending=False, inplace=True)
            print("df before plotting p&l, plotting p_and_l column:\n", df)

            ax2.bar(df.Name, df.p_and_l, color=df.colors)
            ax2.set_title("Tonight's P&L")
            xs = np.arange(len(df.Name))
            ax2.set_xticks(xs)
            ax2.set_xticklabels(df.Name.values,rotation=15)
            fig.tight_layout()

            pwd = os.getcwd()
            print(f'pwd: {pwd}')
            self.pandl_chart_location = '/static/images/pandl_post_hand_' + \
                                        str(self.hand_number) + '_round_' + str(self.betting_round_number) + '.png'
            fig.savefig(pwd + self.pandl_chart_location)
            #plt.close('all')

        return

    def calculate_bankrolls(self,players):
        '''Calculate bankrolls from evening bets and winnings'''

        tmp_list=[]
        for i,p in enumerate(players):
            p.total_winnings = sum(p.evening_winnings)
            p.total_bets = sum(p.evening_bets)
            p.p_and_l = p.total_winnings - p.total_bets
            p.bankroll = self.initial_player_funds + p.total_winnings - p.total_bets
            players[i] = p
            tmp_list.append([self.hand_number,self.betting_round_number,p.p_nickname,p.bankroll,
                             p.in_pot,p.total_bets,p.total_winnings,p.p_and_l])

        self.player_funds_df=pd.DataFrame(columns=['Hand','Betting_Round','Name','Bankroll','In_Pot','Total_Bets',
                        'Total_Winnings','p_and_l'],data=tmp_list)
        self.player_funds_df.sort_values('p_and_l',ascending=False,inplace=True)

        pd.set_option('display.max_columns', None)
        print('Dealer calculated player funds:\n',self.player_funds_df)
        return

    def evaluate_hands_calc_winnings(self,players):
        '''Replace logic in flask app to evaluate hands and assign winnings'''

        self.active_player = "No one"

        declared_high,declared_low = self.get_high_low_hands(players)
        high_hand_df, trash_high = self.evaluate_all_hands(declared_high)
        trash_low, low_hand_df = self.evaluate_all_hands(declared_low)

        # Check for everyone going the same way:
        try:
            name_check = high_hand_df['Name'][0]
        except:
            name_check='No One'

        if name_check == 'No One':
            print("high side found no one.")
            self.low_pot += self.high_pot
            self.high_pot = 0

        name_check='No One'
        try:
            name_check = low_hand_df['Name'][0]
        except:
            name_check='No One'
        if name_check == 'No One':
            print("low side found no one.")
            self.high_pot += self.low_pot
            self.low_pot = 0

        ###########

        high_hand_df = self.calc_winnings(high_hand_df, self.high_pot)
        low_hand_df = self.calc_winnings(low_hand_df, self.low_pot)

        self.high_hand_df = high_hand_df #Save for later
        self.low_hand_df = low_hand_df #Save for later

        # Make round and nightly scores
        if not self.summaries_made:
            self.make_pandl_df(players, high_hand_df, low_hand_df)
            self.make_summary_plots_no_pyplot(players)
            self.summaries_made = True

            self.total_player_bankroll = 0

            rolling_df = self.player_funds_df[['Name','In_Pot','Total_Bets','Total_Winnings','p_and_l']]
            rolling_df = rolling_df.sort_values('p_and_l', ascending=False)
            rolling_df.rename(columns={"Total_Bets": "Ante/Bet", "Total_Winnings": "Winnings", "p_and_l": "Profit"}, inplace=True)
            rolling_df = rolling_df[["Name","Ante/Bet", "Winnings", "Profit"]]
            self.rolling_df = rolling_df
            print('rolling_df\n', rolling_df)

        else:
            pass

        #### Total_funds_check
        self.total_player_bankroll=rolling_df['Profit'].sum()+500*len(players)

        if (self.total_player_bankroll % self.initial_player_funds == 0):
            self.total_funds_check =True
        else:
            self.total_funds_check = False
        ####

        self.adjust_hi_lo_show_down_displays()
        self.active_player = "No one"

        self.calculate_bankrolls(players)

        self.done_scoring = True
        self.hand_in_progress = False

        self.showdown = True
        return

    def get_local_time(self,target_tz='US/Eastern'):
        # define eastern timezone
        my_tz = timezone(target_tz)
        current_time=dt.datetime.now(my_tz)
        return f"{current_time.date()}",f"{current_time.time()}"

    def save_summary_data(self,summary_dir):
        '''Save a temmporary copy of the hand summary.  Append it to the evening_bets
        summary'''

        tmp_df=self.rolling_df.copy()
        tmp_columns=tmp_df.columns

        tmp_df['hand']=self.hand_number

        da_date,da_time=self.get_local_time()
        tmp_df['date']=da_date
        tmp_df['time']=da_time
        new_cols=['date','time','hand']+[x for x in tmp_df.columns if x not in ['date','time','hand']]
        tmp_df=tmp_df[new_cols]
        print(tmp_df)

        tmp_df.to_csv(summary_dir+f"sum_{da_date}_gm_{self.game_number}_hand_{self.hand_number}.csv")
        return

    # Game list manually initialized 6/5/2020
    def initialize_game_times(self):
        target_tz='US/Eastern'
        my_tz = timezone(target_tz)
        current_time=dt.datetime.now(my_tz)
        tmp_df=pd.DataFrame(columns=['Start','Game'],data=[[current_time,0]])
        tmp_df.to_csv('C:\\Users\\bill_\\github\\pic_a_wheel\\performance_summaries\\game_starts.csv')
        print(tmp_df)
        return tmp_df


    def set_game_number(self,summary_dir):
        target_tz='US/Eastern'
        my_tz = timezone(target_tz)
        current_time=dt.datetime.now(my_tz)
        parse_dates=['Start']
        games_df=pd.read_csv(summary_dir+'game_starts.csv',
                             parse_dates=parse_dates,index_col=0)
        max_game_date=games_df['Start'].max()
        print('max_game_date',max_game_date)

        date_now=dt.datetime.now(my_tz)
        print(date_now.date(),max_game_date.date())

        if date_now.date() == max_game_date.date():
            print("Found today's date in games list.")
            last_game=games_df.loc[games_df.Start==max_game_date,'Game'].max()
            this_game=last_game+1
            new_row={'Start':date_now,'Game':this_game}
            games_df=games_df.append(new_row, ignore_index=True)
            games_df.to_csv(summary_dir+'game_starts.csv')
            print(games_df)

        else:
            print("Didn't find today's date in games list.")
            this_game=1
            new_row={'Start':date_now,'Game':this_game}
            games_df=games_df.append(new_row, ignore_index=True)
            games_df.to_csv(summary_dir+'game_starts.csv')
            print(games_df)

        self.game_number = this_game
        return
