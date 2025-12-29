from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256))
    
    # Company/Business Information
    company_name = db.Column(db.String(200))
    company_address = db.Column(db.String(300))
    company_logo = db.Column(db.String(200))  # Path to uploaded logo
    
    # Subscription Plan (Section 6.1)
    # Choices: 'Starter', 'Professionnel', 'Premium'
    plan = db.Column(db.String(20), default='Starter')
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    @property
    def property_limit(self):
        """Returns the maximum number of properties allowed for the user's plan"""
        limits = {
            'Starter': 5,
            'Professionnel': 20,
            'Premium': 50
        }
        return limits.get(self.plan, 5)

    @property
    def can_add_property(self):
        """Checks if the user has reached their property limit"""
        from app.models.property import Property
        current_count = Property.query.filter_by(user_id=self.id, is_deleted=False).count()
        return current_count < self.property_limit

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_sec=1800):
        from flask import current_app
        from itsdangerous import URLSafeTimedSerializer
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps(self.id, salt='password-reset-salt')

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        from flask import current_app
        from itsdangerous import URLSafeTimedSerializer
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, salt='password-reset-salt', max_age=expires_sec)
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f'<User {self.email}>'
