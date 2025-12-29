from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, StringField, IntegerField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Optional
from datetime import datetime

class PaymentForm(FlaskForm):
    tenant_id = SelectField('Locataire', coerce=int, validators=[DataRequired()])
    
    # Breakdown of payment
    rent = FloatField('Loyer', validators=[DataRequired(), NumberRange(min=0)])
    charges = FloatField('Charges', validators=[Optional(), NumberRange(min=0)], default=0)
    penalties = FloatField('Pénalités', validators=[Optional(), NumberRange(min=0)], default=0)
    discount = FloatField('Remise', validators=[Optional(), NumberRange(min=0)], default=0)
    amount = FloatField('Montant Total', validators=[DataRequired(), NumberRange(min=0)])
    
    date = DateField('Date de paiement', default=datetime.utcnow, validators=[DataRequired()])
    
    period_month = SelectField('Mois', coerce=int, choices=[
        (1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'),
        (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'),
        (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')
    ], validators=[DataRequired()])
    
    period_year = IntegerField('Année', default=datetime.now().year, validators=[DataRequired()])
    
    payment_method = SelectField('Mode de paiement', choices=[
        ('Espèces', 'Espèces'),
        ('Wave', 'Wave'),
        ('Orange Money', 'Orange Money'),
        ('Virement', 'Virement'),
        ('Autre', 'Autre')
    ], validators=[DataRequired()])
    
    transaction_ref = StringField('Référence transaction', validators=[Optional()])
    notes = TextAreaField('Notes', validators=[Optional()])
    
    submit = SubmitField('Enregistrer le paiement')
