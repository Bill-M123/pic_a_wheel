class Game():
    '''Game structure data.'''

    def __init__(self):
        self.players_logged_in=[]
        self.betting_rounds = 4
        self.max_raises = 3
        self.high_low = "high-low"
        self.delta = False
        self.omaha = False
        self.ante = 50
        self.game = 'Unknown'
        return

    def set_pic_a_wheel(self):
        self.game = 'pic_a_wheel'
        self.common_cards = [3, 3, 2]
        self.hands = [[], []]
        self.hands_count = [2, 2]
        self.p_common = 1

        self.common_rows=max(self.common_cards) #set the max number of common cards per column
        self.common_cols=len(self.common_cards) #set the max number of common columns for jinja use

        self.valid_combos=[[[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1]]]

        self.flip_list=[[[0,0],[0,1],[0,2]],[[1,0],[1,1],[1,2]],[[2,0],[2,1]]]

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

    def set_slot_machine(self):
        self.game = 'slot_machine'
        self.common_cards = [4, 4, 4]
        self.hands = [[], []]
        self.hands_count = [2, 2]
        self.p_common = 1

        self.common_rows=max(self.common_cards) #set the max number of common cards per column
        self.common_cols=len(self.common_cards) #set the max number of common columns for jinja use

        self.valid_combos=[]

        c1=[[0,0],[1,0],[2,0],[3,0]]
        c2=[[0,1],[1,1],[2,1],[3,1]]
        c3=[[0,2],[1,2],[2,2],[3,2]]

        self.valid_combos=[]
        for i in c1:
            for j in c2:
                for k in c3:
                    self.valid_combos.append([i,j,k])

        self.flip_list=[[[0,0],[0,1],[0,2],[0,3]],
                        [[2,0],[2,1],[2,2],[2,3]],
                        [[1,0],[1,1],[1,2],[1,3]]]

        return

    def set_tic_tac_toe_w_plex(self):
        self.game = 'tic_tac_toe'
        self.common_cards = [3, 4, 3]
        self.hands = [[], []]
        self.hands_count = [2, 2]
        self.p_common = 1

        self.common_rows=max(self.common_cards) #set the max number of common cards per column
        self.common_cols=len(self.common_cards) #set the max number of common columns for jinja use

        self.valid_combos=[[[0,0],[0,1],[0,2],[3,1]],[[1,0],[1,1],[1,2],[3,1]],
                            [[2,0],[2,1],[2,2],[3,1]],[[0,0],[1,0],[2,0],[3,1]],
                            [[0,1],[1,1],[2,1],[3,1]],[[0,2],[1,2],[2,2],[3,1]],
                            [[0,0],[1,1],[2,2],[3,1]],[[0,2],[1,1],[2,0],[3,1]]]

        self.flip_list=[[[0,0],[0,1],[1,0]],[[2,2],[1,2],[2,1]],[[0,2],[1,1],[0,2]]]

        return
