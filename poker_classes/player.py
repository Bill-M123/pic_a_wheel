import os
import json
import datetime as dt

class Player():
    '''The player class holds player information including the players hand and
    bankroll.'''

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
        self.folded_hands=['folded' for x in self.hands]
        self.common_cards=[]
        self.in_pot=0
        self.this_round_per_side=0
        self.last_bet=0
        self.high_hands=[]
        self.low_hands=[]
        self.in_hand=True  #Flag for in hand
        self.at_table=True #Flag for at table
        self.check_player_existence()

    def split_cards(self,cards):
        self.hands=['AS','AD']
        return hands

    def get_hands(self):
        return self.hands

    def fold_decisions(self):
        # Fold decisions for player
        print(self.p_nickname,self.hands,self.common_cards)
        for h in range(len(self.hands)):
            if self.hands[h]=='folded':
                pass

            else:
                fold_action=input(f'Fold hand {self.hands[h]}, common {self.common_cards}? fold=fold ')
                if fold_action=='fold':
                    self.hands[h]='folded'

        if self.hands==self.folded_hands:
            self.common_cards='folded'
        print('\n')
        return

    def open_bet_decisions(self,p,dealer,game):
        '''Takes place of previous actions method.  Accepts dealer and game,
        uses attributes from those classes to determine action options for
        the player.'''

        print('Betting Options:')

        #Previously folded
        if self.hands==self.folded_hands:
            print('You folded previously.  No decisions to make.')
            return

        # No action yet
        elif (dealer.who_opened=='No one'):
            print('You may BET, CHECK, or FOLD')
            options=['bet','check','fold']

        #Bet on table
        else:
            # Raises left
            if (dealer.num_raises<=game.max_raises)&\
            (dealer.bet_per_side>0):
                remaining_raises=game.max_raises-dealer.num_raises
                print(f"The bet is {dealer.bet_per_side}")
                print(f'There are {remaining_raises} raises left.')
                print('You may CALL, RAISE or FOLD')
                options=['call','raise','fold']

            elif(dealer.num_raises<=game.max_raises)&\
            (dealer.bet_per_side==0):
                remaining_raises=game.max_raises-dealer.num_raises
                print(f"The bet is {dealer.bet_per_side}")
                print(f'There are {remaining_raises} raises left.')
                print('You may CHECK, CALL, RAISE or FOLD')
                options=['check','call','raise','fold']

            #No raises left
            else:
                print(f'There are no raises left.')
                print('You may CALL or FOLD')
                options=['call','fold']

        invalid_action=True
        while invalid_action:
            action=input('Enter choice: ')
            if action in options:
                invalid_action=False
            else:
                print(f"That is an invalid choice.  Valid choices are: {options} Try again.")


        if action=='check':
            pass

        elif action=='bet':
            bet_options=[5,10,15,20]
            amount=self.get_amount(bet_options)

            dealer.bet_per_side+=amount
            dealer.who_opened=self.p_nickname

            self.bankroll-= amount*len([x for x in self.hands if x!='folded'])
            self.in_pot+= amount*len([x for x in self.hands if x!='folded'])
            self.last_bet= amount
            self.this_round_per_side += amount

            print(f"{self.p_nickname} now has {self.in_pot} in pot, has bet {self.this_round_per_side} per side and has a bankroll of {self.bankroll}")
            return

        elif action=='call':
            to_add=dealer.bet_per_side-self.last_bet

            self.bankroll-= to_add*len([x for x in self.hands if x!='folded'])
            self.in_pot+= to_add*len([x for x in self.hands if x!='folded'])
            self.last_bet += to_add
            self.this_round_per_side += to_add

            print(f"{self.p_nickname} now has {self.in_pot} in pot, has bet {self.this_round_per_side} per side and has a bankroll of {self.bankroll}")
            return

        elif action=='raise':
            to_add=dealer.bet_per_side-self.last_bet

            raise_options=[5,10,15,20]
            da_raise=self.get_amount(raise_options)

            to_add += da_raise

            self.bankroll-= to_add*len([x for x in self.hands if x!='folded'])
            self.in_pot+= to_add*len([x for x in self.hands if x!='folded'])
            self.last_bet += to_add
            self.this_round_per_side += to_add

            dealer.num_raises +=1
            dealer.bet_per_side += da_raise
            dealer.last_raise=self.p_nickname

            print(f"{self.p_nickname} now has {self.in_pot} in pot, has bet {self.this_round_per_side} per side and has a bankroll of {self.bankroll}")
            print(f"Raises left: {game.max_raises-dealer.num_raises}")
            return

    def get_amount(self, choices):
        '''Enter bet/increase, trap for errors.'''
        invalid_action=True
        while invalid_action:
            amount=int(input(f'Enter bet amount {choices}: '))
            if amount in choices:
                invalid_action=False
            else:
                print(f"That is an invalid choice.  Valid choices are: {choices} Try again.")
        return amount

    # Remove  Need separate actions
    def action(self,action='check',amount=0):
        '''There are 3 possible player actions at for each hand for each round:
        check:  No impact, player remains in hand.
        fold:  Player drops from hand
        bet:  Player takes money from bankroll, adds it to pot, and remains in hand.

        Function returns amount to be added to player_position.'''

        if action=='fold':
            print('Folding action not complete.  Need to add hands control '+\
            'must include hand id')
            return 0

        elif action=='bet':
            self.bankroll-=amount
            self.in_pot+=amount
            self.last_bet+=amount
            return amount

        elif action=='check':
            return 0

        else:
            return 0

    def add_funds(self,amount):
        self.bankroll+=amount
        now=dt.datetime.now()
        self.deposits.append(now.strftime("%x %H:%M:%S")+f' {amount}')
        return

    def check_player_existence(self):
        existing_players=os.listdir(self.player_dir)
        player_file=self.p_nickname+'.json'

        if player_file in existing_players:
            print(f'Found {self.p_nickname}')
            with open(self.player_dir+player_file) as f:
                data = json.load(f)

            self.p_name=data['p_name']
            self.p_nickname=data['p_nickname']
            self.email=data['email']
            self.password=data['password']
            self.bankroll=data['bankroll']
            self.deposits=data['deposits']

        else:
            print(f"{self.p_nickname} not found.")
            self.save_player_data()

        return

    def save_player_data(self):
        player_file=self.p_nickname+'.json'
        data={}

        data['p_name']=self.p_name
        data['p_nickname']=self.p_nickname
        data['email']=self.email
        data['password']=self.password
        data['bankroll']=self.bankroll
        data['deposits']=self.deposits
        json_data=json.dumps(data)

        with open(self.player_dir+player_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
