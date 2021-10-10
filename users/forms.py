from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Email, Length, EqualTo, ValidationError


def special_characters_search(form, field):
    exclude_special_characters = "*?!'^%&/()=}][{$#@<>"
    for characters in field.data:
        if characters in exclude_special_characters:
            raise ValidationError(f"Special characters {characters} are not allowed.")


class RegisterForm(FlaskForm):
    email = StringField(validators=[Required(), Email()])
    firstname = StringField(validators=[Required(), special_characters_search])
    lastname = StringField(validators=[Required(), special_characters_search])
    phone = StringField(validators=[Required()])
    password = PasswordField(validators=[Required(), Length(min=6, max=12, message='Password needs to have a minimum '
                                                                                   'length of 6 characters or a '
                                                                                   'maximum of 12.')])
    confirm_password = PasswordField(validators=[Required(), EqualTo('password', message='Both passwords inputs must '
                                                                                         'match.')])
    pin_key = StringField(validators=[Required()])
    submit = SubmitField()
