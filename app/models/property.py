from app import db
from datetime import datetime

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Appartement, Villa, etc.
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    neighborhood = db.Column(db.String(100))
    
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    surface = db.Column(db.Float)  # m2
    
    rent_amount = db.Column(db.Float, nullable=False)
    charges = db.Column(db.Float, default=0.0)
    security_deposit = db.Column(db.Float, default=0.0)
    
    
    status = db.Column(db.String(20), default='Vacant')  # Vacant, Occupe, Maintenance
    equipment = db.Column(db.Text)  # JSON string: parking, jardin, meublé, etc.
    photos = db.Column(db.Text) # JSON string of filenames
    description = db.Column(db.Text)
    
    # Soft delete
    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    user = db.relationship('User', backref=db.backref('properties', lazy=True))
    
    @property
    def photo_list(self):
        import json
        if self.photos:
            return json.loads(self.photos)
        return []
    
    @property
    def equipment_list(self):
        import json
        if self.equipment:
            return json.loads(self.equipment)
        return []

    def __repr__(self):
        return f'<Property {self.name}>'
