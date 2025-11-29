from io import BytesIO
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def generate_pdf_report(df: pd.DataFrame, summary_text: str) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    elements = []

    # Title
    title = Paragraph("Auto Data Explorer – Summary Report", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Basic info
    info_text = f"Rows: {df.shape[0]} &nbsp;&nbsp;&nbsp; Columns: {df.shape[1]}"
    elements.append(Paragraph(info_text, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Summary text
    elements.append(Paragraph("<b>Summary:</b>", styles["Heading2"]))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(summary_text.replace("\n", "<br/>"), styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Descriptive stats (top few rows)
    try:
        desc = df.describe().round(3)
        desc = desc.head(8)
        table_data = [ ["Column"] + desc.columns.tolist() ]
        for idx, row in desc.iterrows():
            table_data.append([str(idx)] + [str(v) for v in row.values])

        table = Table(table_data, repeatRows=1)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#222222")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ]
            )
        )
        elements.append(Paragraph("<b>Descriptive Statistics:</b>", styles["Heading2"]))
        elements.append(Spacer(1, 6))
        elements.append(table)
    except Exception:
        # ignore stats if something fails
        pass

    doc.build(elements)
    buffer.seek(0)
    return buffer
