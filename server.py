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

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Add user to session"""

    email = request.form['username']
    password = request.form['password']

    # check if email in db

    try: 
        user = User.query.filter(User.email == email).one()

        # flash("You're already logged in as {}".format(email))
        # return render_template('homepage.html')
        if user.password == password:

            session['email'] = email
            session['password'] = password

            flash("Successfully logged in")

            return render_template("homepage.html")
            # validate pw via pw in database
        else:
            flash("Password incorrect.")
            return render_template("homepage.html")


    except:
        return redirect("/register")
        # redirect to register
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    del session['email']
    del session['password']
    flash("Successfully logged out")

    return render_template("homepage.html")

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

@app.route('/users/<user>')
def show_user_info(user):
    """Show information about user"""

    # get age, zipcode, and list of movies rated by user from db
    # user_id = request.args.get('user.user_id')
    user = User.query.get(user)
    age = user.age
    zipcode = user.zipcode

    user_id = user.user_id 

    ratings_list = Rating.query.filter(Rating.user_id == user_id).all()
    
    movie_names = []
    for rating in ratings_list:

        # this query doesn't work yet 
        movie_name = Movie.query.filter(Movie.rating_id == rating["rating_id"]).all()
        movie_names.append(movie_name)


    return render_template('user_details.html',
                                user=user,
                                age=age,
                                zipcode=zipcode,
                                ratings=ratings_list,
                                movies=movie_list)


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
