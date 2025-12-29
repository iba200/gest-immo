from app import db
from datetime import datetime

import builtins

class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20), unique=True, nullable=False, index=True)
    
    job_description = db.Column(db.String(200))
    emergency_contact = db.Column(db.String(100))
    documents = db.Column(db.Text) # JSON string of filenames (CNI, Contract, etc.)
    
    
    is_active = db.Column(db.Boolean, default=True)
    
    # Soft delete
    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, index=True) # Nullable for now to ease migration, but logic should enforce it
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), index=True)
    property = db.relationship('Property', backref=db.backref('tenants', lazy=True))
    
    @builtins.property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @builtins.property
    def document_list(self):
        import json
        if self.documents:
            return json.loads(self.documents)
        return []

    def __repr__(self):
        return f'<Tenant {self.first_name} {self.last_name}>'
