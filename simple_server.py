from flask import Flask
from flask import render_template

app=Flask(__name__)

@app.route('/')
def index():
    return '<h1>This shows the simplest home page, it renders a simple header</h1>'

@app.route('/clyde')
def info():
    return "<h1>My name is Clyde</h1>"

@app.route('/user/<name>')
def user(name):
    return f"<h1>This is {name}'s page</h1><p style='font-size:30px;'>10 &#9824;</p>"

@app.route('/raw_table')
def raw_table():
    return render_template('test3.html')

@app.route('/da_var')
def some_func():
    my_var={'name':'Barry Bornstein',
            'favorite_bet':'20 cents'}
    return render_template('test_var.html',my_variable=my_var)


if __name__=='__main__':
    app.run(debug=True)
