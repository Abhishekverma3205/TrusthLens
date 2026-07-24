import io
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def create_pdf(news_text, prediction, confidence, explanation):
    """
    Generates a PDF analysis report and returns a BytesIO object.
    """
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontSize=22,
        textColor=colors.HexColor("#5b21b6"),
        spaceAfter=6,
        alignment=TA_CENTER
    )

    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#6b7280"),
        spaceAfter=20,
        alignment=TA_CENTER
    )

    section_style = ParagraphStyle(
        "SectionStyle",
        parent=styles["Heading2"],
        fontSize=12,
        textColor=colors.HexColor("#1e1b4b"),
        spaceBefore=16,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#374151"),
        leading=16,
        spaceAfter=8
    )

    label_color = colors.HexColor("#dc2626") if prediction == "FAKE NEWS" else colors.HexColor("#16a34a")

    verdict_style = ParagraphStyle(
        "VerdictStyle",
        parent=styles["Normal"],
        fontSize=24,
        textColor=label_color,
        alignment=TA_CENTER,
        spaceBefore=8,
        spaceAfter=8,
        fontName="Helvetica-Bold"
    )

    content = []

    # ── Header ───────────────────────────────────────────────
    content.append(Paragraph("🧠 TruthLens AI", title_style))
    content.append(Paragraph("Fake News Detection Report", subtitle_style))
    content.append(Paragraph(
        f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
        subtitle_style
    ))
    content.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e5e7eb")))

    # ── Verdict ───────────────────────────────────────────────
    content.append(Spacer(1, 0.4*cm))
    content.append(Paragraph("ANALYSIS VERDICT", section_style))

    verdict_table = Table(
        [[Paragraph(prediction, verdict_style),
          Paragraph(f"Confidence: {confidence:.1f}%", ParagraphStyle(
              "ConfStyle", parent=styles["Normal"],
              fontSize=14, textColor=colors.HexColor("#6b7280"),
              alignment=TA_CENTER, spaceBefore=4
          ))]],
        colWidths=["50%", "50%"]
    )
    verdict_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#fef2f2") if prediction == "FAKE NEWS" else colors.HexColor("#f0fdf4")),
        ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#f9fafb")),
        ("ROUNDEDCORNERS", [8]),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#e5e7eb")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e7eb")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    content.append(verdict_table)

    # ── Article Text ─────────────────────────────────────────
    content.append(Spacer(1, 0.4*cm))
    content.append(Paragraph("ARTICLE TEXT ANALYZED", section_style))
    preview = news_text[:800] + ("..." if len(news_text) > 800 else "")
    content.append(Paragraph(preview, body_style))

    # ── Key Words ─────────────────────────────────────────────
    if explanation:
        content.append(Spacer(1, 0.3*cm))
        content.append(Paragraph("TOP INFLUENTIAL KEYWORDS", section_style))

        kw_data = [["#", "Keyword", "TF-IDF Score"]]
        for i, kw in enumerate(explanation[:10], 1):
            kw_data.append([str(i), kw["word"], f"{kw['score']:.4f}"])

        kw_table = Table(kw_data, colWidths=[1*cm, 9*cm, 4*cm])
        kw_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e1b4b")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f9fafb"), colors.white]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e7eb")),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ]))
        content.append(kw_table)

    # ── Footer ────────────────────────────────────────────────
    content.append(Spacer(1, 0.6*cm))
    content.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e5e7eb")))
    content.append(Spacer(1, 0.2*cm))
    content.append(Paragraph(
        "This report is generated by TruthLens AI. Results are based on ML analysis "
        "and should be used as a guide, not a definitive verdict.",
        ParagraphStyle("Footer", parent=styles["Normal"], fontSize=8,
                       textColor=colors.HexColor("#9ca3af"), alignment=TA_CENTER)
    ))

    doc.build(content)
    buffer.seek(0)
    return buffer
