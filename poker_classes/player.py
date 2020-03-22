import os
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
        self.player_position=20
        self.total_deals_tonight=0
        self.seconds_thinking=0
        self.hands=[[],[]]
        self.status='out'
        self.in_pot=0
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
            self.in_pot=0
            return 0

        elif action=='bet':
            self.bankroll-=amount
            self.in_pot+=amount
            return amount

        elif action=='check':
            return 0

        else:
            return 0

    def add_funds(self,amount):
        self.bankroll+=amount
        return

    def check_player_existence(self):
        existing_players=os.listdir(self.player_dir)
        player_file=self.p_nickname+'.txt'

        if player_file in existing_players:
            print(f'Found {self.p_nickname}')
        else:
            print(f"{self.p_nickname} not found.")
        return
