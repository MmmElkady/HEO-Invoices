from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import io

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    client_name = request.form['client_name']
    client_address = request.form['client_address']
    item = request.form['item']
    qty = int(request.form['qty'])
    price = float(request.form['price'])
    total = qty * price

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("فاتورة", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"العميل: {client_name}", styles['Normal']))
    elements.append(Paragraph(f"العنوان: {client_address}", styles['Normal']))
    elements.append(Spacer(1, 12))

    data = [["البند", "الكمية", "السعر", "الإجمالي"],
            [item, qty, f"{price:.2f}", f"{total:.2f}"]]
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("شكرًا لتعاملكم معنا ❤️", styles['Italic']))

    doc.build(elements)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="invoice.pdf", mimetype='application/pdf')

if __name__ == "__main__":
    app.run()
