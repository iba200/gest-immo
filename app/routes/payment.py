from flask import Blueprint, render_template, redirect, url_for, flash, request, make_response
from flask_login import login_required, current_user
from app import db
from app.models.payment import Payment
from app.models.tenant import Tenant
from app.models.property import Property
from app.forms.payment import PaymentForm
from app.utils.pdf import generate_receipt_pdf
from datetime import datetime

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/')
@login_required
def index():
    # Base query: only payments for properties owned by current user
    query = Payment.query.join(Property).filter(Property.user_id == current_user.id)
    
    # Get filter parameters
    status = request.args.get('status', '')
    tenant_id = request.args.get('tenant_id', '')
    property_id = request.args.get('property_id', '')
    month = request.args.get('month', '')
    year = request.args.get('year', '')
    
    # Apply filters
    if status:
        query = query.filter(Payment.status == status)
    if tenant_id:
        query = query.filter(Payment.tenant_id == int(tenant_id))
    if property_id:
        query = query.filter(Payment.property_id == int(property_id))
    if month:
        query = query.filter(Payment.period_month == int(month))
    if year:
        query = query.filter(Payment.period_year == int(year))
    
    # Pagination (Section 8.2)
    page = request.args.get('page', 1, type=int)
    per_page = 50
    pagination = query.order_by(Payment.date.desc()).paginate(page=page, per_page=per_page, error_out=False)
    payments = pagination.items
    
    # Get filter options
    tenants = Tenant.query.filter_by(user_id=current_user.id, is_deleted=False).all()
    properties = Property.query.filter_by(user_id=current_user.id, is_deleted=False).all()
    
    return render_template('payments/list.html', 
                         payments=payments,
                         pagination=pagination,
                         tenants=tenants,
                         properties=properties,
                         filters={
                             'status': status,
                             'tenant_id': tenant_id,
                             'property_id': property_id,
                             'month': month,
                             'year': year
                         })

@payment_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    form = PaymentForm()
    
    # Set default values for period if not submitted
    if request.method == 'GET':
        now = datetime.now()
        form.period_month.data = now.month
        form.period_year.data = now.year

    # Populate tenants dropdown with property data
    tenants = Tenant.query.filter_by(user_id=current_user.id, is_deleted=False).all()
    tenant_choices = []
    tenant_data = {}  # For JavaScript access
    
    for t in tenants:
        label = f"{t.full_name} - {t.property.name if t.property else 'Aucun bien'}"
        tenant_choices.append((t.id, label))
        
        # Store property data for JavaScript
        if t.property:
            tenant_data[t.id] = {
                'rent': float(t.property.rent_amount),
                'charges': float(t.property.charges or 0)
            }
    
    form.tenant_id.choices = tenant_choices
    
    # Pre-fill rent and charges if tenant is selected (via URL param)
    tenant_id = request.args.get('tenant_id')
    if tenant_id and request.method == 'GET':
        tenant = Tenant.query.get(tenant_id)
        if tenant and tenant.property and tenant.property.user_id == current_user.id:
            form.tenant_id.data = int(tenant_id)
            form.rent.data = tenant.property.rent_amount
            form.charges.data = tenant.property.charges or 0
            form.amount.data = form.rent.data + form.charges.data
    
    if form.validate_on_submit():
        tenant = Tenant.query.get(form.tenant_id.data)
        if not tenant or not tenant.property:
            flash('Ce locataire n\'a pas de bien assigné.', 'error')
        
        # Verify ownership
        elif tenant.property.user_id != current_user.id:
            flash('Accès non autorisé.', 'error')
            return redirect(url_for('payment.index'))
        
        # Check for duplicate payment (same property + same period)
        else:
            existing_payment = Payment.query.filter_by(
                property_id=tenant.property.id,
                period_month=form.period_month.data,
                period_year=form.period_year.data
            ).first()
            
            if existing_payment:
                flash(f'Un paiement existe déjà pour {tenant.property.name} pour le mois {form.period_month.data}/{form.period_year.data}.', 'error')
            else:
                payment = Payment(
                    receipt_number=Payment.generate_receipt_number(),
                    tenant_id=tenant.id,
                    property_id=tenant.property.id,
                    rent=form.rent.data,
                    charges=form.charges.data or 0,
                    penalties=form.penalties.data or 0,
                    discount=form.discount.data or 0,
                    amount=form.amount.data,
                    date=form.date.data,
                    period_month=form.period_month.data,
                    period_year=form.period_year.data,
                    payment_method=form.payment_method.data,
                    transaction_ref=form.transaction_ref.data,
                    notes=form.notes.data
                )
                
                db.session.add(payment)
                db.session.commit()
                flash(f'Paiement de {form.amount.data} FCFA enregistré avec succès. Quittance N° {payment.receipt_number}', 'success')
                return redirect(url_for('payment.index'))
        
    return render_template('payments/create.html', form=form, title='Nouveau Paiement', tenant_data=tenant_data)

@payment_bp.route('/<int:id>/receipt')
@login_required
def receipt(id):
    payment = Payment.query.get_or_404(id)
    if payment.prop.user_id != current_user.id:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('payment.index'))
        
    pdf = generate_receipt_pdf(payment)
    if pdf:
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename=quittance_{payment.period_year}_{payment.period_month}_{payment.tenant.last_name}.pdf'
        return response
    else:
        flash('Erreur lors de la génération du PDF.', 'error')
        return redirect(url_for('payment.index'))

