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
        self.common_cards=[]
        self.status='out'
        self.in_pot=0
        self.last_bet=0
        self.in_hand=True
        self.check_player_existence()

    def split_cards(self,cards):
        self.hands=['AS','AD']
        return hands

    def get_hands(self):
        return self.hands

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
