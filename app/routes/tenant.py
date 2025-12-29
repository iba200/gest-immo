from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.tenant import Tenant
from app.models.property import Property
from app.forms.tenant import TenantForm
from datetime import datetime
tenant_bp = Blueprint('tenant', __name__)

@tenant_bp.route('/')
@login_required
def index():
    # Pagination (Section 8.2)
    page = request.args.get('page', 1, type=int)
    per_page = 50
    # Only show non-deleted tenants for the current user
    pagination = Tenant.query.filter_by(user_id=current_user.id, is_deleted=False).order_by(Tenant.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    tenants = pagination.items
    return render_template('tenants/list.html', tenants=tenants, pagination=pagination)

@tenant_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    form = TenantForm()
    # Get user's vacant properties for assignment selection
    properties = Property.query.filter_by(user_id=current_user.id).all() 
    # Logic to pass properties to template or form handling triggers here
    # For MVP we might want to select property in the URL or form
    
    if form.validate_on_submit():
        tenant = Tenant(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
            job_description=form.job_description.data,
            emergency_contact=form.emergency_contact.data,
            user_id=current_user.id
        )
        
        # Handle Documents
        import json
        from app.utils.file_upload import save_file
        
        saved_docs = []
        if form.documents.data:
             filename = save_file(form.documents.data, 'tenants', max_size_mb=16)
             if filename:
                 saved_docs.append(filename)
             else:
                 flash(f"Le document {form.documents.data.filename} est trop volumineux (max 16MB).", "warning")
        
        tenant.documents = json.dumps(saved_docs)
        
        # Handle property assignment
        property_id = request.form.get('property_id') or request.args.get('property_id')
        if property_id:
            prop = Property.query.get(property_id)
            if prop and prop.user_id == current_user.id:
                tenant.property_id = prop.id
                prop.status = 'Occupe'
        
        db.session.add(tenant)
        db.session.commit()
        flash('Locataire ajouté avec succès.', 'success')
        return redirect(url_for('tenant.index'))
        
    return render_template('tenants/create.html', form=form, title='Nouveau Locataire', properties=properties)

@tenant_bp.route('/<int:id>')
@login_required
def show(id):
    tenant = Tenant.query.get_or_404(id)
    if not tenant.property or tenant.property.user_id != current_user.id:
         # Note: Tenant might not have a property assigned yet if we allow that. 
         # But for security better check ownership. 
         # If unassigned, we might need another check or disallow unassigned creation.
         if tenant.property and tenant.property.user_id != current_user.id:
            flash('Accès non autorisé.', 'error')
            return redirect(url_for('tenant.index'))
            
    return render_template('tenants/show.html', tenant=tenant)

@tenant_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    tenant = Tenant.query.get_or_404(id)
    if tenant.property and tenant.property.user_id != current_user.id:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('tenant.index'))
    
    form = TenantForm(obj=tenant)
    properties = Property.query.filter_by(user_id=current_user.id).all()
    
    if form.validate_on_submit():
        form.populate_obj(tenant)
        
        # Handle property assignment change
        new_property_id = request.form.get('property_id')
        if new_property_id:
            # If changing property
            if not tenant.property_id or str(tenant.property_id) != new_property_id:
                # Set old property to Vacant if exists
                if tenant.property:
                    tenant.property.status = 'Vacant'
                
                # Set new property
                prop = Property.query.get(new_property_id)
                if prop and prop.user_id == current_user.id:
                    tenant.property_id = prop.id
                    prop.status = 'Occupe'
        elif new_property_id == "": # Explicitly set to None/Empty
             if tenant.property:
                tenant.property.status = 'Vacant'
                tenant.property_id = None

        
        db.session.commit()
        flash('Locataire modifié avec succès.', 'success')
        return redirect(url_for('tenant.show', id=tenant.id))
        
    return render_template('tenants/create.html', form=form, properties=properties, title='Modifier le locataire', tenant=tenant)

@tenant_bp.route('/<int:id>/archive', methods=['POST'])
@login_required
def archive(id):
    """Archive (soft delete) a tenant"""
    tenant = Tenant.query.get_or_404(id)
    if tenant.user_id != current_user.id:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('tenant.index'))
    
    # Free up property if assigned
    if tenant.property:
        tenant.property.status = 'Vacant'
        tenant.property_id = None
    
    # Soft delete
    tenant.is_deleted = True
    tenant.deleted_at = datetime.utcnow()
    db.session.commit()
    flash(f'Locataire "{tenant.full_name}" archivé avec succès.', 'success')
    return redirect(url_for('tenant.index'))
