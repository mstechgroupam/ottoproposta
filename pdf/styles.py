"""Estilos centralizados: cores, fontes e ParagraphStyles para o PDF."""
import os
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Fontes ──────────────────────────────────────────────────────────────────
_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_FONTS_DIR = os.path.join(_BASE, "static", "fonts")

_fonts_registered = False

def registrar_fontes():
    global _fonts_registered
    if _fonts_registered:
        return
    regular = os.path.join(_FONTS_DIR, "DejaVuSans.ttf")
    bold    = os.path.join(_FONTS_DIR, "DejaVuSans-Bold.ttf")
    if os.path.exists(regular):
        pdfmetrics.registerFont(TTFont("DejaVu", regular))
        pdfmetrics.registerFont(TTFont("DejaVuB", bold))
        pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVuB")
        _fonts_registered = True

# ── Paleta ───────────────────────────────────────────────────────────────────
AZUL        = HexColor("#1B3A6B")
AZUL_CLARO  = HexColor("#2D5A9E")
LARANJA     = HexColor("#F7941D")
VERDE       = HexColor("#4CAF50")
CINZA       = HexColor("#F5F5F5")
CINZA_BORDA = HexColor("#DDDDDD")
CINZA_TEXTO = HexColor("#555555")
BRANCO      = white
PRETO       = black

# ── Fonte padrão ─────────────────────────────────────────────────────────────
# Será atualizada para DejaVu após registrar_fontes() ser chamada
F  = "DejaVu"
FB = "DejaVuB"

# ── Estilos de parágrafo ─────────────────────────────────────────────────────
def _s(name, **kw):
    return ParagraphStyle(name, **kw)

# Capa
CAPA_TITULO = _s("CapaTitulo",
    fontName=FB, fontSize=32, textColor=AZUL,
    alignment=TA_CENTER, spaceAfter=4*mm, leading=36)

CAPA_SUBTITULO = _s("CapaSub",
    fontName=FB, fontSize=14, textColor=BRANCO,
    alignment=TA_CENTER, spaceAfter=2*mm)

CAPA_PROPOSTA_LABEL = _s("CapaPropostaLabel",
    fontName=FB, fontSize=13, textColor=AZUL,
    alignment=TA_CENTER, spaceAfter=3*mm)

CAPA_DATA = _s("CapaData",
    fontName=F, fontSize=10, textColor=CINZA_TEXTO,
    alignment=TA_CENTER, spaceAfter=2*mm)

CAPA_PREP_PARA = _s("CapaPrepPara",
    fontName=FB, fontSize=11, textColor=AZUL,
    alignment=TA_CENTER, spaceAfter=3*mm)

CAPA_CLIENTE = _s("CapaCliente",
    fontName=FB, fontSize=18, textColor=BRANCO,
    alignment=TA_CENTER, spaceAfter=2*mm)

CAPA_RODAPE = _s("CapaRodape",
    fontName=F, fontSize=9, textColor=CINZA_TEXTO,
    alignment=TA_CENTER, spaceAfter=1*mm)

# Seção
SEC_HEADER = _s("SecHeader",
    fontName=FB, fontSize=12, textColor=BRANCO,
    alignment=TA_LEFT, leftIndent=4*mm,
    spaceBefore=1*mm, spaceAfter=1*mm)

# Conteúdo geral
CORPO = _s("Corpo",
    fontName=F, fontSize=10, textColor=CINZA_TEXTO,
    alignment=TA_JUSTIFY, leading=15, spaceAfter=4*mm)

CORPO_LEFT = _s("CorpoLeft",
    fontName=F, fontSize=10, textColor=CINZA_TEXTO,
    alignment=TA_LEFT, leading=15, spaceAfter=3*mm)

LABEL = _s("Label",
    fontName=FB, fontSize=10, textColor=AZUL,
    alignment=TA_LEFT, spaceAfter=1*mm)

