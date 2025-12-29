from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Removed duplicate 'from flask_mail import Mail'

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"]) # Initialized limiter globally
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
login_manager.login_message_category = 'info' # Added this line as per the provided edit snippet

def create_app(config_class=Config): # Changed default config_class to Config
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    limiter.init_app(app) # Initialized limiter with app

    # Register Blueprints
    # from app.routes import main as main_blueprint
    # app.register_blueprint(main_blueprint)
    
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.routes.property import property_bp
    app.register_blueprint(property_bp, url_prefix='/properties')
    
    from app.routes.tenant import tenant_bp
    app.register_blueprint(tenant_bp, url_prefix='/tenants')
    
    from app.routes.payment import payment_bp
    app.register_blueprint(payment_bp, url_prefix='/payments')
    
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    register_error_handlers(app)
    
    from app.cli import automation_cli
    app.cli.add_command(automation_cli)

    return app

def register_error_handlers(app):
    from flask import render_template
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
