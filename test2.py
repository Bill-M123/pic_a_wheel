import os

class Dealer():
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
        self.display_suits_dict={'S':'\u2660','C':'\u2663','H':'\u2665','D':'\u2666',}
        self.display_rank_dict={1:'A',11:'J',12:'Q',13:'K',2:2,3:3,4:4,5:5,6:6,
                7:7,8:8,9:9,10:10}


        self.new_betting_order=[]
        self.betting_complete=False
        self.new_bet=False

class Player():
    def __init__(self,player_dir='',name='',nickname='',email='place_holder@place_holder.com',
        password='password'):
        self.p_name=name
        self.p_nickname='_'.join(nickname.split(' '))
        self.email=email
        self.password=password
        self.player_dir=player_dir
        self.bankroll=0
        self.deposits=[]
        self.player_position=20
        self.total_deals_tonight=0
        self.seconds_thinking=0
        self.hands=[[],[]]
        self.hands_pr=[[],[]]
        self.backs_pr=['backs','backs']
        self.folded_hands=[[] for x in self.hands]
        self.common_cards=[]
        self.common_cards_pr=['backs']
        self.in_pot=0
        self.this_round_per_side=0
        self.last_bet=0
        self.high_hands=[]
        self.low_hands=[]
        self.in_hand=True  #Flag for in hand
        self.at_table=True #Flag for at table


    def add_funds(self,amount):
        self.bankroll+=amount
        return

    def make_bet(self,amount):
        self.bankroll-=amount
        return

def analyze_action(action,action_amount,players,player,dealer):

        #check for end of round
        if dealer.last_raise==dealer.new_betting_order[0].p_nickname:
            print(f"Got around to {dealer.last_raise}, this round betting ends")
            dealer.new_bet==False
            return player,dealer

        dealer.last_bettor=dealer.new_betting_order.pop(0)
        new_betting_order=dealer.new_betting_order.copy()
        max_bet=max([x.this_round_per_side for x in players])
        #call

        if (action=='check') and (player.this_round_per_side < max_bet):
            action='call'

        if action =='fold':
            pass

        elif action == 'check':

            dealer.new_betting_order=new_betting_order.copy()
            dealer.new_betting_order.append(dealer.last_bettor)


        elif action == 'call':
            action_price=max_bet-player.this_round_per_side

            dealer.new_betting_order=new_betting_order.copy()
            dealer.new_betting_order.append(dealer.last_bettor)
            dealer.pot+=action_price
            dealer.new_bet=False
            player.bankroll-=action_price
            player.this_round_per_side+=action_price
            tmp=[x.p_nickname for x in dealer.new_betting_order]


        else:
            action_price=max_bet-player.this_round_per_side
            da_raise=action_amount#int(action.split('_')[1])

            dealer.new_betting_order=new_betting_order.copy()
            dealer.new_betting_order.append(dealer.last_bettor)
            dealer.pot=dealer.pot+action_price+da_raise
            dealer.last_raise=player.p_nickname
            dealer.new_bet=True

            if dealer.who_opened=='No one':
                dealer.who_opened=player.p_nickname

            player.bankroll=player.bankroll-action_price-da_raise
            player.this_round_per_side=player.this_round_per_side+action_price+da_raise
            tmp=[x.p_nickname for x in dealer.new_betting_order]

        return  player,dealer


working_dir=os.getcwd()
app_dir=working_dir+'/poker_classes/'
player_dir=working_dir+'/existing_players/'

dealer=Dealer()
alba=Player(player_dir,name='John Alba',nickname='JohnAlba')
bornstein=Player(player_dir,name='Bill Murphy',nickname='Bornstein')
clyde=Player(player_dir,name='Bob Vincent',nickname='Clyde')
brian=Player(player_dir,name='Brian Mercer',nickname='Mercer')
ed=Player(player_dir,name='Ed Mulhern',nickname='Ed')

players=[alba,bornstein,clyde,brian,ed]
for i,p in enumerate(players):
    p.add_funds(500) #add funds
    p.player_position = i # set table position


player_list=players
action='call'
action_amount=25

dealer.new_betting_order=players.copy()

actions={1:'check',2:'call',3:'bet'}

players=[alba,bornstein,clyde,brian,ed]

while not dealer.betting_complete:

    guy=dealer.new_betting_order[0]
    action=actions[int(input(f"Input action for {guy.p_nickname}: {actions}"))]
    action_amount=int(input(f"Amount: 5,10, 15, or 20 "))

    guy,dealer=analyze_action(action,action_amount,players,guy,dealer)

    tmp=[x.p_nickname for x in dealer.new_betting_order]

    for p in players:
        if guy.p_nickname==p.p_nickname:
            p=guy


    if (dealer.last_raise==guy.p_nickname) & (not dealer.new_bet):
        dealer.betting_complete=True
        print("agreed")

for guy in players:
    print(f"{guy.p_nickname,guy.bankroll,guy.this_round_per_side}")

print(f"Total Pot: {dealer.pot}")
print(f"{dealer.who_opened} opened")
print(f"{dealer.last_raise} made the last bet.")

uncomplete= not dealer.betting_complete
print(f"Initial betting flag {dealer.betting_complete} inverse {uncomplete}")
