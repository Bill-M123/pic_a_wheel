from flask import Flask
from flask import render_template



#######Additional imports from clyde

from flask import flash
from flask import request, session, redirect, url_for
from flask_login import LoginManager,UserMixin

#########################
from flask_login import login_required,current_user


app = Flask("demo")
app.config["TESTING"] = True
app.config["SECRET_KEY"] = "thisisverysecret"
app.config["OBSERVE_AUTO_BIND_VIEWS"] = True

login_manager = LoginManager(app)
login_manager.init_app(app)

class User(UserMixin):
        username = "alice"

        def get_id(self):
            return 1

@app.route("/login", methods=["GET"])
def login_handler():
        if request.form.get("username") == "bad":
            abort(403)
        return f'Bad Username'

@app.route("/hello", methods=["GET"])
def hello():
        from flask_login import current_user, login_user

        login_user(User())

        return f"hello, {current_user.username}"

@app.route("/error", methods=["GET"])
def error():
        errorcode = request.form.get("errorcode")
        if errorcode is not None:
            abort(int(errorcode))
        return make_response("", 200)

        with app.app_context():
            yield app

if __name__=='__main__':
    app.run(debug=True)
