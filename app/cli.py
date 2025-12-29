from flask.cli import AppGroup
from app import db
from app.models.tenant import Tenant
from app.models.payment import Payment
from app.models.property import Property  # Ensure models are loaded
from app.utils.sms import SMSService
from datetime import datetime

automation_cli = AppGroup('automation')

@automation_cli.command('check-payments')
def check_payments():
    """Checks for unpaid rents and sends SMS reminders."""
    print("Starting payment check...")
    
    # Logic:
    # 1. Identify current month/year
    # 2. Find tenants with active properties
    # 3. Check if they have a payment for current month
    # 4. If not, send SMS
    
    now = datetime.now()
    month = now.month
    year = now.year
    
    # Tenants with active property (status 'Occupe')
    # Or just check all tenants with a property_id
    tenants = Tenant.query.filter(Tenant.property_id != None).all()
    
    for tenant in tenants:
        # Check payment
        payment = Payment.query.filter_by(
            tenant_id=tenant.id,
            period_month=month,
            period_year=year
        ).first()
        
        if not payment:
            # Unpaid
            print(f"Tenant {tenant.full_name} has NOT paid for {month}/{year}.")
            
            # Send SMS
            message = f"Bonjour {tenant.first_name}, sauf erreur, le loyer de {month}/{year} pour {tenant.property.name} est en attente. Merci de régulariser."
            SMSService.send_sms(tenant.phone, message)
        else:
             print(f"Tenant {tenant.full_name} has paid.")
             
    print("Payment check complete.")
