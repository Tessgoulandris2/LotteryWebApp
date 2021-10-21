import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Email, Length, EqualTo, ValidationError


def special_characters_search(form, field):
    exclude_special_characters = "*?!'^%&/()=}][{$#@<>"
    for characters in field.data:
        if characters in exclude_special_characters:
            raise ValidationError(f"Special characters {characters} are not allowed.")


def password_authentication(self, password):
    p = re.compile(r'(?=.*\d)(?=.*[a-zA-Z])(?=.*[SPECIAL CHARACTERS])')
    if not p.match(self.password.data):
        raise ValidationError("Password must contain 1 digit and 1 upper and lowercase letter and 1 special "
                              "character.")


def phone_format(self, field):
    p = re.compile(r'\d{4}-\d{3}-\d{4}')
    if not p.match(field.data):
        raise ValidationError(f"Please enter your phone number in the format XXXX-XXX-XXXX.")


class RegisterForm(FlaskForm):
    email = StringField(validators=[Required(), Email()])
    firstname = StringField(validators=[Required(), special_characters_search])
    lastname = StringField(validators=[Required(), special_characters_search])
    phone = StringField(validators=[Required(), phone_format])
    password = PasswordField(validators=[Required(), Length(min=6, max=12, message='Password needs to have a minimum '
                                                                                   'length of 6 characters or a '
                                                                                   'maximum of 12.'),
                                         password_authentication])
    confirm_password = PasswordField(validators=[Required(), EqualTo('password', message='Both passwords inputs must '
                                                                                         'match.')])
    pin_key = StringField(validators=[Required(), Length(32, message='Pin Key must be 32 characters long')])
    submit = SubmitField()


class LoginForm(FlaskForm):
    email = StringField(validators=[Required(), Email()])
    password = PasswordField(validators=[Required()])
    submit = SubmitField()