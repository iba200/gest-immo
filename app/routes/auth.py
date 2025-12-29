from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db, limiter
from app.models.user import User
from app.forms.auth import LoginForm, RegistrationForm, ProfileForm, ResetPasswordRequestForm, ResetPasswordForm
from urllib.parse import urlsplit

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per 15 minutes")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Try email first
        user = User.query.filter_by(email=form.identifier.data).first()
        # If not found by email, try phone
        if not user:
            user = User.query.filter_by(phone=form.identifier.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Email/Téléphone ou mot de passe invalide', 'error')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.dashboard') # Redirect to dashboard after login
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Connexion', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Félicitations, vous êtes maintenant inscrit !', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Inscription', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    from app.forms.auth import ProfileForm
    form = ProfileForm(obj=current_user)
    
    if form.validate_on_submit():
        # Check uniqueness if changed
        if form.email.data != current_user.email:
             if User.query.filter_by(email=form.email.data).first():
                 flash('Email déjà utilisé.', 'error')
                 return render_template('auth/profile.html', form=form)
        
        if form.phone.data != current_user.phone:
             if User.query.filter_by(phone=form.phone.data).first():
                 flash('Téléphone déjà utilisé.', 'error')
                 return render_template('auth/profile.html', form=form)

        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.company_name = form.company_name.data
        current_user.company_address = form.company_address.data
        
        # Handle logo upload
        if form.company_logo.data:
            from app.utils.file_upload import save_file
            filename = save_file(form.company_logo.data, 'logos', max_size_mb=2)
            if filename:
                current_user.company_logo = filename
            else:
                flash("Le logo est trop volumineux (max 2MB).", "warning")
        
        db.session.commit()
        flash('Profil mis à jour avec succès.', 'success')
        return redirect(url_for('auth.profile'))
        
    return render_template('auth/profile.html', title='Mon Profil', form=form)

@auth_bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    from app.forms.auth import ResetPasswordRequestForm
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.get_reset_token()
            from app.utils.email import send_email
            
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            html_body = render_template('auth/email/reset_password.html', user=user, url=reset_url)
            text_body = render_template('auth/email/reset_password.txt', user=user, url=reset_url)
            
            send_email('Réinitialisation de votre mot de passe',
                       current_app.config['MAIL_DEFAULT_SENDER'],
                       [user.email],
                       text_body,
                       html_body)
            
        flash('Consultez votre email pour les instructions.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', title='Mot de passe oublié', form=form)

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    user = User.verify_reset_token(token)
    if not user:
        flash('Lien invalide ou expiré.', 'error')
        return redirect(url_for('auth.login'))
        
    from app.forms.auth import ResetPasswordForm
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Votre mot de passe a été réinitialisé.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/reset_password.html', title='Nouveau mot de passe', form=form)