@payment_bp.route('/<int:id>/email')
@login_required
def email_receipt(id):
    payment = Payment.query.get_or_404(id)
    if payment.prop.user_id != current_user.id:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('payment.index'))
    
    if not payment.tenant.email:
        flash('Le locataire n\'a pas d\'adresse email.', 'error')
        return redirect(url_for('payment.index'))

    from app.utils.pdf import generate_receipt_pdf
    from app.utils.email import send_async_email
    from flask_mail import Message
    from flask import current_app
    
    pdf = generate_receipt_pdf(payment)
    if pdf:
        msg = Message(f"Quittance de loyer - {payment.period_month}/{payment.period_year}",
                      sender=current_app.config['MAIL_DEFAULT_SENDER'],
                      recipients=[payment.tenant.email])
        msg.body = f"Bonjour {payment.tenant.first_name},\n\nVeuillez trouver ci-joint votre quittance de loyer pour la période {payment.period_month}/{payment.period_year}.\n\nCordialement,\n{current_user.first_name} {current_user.last_name}"
        msg.attach(f"quittance_{payment.period_year}_{payment.period_month}.pdf", "application/pdf", pdf)
        
        # Using a thread here manually or just calling standard send_email util if it supported attachments
        # My util created earlier supports html/text but not attachments directly in arguments
        # So I'll use the threaded approach manually here or update util.
        # For simplicity, let's use the util I made? No, it doesn't support attachments.
        # I'll just use the raw Mail object with a thread wrapper if I can import 'mail' 
        # But 'mail' is in app/__init__.py. 
        # Let's just import the send_async_email helper from utils/email.py if I exported it.
        # I did export it in the previous step content.
        
        from app.utils.email import send_async_email
        from threading import Thread
        from flask import current_app
        
        # Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
        # Actually my util `send_async_email` takes (app, msg). Good.
        
        Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
        
        flash('Quittance envoyée par email.', 'success')
    else:
        flash('Erreur lors de la génération du PDF.', 'error')
        
    return redirect(url_for('payment.index'))

@payment_bp.route('/export/csv')
@login_required
def export_csv():
    import csv
    import io
    from flask import Response

    # Get payments
    payments = Payment.query.join(Property).filter(Property.user_id == current_user.id).order_by(Payment.date.desc()).all()

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Date', 'Locataire', 'Bien', 'Montant (FCFA)', 'Période', 'Mode de Paiement', 'Référence', 'Notes'])
    
    # Rows
    for payment in payments:
        writer.writerow([
            payment.date.strftime('%Y-%m-%d'),
            payment.tenant.full_name,
            payment.prop.name,
            payment.amount,
            f"{payment.period_month}/{payment.period_year}",
            payment.payment_method,
            payment.transaction_ref or '',
            payment.notes or ''
        ])
        
    
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename=paiements_export_{datetime.now().strftime('%Y%m%d')}.csv"}
    )

@payment_bp.route('/tenant/<int:tenant_id>')
@login_required
def tenant_history(tenant_id):
    """View payment history for a specific tenant"""
    tenant = Tenant.query.get_or_404(tenant_id)
    
    # Verify ownership
    if tenant.user_id != current_user.id:
        flash('Accès non autorisé.', 'error')
        return redirect(url_for('payment.index'))
    
    # Get all payments for this tenant
    payments = Payment.query.filter_by(tenant_id=tenant_id).order_by(
        Payment.period_year.desc(), 
        Payment.period_month.desc()
    ).all()
    
    # Calculate statistics
    total_paid = sum(p.amount for p in payments)
    total_payments = len(payments)
    
    return render_template('payments/tenant_history.html',
                         tenant=tenant,
                         payments=payments,
                         total_paid=total_paid,
                         total_payments=total_payments)

@payment_bp.route('/monthly-summary')
@login_required
def monthly_summary():
    """Display monthly revenue summary"""
    from sqlalchemy import func, extract
    
    # Get all payments for current user's properties
    payments = Payment.query.join(Property).filter(
        Property.user_id == current_user.id
    ).all()
    
    # Group by month/year
    monthly_data = {}
    for payment in payments:
        key = f"{payment.period_year}-{payment.period_month:02d}"
        if key not in monthly_data:
            monthly_data[key] = {
                'year': payment.period_year,
                'month': payment.period_month,
                'total_amount': 0,
                'total_rent': 0,
                'total_charges': 0,
                'total_penalties': 0,
                'payment_count': 0,
                'late_count': 0
            }
        
        monthly_data[key]['total_amount'] += payment.amount
        monthly_data[key]['total_rent'] += payment.rent
        monthly_data[key]['total_charges'] += payment.charges
        monthly_data[key]['total_penalties'] += payment.penalties
        monthly_data[key]['payment_count'] += 1
        if payment.is_late:
            monthly_data[key]['late_count'] += 1
    
    # Sort by year-month descending
    sorted_data = sorted(monthly_data.values(), 
                        key=lambda x: (x['year'], x['month']), 
                        reverse=True)
    
    # Calculate totals
    total_revenue = sum(d['total_amount'] for d in sorted_data)
    total_payments = sum(d['payment_count'] for d in sorted_data)
    
    return render_template('payments/monthly_summary.html',
                         monthly_data=sorted_data,
                         total_revenue=total_revenue,
                         total_payments=total_payments)

