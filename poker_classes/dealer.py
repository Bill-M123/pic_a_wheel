import random as random
import pandas as pd
from collections import Counter
from itertools import combinations


import json

class Dealer():
    '''The dealer class is responsible for moving the cards, and holding the
    common cards.'''

    def __init__(self):
        self.perform_reset=False
        self.new_deck=[(rank, suit) for rank in range(1,14) for suit in ['S','H','C','D']]
        self.first_deal=True
        self.deal_complete=False

        self.dealer_position=0
        self.active_player='Bornstein'
        self.deal_complete=False
        self.pot=0
        self.common_cards=[] # Will have separate lists for each flip
        self.common_cards_pr=[]
        self.common_cards_flipped=[False,False,False] #True/False for each flip
        self.bet_per_side=0
        self.declare_done=False
        self.round_complete=False
        self.num_raises=0
        self.who_opened='No one'
        self.last_raise='No one'
        self.display_dict={1:'A',11:'J',12:'Q',13:'K',2:2,3:3,4:4,5:5,6:6,
                7:7,8:8,9:9,10:10}



    def reset_table(self,players,this_game):
        '''Resets all table related values for players and dealer.'''
        self.__init__()

        return

    def assign_new_dealer(self,players):
        '''Get next dealer position'''
        print(f'Old dealer position: {self.dealer_position}',end=' ')
        num_players=len(players)
        if self.first_deal==True:
            self.first_deal=False
            print(f'New dealer position: {self.dealer_position}, first deal.')
            return
        else:
            self.dealer_position+=1
            if self.dealer_position==num_players:
                self.dealer_position=0
            print(f'New dealer position: {self.dealer_position}')
            return

    def take_ante(self,dealing_player,ante=50):
        '''Takes ante from player, deposits in live pot'''
        dealing_player.bankroll-=ante
        self.pot+=ante
        return

    def shuffle_deck(self,deck):
        '''Shuffles card in deck, returns decl'''
        random.shuffle(deck)
        return deck

    def deal_card(self,deck):
        '''Return single card, and adjusted deck'''
        card=deck.pop(0)
        return card,deck

    def deal_cards(self,players,game):

        new_deck=self.new_deck.copy()
        shuffled=self.shuffle_deck(new_deck)

        #deal
        for p in players:
            p.hands=game.hands

        for p in players:
            card_count=0
            p.hands=[[] for x in game.hands_count]
            for i,c in enumerate(game.hands_count):
                for h in range(c):

                    if card_count<c:
                        card,shuffled=self.deal_card(shuffled)
                        p.hands[i].append(card)

                    else:
                        pass
            card_count+=1

            p.common_cards=[]
            for c in range(game.p_common):
                card,shuffled=self.deal_card(shuffled)
                p.common_cards.append(card)


        self.common_cards=[[] for x in range(len(game.common_cards))]
        for i,flip in enumerate(game.common_cards):
            for f in range(flip):
                card,shuffled=self.deal_card(shuffled)
                self.common_cards[i].append(card)

        self.common_cards_flipped=[]
        for flip in self.common_cards:
            self.common_cards_flipped.append(False)

        return shuffled

    def check_which_players_are_folded(self,players):
        '''Accepts a list of player objects, compares remaining hands
        to a completely folded hand and sets p.in_hand'''
        for p in players:
            p.in_hand=not all(x=='folded' for x in p.hands)
            print(p.p_nickname,p.hands,'in hand: ',p.in_hand)
        return

    def get_possible_hands(self,this_hand,common,omaha=False):
        '''return a list of all possible hands based on hand and common cards.
        Sets omaha flag which drives to two cards from hand'''

        cards_from_hand=list(range(1,len(this_hand)+1))

        if omaha:
            cards_from_hand=[2]
        possibles=[]
        for hand_cards in cards_from_hand:
            for h in combinations(this_hand,hand_cards):
                for com in combinations(common,5-hand_cards):
                    possibles+=[list(h)+list(com)]
        return possibles

    def rank_single_hand(self,hand):
        '''accept list of 5 cards, return hand rank
        If Ace, run calculations twice, returns a list of best hand(s).'''

        # Separate cards into ranks and suits
        rank_list=[x[0] for x in hand]
        suits_list=[x[1] for x in hand]

        # Find two most common combinations, allows id of all hands including fh
        cnt_rnk=Counter(rank_list)
        mc_1=cnt_rnk.most_common()[0]
        mc_2=cnt_rnk.most_common()[1]

        # Set flush flag
        flush_flag=False
        if len(list(set(suits_list)))==1:
            flush_flag=True

        #set ace_flag and hand combinations to try

        hand_options=[rank_list.copy()]
        ace_flag=False
        if 1 in rank_list:
            ace_flag=True
            a_h_list=[x if x!=1 else 14 for x in rank_list]
            a_l_list=rank_list
            hand_options=[a_h_list,a_l_list]

        high_hands=[]
        low_hands=[]

        for tmp in hand_options:

            hand_decision=False

            if not flush_flag:

                if (mc_1[1]==2) & (mc_2[1]==1)&(hand_decision==False):

                    show=[x for x in tmp if x == mc_1[0]]+\
                        sorted([x for x in tmp if x != mc_1[0]],reverse=True)

                    show_low=[x for x in tmp if x == mc_1[0]]+\
                        sorted([x for x in tmp if x != mc_1[0]])

                    high_hands.append((8,f"Pair",show,hand))
                    low_hands.append((2,f"Pair",show_low,hand))

                elif (mc_1[1]==2) & (mc_2[1]==2)&(hand_decision==False):

                    if mc_1[0]>mc_2[0]:
                        a=mc_1[0]
                        b=mc_2[0]
                    else:
                        a=mc_2[0]
                        b=mc_1[0]
                    show=[x for x in tmp if x == a]+\
                        [x for x in tmp if x == b]+\
                        sorted([x for x in tmp if (x != mc_1[0])&(x != mc_2[0])],
                            reverse=True)

                    show_low=[x for x in tmp if x == a]+\
                        [x for x in tmp if x == b]+\
                        sorted([x for x in tmp if (x != mc_1[0])&(x != mc_2[0])])

                    high_hands.append((7,f"Two Pair",show,hand))
                    low_hands.append((3,f"Two Pair",show_low,hand))

                elif (mc_1[1]==3) & (mc_2[1]==1)&(hand_decision==False):

                    show=[x for x in tmp if x == mc_1[0]]+\
                        sorted([x for x in tmp if x != mc_1[0]],reverse=True)
                    show_low=[x for x in tmp if x == mc_1[0]]+\
                        sorted([x for x in tmp if x != mc_1[0]])

                    high_hands.append((6,f"Three of a Kind",show,hand))
                    low_hands.append((4,f"Three of a Kind",show_low,hand))

                elif (max(rank_list)-min(rank_list)==4)&\
                    (len(set(rank_list))==5)&(hand_decision==False):
                    #best_hands.append((5,'Straight '+str(sorted(rank_list,reverse=True))))
                    high_hands.append((5,'Straight',sorted(rank_list,reverse=True),hand))
                    low_hands.append((5,'Straight',sorted(rank_list,reverse=True),hand))

                elif (mc_1[1]==3) & (mc_2[1]==2)&(hand_decision==False):

                    show=[x for x in tmp if x == mc_1[0]]+\
                        sorted([x for x in tmp if x != mc_1[0]],reverse=True)

                    high_hands.append((3,f"Full House",show,hand))
                    low_hands.append((7,f"Full House",show,hand))

                elif (mc_1[1]==4) & (mc_2[1]==1)&(hand_decision==False):
                    show=[x for x in tmp if x == mc_1[0]]+\
                        sorted([x for x in tmp if x != mc_1[0]],reverse=True)
                    high_hands.append((2,f'Four of a Kind',show,hand))
                    low_hands.append((8,f'Four of a Kind',show,hand))

                else:
                    high_hands.append((9,'High card',sorted(tmp,reverse=True),hand))
                    low_hands.append((1,'High card',sorted(tmp,reverse=True),hand))

            elif flush_flag:
                if (max(rank_list)-min(rank_list)==4)&(len(set(rank_list))==5)&\
                    (hand_decision==False):
                    high_hands.append((1,f"Straight Flush",sorted(tmp,reverse=True),hand))
                    low_hands.append((9,f"Straight Flush",sorted(tmp),hand))
                else:
                    high_hands.append((4,f"Flush",sorted(tmp,reverse=True),hand))
                    low_hands.append((6,f"Flush",sorted(tmp,reverse=True),hand))
            else:
                high_hands.append('Unknown: '+str(hand))
                low_hands.append('Unknown: '+str(hand))
        return max(high_hands),min(low_hands)

    def evaluate_all_hands(self,players):
        '''Evaluate winning hands from remaining players'''
        high_hand_list=[]
        low_hand_list=[]

        for i,p in enumerate(players):

            p.high_hands=[]
            p.low_hands=[]

            for hand in p.hands:
                high_hand_ranks=[]
                low_hand_ranks=[]

                tmp_hand=hand+p.common_cards
                flat_list = [item for sublist in self.common_cards for item in sublist]
                combos=self.get_possible_hands(tmp_hand,flat_list)
                for c in combos:
                    tmp_high,tmp_low=self.rank_single_hand((c))

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

        high_hand_df=pd.DataFrame(columns=['Name','Rank','Hand','Card_Values'],data=high_hand_list)
        low_hand_df=pd.DataFrame(columns=['Name','Rank','Hand','Card_Values'],data=low_hand_list)

        high_hand_df=high_hand_df.sort_values(['Rank','Card_Values'],ascending=[True,False])
        low_hand_df=low_hand_df.sort_values(['Rank','Card_Values'],ascending=[False,True])

        return high_hand_df, low_hand_df


    def add_to_display_dict(self,player_dict,i,p,Cards):

        player_dict[i]={'name':p.p_nickname,

            'hand_1':[(self.display_dict[Cards.get_simple_u_card_p(p.hands[0][0])[0]],
                        Cards.get_simple_u_card_p(p.hands[0][0])[1]),
                    (self.display_dict[Cards.get_simple_u_card_p(p.hands[0][1])[0]],
                                Cards.get_simple_u_card_p(p.hands[0][1])[1])],

            'common':[(self.display_dict[Cards.get_simple_u_card_p(p.common_cards[0])[0]],
                        Cards.get_simple_u_card_p(p.common_cards[0])[1])],
            'hand_2':[(self.display_dict[Cards.get_simple_u_card_p(p.hands[1][0])[0]],
                        Cards.get_simple_u_card_p(p.hands[1][0])[1]),
                    (self.display_dict[Cards.get_simple_u_card_p(p.hands[1][1])[0]],
                                Cards.get_simple_u_card_p(p.hands[1][1])[1])]}

        return player_dict

    def make_common_display_dict(self,common,Cards):
        common_dict={}
        max_rows=max([len(x) for x in common])

        for i,flip in enumerate(common):
            tmp=[]
            for crd in flip:
                ranker=self.display_dict[Cards.get_simple_u_card_p(crd)[0]]
                suit=Cards.get_simple_u_card_p(crd)[1]
                tmp.append((ranker,suit))

            short_cards=max_rows-len(flip)
            for k in range(short_cards):
                tmp.append(' ')

            common_dict[i]=tmp
        #print(common_dict)
        return common_dict

    def make_player_cards_no_options(self,players,session_name,cards):
        '''Organize cards visible to player'''

        this_player=False
        for p in players:
            print(p.p_nickname,p.hands_pr)
            if session_name==p.p_nickname:
                this_player=p
                print(f'Working on {this_player.p_nickname},hands: {p.hands}, common: {p.common_cards}')
                print(f'Working on {this_player.p_nickname},hands: {p.hands_pr}, common: {p.common_cards_pr}')

        try:
            tmp=[]
            for i,h in enumerate(this_player.hands):
                print
                print('Hands: ',this_player.hands[0],this_player.hands[1],i,h)
                tmp_hand=[]
                if h!="folded":
                    tmp_hand.append([cards.get_simple_u_card_p(h[0]),cards.get_simple_u_card_p(h[1])])
                    tmp.append(tmp_hand[0])
                else:
                    tmp.append(['folded'])
            this_player.hands_pr=tmp

            print('Initial Common: ',this_player.common_cards)

            if this_player.common_cards==[]:
                this_player.common_cards=[]
                this_player.common_cards_pr=[]
            else:
                this_player.common_cards_pr=[cards.get_simple_u_card_p(this_player.common_cards[0])]

            print('Hands: ',this_player.hands_pr)
            print('Common: ',this_player.common_cards_pr)
            print('Passed card string to hex')

        except:
            print('Failed card string to hex')
            pass
        return this_player

    def convert_value_card_to_display(self,c):
        print(f"Card: {c}")
        if c=='backs':
            return c
        return (self.display_dict[c[0]],c[1])

    def convert_value_hand_to_display(self,hand):
        print(f"Convert_hand_input: {hand}")
        if hand==['folded']:
            return hand
        new_hand=[]
        for c in hand:
            new_hand.append(self.convert_value_card_to_display(c))
        return new_hand



