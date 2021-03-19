from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import InputRequired, Length, Email


class RegisterForm(FlaskForm):
    """ Register a user """

    username = StringField("Username",
        validators=[InputRequired(), Length(min=1, max=20)])

    password = PasswordField("Password",
        validators=[InputRequired()])

    email = StringField("Email",
        validators=[InputRequired(), Length(min=1, max=50), Email()])
    
    first_name = StringField("First Name",
        validators=[InputRequired(), Length(min=1, max=30)])

    last_name = StringField("Last Name",
        validators=[InputRequired(), Length(min=1, max=30)])


class LoginForm(FlaskForm):
    """ Login a user """

    username = StringField("Username",
        validators=[InputRequired(), Length(min=1, max=20)])

    password = PasswordField("Password",
        validators=[InputRequired()])


class NoteForm(FlaskForm):
    """Lets user add notes."""
    title = StringField("Title",
        validators=[InputRequired(), Length(min=1, max=100)])
    content = StringField("Content",
        validators=[InputRequired()])
    


