from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, TextAreaField, \
    BooleanField
from wtforms.validators import InputRequired, Regexp, Email, EqualTo, Length, \
    ValidationError

from brocat import app
from brocat.models import Users


# * CUSTOM VALIDATOR
class AllowedExtensions(object):
    def __init__(self, message=None, allowed_extensions=None):
        if not message:
            message = 'This file extension is not allowed.'

        self.message = message
        self.allowed_extensions = allowed_extensions

    def __call__(self, form, field):
        filename = field.data.filename
        if '.' not in filename:
            raise ValidationError(self.message)

        file_format = filename.rsplit('.', 1)[1].lower()
            
        if file_format not in self.allowed_extensions:
            raise ValidationError(self.message)
        
    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        self.__message = value

    @message.getter
    def message(self):
        return self.__message + ' Use ' + ', '.join(self.allowed_extensions) + ' instead.'


class CreateAccountForm(FlaskForm):
    email = StringField(
        label='Email',
        validators=[
            InputRequired('E-mail field is required.'),
            Email('Invalid e-mail address.'),
            Regexp(
                regex=r'[^@]+@[^@]+\.[a-zA-Z]{2,6}',
                message='Use this format your e-mail address someone@example.com.'
            )
        ]
    )
    username = StringField(
        label='Username',
        validators=[
            InputRequired('Username field is required'),
            Length(max=16, message="The username must be less or equal to 16 characters.")
        ]
    )
    password = PasswordField(
        label='Password',
        validators=[
            InputRequired('Password field is required.'),
            EqualTo('confirm_password', message='Passwords must match.'),
            Regexp(
                regex=r'^(?=.*[0-9]+.*)(?=.*[a-zA-Z]+.*)[0-9a-zA-Z]{6,}$',
                message='Password must contain at least one letter, \
                    at least one number, and be longer than six charaters.'
            )
        ]
    )
    confirm_password = PasswordField(label='Confirm Password',
        validators=[InputRequired('Confirm your password.')]
    ) 

    def validate_email(form, email):
        email_exists = Users.query.filter_by(e_mail=email.data).first()
        if email_exists:
            raise ValidationError('Email already exists')
    
    def validate_username(form, username):
        user_exists = Users.query.filter_by(username=username.data).first() 
        if user_exists:
            raise ValidationError('Username already exists')


class LoginForm(FlaskForm):
    username = StringField(label='Username', 
        validators=[InputRequired('Username field is required')]
    )
    password = PasswordField(label='Password',
        validators=[InputRequired('Password field is requiered')]
    )
    remember = BooleanField(label='Remember me?')


class UploadBrocatForm(FlaskForm):
    title = StringField(
        label='Title',
        validators=[
            InputRequired('The Brocat needs a title!'),
            Length(max=100, message='100 is the maximum characters for a title')
        ]
    )
    thumbnail = FileField(
        label='Thumbnail',
        validators=[
            InputRequired('We need an awesome thumbnail!'),
            AllowedExtensions(allowed_extensions=app.config['ALLOWED_IMAGES_EXTENSIONS'])
        ]
    )
    audio = FileField(
        label='Audio', 
        validators=[
            InputRequired('We need your Brocat here!'),
            AllowedExtensions(allowed_extensions=app.config['ALLOWED_AUDIOS_EXTENSIONS'])
        ])
    description = TextAreaField(label='Description')