#############################################################
# Code below currently not used.  To be removed if a need doesn't arise
#############################################################
    def copy_of_rank_single_hand(self,hand_list):
        '''accept list of 5 cards, return hand rank'''
        #Count Similar Card Combinations
        rank_list=[x[0] for x in hand_list]
        suits_list=[x[1] for x in hand_list]

        cnt_rnk=Counter(rank_list)
        #print(cnt.most_common()[0],cnt.most_common()[1])
        mc_1=cnt_rnk.most_common()[0]
        mc_2=cnt_rnk.most_common()[1]

        # Set flush flag
        flush_flag=False
        if len(list(set(suits_list)))==1:
            flush_flag=True

        #set ace_flag
        ace_flag=False
        if 1 in rank_list:
            ace_flag=True
            a_h_list=[x if x!=1 else 14 for x in rank_list]
            a_l_list=rank_list

        tmp=rank_list.copy()
        if ace_flag:
            tmp=a_h_list

        if not flush_flag:

            if (mc_1[1]==2) & (mc_2[1]==1):

                show=[x for x in tmp if x == mc_1[0]]+\
                    sorted([x for x in tmp if x != mc_1[0]],reverse=True)
                return f"Pair {show}"
            elif (mc_1[1]==2) & (mc_2[1]==2):

                if mc_1[0]>mc_2[0]:
                    a=mc_1[0]
                    b=mc_2[0]
                else:
                    a=mc_2[0]
                    b=mc_1[0]
                show=[x for x in tmp if x == a]+\
                    [x for x in tmp if x == b]+\
                    sorted([x for x in tmp if (x != mc_1[0])&(x != mc_2[0])],
                        reverse=True)
                return f"Two Pair {show}"

            elif (mc_1[1]==3) & (mc_2[1]==1):

                show=[x for x in tmp if x == mc_1[0]]+\
                    sorted([x for x in tmp if x != mc_1[0]],reverse=True)
                return f"Three of a Kind {show}"


            elif (max(rank_list)-min(rank_list)==4)&(len(set(rank_list))==5):
                return 'Straight '+str(sorted(rank_list,reverse=True))

            elif (mc_1[1]==3) & (mc_2[1]==2):

                show=[x for x in tmp if x == mc_1[0]]+\
                    sorted([x for x in tmp if x != mc_1[0]],reverse=True)

                return f"Full House {show}"

            elif (mc_1[1]==4) & (mc_2[1]==1):
                show=[x for x in tmp if x == mc_1[0]]+\
                    sorted([x for x in tmp if x != mc_1[0]],reverse=True)
                return f'Four of a Kind {show}'

            else:
                if ace_flag:
                    return 'High_card '+str(sorted(tmp,reverse=True))
                else:
                    #sorted(rank_list,reverse=True)
                    return 'High_card '+str(sorted(rank_list,reverse=True))

        elif flush_flag:
            if (max(rank_list)-min(rank_list)==4)&(len(set(rank_list))==5):
                return f"Straight Flush {sorted(tmp,reverse=True)}"
            else:
                return f"Flush {sorted(tmp,reverse=True)}"
        else:
            return 'Unknown: '+str(hand_list)
