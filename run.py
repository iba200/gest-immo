from app import create_app, db
# Import models here to ensure they are registered with SQLAlchemy
from app.models.user import User

app = create_app()

@app.shell_context_processor
def make_shell_context():
    from app.models.property import Property
    from app.models.payment import Payment
    return {'db': db, 'User': User, 'Property': Property, 'Tenant': Tenant, 'Payment': Payment}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
