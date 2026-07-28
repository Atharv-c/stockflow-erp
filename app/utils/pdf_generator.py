from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Spacer
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle


styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    "Title",
    parent=styles["Title"],
    alignment=TA_CENTER,
    fontSize=22,
    spaceAfter=15,
)


def generate_invoice_pdf(invoice):
    """
    Generate Invoice PDF.
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=(210 * mm, 297 * mm),  # A4
        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20,
    )

    elements = []

    elements.append(
    Paragraph(
        "<b>StockFlow ERP</b>",
        title_style,
    )
)

    elements.append(
    Paragraph(
        "Pune, Maharashtra | GSTIN : 27ABCDE1234F1Z5",
        styles["Normal"],
    )
)

    elements.append(Spacer(1,15))
 
    elements.append(
        Paragraph(
            f"<b>Invoice No:</b> {invoice.invoice_number}",
            styles["Normal"],
        )
    )

    elements.append(
        Paragraph(
            f"<b>Date:</b> {invoice.invoice_date.strftime('%d-%m-%Y')}",
            styles["Normal"],
        )
    )

    elements.append(
        Paragraph(
            f"<b>Customer:</b> {invoice.customer.customer_name}",
            styles["Normal"],
        )
    )

    elements.append(
        Paragraph("<br/>", styles["Normal"])
    )

    data = [
        [
            "Product",
            "Qty",
            "Price",
            "GST %",
            "Total",
        ]
    ]

    for item in invoice.items:

        data.append(
            [
                item.product_name,
                str(item.quantity),
                f"₹ {item.unit_price}",
                f"{item.gst_percent}%",
                f"₹ {item.line_total}",
            ]
        )

    table = Table(
    data,
    colWidths=[180,50,80,60,90],
)

    table.setStyle(
    TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

        ("GRID",(0,0),(-1,-1),0.5,colors.grey),

        ("BACKGROUND",(0,1),(-1,-1),colors.beige),

        ("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("TOPPADDING",(0,0),(-1,-1),7),

        ("ALIGN",(1,1),(-1,-1),"CENTER"),
    ])
)

    elements.append(table)

    elements.append(
        Paragraph("<br/>", styles["Normal"])
    )

    totals = [
    ["Subtotal", f"₹ {invoice.subtotal}"],
    ["GST", f"₹ {invoice.gst_amount}"],
    ["Discount", f"₹ {invoice.discount_amount}"],
    ["Grand Total", f"₹ {invoice.grand_total}"],
]

    total_table = Table(
    totals,
    colWidths=[120,120],
    hAlign="RIGHT",
)

    total_table.setStyle(
    TableStyle([
        ("GRID",(0,0),(-1,-1),0.5,colors.grey),
        ("BACKGROUND",(0,-1),(-1,-1),colors.lightgrey),
        ("FONTNAME",(0,-1),(-1,-1),"Helvetica-Bold"),
    ])
)

    elements.append(Spacer(1,20))
    elements.append(total_table)
    elements.append(Spacer(1,35))

    elements.append(
    Paragraph(
        "<para alignment='right'><b>Authorized Signature</b></para>",
        styles["Normal"],
    )
)

    doc.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf