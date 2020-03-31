from flask import Flask
from flask import render_template

app=Flask(__name__)

@app.route('/')
def index():
    return '<h1>Home page for first deal</h1>'

@app.route('/base_table')
def raw_table():
    player_dict={
        'barry':{'name':'Barry',
            'hand_1':[['10', '\u2666'],['10', '\u2660']],
            'common':[['9', '\u2663'],['9', '\u2665']],
            'hand_2':[['8', '\u2665'],['8', '\u2666']]},
        'john':{'name':'John',
            'hand_1':[['7', '\u2663'],['7', '\u2665']],
            'common':[['6', '\u2660'],['6', '\u2663']],
            'hand_2':[['5', '\u2660'],['5', '\u2666']]},
        'clyde':{'name':'Clyde',
            'hand_1':[['4', '\u2663'],['4', '\u2660']],
            'common':[['3', '\u2663'],['3', '\u2665']],
            'hand_2':[['2', '\u2660'],['2', '\u2666']]},
                }


    return render_template('base_table.html',players=player_dict)

@app.route('/da_var')
def some_func():
    my_var={'name':'Barry Bornstein',
            'favorite_bet':'20 cents'}
    return render_template('test_var.html',my_variable=my_var)


if __name__=='__main__':
    app.run(debug=True)
