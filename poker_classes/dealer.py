import random as random
from collections import Counter

class Dealer():
    '''The dealer class is responsible for moving the cards, and holding the
    common cards.'''

    def __init__(self):
        self.new_deck=[(rank, suit) for rank in range(1,14) for suit in ['S','H','C','D']]
        self.dealer_position=0
        self.common_cards=[]

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

        self.common_cards=[[] for x in range(len(game.common_cards))]
        for i,flip in enumerate(game.common_cards):
            for f in range(flip):
                card,shuffled=self.deal_card(shuffled)
                self.common_cards[i].append(card)

        return shuffled

    def rank_hands(self,hand_list):
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
            a_h_list=[x if x!=1 else 13 for x in rank_list]
            a_l_list=rank_list

        if not flush_flag:
            if (mc_1[1]==2) & (mc_2[1]==1):
                tmp=rank_list.copy()
                if ace_flag:
                    tmp=a_h_list
                show=[x for x in tmp if x == mc_1[0]]+sorted([x for x in tmp if x != mc_1[0]],reverse=True)
                return f"Pair {show}"
            elif (mc_1[1]==2) & (mc_2[1]==2):
                tmp=rank_list.copy()
                if ace_flag:
                    tmp=a_h_list

                if mc_1[0]>mc_2[0]:
                    a=mc_1[0]
                    b=mc_2[0]
                else:
                    a=mc_2[0]
                    b=mc_1[0]
                show=[x for x in tmp if x == a]+\
                    [x for x in tmp if x == b]+\
                    sorted([x for x in tmp if (x != mc_1[0])&(x != mc_2[0])],reverse=True)
                return f"Two Pair {show}"

            elif (mc_1[1]==3) & (mc_2[1]==1):
                return 'Three of a Kind'

            elif (max(rank_list)-min(rank_list)==4)&(len(set(rank_list))==5):
                return 'Straight'
            elif (mc_1[1]==3) & (mc_2[1]==2):
                return 'Full House'
            elif (mc_1[1]==4) & (mc_2[1]==1):
                return 'Four of a Kind'
            else:
                sorted(rank_list,reverse=True)
                return 'High_Card '+str(sorted(rank_list,reverse=True))

        elif flush_flag:
            if (max(rank_list)-min(rank_list)==4)&(len(set(rank_list))==5):
                tmp=rank_list.copy()
                if ace_flag:
                    tmp=a_h_list
                return f"Straight Flush {sorted(tmp,reverse=True)}"
            else:
                tmp=rank_list.copy()
                if ace_flag:
                    tmp=a_h_list
                return f"Flush {sorted(tmp,reverse=True)}"
        else:
            return 'Unknown: '+str(hand_list)
