from flask import Flask, render_template, redirect, flash, session, request

from models import db, connect_db, User, Note

from forms import RegisterForm, LoginForm, NoteForm
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///notes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

@app.route("/")
def homepage():

    return redirect("/register")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('401.html'), 404


@app.route("/register", methods=["GET", "POST"])
def register():
    if "username" in session:
        return redirect(f'/users/{session["username"]}')
    users = User.query.all()
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            username = form.username.data
            password = form.password.data
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data

            user = User.register(username, password, email, first_name, last_name)
            db.session.add(user)
            db.session.commit()

        except IntegrityError:
            if username in users:
                flash("Username already exists.", 'danger')
            else:
                flash("Email already exists", 'danger')
            return render_template('register.html', form=form)

        session["username"] = user.username
        return redirect(f"/users/{username}")
    else:
        return render_template("register.html", form=form)

@app.route("/users/<username>")
def show_secret_page(username):
    users = User.query.all()
    user_dict = dict()
    for user in users:
        user_dict.setdefault(user.username, user.first_name)
        
    if username not in user_dict:
        return render_template("401.html"), 404
 
    user = User.query.get(username)

    if "username" not in session:
        flash("You must be logged in to view!")
        return render_template("401.html"), 401

    elif session["username"] != user.username:
        flash("You are not authorized.")
        return render_template("401.html"), 401

    return render_template("user_info.html", user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(f'/users/{session["username"]}')

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username  # keep logged in
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Incorrect name/password"]

    return render_template("login.html", form=form)

# end-login

@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    session.pop("username", None)

    return redirect("/")


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
     user = User.query.get(username)
     
     db.session.delete(user)

     db.session.commit()
     session.pop("username", None)

     return redirect("/")

@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def add_notes(username):
    user = User.query.get(username)

    form = NoteForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note = Note(title=title, content=content, owner=username)
        db.session.add(note)
        db.session.commit()

        return redirect(f"/users/{username}")

    return render_template("notes.html", form=form)

@app.route("/notes/<int:note_id>/update", methods=["GET", "POST"])
def update_note(note_id):

    note = Note.query.get_or_404(note_id)
    form = NoteForm(obj=note)

    if "username" not in session:
        flash("You must be logged in to update note!")
        return redirect("/")

    if not (session["username"] == note.user.username):
        flash("You're not authorized")
        return redirect("/")

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note.title = title
        note.content = content
        db.session.commit()

        return redirect(f"/users/{note.user.username}")

    return render_template("/update_note.html", form=form)

@app.route("/notes/<int:note_id>/delete", methods=["POST"])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    curr_user = note.user.username

    if "username" not in session:
        flash("You must be logged in to update note!")
        return redirect("401.html"), 401

    if not (session["username"] == curr_user):
        flash("You're not authorized")
        return redirect("401.html"), 401

    db.session.delete(note)
    db.session.commit()

    return redirect(f"/users/{curr_user}")





