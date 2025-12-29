from app import create_app, db
from app.models.user import User
from app.models.property import Property
from app.models.tenant import Tenant
from app.models.payment import Payment
from datetime import datetime, timedelta
import random

app = create_app()

def seed():
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()

        print("Seeding data...")

        # Create User
        user = User(
            first_name='Admin',
            last_name='User',
            email='admin@example.com',
            phone='+221770000000',
            company_name='ImmoGest Agence',
            company_address='Dakar Plateau, Avenue Lamine Gueye'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        print(f"User created: {user.email} / password123")

        # Create Properties
        properties = []
        types = ['Appartement', 'Villa', 'Studio', 'Commercial']
        cities = ['Dakar', 'Thies', 'Saly', 'Saint-Louis']
        
        for i in range(1, 6):
            prop = Property(
                name=f"Residence {i}",
                type=random.choice(types),
                address=f"{i * 10} Rue de la Paix",
                city=random.choice(cities),
                neighborhood=f"Quartier {i}",
                bedrooms=random.randint(1, 5),
                bathrooms=random.randint(1, 3),
                surface=random.randint(50, 200),
                rent_amount=random.randint(150000, 500000),
                charges=random.randint(10000, 50000),
                security_deposit=random.randint(300000, 1000000),
                description=f"Beautiful property number {i} with great amenities.",
                user_id=user.id,
                status='Vacant',
                equipment='["Wifi", "Climatisation"]'
            )
            properties.append(prop)
            db.session.add(prop)
        
        db.session.commit()
        print(f"{len(properties)} Properties created.")

        # Create Tenants
        tenants = []
        for i in range(1, 5):
            tenant = Tenant(
                first_name=f"Tenant",
                last_name=f"{i}",
                email=f"tenant{i}@example.com",
                phone=f"+22177{'0'*6}{i}",
                job_description="Software Engineer",
                emergency_contact="+221708888888",
                user_id=user.id
            )
            # Assign to property
            prop = properties[i-1]
            tenant.property_id = prop.id
            prop.status = 'Occupe'
            
            tenants.append(tenant)
            db.session.add(tenant)
        
        db.session.commit()
        print(f"{len(tenants)} Tenants created and assigned.")

        # Create Payments
        # Create payments for the last 3 months for each tenant
        for tenant in tenants:
            prop = Property.query.get(tenant.property_id)
            current_date = datetime.now()
            
            for offset in range(3): # 0, 1, 2 months back
                # Move date back
                month_date = (current_date.replace(day=1) - timedelta(days=30*offset + 1)).replace(day=5)
                
                # Skip payment for current month (offset 0) for the last tenant to test alerts
                if offset == 0 and tenant == tenants[-1]:
                    continue
                
                payment = Payment(
                    receipt_number=Payment.generate_receipt_number(),
                    tenant_id=tenant.id,
                    property_id=prop.id,
                    rent=prop.rent_amount,
                    charges=prop.charges,
                    amount=prop.rent_amount + prop.charges,
                    date=month_date.date(),
                    period_month=month_date.month,
                    period_year=month_date.year,
                    payment_method='Virement',
                    notes='Payment received correctly.',
                    status='Vérifié'
                )
                db.session.add(payment)
                db.session.flush() # Ensure receipt numbers are generated correctly if sequence depends on it
        
        db.session.commit()
        print("Payments created. (Last tenant has unpaid rent for current month)")

        print("Seeding complete!")

if __name__ == '__main__':
    seed()
