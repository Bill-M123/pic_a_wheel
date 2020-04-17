class Cards():

    def __init__(self):
        return

    def get_simple_u_card_h(self, x_tup):
        '''Accept a tuple organized as: (rank,suit)
        return a tuple that can be used to output simple unicode card.
        One note: this output is for HTML'''

        suits_dict = {'S': '&#9824', 'C': '&#9827', 'H': '&#9829', 'D': '&#9830', }
        return (x_tup[0], suits_dict[x_tup[1]])

    def get_simple_u_card_p(self, x_tup):
        '''Accept a tuple organized as: (rank,suit)
        return a tuple that can be used to output simple unicode card.
        One note: this output is for python output'''

        suits_dict = {'S': '\u2660', 'C': '\u2663', 'H': '\u2665', 'D': '\u2666', }
        return (x_tup[0], suits_dict[x_tup[1]])
