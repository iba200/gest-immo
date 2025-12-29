from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, Regexp, Optional

class TenantForm(FlaskForm):
    first_name = StringField('Prénom', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Nom', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[Optional(), Email()])
    phone = StringField('Téléphone', validators=[
        DataRequired(),
        Regexp(r'^\+221\d{9}$', message="Le format doit être +221XXXXXXXXX")
    ])
    job_description = StringField('Profession / Employeur', validators=[Optional(), Length(max=200)])
    emergency_contact = StringField("Contact d'urgence", validators=[Optional(), Length(max=100)])
    
    documents = FileField('Documents (PDF/Images)', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'pdf'], 'Images et PDF seulement!')
    ])
    
    # Property assignment will be handled dynamically or via a separate logic if needed, 
    # but strictly speaking a SelectField for properties could be here if we pass choices dynamically.
    # For now, we'll keep it simple and manage assignment in the route or a dedicated form if complex.
    
    submit = SubmitField('Enregistrer')
