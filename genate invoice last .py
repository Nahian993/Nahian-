import os
import datetime
import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas  # type: ignore
from reportlab.lib import colors
from reportlab.lib.units import mm

def generate_invoice_pdf(invoice_data, output_path):
    # Create canvas
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4  # (595x842) points for A4

    # -------------------------------
    # Header (Company Info)
    # -------------------------------
    # Draw a subtle background rectangle for the header area
    c.setFillColorRGB(0.95, 0.95, 0.95)
    c.rect(20, height - 120, width - 40, 90, fill=1, stroke=0)
    
    # Company Logo (if any) - uncomment and adjust path if you have one
    # if invoice_data['company'].get('logo'):
    #     c.drawImage(invoice_data['company']['logo'], 25, height - 110, width=50, height=50, mask='auto')
    
    company = invoice_data['company']
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.HexColor("#2a2a2a"))
    c.drawString(90, height - 50, company['name'])
    
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#555555"))
    company_address = company['address'].split('\n')
    y = height - 65
    for line in company_address:
        c.drawString(90, y, line)
        y -= 12

    # Contact Information on right side of header
    c.setFont("Helvetica", 10)
    c.drawRightString(width - 25, height - 50, f"Phone: {company['phone']}")
    c.drawRightString(width - 25, height - 65, f"Email: {company['email']}")
    c.drawRightString(width - 25, height - 80, f"VAT ID: {company['vat_id']}")
    c.setLineWidth(1)
    c.setStrokeColor(colors.lightgrey)
    c.line(25, height - 125, width - 25, height - 125)

    # -------------------------------
    # Customer Info & Invoice Details
    # -------------------------------
    # Divide the area below the header into two columns.
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor("#2a2a2a"))
    c.drawString(25, height - 145, "BILL TO:")
    customer = invoice_data['customer']
    c.setFont("Helvetica", 11)
    c.drawString(25, height - 160, customer['name'])
    c.drawString(25, height - 175, f"Phone: {customer['phone']}")
    if customer.get("email"):
        c.drawString(25, height - 190, f"Email: {customer['email']}")
    if customer.get("address"):
        c.drawString(25, height - 205, customer['address'])

    # Invoice Details (right aligned)
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(width - 25, height - 145, f"Invoice No: {invoice_data['invoice_number']}")
    c.setFont("Helvetica", 11)
    c.drawRightString(width - 25, height - 160, f"Date: {invoice_data['date']}")
    
    # -------------------------------
    # Items Table with Enhanced Styling
    # -------------------------------
    table_top = height - 240
    headers = ["Description", "Qty", "Unit Price", "Warranty", "Total"]
    n_cols = len(headers)
    table_width = width - 40
    col_width = table_width / n_cols

    # Header background for table
    c.setFillColor(colors.HexColor("#2c3e50"))
    c.rect(20, table_top, table_width, 22, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 10)
    for i, header in enumerate(headers):
        x = 20 + i * col_width + 4
        c.drawString(x, table_top + 6, header)

    # Draw table rows with alternating shading
    row_height = 22
    y = table_top - row_height
    c.setFont("Helvetica", 10)
    for idx, item in enumerate(invoice_data['items']):
        # Alternate row background
        if idx % 2 == 0:
            c.setFillColor(colors.whitesmoke)
            c.rect(20, y, table_width, row_height, fill=1, stroke=0)
        c.setFillColor(colors.black)
        c.drawString(24, y + 6, item['description'])
        c.drawString(20 + col_width + 4, y + 6, str(item['qty']))
        c.drawString(20 + 2 * col_width + 4, y + 6, f"${item['unit_price']:.2f}")
        c.drawString(20 + 3 * col_width + 4, y + 6, item['warranty'])
        c.drawString(20 + 4 * col_width + 4, y + 6, f"${item['total']:.2f}")
        # Draw horizontal line
        c.setLineWidth(0.3)
        c.setStrokeColor(colors.lightgrey)
        c.line(20, y, width - 20, y)
        y -= row_height

    # -------------------------------
    # Totals Section
    # -------------------------------
    total_y = y - 20
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(width - 25, total_y, f"Subtotal: ${invoice_data['subtotal']:.2f}")
    c.drawRightString(width - 25, total_y - 15, f"VAT (15%): ${invoice_data['vat']:.2f}")
    c.drawRightString(width - 25, total_y - 30, f"Grand Total: ${invoice_data['grand_total']:.2f}")

    # -------------------------------
    # Elegant Footer with Terms
    # -------------------------------
    footer_text = [
        "TERMS & CONDITIONS:",
        "1. Warranty valid only with original purchase document.",
        "2. Physical and water damage not covered.",
        "3. Prices in BDT; exchange rate fluctuations may apply.",
        "4. Late payments incur 2% monthly interest.",
        "Authorized Signature: ______________________________"
    ]
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    y_footer = 70
    for line in footer_text:
        c.drawString(25, y_footer, line)
        y_footer -= 10

    # Save the PDF file
    c.save()

