from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.property import Property
from app.models.tenant import Tenant
from app.models.payment import Payment
from sqlalchemy import func
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/dashboard')
@login_required
def dashboard():
    # 1. Statistics
    properties = Property.query.filter_by(user_id=current_user.id).all()
    total_properties = len(properties)
    occupied_properties = sum(1 for p in properties if p.status == 'Occupe')
    
    occupancy_rate = 0
    if total_properties > 0:
        occupancy_rate = round((occupied_properties / total_properties) * 100)
        
    total_tenants = Tenant.query.filter_by(user_id=current_user.id).count()
    
    # Revenue for current month
    now = datetime.now()
    current_month_payments = Payment.query.join(Property).filter(
        Property.user_id == current_user.id,
        Payment.period_month == now.month,
        Payment.period_year == now.year
    ).with_entities(func.sum(Payment.amount)).scalar() or 0
    
    # 2. Alerts (Unpaid Rents for current month) - Optimized (Section 8.2)
    # Get all active tenants with their properties linked via joinedload to avoid N+1
    from sqlalchemy.orm import joinedload
    active_tenants = Tenant.query.filter_by(user_id=current_user.id, is_active=True, is_deleted=False).options(joinedload(Tenant.property)).all()
    
    # Get IDs of tenants who HAVE paid this month in one query
    paid_tenant_ids = {p.tenant_id for p in Payment.query.join(Property).filter(
        Property.user_id == current_user.id,
        Payment.period_month == now.month,
        Payment.period_year == now.year
    ).with_entities(Payment.tenant_id).all()}
    
    unpaid_tenants = []
    for tenant in active_tenants:
        if tenant.property and tenant.id not in paid_tenant_ids:
            unpaid_tenants.append({
                'tenant': tenant,
                'amount_due': tenant.property.rent_amount + (tenant.property.charges or 0)
            })
    
    # 3. Revenue Evolution (Last 12 months for Chart.js)
    from datetime import timedelta
    from dateutil.relativedelta import relativedelta
    
    revenue_data = []
    month_labels = []
    
    for i in range(11, -1, -1):  # Last 12 months
        target_date = now - relativedelta(months=i)
        month_revenue = Payment.query.join(Property).filter(
            Property.user_id == current_user.id,
            Payment.period_month == target_date.month,
            Payment.period_year == target_date.year
        ).with_entities(func.sum(Payment.amount)).scalar() or 0
        
        revenue_data.append(int(month_revenue))
        # French month names
        months_fr = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
        month_labels.append(f"{months_fr[target_date.month - 1]} {target_date.year}")
    
    stats = {
        'total_properties': total_properties,
        'occupancy_rate': occupancy_rate,
        'monthly_revenue': current_month_payments,
        'total_tenants': total_tenants,
        'unpaid_count': len(unpaid_tenants),
        'current_month': now.month,
        'revenue_data': revenue_data,
        'month_labels': month_labels
    }
    
    return render_template('dashboard.html', stats=stats, unpaid_tenants=unpaid_tenants, year=now.year)


@main_bp.route('/export/monthly-report')
@login_required
def export_monthly_report():
    """Generate and download a PDF report for the current month"""
    from app.utils.pdf import generate_report_pdf
    from flask import Response
    
    now = datetime.now()
    
    # Get all properties and payments for the month
    properties = Property.query.filter_by(user_id=current_user.id).all()
    payments = Payment.query.join(Property).filter(
        Property.user_id == current_user.id,
        Payment.period_month == now.month,
        Payment.period_year == now.year
    ).order_by(Payment.date.desc()).all()
    
    total_expected = sum(p.rent_amount + (p.charges or 0) for p in properties if p.status == 'Occupe')
    total_received = sum(p.amount for p in payments)
    
    # Unpaid details
    unpaid_total = total_expected - total_received
    
    pdf = generate_report_pdf(
        'reports/monthly_report_pdf.html',
        month=now.month,
        year=now.year,
        payments=payments,
        total_expected=total_expected,
        total_received=total_received,
        unpaid_total=unpaid_total,
        properties_count=len(properties),
        date_generated=now.strftime('%d/%m/%Y %H:%M')
    )
    
    if not pdf:
        return "Erreur lors de la génération du rapport", 500
        
    return Response(
        pdf,
        mimetype="application/pdf",
        headers={"Content-Disposition": f"attachment;filename=Rapport_Mensuel_{now.strftime('%m_%Y')}.pdf"}
    )


@main_bp.route('/help')
@login_required
def help():
    """Render the Help & FAQ page"""
    return render_template('help.html')

