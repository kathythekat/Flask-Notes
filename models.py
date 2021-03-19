from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """ Site User """

    __tablename__ = "users"

    username = db.Column(db.String(20),
                    primary_key=True,
                    nullable=False)

    password = db.Column(db.Text,
                    nullable=False)

    email = db.Column(db.String(50),
                    nullable=False,
                    unique=True)

    first_name = db.Column(db.String(30),
                    nullable=False)

    last_name = db.Column(db.String(30),
                    nullable=False)
    
    notes = db.relationship('Note')

    def __repr__(self):
        """Show info about user."""
        return f"<User username:{self.username} email:{self.email} first_name:{self.first_name} last_name:{self.last_name}>"


    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        hashed = bcrypt.generate_password_hash(pwd).decode("utf8")
        return cls(username=username, password=hashed, email=email, first_name=first_name, last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, pwd):
        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u

        else:
            return False

class Note(db.Model):
    """Notes"""
    __tablename__ = "notes"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    title = db.Column(db.Text,
                    nullable=False)

    content = db.Column(db.Text,
                    nullable=False
                   )
    owner = db.Column(db.String(50),
        db.ForeignKey('users.username', ondelete="CASCADE"))

    user = db.relationship('User')