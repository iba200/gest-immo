from xhtml2pdf import pisa
from flask import render_template
from io import BytesIO

def generate_receipt_pdf(payment):
    """
    Generates a PDF receipt for a given payment.
    """
    try:
        # Render HTML template with payment data
        html = render_template('payments/receipt_pdf.html', payment=payment)
        
        # Create PDF
        result_file = BytesIO()
        pisa_status = pisa.CreatePDF(
            src=html,
            dest=result_file
        )
        
        if pisa_status.err:
            return None
            
        return result_file.getvalue()
        
    except Exception as e:
        print(f"PDF Generation Error: {e}")
        return None

def generate_report_pdf(template_name, **kwargs):
    """
    Generates a PDF report from a template and context.
    """
    try:
        # Render HTML template with context data
        html = render_template(template_name, **kwargs)
        
        # Create PDF
        result_file = BytesIO()
        pisa_status = pisa.CreatePDF(
            src=html,
            dest=result_file
        )
        
        if pisa_status.err:
            return None
            
        return result_file.getvalue()
        
    except Exception as e:
        print(f"Report PDF Generation Error: {e}")
        return None
