from weasyprint import HTML
from flask import render_template
import os

def generate_receipt_pdf(payment):
    """
    Generates a PDF receipt for a given payment using WeasyPrint.
    """
    try:
        # Render HTML template with payment data
        html = render_template('payments/receipt_pdf.html', payment=payment)
        
        # Create PDF using WeasyPrint
        # baseURL is important for relative links (images, css)
        pdf_bytes = HTML(string=html).write_pdf()
        
        return pdf_bytes
        
    except Exception as e:
        print(f"WeasyPrint Receipt Generation Error: {e}")
        return None

def generate_report_pdf(template_name, **kwargs):
    """
    Generates a PDF report from a template and context using WeasyPrint.
    """
    try:
        # Render HTML template with context data
        html = render_template(template_name, **kwargs)
        
        # Create PDF using WeasyPrint
        pdf_bytes = HTML(string=html).write_pdf()
        
        return pdf_bytes
        
    except Exception as e:
        print(f"WeasyPrint Report Generation Error: {e}")
        return None
