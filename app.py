from flask import Flask, request, make_response, render_template, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import *

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

### Models ###


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


@app.route("/")
def index():
    return render_template("pages/index.html")


@app.route("/profile/<user>")
def profile(user):
    return render_template("pages/profile.html", user=user)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        # return redirect(url_for('index'))
    return render_template('pages/add.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))

## Hooks ###

# @app.before_request
# def before_request():
#     print(request.method, request.endpoint)

# @app.after_request
# def after_request(response):
#     print(response.status)
#     print(response.headers)
#     print(response.get_data())
#     return response


if __name__ == "__main__":
    app.run()
