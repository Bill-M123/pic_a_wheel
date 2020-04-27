class Game():
    '''Game structure data.'''

    def __init__(self):
        self.players_logged_in=[]
        self.betting_rounds = 4
        self.max_raises = 3
        self.high_low = "high-low"
        self.delta = False
        self.ante = 50
        return

    def set_pic_a_wheel(self):
        self.game = 'pick_a_wheel'
        self.common_cards = [3, 3, 2]
        self.hands = [[], []]
        self.hands_count = [2, 2]
        self.p_common = 1

        return
