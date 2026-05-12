from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                Table, TableStyle, HRFlowable, Image,
                                KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER

W, H = letter

# ── PALETTE ────────────────────────────────────────────────────────────────
NAVY     = colors.HexColor("#0D1B2A")
BLUE     = colors.HexColor("#0B1E6B")   # very dark blue
BLUE_LT  = colors.HexColor("#D0DBFA")   # tint to match
ESGREEN  = colors.HexColor("#7AB51E")
LIGHT    = colors.HexColor("#F7F8FA")
MUTED    = colors.HexColor("#8A94A6")
DARK     = colors.HexColor("#1A2340")
WHITE    = colors.white
BORDER   = colors.HexColor("#D1D9E6")

LMARGIN = RMARGIN = 2*cm
AVAIL = W - LMARGIN - RMARGIN

doc = SimpleDocTemplate(
    "/home/claude/cotizacion_energia_simple_v9.pdf",
    pagesize=letter,
    leftMargin=LMARGIN, rightMargin=RMARGIN,
    topMargin=2*cm, bottomMargin=2*cm,
    title="Propuesta Económica - Herramienta de Diagnóstico de Energía Solar"
)

def S(name, **kw):
    return ParagraphStyle(name, **kw)

sEyebrow = S("sEyebrow", fontName="Helvetica-Bold", fontSize=8,  textColor=BLUE,  leading=10, letterSpacing=2)
sBodyMut = S("sBodyMut", fontName="Helvetica",      fontSize=8,  textColor=MUTED, leading=12)
sMeta    = S("sMeta",    fontName="Helvetica",      fontSize=8,  textColor=MUTED, leading=11)
sConc    = S("sConc",    fontName="Helvetica-Bold", fontSize=9,  textColor=DARK,  leading=13)
sDesc    = S("sDesc",    fontName="Helvetica",      fontSize=8.5,textColor=DARK,  leading=12)
sTotal   = S("sTotal",   fontName="Helvetica-Bold", fontSize=10, textColor=WHITE, leading=14, alignment=TA_RIGHT)
sTotLbl  = S("sTotLbl",  fontName="Helvetica-Bold", fontSize=10, textColor=WHITE, leading=14)
sFoot    = S("sFoot",    fontName="Helvetica",      fontSize=7.5,textColor=MUTED, leading=10, alignment=TA_CENTER)
sNote    = S("sNote",    fontName="Helvetica-Oblique", fontSize=8, textColor=MUTED, leading=11)
sExcl    = S("sExcl",    fontName="Helvetica-Bold", fontSize=8,  textColor=BLUE,  leading=12)
sExclBod = S("sExclBod", fontName="Helvetica",      fontSize=8,  textColor=DARK,  leading=12)
sAmt     = S("sAmt",     fontName="Helvetica",      fontSize=10, textColor=BLUE,  leading=14, alignment=TA_RIGHT)
sAmtEmp  = S("sAmtEmp",  fontName="Helvetica",      fontSize=9,  textColor=DARK,  leading=13)

story = []

# ── HEADER ─────────────────────────────────────────────────────────────────
logo = Image("/home/claude/energia-simple-logo.png", width=3.8*cm, height=1.4*cm)
hdr = Table([[
    logo, "",
    Paragraph(
        "Número de cotización: <b>002-ES</b><br/>"
        "Fecha de emisión: <b>Mayo 2026</b><br/>"
        "Vigencia: <b>14 días</b>",
        S("mR", fontName="Helvetica", fontSize=8, textColor=MUTED,
          leading=12, alignment=TA_RIGHT))
]], colWidths=[5*cm, AVAIL - 10.5*cm, 5.5*cm])
hdr.setStyle(TableStyle([
    ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ("BACKGROUND",   (0,0), (-1,-1), WHITE),
    ("TOPPADDING",   (0,0), (-1,-1), 10),
    ("BOTTOMPADDING",(0,0), (-1,-1), 10),
]))
story.append(hdr)
story.append(HRFlowable(width="100%", thickness=1.5, color=NAVY, spaceAfter=14))

# ── RECIPIENT ──────────────────────────────────────────────────────────────
recip = Table([
    [Paragraph("Cotización para:", sMeta),  "", Paragraph("Emisor:", sMeta)],
    [Paragraph("<b>Ing. Ernesto Reyes Martínez</b>",
               S("rN", fontName="Helvetica-Bold", fontSize=10, textColor=NAVY, leading=14)),
     "",
     Paragraph("<b>Patricio González Aceves</b>",
               S("rE", fontName="Helvetica-Bold", fontSize=10, textColor=NAVY, leading=14))],
    [Paragraph("ernesto.reyes@energiasimple.com", sBodyMut), "",
     Paragraph("pgzzaceves@gmail.com", sBodyMut)],
    [Paragraph("+52 81 2001 4443", sBodyMut), "",
     Paragraph("+52 81 2622 4761", sBodyMut)],
], colWidths=[8*cm, 1.5*cm, AVAIL - 9.5*cm])
recip.setStyle(TableStyle([
    ("VALIGN",     (0,0), (-1,-1), "TOP"),
    ("BACKGROUND", (0,0), (-1,-1), WHITE),
]))
story.append(recip)
story.append(Spacer(1, 16))