def generate_invoice():
    # Retrieve input values from the GUI
    customer_name = entry_name.get()
    customer_phone = entry_phone.get()
    watch_model = entry_model.get()
    quantity = int(entry_quantity.get())
    unit_price = float(entry_price.get())

    # Calculate totals
    subtotal = quantity * unit_price
    vat = round(subtotal * 0.15, 2)  # 15% VAT
    total = subtotal + vat

    # Generate Invoice Number using current datetime (8 to 14 characters)
    invoice_number = f"INV-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')[-8:]}"
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Folder to save the generated invoice PDF
    save_folder = r"C:\Users\paxso\Downloads\invoice"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    filename = f"Invoice_{invoice_number}.pdf"
    pdf_path = os.path.join(save_folder, filename)

    # Prepare invoice data
    invoice_data = {
        "company": {
            "name": "Crown Watch Co.",
            "address": "78/2, Masjid Market,\nPatuatuli Road,\nOpposite Sumna Hospital,\nDhaka 1100",
            "phone": "+880 171 588 1701",
            "email": "humayunkabir@gmail.com",
            "vat_id": "123456789"
        },
        "customer": {
            "name": customer_name,
            "phone": customer_phone,
            "email": "",  # Optional
            "address": ""  # Optional
        },
        "invoice_number": invoice_number,
        "date": current_datetime,
        "items": [
            {"description": watch_model, "qty": quantity, "unit_price": unit_price, "warranty": "2 Years", "total": subtotal}
        ],
        "subtotal": subtotal,
        "vat": vat,
        "grand_total": total
    }

    generate_invoice_pdf(invoice_data, pdf_path)
    messagebox.showinfo("Invoice Generated", f"Invoice saved as: {pdf_path}")

# -------------------------------
# GUI Setup using Tkinter
# -------------------------------
root = tk.Tk()
root.title("Watch Invoice Generator")
root.geometry("400x400")

tk.Label(root, text="Customer Name:").pack(anchor="w", padx=20, pady=2)
entry_name = tk.Entry(root, width=40)
entry_name.pack(padx=20)

tk.Label(root, text="Customer Phone:").pack(anchor="w", padx=20, pady=2)
entry_phone = tk.Entry(root, width=40)
entry_phone.pack(padx=20)

tk.Label(root, text="Watch Model:").pack(anchor="w", padx=20, pady=2)
entry_model = tk.Entry(root, width=40)
entry_model.pack(padx=20)

tk.Label(root, text="Quantity:").pack(anchor="w", padx=20, pady=2)
entry_quantity = tk.Entry(root, width=40)
entry_quantity.pack(padx=20)

tk.Label(root, text="Unit Price ($):").pack(anchor="w", padx=20, pady=2)
entry_price = tk.Entry(root, width=40)
entry_price.pack(padx=20)

tk.Button(root, text="Generate Invoice", command=generate_invoice, bg="green", fg="white").pack(pady=20)

root.mainloop()
