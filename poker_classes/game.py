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

    def set_tic_tac_toe(self):
        self.game = 'tic_tac_toe'
        self.common_cards = [3, 3, 3]
        self.hands = [[], []]
        self.hands_count = [2, 2]
        self.p_common = 1

        self.common_rows=max(self.common_cards) #set the max number of common cards per column
        self.common_cols=len(self.common_cards) #set the max number of common columns for jinja use

        self.valid_combos=[[[0,0],[0,1],[0,2]],[[1,0],[1,1],[1,2]],[[2,0],[2,1],[2,2]],
                            [[0,0],[1,0],[2,0]],[[0,1],[1,1],[2,1]],[[0,2],[1,2],[2,2]],
                            [[0,0],[1,1],[2,2]],[[0,2],[1,1],[2,0]]]

        self.flip_list=[[[0,0],[0,1],[1,0]],[[2,2],[1,2],[2,1]],[[0,2],[1,1],[0,2]]]

        return

    def set_three_phase(self):
        self.game = 'three_phase'
        self.common_cards = [3, 3, 3]
        self.hands = [[], []]
        self.hands_count = [2, 2]
        self.p_common = 1

        self.common_rows=max(self.common_cards) #set the max number of common cards per column
        self.common_cols=len(self.common_cards) #set the max number of common columns for jinja use

        self.valid_combos=[[[0,0],[1,1],[2,2]],
                            [[0,0],[2,1],[1,2]],
                            [[1,0],[0,2],[2,2]],
                            [[1,0],[2,1],[0,2]],
                            [[2,0],[0,1],[1,2]],
                            [[2,0],[1,1],[0,2]]]

        self.flip_list=[[[0,0],[0,1],[1,0]],[[2,2],[1,2],[2,1]],[[0,2],[1,1],[0,2]]]

        return
