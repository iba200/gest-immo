import traceback
import sys

try:
    from weasyprint import HTML
    print("Import success")
    pdf = HTML(string="<h1>Test</h1>").write_pdf()
    print("Generation success")
except Exception as e:
    with open("weasyprint_error.log", "w") as f:
        f.write(str(e))
        f.write("\n\n" + traceback.format_exc())
    print("Error captured in weasyprint_error.log")