VALOR = _s("Valor",
    fontName=F, fontSize=10, textColor=CINZA_TEXTO,
    alignment=TA_LEFT)

LABEL_GRANDE = _s("LabelGrande",
    fontName=FB, fontSize=13, textColor=AZUL,
    alignment=TA_CENTER, spaceAfter=1*mm)

VALOR_GRANDE = _s("ValorGrande",
    fontName=FB, fontSize=20, textColor=AZUL,
    alignment=TA_CENTER, spaceAfter=2*mm)

VALOR_KPI = _s("ValorKPI",
    fontName=FB, fontSize=22, textColor=BRANCO,
    alignment=TA_CENTER)

LABEL_KPI = _s("LabelKPI",
    fontName=FB, fontSize=9, textColor=BRANCO,
    alignment=TA_CENTER, spaceAfter=1*mm)

# Bullet
BULLET = _s("Bullet",
    fontName=F, fontSize=10, textColor=CINZA_TEXTO,
    alignment=TA_LEFT, leading=15,
    leftIndent=5*mm, spaceAfter=2*mm, firstLineIndent=-5*mm)

# FAQ
FAQ_P = _s("FAQP",
    fontName=FB, fontSize=10, textColor=AZUL,
    alignment=TA_LEFT, spaceAfter=2*mm, spaceBefore=4*mm)

FAQ_R = _s("FAQR",
    fontName=F, fontSize=10, textColor=CINZA_TEXTO,
    alignment=TA_JUSTIFY, leading=14, leftIndent=3*mm, spaceAfter=2*mm)

# Passo numerado - título
PASSO_TITULO = _s("PassoTitulo",
    fontName=FB, fontSize=11, textColor=AZUL,
    alignment=TA_LEFT, spaceAfter=1*mm)

PASSO_DESC = _s("PassoDesc",
    fontName=F, fontSize=9, textColor=CINZA_TEXTO,
    alignment=TA_JUSTIFY, leading=13)

# Rodapé de página
RODAPE = _s("Rodape",
    fontName=F, fontSize=8, textColor=CINZA_TEXTO,
    alignment=TA_CENTER)

# Subsecção (título menor, com cor)
SUBSEC = _s("Subsec",
    fontName=FB, fontSize=11, textColor=AZUL,
    alignment=TA_LEFT, spaceAfter=2*mm, spaceBefore=3*mm)

# Garantia
GAR_NOME = _s("GarNome",
    fontName=FB, fontSize=10, textColor=AZUL,
    alignment=TA_LEFT, spaceAfter=1*mm)

GAR_DESC = _s("GarDesc",
    fontName=F, fontSize=9, textColor=CINZA_TEXTO,
    alignment=TA_LEFT)

GAR_PRAZO = _s("GarPrazo",
    fontName=FB, fontSize=11, textColor=VERDE,
    alignment=TA_RIGHT)

# Diferencial (card)
DIF_TITULO = _s("DifTitulo",
    fontName=FB, fontSize=10, textColor=AZUL,
    alignment=TA_LEFT, spaceAfter=1*mm)

DIF_DESC = _s("DifDesc",
    fontName=F, fontSize=9, textColor=CINZA_TEXTO,
    alignment=TA_LEFT, leading=13)

# Impacto
IMPACTO_NUM = _s("ImpactoNum",
    fontName=FB, fontSize=20, textColor=VERDE,
    alignment=TA_CENTER)

IMPACTO_LABEL = _s("ImpactoLabel",
    fontName=F, fontSize=9, textColor=CINZA_TEXTO,
    alignment=TA_CENTER)

# Assinatura
ASSINATURA_LINHA = _s("AssinaturaLinha",
    fontName=F, fontSize=9, textColor=CINZA_TEXTO,
    alignment=TA_CENTER, spaceAfter=0)

TERMOS = _s("Termos",
    fontName=F, fontSize=9, textColor=CINZA_TEXTO,
    alignment=TA_LEFT, leading=14, spaceAfter=2*mm)
