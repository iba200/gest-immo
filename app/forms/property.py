from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, FloatField, SelectField, SelectMultipleField, TextAreaField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class PropertyForm(FlaskForm):
    name = StringField('Nom du bien', validators=[DataRequired(), Length(max=100)])
    type = SelectField('Type', choices=[
        ('Appartement', 'Appartement'),
        ('Maison', 'Maison'),
        ('Villa', 'Villa'),
        ('Studio', 'Studio'),
        ('Magasin', 'Magasin'),
        ('Bureau', 'Bureau'),
        ('Autre', 'Autre')
    ], validators=[DataRequired()])
    
    address = StringField('Adresse', validators=[DataRequired(), Length(max=200)])
    city = StringField('Ville', validators=[DataRequired(), Length(max=100)])
    neighborhood = StringField('Quartier', validators=[Optional(), Length(max=100)])
    
    bedrooms = IntegerField('Chambres', validators=[Optional(), NumberRange(min=0)])
    bathrooms = IntegerField('Salles de bain', validators=[Optional(), NumberRange(min=0)])
    surface = FloatField('Surface (m²)', validators=[Optional(), NumberRange(min=0)])
    
    rent_amount = FloatField('Loyer Mensuel', validators=[DataRequired(), NumberRange(min=0)])
    charges = FloatField('Charges Mensuelles', validators=[Optional(), NumberRange(min=0)])
    security_deposit = FloatField('Caution', validators=[Optional(), NumberRange(min=0)])
    
    equipment = SelectMultipleField('Équipements', choices=[
        ('parking', 'Parking'),
        ('jardin', 'Jardin'),
        ('meuble', 'Meublé'),
        ('piscine', 'Piscine'),
        ('climatisation', 'Climatisation'),
        ('wifi', 'WiFi'),
        ('gardien', 'Gardien')
    ], validators=[Optional()])
    
    photos = MultipleFileField('Photos', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images seulement!')
    ])

    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Enregistrer')
