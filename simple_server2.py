from flask import Flask, flash, redirect, render_template, request, url_for

app=Flask(__name__)

@app.route('/')
def index():
    return render_template(
        'test_drop.html',
        data=[{'action':'keep'}, {'action':'fold'},])

@app.route("/test" , methods=['GET', 'POST'])
def test():
    select = request.form.get('Hand_1')
    print(f"Select: {select}")
    return(str(select)) # just to see what select is

if __name__=='__main__':
    app.run(debug=True)
