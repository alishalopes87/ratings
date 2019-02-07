"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/login', methods=['POST'])
def login():
    """Add user to session"""

    email = request.form['username']
    password = request.form['password']

    # check if email in db
    try:
        User.query.filter(User.email == email).one()

        # check if already logged in via session
        if email in session:

            flash("You're already logged in as {}".format(email))
            return render_template('homepage.html')

        else:
            user = User.query.filter(User.email == email).one()
            if user.password == password:

                session['email'] = email
                session['password'] = password

            flash("Successfully logged in")

            return render_template("homepage.html")
            # validate pw via pw in database

    except:
        return redirect("/register")
        # redirect to register


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html",
                            users=users)

@app.route('/register', methods=["GET"])
def register_form():
    """Recieve user information"""

    return render_template("register_form.html")

@app.route('/register', methods=["POST"])
def register_process():
    """Add user information to database"""

    email = request.form["email"]
    password = request.form['password']

    try:
        User.query.filter(User.email == email ).one()
    
    except:
        user = User(email=email,
                    password=password)
        
        db.session.add(user)
        db.session.commit()

    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
