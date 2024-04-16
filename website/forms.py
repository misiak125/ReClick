from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

from .models import User


class LoginForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField('Remember me', validators=[])


class RegisterForm(FlaskForm):
    email = EmailField(
        "email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    username = StringField(
        'username', validators=[Length(min=4, max=25)]
    )
    password = PasswordField(
        "password", validators=[
            DataRequired(), 
            Length(min=6, max=25), 
            Regexp(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}$', message="Password must contain at least one digit, one lowercase letter, and one uppercase letter.")
        ]
    )
    confirm = PasswordField(
        "confirm password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    show_password = BooleanField(
        'Show password', 
        id='check',
        validators=[]
        )

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords must match")
            return False
        return True