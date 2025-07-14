# import tkinter as tk
# from tkinter import ttk, messagebox
# import datetime
# from reportlab.lib.utils import ImageReader
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.colors import black, white, HexColor, lightgrey
# import sqlite3
# import os

# # ---------- DATABASE SETUP ----------
# def init_db():
#     conn = sqlite3.connect("invoices.db")
#     c = conn.cursor()
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS invoices (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             customer_name TEXT,
#             email TEXT,
#             phone TEXT,
#             invoice_number TEXT UNIQUE,
#             transaction_id TEXT,
#             currency TEXT,
#             gateway TEXT,
#             total_amount TEXT,
#             invoice_date TEXT
#         )
#     ''')
#     conn.commit()
#     conn.close()

# def save_invoice_to_db(data):
#     try:
#         conn = sqlite3.connect("invoices.db")
#         c = conn.cursor()
#         c.execute('''
#             INSERT INTO invoices (
#                 customer_name, email, phone,
#                 invoice_number, transaction_id,
#                 currency, gateway, total_amount, invoice_date
#             ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#         ''', (
#             data['invoice_details']['invoice_to'],
#             data['invoice_details']['email'],
#             data['invoice_details']['phone'],
#             data['invoice_details']['invoice_number'],
#             data['invoice_details']['transaction_id'],
#             data['invoice_details']['currency'],
#             data['payment_method']['gateway'],
#             data['summary_of_charges']['total'],
#             data['invoice_details']['invoice_date']
#         ))
#         conn.commit()
#         conn.close()
#     except sqlite3.IntegrityError:
#         messagebox.showerror("Database Error", "Invoice number already exists!")

# # ---------- PDF GENERATOR ----------
# def generate_invoice_pdf(data, filename="invoice.pdf"):
#     from reportlab.lib.utils import ImageReader
#     from reportlab.pdfgen import canvas
#     from reportlab.lib.pagesizes import A4
#     from reportlab.lib.colors import black, white, HexColor, lightgrey
#     import os

#     PAGE_WIDTH, _ = A4
#     PAGE_HEIGHT = 700
#     MARGIN = 30
#     CONTENT_WIDTH = PAGE_WIDTH - 2 * MARGIN

#     c = canvas.Canvas(filename, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
#     c.setTitle(f"Invoice {data['invoice_details']['invoice_number']}")

#     # Colors
#     PRIMARY_COLOR = HexColor("#2176C1")
#     SECONDARY_COLOR = HexColor("#E0E0E0")
#     TEXT_COLOR = black
#     LIGHT_SKY_BLUE = HexColor("#87CEFA")
#     GREY_COLOR = HexColor("#808080")

#     # Main Border
#     c.setStrokeColor(SECONDARY_COLOR)
#     c.setLineWidth(1)
#     c.rect(MARGIN, MARGIN, CONTENT_WIDTH, PAGE_HEIGHT - 2 * MARGIN, stroke=1, fill=0)

#     # Header
#     header_y = PAGE_HEIGHT - MARGIN - 70
#     logo_path = "asset/logo.png"
#     if os.path.exists(logo_path):
#         logo = ImageReader(logo_path)
#         c.setFillColor(white)
#         c.circle(MARGIN + 55, PAGE_HEIGHT - MARGIN - 55, 45, fill=1, stroke=0)
#         c.drawImage(logo, MARGIN + 10, PAGE_HEIGHT - MARGIN - 100, width=90, height=90, mask='auto')

#     # Title
#     c.setFont("Helvetica-Bold", 20)
#     c.setFillColor(PRIMARY_COLOR)
#     title = "PAYMENT INVOICE RECEIPT"
#     title_width = c.stringWidth(title, "Helvetica-Bold", 20)
#     c.drawString((PAGE_WIDTH - title_width)/2 + 114, PAGE_HEIGHT - MARGIN - 50, title)

#     # TAN / GST / Website
#     c.setFont("Helvetica", 10)
#     c.setFillColor(TEXT_COLOR)
#     c.drawString(MARGIN + 20, PAGE_HEIGHT - MARGIN - 95, f"TAN : {data['header']['tan']}    |    GST : {data['header']['gst']}")
#     website_text = data['header']['website']
#     c.drawRightString(PAGE_WIDTH - MARGIN - 20, PAGE_HEIGHT - MARGIN - 95, website_text)

#     # Invoice Details (Left + Right)
#     details_y = PAGE_HEIGHT - MARGIN - 130
#     c.setFont("Helvetica-Bold", 11)
#     c.drawString(MARGIN + 20, details_y, "Invoice to:")
#     c.setFont("Helvetica", 10)
#     for i, line in enumerate([
#         data['invoice_details']['invoice_to'],
#         data['invoice_details']['email'],
#         data['invoice_details']['phone']
#     ]):
#         c.drawString(MARGIN + 20, details_y - 15 * (i + 1), line)

#     meta_x = MARGIN + 340
#     label_gap = 100
#     for i, (label, value) in enumerate([
#         ("Invoice Number", data['invoice_details']['invoice_number']),
#         ("Invoice Date", data['invoice_details']['invoice_date']),
#         ("Transaction Id", data['invoice_details']['transaction_id']),
#         ("Currency", data['invoice_details']['currency'])
#     ]):
#         c.setFont("Helvetica-Bold", 10)
#         c.drawString(meta_x, details_y - 15 * i, f"{label}:")
#         c.setFont("Helvetica", 10)
#         c.drawString(meta_x + label_gap, details_y - 15 * i, value)

#     # --- Table Section ---
#     table_start_y = details_y - 90
#     row_height = 20

#     columns = [
#         {"title": "NO", "width": 40},
#         {"title": "COURSE CODE - DESCRIPTION", "width": 230},
#         {"title": "QTY", "width": 50},
#         {"title": "PRICE", "width": 90},
#         {"title": "TOTAL", "width": 90}
#     ]

#     # Column X positions
#     col_x_positions = [MARGIN + 15]
#     for col in columns:
#         col_x_positions.append(col_x_positions[-1] + col["width"])

#     # Header background
#     c.setFillColor(PRIMARY_COLOR)
#     c.rect(col_x_positions[0], table_start_y, col_x_positions[-1] - col_x_positions[0], row_height, fill=1)

#     # Header text
#     c.setFillColor(white)
#     c.setFont("Helvetica-Bold", 10)
#     for i, col in enumerate(columns):
#         c.drawString(col_x_positions[i] + 5, table_start_y + 5, col["title"])

#     # Table rows
#     c.setFont("Helvetica", 10)
#     c.setFillColor(TEXT_COLOR)
#     for row_num, item in enumerate(data['course_details'], 1):
#         row_y = table_start_y - row_num * row_height
#         values = [
#             str(item["no"]),
#             item["course_code_description"],
#             str(item["qty"]),
#             item["price"],
#             item["total"]
#         ]
#         for i, val in enumerate(values):
#             c.drawString(col_x_positions[i] + 5, row_y + 5, val)

#     # Vertical lines
#     c.setStrokeColor(LIGHT_SKY_BLUE)
#     c.setLineWidth(0.8)
#     for x in col_x_positions:
#         c.line(x, table_start_y, x, table_start_y - row_height * (len(data['course_details']) + 1))

#     # Horizontal lines
#     for i in range(len(data['course_details']) + 2):
#         y = table_start_y - i * row_height
#         c.line(col_x_positions[0], y, col_x_positions[-1], y)

#     # Payment Section
#     payment_y = table_start_y - row_height * (len(data['course_details']) + 2) - 20
#     c.setFillColor(PRIMARY_COLOR)
#     c.rect(MARGIN + 15, payment_y, 160, 18, fill=1)
#     c.setFillColor(white)
#     c.setFont("Helvetica-Bold", 10)
#     c.drawString(MARGIN + 25, payment_y + 5, "PAYMENT METHOD :")
#     c.setFillColor(TEXT_COLOR)
#     c.setFont("Helvetica", 10)
#     c.drawString(MARGIN + 25, payment_y - 15, f"Payment Gateway : {data['payment_method']['gateway']}")
#     c.drawString(MARGIN + 25, payment_y - 30, f"Payment Status : {data['payment_method']['status']}")

#     # Summary Section
#     summary_y = payment_y + 25
#     summary_x_label = PAGE_WIDTH - MARGIN - 130
#     summary_x_value = PAGE_WIDTH - MARGIN - 15
#     for i, (label, value) in enumerate([
#         ("Sub Total", data['summary_of_charges']['sub_total']),
#         ("GST-18%", data['summary_of_charges']['gst_18_percent']),
#         ("Total", data['summary_of_charges']['total'])
#     ]):
#         is_total = label == "Total"
#         c.setFont("Helvetica-Bold" if is_total else "Helvetica", 10)
#         c.drawString(summary_x_label, summary_y - 15 * (i + 1), f"{label} :")
#         c.drawRightString(summary_x_value, summary_y - 15 * (i + 1), value)

#     # Paid Stamp (optional)
#     paid_stamp_path = "asset/paid.png"
#     if os.path.exists(paid_stamp_path):
#         stamp = ImageReader(paid_stamp_path)
#         c.drawImage(stamp, MARGIN + 30, payment_y - 130, width=80, height=80, mask='auto')

#     # Footer
#     c.setFont("Helvetica-Bold", 11)
#     c.drawString(PAGE_WIDTH - MARGIN - 180, payment_y - 90, "Thank you for enrolling with us!")
#     c.setStrokeColor(SECONDARY_COLOR)
#     c.line(MARGIN + 20, 120, PAGE_WIDTH - MARGIN - 20, 120)
#     c.setFont("Helvetica-Oblique", 10)
#     c.drawCentredString(PAGE_WIDTH / 2, 130, "This document is electronically generated and valid without a signature.")
#     c.setFont("Helvetica", 10)
#     c.drawCentredString(PAGE_WIDTH / 2, 90, data['footer_contact']['address'])
#     c.drawCentredString(PAGE_WIDTH / 2, 70, f"📞 {data['footer_contact']['phone']}    ✉ {data['footer_contact']['email']}")

#     c.save()

# # ---------- MAIN WINDOW ----------
# def show_main_window():
#     root = tk.Tk()
#     root.title("Admin Portal + Invoice Generator")
#     root.geometry("800x700")

#     course_map = {
#         "DevOps with AI - Course": 30000,
#         "DevOps with AI Master's Program": 35000,
#         "MLOps Master's Program": 40000
#     }

#     selected_courses = []  # Will store tuples of (course_name, course_code)

#     # Variables
#     name_var = tk.StringVar()
#     email_var = tk.StringVar()
#     phone_var = tk.StringVar()
#     invoice_no_var = tk.StringVar()
#     transaction_id_var = tk.StringVar()
#     currency_var = tk.StringVar(value="INR")
#     gateway_var = tk.StringVar(value="PayU Money")
#     course_var = tk.StringVar()
#     course_code_var = tk.StringVar()  # New variable for course codes
#     selected_text = tk.StringVar(value="No course selected")

#     currencies = ["INR", "USD", "EUR", "GBP", "AED", "CAD", "SGD"]
#     gateways = ["PayU Money", "Razorpay", "Stripe"]

#     # ------- Course Selection Functions -------
#     def add_selected_course(event=None):
#         course = course_var.get()
#         if course and course not in [c[0] for c in selected_courses]:
#             # Create popup window for course code entry
#             code_popup = tk.Toplevel(root)
#             code_popup.title("Enter Course Code")
#             code_popup.geometry("300x150")
            
#             tk.Label(code_popup, text=f"Enter code for {course}:").pack(pady=10)
#             code_entry = tk.Entry(code_popup, textvariable=course_code_var)
#             code_entry.pack(pady=5)
            
#             def confirm_code():
#                 if course_code_var.get():
#                     selected_courses.append((course, course_code_var.get()))
#                     update_selected_display()
#                     code_popup.destroy()
#                     course_code_var.set("")  # Clear for next entry
            
#             tk.Button(code_popup, text="Confirm", command=confirm_code).pack(pady=10)
#             code_popup.grab_set()  # Make popup modal

#     def update_selected_display():
#         display_text = ""
#         for course, code in selected_courses:
#             display_text += f"{code} - {course}\n"
#         selected_text.set(display_text if selected_courses else "No course selected")

#     def remove_selected_course():
#         if selected_courses:
#             selected_courses.pop()
#             update_selected_display()

#     # ------- Main UI -------
#     frame = tk.Frame(root)
#     frame.pack(pady=20)

#     # Customer Information
#     for i, (label, var) in enumerate([
#         ("Customer Name", name_var), ("Email", email_var), ("Phone", phone_var),
#         ("Invoice Number", invoice_no_var), ("Transaction ID", transaction_id_var)
#     ]):
#         tk.Label(frame, text=label + ":").grid(row=i, column=0, sticky="e", padx=5, pady=5)
#         tk.Entry(frame, textvariable=var, width=30).grid(row=i, column=1, padx=5, pady=5)

#     # Course Selection
#     tk.Label(frame, text="Select Course:").grid(row=6, column=0, sticky="e", padx=5)
#     course_dropdown = ttk.Combobox(frame, textvariable=course_var, 
#                                  values=list(course_map.keys()), state="readonly", width=28)
#     course_dropdown.grid(row=6, column=1, sticky="w")
#     course_dropdown.bind("<<ComboboxSelected>>", add_selected_course)

#     # Selected Courses Display
#     tk.Label(frame, text="Selected Courses:").grid(row=7, column=0, sticky="ne", padx=5)
#     tk.Label(frame, textvariable=selected_text, wraplength=350, justify="left", 
#             anchor="w").grid(row=7, column=1, sticky="w", padx=5)

#     # Remove Course Button
#     tk.Button(frame, text="Remove Last Course", command=remove_selected_course).grid(row=8, column=1, sticky="w", pady=5)

#     # Payment Options
#     ttk.Combobox(frame, textvariable=currency_var, values=currencies, 
#                 state="readonly", width=28).grid(row=9, column=1, pady=5)
#     ttk.Combobox(frame, textvariable=gateway_var, values=gateways, 
#                 state="readonly", width=28).grid(row=10, column=1, pady=5)
#     tk.Label(frame, text="Currency:").grid(row=9, column=0, sticky="e", padx=5)
#     tk.Label(frame, text="Payment Gateway:").grid(row=10, column=0, sticky="e", padx=5)

#     # ------- Invoice Generation -------
#     def generate_invoice():
#         if not selected_courses:
#             messagebox.showerror("Error", "Select at least one course.")
#             return

#         total = 0
#         course_details = []
#         for i, (course, code) in enumerate(selected_courses, 1):
#             price = course_map[course]
#             course_details.append({
#                 "no": i,
#                 "course_code_description": f"{code} - {course}",
#                 "qty": 1,
#                 "price": f"{currency_var.get()} {price:,.2f}",
#                 "total": f"{currency_var.get()} {price:,.2f}"
#             })
#             total += price

#         data = {
#             "header": {
#                 "tan": "PTNK04889D", 
#                 "gst": "10BQSPS8538Q1ZS", 
#                 "website": "SKILLFYME.COM"
#             },
#             "invoice_details": {
#                 "invoice_to": name_var.get(), 
#                 "email": email_var.get(), 
#                 "phone": phone_var.get(),
#                 "invoice_number": invoice_no_var.get(),
#                 "invoice_date": datetime.datetime.now().strftime("%d-%b-%Y"),
#                 "transaction_id": transaction_id_var.get(), 
#                 "currency": currency_var.get()
#             },
#             "course_details": course_details,
#             "payment_method": {
#                 "gateway": gateway_var.get(), 
#                 "status": "Paid"
#             },
#             "summary_of_charges": {
#                 "sub_total": f"{currency_var.get()} {round(total / 1.18, 2):,.2f}",
#                 "gst_18_percent": f"{currency_var.get()} {round(total - total / 1.18, 2):,.2f}",
#                 "total": f"{currency_var.get()} {total:,.2f}"
#             },
#             "footer_contact": {
#                 "address": "Skillfyme, 5th Floor, Olsen Spaces, Site No. 1165, 5th Main, Sector 7 HSR Layout, Bengaluru - 560102, Karnataka, India",
#                 "phone": "91484639985", 
#                 "email": "support@skillfyme.in"
#             }
#         }

#         filename = f"Invoice_{invoice_no_var.get()}.pdf"
#         generate_invoice_pdf(data, filename)
#         save_invoice_to_db(data)
#         messagebox.showinfo("Success", f"Invoice generated and saved: {filename}")

#     # Generate Invoice Button
#     tk.Button(root, text="Generate Invoice PDF", command=generate_invoice, 
#              bg="green", fg="white", width=30).pack(pady=20)

#     root.mainloop()

# # ---------- LOGIN ----------
# def show_login():
#     login = tk.Tk()
#     login.title("Admin Login")
#     login.geometry("300x200")

#     user_var = tk.StringVar()
#     pass_var = tk.StringVar()

#     def login_action():
#         if user_var.get() == "admin" and pass_var.get() == "admin123":
#             login.destroy()
#             show_main_window()
#         else:
#             messagebox.showerror("Login Failed", "Invalid credentials")

#     tk.Label(login, text="Username:").pack(pady=5)
#     tk.Entry(login, textvariable=user_var).pack()
#     tk.Label(login, text="Password:").pack(pady=5)
#     tk.Entry(login, textvariable=pass_var, show="*").pack()
#     tk.Button(login, text="Login", command=login_action, bg="blue", fg="white").pack(pady=20)
#     login.mainloop()

# # ---------- MAIN ----------
# if __name__ == "__main__":
#     init_db()
#     show_login()











import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black, white, HexColor, lightgrey
import sqlite3
import os
from pathlib import Path

# ---------- DATABASE SETUP ----------
def init_db():
    conn = sqlite3.connect("invoices.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            email TEXT,
            phone TEXT,
            invoice_number TEXT UNIQUE,
            transaction_id TEXT UNIQUE,
            currency TEXT,
            gateway TEXT,
            total_amount TEXT,
            invoice_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_invoice_to_db(data):
    try:
        conn = sqlite3.connect("invoices.db")
        c = conn.cursor()
        c.execute('''
            INSERT INTO invoices (
                customer_name, email, phone,
                invoice_number, transaction_id,
                currency, gateway, total_amount, invoice_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['invoice_details']['invoice_to'],
            data['invoice_details']['email'],
            data['invoice_details']['phone'],
            data['invoice_details']['invoice_number'],
            data['invoice_details']['transaction_id'],
            data['invoice_details']['currency'],
            data['payment_method']['gateway'],
            data['summary_of_charges']['total'],
            data['invoice_details']['invoice_date']
        ))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError as e:
        if "invoice_number" in str(e):
            messagebox.showerror("Database Error", "Invoice number already exists!")
        elif "transaction_id" in str(e):
            messagebox.showerror("Database Error", "Transaction ID already exists!")
        return False

def check_existing_transaction_id(transaction_id):
    conn = sqlite3.connect("invoices.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM invoices WHERE transaction_id = ?", (transaction_id,))
    count = c.fetchone()[0]
    conn.close()
    return count > 0

# ---------- PDF GENERATOR ----------
def generate_invoice_pdf(data, filename="invoice.pdf"):
    PAGE_WIDTH, _ = A4
    PAGE_HEIGHT = 700
    MARGIN = 30
    CONTENT_WIDTH = PAGE_WIDTH - 2 * MARGIN

    c = canvas.Canvas(filename, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    c.setTitle(f"Invoice {data['invoice_details']['invoice_number']}")

    PRIMARY_COLOR = HexColor("#2176C1")
    SECONDARY_COLOR = HexColor("#E0E0E0")
    TEXT_COLOR = black
    LIGHT_SKY_BLUE = HexColor("#87CEFA")
    GREY_COLOR = HexColor("#808080")

    c.setStrokeColor(SECONDARY_COLOR)
    c.setLineWidth(1)
    c.rect(MARGIN, MARGIN, CONTENT_WIDTH, PAGE_HEIGHT - 2 * MARGIN, stroke=1, fill=0)

    header_y = PAGE_HEIGHT - MARGIN - 70
    logo_path = "asset/logo.png"
    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        c.setFillColor(white)
        c.circle(MARGIN + 55, PAGE_HEIGHT - MARGIN - 55, 45, fill=1, stroke=0)
        c.drawImage(logo, MARGIN + 10, PAGE_HEIGHT - MARGIN - 100, width=90, height=90, mask='auto')

    c.setFont("Helvetica-Bold", 20)
    c.setFillColor("#2176C1")
    title = "PAYMENT INVOICE RECEIPT"
    title_width = c.stringWidth(title, "Helvetica-Bold", 20)
    c.drawString((PAGE_WIDTH - title_width)/2 + 114, PAGE_HEIGHT - MARGIN - 45, title)
    
    # Calculate positions
    header_y = PAGE_HEIGHT - MARGIN - 80
    website = data['header']['website']

    # Get text dimensions
    c.setFont("Helvetica-Bold", 12)
    website_width = c.stringWidth(website, "Helvetica-Bold", 12)
    c.setFont("Helvetica", 10)
    tan_text = f"TAN: {data['header']['tan']} | GST: {data['header']['gst']}"
    tan_width = c.stringWidth(tan_text, "Helvetica", 10)

    # Calculate line positions
    line_start = MARGIN + 20  # Aligns with T in TAN below
    line_end = PAGE_WIDTH - MARGIN - 20 - website_width - 5  # Stops 5px before S

    # Draw horizontal line in grey
    c.setStrokeColor(lightgrey)
    c.setLineWidth(1)
    c.line(line_start, header_y, line_end, header_y)

    # Draw website text right-aligned in grey
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(black)
    c.drawRightString(PAGE_WIDTH - MARGIN - 20, header_y - 5, website)

    # Draw TAN/GST info aligned with line start (black)
    c.setFont("Helvetica", 10)
    c.setFillColor(black)
    c.drawString(line_start, header_y - 25, tan_text)

    # Adjust content position below
    details_y = header_y - 50  
    details_y = PAGE_HEIGHT - MARGIN - 130
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN + 20, details_y, "Invoice to:")
    c.setFont("Helvetica", 10)
    for i, line in enumerate([
        data['invoice_details']['invoice_to'],
        data['invoice_details']['email'],
        data['invoice_details']['phone']
    ]):
        c.drawString(MARGIN + 20, details_y - 15 * (i + 1), line)

    meta_x = MARGIN + 340
    label_gap = 100
    for i, (label, value) in enumerate([
        ("Invoice Number", data['invoice_details']['invoice_number']),
        ("Invoice Date", data['invoice_details']['invoice_date']),
        ("Transaction Id", data['invoice_details']['transaction_id']),
        ("Currency", data['invoice_details']['currency'])
    ]):
        c.setFont("Helvetica-Bold", 10)
        c.drawString(meta_x, details_y - 15 * i, f"{label}:")
        c.setFont("Helvetica", 10)
        c.drawString(meta_x + label_gap, details_y - 15 * i, value)

    table_start_y = details_y - 90
    row_height = 20

    columns = [
        {"title": "NO", "width": 40},
        {"title": "COURSE CODE - DESCRIPTION", "width": 230},
        {"title": "QTY", "width": 50},
        {"title": "PRICE", "width": 90},
        {"title": "TOTAL", "width": 90}
    ]

    col_x_positions = [MARGIN + 15]
    for col in columns:
        col_x_positions.append(col_x_positions[-1] + col["width"])

    if data['course_details']:
        c.setFillColor(PRIMARY_COLOR)
        c.rect(col_x_positions[0], table_start_y, col_x_positions[-1] - col_x_positions[0], row_height, fill=1)

        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 10)
        for i, col in enumerate(columns):
            c.drawString(col_x_positions[i] + 5, table_start_y + 5, col["title"])

        c.setFont("Helvetica", 10)
        c.setFillColor(TEXT_COLOR)
        for row_num, item in enumerate(data['course_details'], 1):
            row_y = table_start_y - row_num * row_height
            values = [
                str(item["no"]),
                item["course_code_description"],
                str(item["qty"]),
                item["price"],
                item["total"]
            ]
            for i, val in enumerate(values):
                c.drawString(col_x_positions[i] + 5, row_y + 5, val)

        c.setStrokeColor(LIGHT_SKY_BLUE)
        c.setLineWidth(0.8)
        for x in col_x_positions:
            c.line(x, table_start_y, x, table_start_y - row_height * len(data['course_details']))

        for i in range(len(data['course_details']) + 1):
            y = table_start_y - i * row_height
            c.line(col_x_positions[0], y, col_x_positions[-1], y)

        payment_y = table_start_y - row_height * (len(data['course_details']) + 1) - 20
    else:
        payment_y = table_start_y - 20

    c.setFillColor(PRIMARY_COLOR)
    c.rect(MARGIN + 15, payment_y, 160, 18, fill=1)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN + 25, payment_y + 5, "PAYMENT METHOD :")
    c.setFillColor(TEXT_COLOR)
    c.setFont("Helvetica", 10)
    c.drawString(MARGIN + 25, payment_y - 15, f"Payment Gateway : {data['payment_method']['gateway']}")
    c.drawString(MARGIN + 25, payment_y - 30, f"Payment Status : {data['payment_method']['status']}")

    summary_y = payment_y + 25
    summary_x_label = PAGE_WIDTH - MARGIN - 120
    summary_x_value = PAGE_WIDTH - MARGIN - 15
    line_spacing = 20
    
    for i, (label, value) in enumerate([
        ("Sub Total", data['summary_of_charges']['sub_total']),
        ("GST-18%", data['summary_of_charges']['gst_18_percent']),
        ("Total", data['summary_of_charges']['total'])
    ]):
        is_total = label == "Total"
        c.setFont("Helvetica-Bold" if is_total else "Helvetica", 12 if is_total else 10)
        
        if is_total:
            summary_y -= 10
            
        c.drawRightString(summary_x_label, summary_y - line_spacing * (i + 1), f"{label}:")
        c.drawRightString(summary_x_value, summary_y - line_spacing * (i + 1), value)
        
        if label == "GST-18%":
            c.setStrokeColor(SECONDARY_COLOR)
            c.line(summary_x_label - 10, summary_y - line_spacing * (i + 1) - 8, 
                  summary_x_value, summary_y - line_spacing * (i + 1) - 8)

    paid_stamp_path = "asset/paid.png"
    if os.path.exists(paid_stamp_path):
        stamp = ImageReader(paid_stamp_path)
        c.drawImage(stamp, MARGIN + 30, payment_y - 130, width=80, height=80, mask='auto')

    c.setFont("Helvetica-Bold", 11)
    c.drawString(PAGE_WIDTH - MARGIN - 180, payment_y - 90, "Thank you for enrolling with us!")
    c.setStrokeColor(SECONDARY_COLOR)
    c.line(MARGIN + 20, 120, PAGE_WIDTH - MARGIN - 20, 120)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(PAGE_WIDTH / 2, 130, "This document is electronically generated and valid without a signature.")
    c.setFont("Helvetica", 9.5)
    c.drawCentredString(PAGE_WIDTH / 2, 90, data['footer_contact']['address'])
    c.drawCentredString(PAGE_WIDTH / 2, 70, f"📞 {data['footer_contact']['phone']}    ✉ {data['footer_contact']['email']}")

    c.save()

# ---------- MAIN WINDOW ----------
def show_main_window():
    root = tk.Tk()
    root.title("Admin Portal + Invoice Generator")
    root.geometry("800x700")

    available_courses = [
        "DevOps with AI - Course",
        "DevOps with AI Master's Program",
        "MLOps Master's Program"
    ]

    selected_courses = []

    # Variables
    name_var = tk.StringVar()
    email_var = tk.StringVar()
    phone_var = tk.StringVar()
    invoice_no_var = tk.StringVar()
    transaction_id_var = tk.StringVar()
    currency_var = tk.StringVar(value="INR")
    gateway_var = tk.StringVar(value="PayU Money")
    course_var = tk.StringVar()
    course_code_var = tk.StringVar()
    course_price_var = tk.StringVar()
    selected_text = tk.StringVar(value="No course selected")

    currencies = ["INR", "USD", "EUR", "GBP", "AED", "CAD", "SGD"]
    gateways = ["PayU Money", "Razorpay", "Stripe"]

    def add_selected_course(event=None):
        course = course_var.get()
        if course and course not in [c[0] for c in selected_courses]:
            code_popup = tk.Toplevel(root)
            code_popup.title("Enter Course Details")
            code_popup.geometry("300x200")
            
            tk.Label(code_popup, text=f"Details for {course}:").pack(pady=5)
            
            tk.Label(code_popup, text="Course Code:").pack()
            code_entry = tk.Entry(code_popup, textvariable=course_code_var)
            code_entry.pack()
            
            tk.Label(code_popup, text="Price:").pack()
            price_entry = tk.Entry(code_popup, textvariable=course_price_var)
            price_entry.pack()
            
            def confirm_code():
                if course_code_var.get() and course_price_var.get():
                    try:
                        price = float(course_price_var.get())
                        selected_courses.append((course, course_code_var.get(), price))
                        update_selected_display()
                        code_popup.destroy()
                        course_code_var.set("")
                        course_price_var.set("")
                    except ValueError:
                        messagebox.showerror("Error", "Please enter a valid price number")
            
            tk.Button(code_popup, text="Confirm", command=confirm_code).pack(pady=10)
            code_popup.grab_set()

    def update_selected_display():
        display_text = ""
        for course, code, price in selected_courses:
            display_text += f"{code} - {course} ({currency_var.get()} {price:.2f})\n"
        selected_text.set(display_text if selected_courses else "No course selected")

    def remove_selected_course():
        if selected_courses:
            selected_courses.pop()
            update_selected_display()

    frame = tk.Frame(root)
    frame.pack(pady=20)

    for i, (label, var) in enumerate([
        ("Customer Name", name_var), ("Email", email_var), ("Phone", phone_var),
        ("Invoice Number", invoice_no_var), ("Transaction ID", transaction_id_var)
    ]):
        tk.Label(frame, text=label + ":").grid(row=i, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(frame, textvariable=var, width=30).grid(row=i, column=1, padx=5, pady=5)

    tk.Label(frame, text="Select Course:").grid(row=6, column=0, sticky="e", padx=5)
    course_dropdown = ttk.Combobox(frame, textvariable=course_var, 
                                 values=available_courses, state="readonly", width=28)
    course_dropdown.grid(row=6, column=1, sticky="w")
    course_dropdown.bind("<<ComboboxSelected>>", add_selected_course)

    tk.Label(frame, text="Selected Courses:").grid(row=7, column=0, sticky="ne", padx=5)
    tk.Label(frame, textvariable=selected_text, wraplength=350, justify="left", 
            anchor="w").grid(row=7, column=1, sticky="w", padx=5)

    tk.Button(frame, text="Remove Last Course", command=remove_selected_course).grid(row=8, column=1, sticky="w", pady=5)

    ttk.Combobox(frame, textvariable=currency_var, values=currencies, 
                state="readonly", width=28).grid(row=9, column=1, pady=5)
    ttk.Combobox(frame, textvariable=gateway_var, values=gateways, 
                state="readonly", width=28).grid(row=10, column=1, pady=5)
    tk.Label(frame, text="Currency:").grid(row=9, column=0, sticky="e", padx=5)
    tk.Label(frame, text="Payment Gateway:").grid(row=10, column=0, sticky="e", padx=5)

    def generate_invoice():
        if not selected_courses:
            messagebox.showerror("Error", "Select at least one course.")
            return

        # Check for duplicate transaction ID
        transaction_id = transaction_id_var.get()
        if check_existing_transaction_id(transaction_id):
            messagebox.showerror("Error", "This Transaction ID has already been used. Please use a different one.")
            return

        # Check for empty fields
        if not all([name_var.get(), email_var.get(), phone_var.get(), invoice_no_var.get(), transaction_id_var.get()]):
            messagebox.showerror("Error", "Please fill all required fields.")
            return

        total = 0
        course_details = []
        for i, (course, code, price) in enumerate(selected_courses, 1):
            course_details.append({
                "no": i,
                "course_code_description": f"{code} - {course}",
                "qty": 1,
                "price": f"{currency_var.get()} {price:,.2f}",
                "total": f"{currency_var.get()} {price:,.2f}"
            })
            total += price

        is_inr = currency_var.get() == "INR"
        
        if is_inr:
            sub_total = round(total / 1.18, 2)
            gst_amount = round(total - sub_total, 2)
            summary_charges = {
                "sub_total": f"{currency_var.get()} {sub_total:,.2f}",
                "gst_18_percent": f"{currency_var.get()} {gst_amount:,.2f}",
                "total": f"{currency_var.get()} {total:,.2f}"
            }
        else:
            summary_charges = {
                "sub_total": f"{currency_var.get()} {total:,.2f}",
                "gst_18_percent": f"{currency_var.get()} 0.00",
                "total": f"{currency_var.get()} {total:,.2f}"
            }

        data = {
            "header": {
                "tan": "PTNK04889D", 
                "gst": "10BQSPS8538Q1ZS", 
                "website": "SKILLFYME.COM"
            },
            "invoice_details": {
                "invoice_to": name_var.get(), 
                "email": email_var.get(), 
                "phone": phone_var.get(),
                "invoice_number": invoice_no_var.get(),
                "invoice_date": datetime.datetime.now().strftime("%d-%b-%Y"),
                "transaction_id": transaction_id_var.get(), 
                "currency": currency_var.get()
            },
            "course_details": course_details,
            "payment_method": {
                "gateway": gateway_var.get(), 
                "status": "Paid"
            },
            "summary_of_charges": summary_charges,
            "footer_contact": {
                "address": "Skillfyme, 5th Floor, Olsen Spaces, Site No. 1165, 5th Main, Sector 7 HSR Layout, Bengaluru - 560102, Karnataka, India",
                "phone": "91484639985", 
                "email": "support@skillfyme.in"
            }
        }

        base_filename = f"Invoice_{invoice_no_var.get()}"
        filename = f"{base_filename}.pdf"
        counter = 1
        
        # Find a non-existing filename
        while Path(filename).exists():
            filename = f"{base_filename}_{counter}.pdf"
            counter += 1
        
        try:
            generate_invoice_pdf(data, filename)
            if save_invoice_to_db(data):
                messagebox.showinfo("Success", f"Invoice generated and saved: {filename}")
                # Clear form after successful generation
                name_var.set("")
                email_var.set("")
                phone_var.set("")
                invoice_no_var.set("")
                transaction_id_var.set("")
                selected_courses.clear()
                update_selected_display()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate invoice: {str(e)}")

    tk.Button(root, text="Generate Invoice PDF", command=generate_invoice, 
             bg="green", fg="white", width=30).pack(pady=20)

    root.mainloop()

# ---------- LOGIN ----------
def show_login():
    login = tk.Tk()
    login.title("Admin Login")
    login.geometry("300x200")

    user_var = tk.StringVar()
    pass_var = tk.StringVar()

    def login_action():
        if user_var.get() == "admin" and pass_var.get() == "admin123":
            login.destroy()
            show_main_window()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    tk.Label(login, text="Username:").pack(pady=5)
    tk.Entry(login, textvariable=user_var).pack()
    tk.Label(login, text="Password:").pack(pady=5)
    tk.Entry(login, textvariable=pass_var, show="*").pack()
    tk.Button(login, text="Login", command=login_action, bg="blue", fg="white").pack(pady=20)
    login.mainloop()

# ---------- MAIN ----------
if __name__ == "__main__":
    init_db()
    show_login()