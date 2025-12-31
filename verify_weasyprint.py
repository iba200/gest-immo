from app import create_app, db
from app.models.payment import Payment
from app.utils.pdf import generate_receipt_pdf
import os
import traceback
from weasyprint import HTML

app = create_app()

def test_minimal():
    print("Testing minimal WeasyPrint generation...")
    try:
        pdf_bytes = HTML(string="<h1>Test</h1>").write_pdf()
        print(f"Minimal test success! Size: {len(pdf_bytes)}")
        return True
    except Exception:
        print("Minimal test failed!")
        traceback.print_exc()
        return False

def verify_weasyprint():
    if not test_minimal():
        return
        
    with app.app_context():
        # Get a payment to test with
        payment = Payment.query.first()
        if not payment:
            print("No payments found in database to test with.")
            return
            
        print(f"Testing PDF generation for payment ID: {payment.id}")
        try:
            pdf_bytes = generate_receipt_pdf(payment)
            if pdf_bytes:
                filename = "verify_weasyprint.pdf"
                with open(filename, "wb") as f:
                    f.write(pdf_bytes)
                print(f"Success! PDF generated and saved to {os.path.abspath(filename)}")
                print(f"File size: {len(pdf_bytes)} bytes")
            else:
                print("Failed to generate PDF (returned None).")
        except Exception:
            traceback.print_exc()

if __name__ == "__main__":
    verify_weasyprint()
