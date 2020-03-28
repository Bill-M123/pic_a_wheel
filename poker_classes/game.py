class Game():
    '''Game structure data.  Defaults to pic_a_wheel.'''

    def __inti__(self):
        '''Defaults to pic_a_wheel'''
        self.game='pick_a_wheel'
        self.betting_rounds=4
        self.common_cards=[3,2,2]
        self.high_low="high-low"
        self.ante=50
        self.hands=[[],[]]
        self.hands_count=[2,2]
        self.p_common=1
        self.delta=False

    def set_pic_a_wheel(self):
        self.game='pic_a_wheel'
        self.betting_rounds=4
        self.common_cards=[3,2,2]
        self.high_low="high-low"
        self.ante=50
        self.hands=[[],[]]
        self.common_hand=[]
        self.hands_count=[2,2]
        self.p_common=1
        self.delta=False
        return