# ── SECTION TITLE ──────────────────────────────────────────────────────────
story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=10))
story.append(Paragraph("PLAN DE IMPLEMENTACIÓN - HERRAMIENTA DE DIAGNÓSTICO DE ENERGÍA SOLAR", sEyebrow))
story.append(Spacer(1, 6))

# ── TABLE HELPERS ──────────────────────────────────────────────────────────
COL_CONC  = 3.5*cm
COL_MONTO = 3.0*cm
COL_DESC  = AVAIL - COL_CONC - COL_MONTO
col_w = [COL_CONC, COL_DESC, COL_MONTO]

PAD = [
    ("TOPPADDING",    (0,0), (-1,-1), 7),
    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ("LEFTPADDING",   (0,0), (-1,-1), 7),
    ("RIGHTPADDING",  (0,0), (-1,-1), 7),
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ("ALIGN",         (2,0), (2,-1),  "RIGHT"),
    ("LINEBELOW",     (0,0), (-1,-1), 0.4, BORDER),
]

def th(txt, align=None):
    kw = dict(fontName="Helvetica-Bold", fontSize=8, textColor=MUTED, leading=10)
    if align: kw["alignment"] = align
    return Paragraph(txt, S(f"th{txt}", **kw))

def ph_style(name):
    return S(name, fontName="Helvetica-Bold", fontSize=8,
             textColor=BLUE, leading=10, letterSpacing=1.3)

def row(titulo, desc, precio=""):
    ps = sAmt if precio else sAmtEmp
    return [Paragraph(titulo, sConc), Paragraph(desc, sDesc), Paragraph(precio, ps)]

# ── COLUMN HEADER TABLE ────────────────────────────────────────────────────
hdr_tbl = Table(
    [[th("Concepto"), th("Descripción"), th("Monto", TA_RIGHT)]],
    colWidths=col_w
)
hdr_tbl.setStyle(TableStyle(PAD + [
    ("BACKGROUND", (0,0), (-1,0), LIGHT),
]))
story.append(hdr_tbl)

# ── ETAPA TABLE BUILDER ────────────────────────────────────────────────────
def make_etapa(phase_label, items, price_anchor):
    """
    items: list of (titulo, desc) tuples
    price_anchor: the price string shown merged across all item rows
    """
    n = len(items)
    rows = [
        [Paragraph(phase_label, ph_style(f"ph{phase_label}")), "", ""],
    ] + [
        row(t, d, price_anchor if i == 0 else "")
        for i, (t, d) in enumerate(items)
    ]
    # row 0: phase header spans cols 0-1
    # col 2, rows 1..n: price span
    span_cmds = [
        ("SPAN", (0,0), (1,0)),           # phase header cols
        ("SPAN", (2,1), (2, n)),          # price across item rows
    ]
    style = TableStyle(PAD + span_cmds + [
        ("BACKGROUND",  (0,0), (-1,0),  BLUE_LT),
        ("LINEBELOW",   (0,0), (-1,0),  0, WHITE),   # no line under phase header
        ("VALIGN",      (2,1), (2, n),  "MIDDLE"),    # price vertically centered
    ])
    tbl = Table(rows, colWidths=col_w)
    tbl.setStyle(style)
    return tbl

# ── ETAPA 1 ─────────────────────────────────────────────────────────────────
e1 = make_etapa(
    "ETAPA 1 - DESCUBRIMIENTO - Semanas 1-2",
    [
        ("Entrevistas de descubrimiento",
         "Sesiones de trabajo con dirección y equipo de ventas de Energía Simple "
         "para mapear el proceso comercial actual, revisar tarifas, portafolio de "
         "productos y flujos de atención al prospecto."),
        ("Gestión de accesos y configuración de branding",
         "Solicitud y configuración de accesos a dominio, hosting, Meta Ads y CRM. "
         "Aplicación del branding de Energía Simple: colores, logotipo y parámetros "
         "visuales en el entorno del diagnóstico."),
        ("Definición técnica de integraciones",
         "Levantamiento de requisitos técnicos: CRM de Energía Simple, webhooks "
         "necesarios, flujos de automatización y permisos de acceso para la "
         "integración completa del diagnóstico."),
    ],
    "$10,667.00"
)
story.append(e1)

