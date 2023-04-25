import functools
import logging
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
from flask import current_app
from logging.handlers import SMTPHandler


bp = Blueprint('auth', __name__, url_prefix='/auth')

mail_handler = SMTPHandler(
    mailhost=('127.0.0.1',8025),
    fromaddr='manikanta.reddy@thinkitive.com',
    toaddrs=['reddymani707@gmail.com'],
    subject='Application Error'
)
mail_handler.setLevel(logging.ERROR)
mail_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view

@bp.route('/index', methods=('GET', 'POST'))
def index():
    if 'username' in session:
        print(session["username"],'----------username')
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username."
            current_app.logger.info('%s invalid username', username)
            current_app.logger.addHandler(mail_handler)
            current_app.logger.debug("Logging -loged in")
            current_app.logger.info('U logged in')
            current_app.logger.warning("You are logging Working")
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."
            current_app.logger.info('%s invalid password', password)

        if error is None:
            # store the user id in a new session and return to the index
            current_app.logger.info('%s logged in successfully', user["username"])
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("blog.index"))

        flash(error)

    return render_template("auth/login.html")

@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("blog.index"))

