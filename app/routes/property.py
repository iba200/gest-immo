from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.property import Property
from app.forms.property import PropertyForm
from datetime import datetime

property_bp = Blueprint('property', __name__)

@property_bp.route('/')
@login_required
def index():
    # Base query: only non-deleted properties for current user
    query = Property.query.filter_by(user_id=current_user.id, is_deleted=False)
    
    # Get filter parameters
    property_type = request.args.get('type', '')
    status = request.args.get('status', '')
    city = request.args.get('city', '')
    search = request.args.get('search', '')
    
    # Apply filters
    if property_type:
        query = query.filter_by(type=property_type)
    if status:
        query = query.filter_by(status=status)
    if city:
        query = query.filter(Property.city.ilike(f'%{city}%'))
    if search:
        query = query.filter(
            (Property.name.ilike(f'%{search}%')) | 
            (Property.address.ilike(f'%{search}%'))
        )
    
    # Pagination (Section 8.2)
    page = request.args.get('page', 1, type=int)
    per_page = 50
    pagination = query.order_by(Property.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    properties = pagination.items
    
    # Get unique cities for filter dropdown
    cities = db.session.query(Property.city).filter_by(
        user_id=current_user.id, is_deleted=False
    ).distinct().all()
    cities = [c[0] for c in cities]
    
    return render_template('properties/list.html', 
                         properties=properties,
                         pagination=pagination,
                         cities=cities,
                         filters={
                             'type': property_type,
                             'status': status,
                             'city': city,
                             'search': search
                         })

@property_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    # Check property limit (Section 6.1)
    if not current_user.can_add_property:
        flash(f'Vous avez atteint la limite de {current_user.property_limit} biens pour votre forfait {current_user.plan}. Veuillez passer au forfait supérieur.', 'warning')
        return redirect(url_for('property.index'))

    form = PropertyForm()
    if form.validate_on_submit():
        property = Property(
            name=form.name.data,
            type=form.type.data,
            address=form.address.data,
            city=form.city.data,
            neighborhood=form.neighborhood.data,
            bedrooms=form.bedrooms.data,
            bathrooms=form.bathrooms.data,
            surface=form.surface.data,
            rent_amount=form.rent_amount.data,
            charges=form.charges.data,
            security_deposit=form.security_deposit.data,
            description=form.description.data,
            user_id=current_user.id
        )
        
        # Handle Equipment (multiple selection)
        import json
        if form.equipment.data:
            property.equipment = json.dumps(form.equipment.data)
        
        # Handle Photos
        from app.utils.file_upload import save_file
        
        saved_photos = []
        if form.photos.data:
            for photo in form.photos.data:
                filename = save_file(photo, 'properties', max_size_mb=5)
                if filename:
                    saved_photos.append(filename)
                else:
                    flash(f"La photo {photo.filename} est trop volumineuse (max 5MB).", "warning")
        
        property.photos = json.dumps(saved_photos)
        
        db.session.add(property)
        db.session.commit()
        flash('Bien immobilier ajouté avec succès.', 'success')
        return redirect(url_for('property.index'))
    return render_template('properties/create.html', form=form, title='Ajouter un bien')

@property_bp.route('/<int:id>')
@login_required
def show(id):
    property = Property.query.get_or_404(id)
    if property.user_id != current_user.id:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('property.index'))
    return render_template('properties/show.html', property=property)

@property_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    property = Property.query.get_or_404(id)
    if property.user_id != current_user.id:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('property.index'))
    
    form = PropertyForm(obj=property)
    if form.validate_on_submit():
        form.populate_obj(property)
        db.session.commit()
        flash('Bien mis à jour avec succès.', 'success')
        return redirect(url_for('property.show', id=property.id))
        
    return render_template('properties/create.html', form=form, title='Modifier le bien')

@property_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    property = Property.query.get_or_404(id)
    if property.user_id != current_user.id:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('property.index'))
    
    # Soft delete
    property.is_deleted = True
    property.deleted_at = datetime.utcnow()
    db.session.commit()
    flash(f'Bien "{property.name}" supprimé avec succès.', 'success')
    return redirect(url_for('property.index'))