# ── ETAPA 2 ─────────────────────────────────────────────────────────────────
e2 = make_etapa(
    "ETAPA 2 - IMPLEMENTACIÓN - Semanas 3-4",
    [
        ("Herramienta de diagnóstico de energía solar configurada",
         "Configuración de la herramienta de diagnóstico de energía solar interactiva con branding de Energía "
         "Simple, parámetros técnicos, tarifas vigentes y URL pública lista para "
         "compartir con prospectos."),
        ("Integración completa con CRM",
         "Conexión del formulario de captura al CRM via webhook. Email automático "
         "al prospecto con su diagnóstico de energía solar personalizado. Notificación interna "
         "al vendedor con los datos completos del lead."),
        ("Pruebas internas end-to-end",
         "Validación completa del flujo desde el llenado del diagnóstico hasta la "
         "llegada del lead al CRM. Ajuste de parámetros y corrección de errores "
         "previo al lanzamiento."),
    ],
    "$10,667.00"
)
story.append(e2)

# ── ETAPA 3 ──────────────────────────────────────────────────────────────────
e3 = make_etapa(
    "ETAPA 3 - LANZAMIENTO Y ENTREGA - Semanas 5-8",
    [
        ("Capacitación al equipo de ventas",
         "Sesión con el equipo comercial: uso de la herramienta, interpretación de "
         "resultados del diagnóstico y proceso de seguimiento de leads generados."),
        ("Deploy y Campañas Meta",
         "Publicación en el dominio de Energía Simple. Activación de campañas Meta "
         "Ads: diseño de artes, segmentación de audiencias, configuración del "
         "Meta Pixel y puesta en marcha."),
        ("Entrega formal y documentación",
         "Handoff completo con documentación técnica, guía de uso, manual de "
         "administración y entrega de accesos y credenciales del proyecto."),
    ],
    "$10,666.00"
)
story.append(KeepTogether([e3]))
story.append(Spacer(1, 14))

# ── EXCLUSIVITY BOX (blue, thin border) ────────────────────────────────────
excl_tbl = Table([
    [Paragraph("EXCLUSIVIDAD GARANTIZADA", sExcl)],
    [Paragraph(
        "La herramienta se mantiene configurada únicamente para Energía Simple. "
        "No se replica ni comercializa esta implementación con competidores directos "
        "en el sector solar de la región.",
        sExclBod)],
], colWidths=[AVAIL])
excl_tbl.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,-1), BLUE_LT),
    ("TOPPADDING",   (0,0), (-1,-1), 9),
    ("BOTTOMPADDING",(0,0), (-1,-1), 9),
    ("LEFTPADDING",  (0,0), (-1,-1), 14),
    ("RIGHTPADDING", (0,0), (-1,-1), 14),
    ("LINEBELOW",    (0,0), (-1,-1), 0.6, BLUE),
    ("LINEABOVE",    (0,0), (0, 0),  0.6, BLUE),
    ("LINEBEFORE",   (0,0), (0,-1),  0.6, BLUE),
    ("LINEAFTER",    (-1,0),(-1,-1), 0.6, BLUE),
    ("VALIGN",       (0,0), (-1,-1), "TOP"),
]))
story.append(excl_tbl)
story.append(Spacer(1, 16))

# ── TOTAL BAR ──────────────────────────────────────────────────────────────
tot_tbl = Table([[
    Paragraph("Total (sin IVA)", sTotLbl),
    Paragraph("$32,000.00 MXN", sTotal),
]], colWidths=[AVAIL - 5*cm, 5*cm])
tot_tbl.setStyle(TableStyle([
    ("BACKGROUND",   (0,0), (-1,-1), BLUE),
    ("TOPPADDING",   (0,0), (-1,-1), 12),
    ("BOTTOMPADDING",(0,0), (-1,-1), 12),
    ("LEFTPADDING",  (0,0), (-1,-1), 14),
    ("RIGHTPADDING", (0,0), (-1,-1), 14),
    ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ("ALIGN",        (1,0), (1,0),   "RIGHT"),
]))
story.append(tot_tbl)
story.append(Spacer(1, 8))
story.append(Paragraph(
    "* Precios no incluyen IVA. Tres pagos: $10,667 al inicio (Etapa 1), $10,667 en Semana 3 (Etapa 2), "
    "$10,666 en Semana 5 (Etapa 3).", sNote))
story.append(Paragraph(
    "* Duración total del proyecto: 8 semanas desde el inicio formal.", sNote))
story.append(Spacer(1, 20))

# ── FOOTER ─────────────────────────────────────────────────────────────────
story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=8))
story.append(Paragraph(
    "CONTENIDO CONFIDENCIAL  -  pgzzaceves@gmail.com  -  +52 81 2622 4761", sFoot))

doc.build(story)
print("Done")
