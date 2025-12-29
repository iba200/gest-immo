import os
from flask import Flask
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Mail
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

mail = Mail(app)

def test_email():
    with app.app_context():
        msg = Message("Test Mail ImmoGest",
                      recipients=[app.config['MAIL_USERNAME']])
        msg.body = "Ceci est un message de test pour vérifier la configuration e-mail de votre application ImmoGest."
        
        try:
            print(f"Tentative d'envoi d'un e-mail à {app.config['MAIL_USERNAME']}...")
            mail.send(msg)
            print("Succès ! L'e-mail a été envoyé correctement.")
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'e-mail : {str(e)}")

if __name__ == "__main__":
    test_email()
