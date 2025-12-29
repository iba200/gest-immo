from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, Optional, ValidationError
from app.models.user import User

class LoginForm(FlaskForm):
    identifier = StringField('Email ou Téléphone', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')

class RegistrationForm(FlaskForm):
    first_name = StringField('Prénom', validators=[DataRequired(), Length(max=100)])
    last_name = StringField('Nom', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Téléphone', validators=[
        DataRequired(),
        Regexp(r'^\+221\d{9}$', message="Le téléphone doit être au format +221XXXXXXXXX")
    ])
    password = PasswordField('Mot de passe', validators=[
        DataRequired(),
        Length(min=8, message="Le mot de passe doit contenir au moins 8 caractères."),
        Regexp(r'(?=.*[A-Z])(?=.*\d)', message="Le mot de passe doit contenir au moins 1 majuscule et 1 chiffre.")
    ])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(), 
        EqualTo('password', message="Les mots de passe doivent correspondre.")
    ])
    submit = SubmitField('S\'inscrire')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Cet email est déjà utilisé.')

    def validate_phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('Ce numéro de téléphone est déjà utilisé.')

class ProfileForm(FlaskForm):
    first_name = StringField('Prénom', validators=[DataRequired(), Length(max=100)])
    last_name = StringField('Nom', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Téléphone', validators=[
        DataRequired(),
        Regexp(r'^\+221\d{9}$', message="Le téléphone doit être au format +221XXXXXXXXX")
    ])
    
    # Company Information
    company_name = StringField('Nom Entreprise/Activité', validators=[Optional(), Length(max=200)])
    company_address = TextAreaField('Adresse Entreprise', validators=[Optional(), Length(max=300)])
    company_logo = FileField('Logo Entreprise', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images seulement (JPG, PNG)')
    ])
    
    submit = SubmitField('Mettre à jour')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Demander un nouveau mot de passe')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nouveau mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(), 
        EqualTo('password', message="Les mots de passe doivent correspondre.")
    ])
    submit = SubmitField('Réinitialiser le mot de passe')
