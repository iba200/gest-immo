from app import db
from datetime import datetime

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receipt_number = db.Column(db.String(20), unique=True, nullable=False)  # IMO-2025-0001
    
    # Payment breakdown
    rent = db.Column(db.Float, nullable=False)  # Loyer de base
    charges = db.Column(db.Float, default=0.0)  # Charges mensuelles
    penalties = db.Column(db.Float, default=0.0)  # Pénalités de retard
    discount = db.Column(db.Float, default=0.0)  # Remise éventuelle
    amount = db.Column(db.Float, nullable=False)  # Total = rent + charges + penalties - discount
    
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    
    period_month = db.Column(db.Integer, nullable=False) # 1-12
    period_year = db.Column(db.Integer, nullable=False)  # 2024, 2025
    
    payment_method = db.Column(db.String(50), nullable=False) # Cash, Wave, OM, Virement
    transaction_ref = db.Column(db.String(100)) # Optional reference
    
    status = db.Column(db.String(20), default='Vérifié') # Vérifié, En attente (if online)
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False, index=True)
    tenant = db.relationship('Tenant', backref=db.backref('payments', lazy=True))
    
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False, index=True)
    prop = db.relationship('Property', backref=db.backref('payments', lazy=True))
    
    @staticmethod
    def generate_receipt_number():
        """Generate unique receipt number: IMO-YYYY-XXXX"""
        from datetime import datetime
        year = datetime.now().year
        # Get last payment of current year
        last_payment = Payment.query.filter(
            Payment.receipt_number.like(f'IMO-{year}-%')
        ).order_by(Payment.id.desc()).first()
        
        if last_payment:
            # Extract number and increment
            last_num = int(last_payment.receipt_number.split('-')[-1])
            new_num = last_num + 1
        else:
            new_num = 1
        
        return f'IMO-{year}-{new_num:04d}'
    
    @property
    def is_late(self):
        """Check if payment is late (received more than 10 days after expected date)"""
        from datetime import datetime, timedelta
        from calendar import monthrange
        
        # Expected payment date: last day of the period month
        _, last_day = monthrange(self.period_year, self.period_month)
        expected_date = datetime(self.period_year, self.period_month, last_day).date()
        
        # Payment is late if received more than 10 days after expected
        grace_period = timedelta(days=10)
        return self.date > (expected_date + grace_period)
    
    def __repr__(self):
        return f'<Payment {self.receipt_number} - {self.amount} FCFA>'
