from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, BooleanField, SubmitField   
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, ValidationError
from werkzeug.utils import secure_filename
from .models import User
from markupsafe import Markup

def file_type_check(form, field):
    if field.data:
        filename = field.data.filename
        if not (filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg')):
            raise ValidationError('Invalid file type. Only .jpg, .jpeg and .png files are allowed.')

class ProfilePictureForm(FlaskForm):
    profile_picture = FileField('Profile Picture', validators=[file_type_check])
    submit = SubmitField('Upload')

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

    #submit_value = Markup('<button class=login-button" id="login-button-login">SIGN UP</button>')
    submit = SubmitField()

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


class SearchUserForm(FlaskForm):
    search=StringField("search user", validators=[Length(min=0, max=25)])

class CommentForm(FlaskForm):
    comment = StringField('Comment this profile', validators=[DataRequired(), Length(min=1, max=300, message="Use at most 300 characters.")])

    def validate(self):
        return True