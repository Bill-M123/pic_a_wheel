import random as random
from collections import Counter

import json

class Dealer():
    '''The dealer class is responsible for moving the cards, and holding the
    common cards.'''

    def __init__(self):
        self.new_deck=[(rank, suit) for rank in range(1,14) for suit in ['S','H','C','D']]
        self.dealer_position=0
        self.pot=0
        self.common_cards=[] # Will have separate lists for each flip
        self.common_cards_flipped=[] #True/False for each flip
        self.bet_per_side=0
        self.round_open=False
        self.num_raises=0
        self.who_opened='No one'
        self.last_raise='No one'


    def shuffle_deck(self,deck):
        random.shuffle(deck)
        return deck

    def deal_card(self,deck):
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

    def rank_hands(self,hand_list):
        '''accept list of 5 cards, return hand rank
        If Ace, run calculations twice, returns a list of best hand(s).'''

        # Separate cards into ranks and suits
        rank_list=[x[0] for x in hand_list]
        suits_list=[x[1] for x in hand_list]

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

        best_hands=[]

        for tmp in hand_options:

            hand_decision=False

            if not flush_flag:

                if (mc_1[1]==2) & (mc_2[1]==1)&(hand_decision==False):

                    show=[x for x in tmp if x == mc_1[0]]+\
                        sorted([x for x in tmp if x != mc_1[0]],reverse=True)
                    best_hands.append(f"Pair {show}")

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
                    best_hands.append(f"Two Pair {show}")

                elif (mc_1[1]==3) & (mc_2[1]==1)&(hand_decision==False):

                    show=[x for x in tmp if x == mc_1[0]]+\
                        sorted([x for x in tmp if x != mc_1[0]],reverse=True)
                    best_hands.append(f"Three of a Kind {show}")


                elif (max(rank_list)-min(rank_list)==4)&\
                    (len(set(rank_list))==5)&(hand_decision==False):
                    best_hands.append('Straight '+str(sorted(rank_list,reverse=True)))

                elif (mc_1[1]==3) & (mc_2[1]==2)&(hand_decision==False):

                    show=[x for x in tmp if x == mc_1[0]]+\
                        sorted([x for x in tmp if x != mc_1[0]],reverse=True)

                    best_hands.append(f"Full House {show}")

                elif (mc_1[1]==4) & (mc_2[1]==1)&(hand_decision==False):
                    show=[x for x in tmp if x == mc_1[0]]+\
                        sorted([x for x in tmp if x != mc_1[0]],reverse=True)
                    best_hands.append(f'Four of a Kind {show}')

                else:
                    best_hands.append('High_card '+str(sorted(tmp,reverse=True)))

            elif flush_flag:
                if (max(rank_list)-min(rank_list)==4)&(len(set(rank_list))==5)&\
                    (hand_decision==False):
                    best_hands.append(f"Straight Flush {sorted(tmp,reverse=True)}")
                else:
                    best_hands.append(f"Flush {sorted(tmp,reverse=True)}")
            else:
                best_hands.append('Unknown: '+str(hand_list))
        return best_hands


#############################################################
# Code below currently not used.  To be removed if a need doesn't arise
#############################################################
    def copy_of_rank_hands(self,hand_list):
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
