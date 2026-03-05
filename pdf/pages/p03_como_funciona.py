"""Página 3 — Como funciona o sistema de energia solar fotovoltaica."""
import os
from reportlab.platypus import Paragraph, Spacer, Image
from reportlab.platypus.flowables import Flowable
from reportlab.lib.units import mm
from config import IMG_DIAGRAMA
from pdf.styles import (AZUL, LARANJA, VERDE,
                         FB, F, CORPO, LABEL, SUBSEC)
from pdf.components.section_title import SectionTitle

# Componentes usando canvas puro — sem emojis que podem falhar na fonte
COMPONENTES = [
    (LARANJA, "Painéis Solares",
     "Captam a luz do sol e a convertem em energia elétrica (corrente contínua)."),
    (AZUL,    "Inversor",
     "Converte a energia dos painéis (CC) em energia utilizável em casa (CA)."),
    (VERDE,   "Medidor Bidirecional",
     "Mede a energia consumida e a excedente injetada na rede da concessionária."),
    (AZUL,    "Quadro de Distribuição",
     "Distribui a energia para os equipamentos da sua residência ou comércio."),
]


class ComponenteItem(Flowable):
    """Marcador colorido + título + descrição, desenhado via canvas."""

    def __init__(self, cor, titulo, desc):
        super().__init__()
        self.cor    = cor
        self.titulo = titulo
        self.desc   = desc

    def wrap(self, available_width, available_height):
        self._larg = available_width
        self._alt  = 14*mm
        return (available_width, self._alt)

    def draw(self):
        from reportlab.platypus import Paragraph
        from pdf.styles import LABEL, CORPO
        c = self.canv
        r = 3*mm
        cy = self._alt / 2

        # Círculo de cor
        c.setFillColor(self.cor)
        c.circle(r, cy, r, fill=1, stroke=0)

        # Título
        txt_x = r * 2 + 3*mm
        txt_w = self._larg - txt_x
        p_tit = Paragraph(self.titulo, LABEL)
        tw, th = p_tit.wrap(txt_w, 999)
        p_tit.drawOn(c, txt_x, cy + 1*mm)

        # Desc
        p_desc = Paragraph(self.desc, CORPO)
        dw, dh = p_desc.wrap(txt_w, 999)
        p_desc.drawOn(c, txt_x, cy - dh - 0.5*mm)


def build(dados: dict) -> list:
    story = []

    story.append(SectionTitle(
        "COMO FUNCIONA O SISTEMA DE ENERGIA SOLAR FOTOVOLTAICA", AZUL))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph(
        "O sistema de energia solar fotovoltaica converte a luz do sol diretamente "
        "em energia elétrica através de painéis solares. É uma fonte de energia limpa, "
        "renovável e econômica que pode reduzir drasticamente sua conta de luz. "
        "Entenda como funciona cada etapa do processo:", CORPO))
    story.append(Spacer(1, 3*mm))

    story.append(SectionTitle("1. DIAGRAMA DO SISTEMA COMPLETO", AZUL,
                               altura=7*mm, font_size=10))
    story.append(Spacer(1, 3*mm))

    if os.path.exists(IMG_DIAGRAMA):
        try:
            img = Image(IMG_DIAGRAMA, width=140*mm, height=90*mm)
            img.hAlign = "CENTER"
            story.append(img)
        except Exception:
            pass

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Componentes Principais:", SUBSEC))
    story.append(Spacer(1, 2*mm))

    for cor, titulo, desc in COMPONENTES:
        story.append(ComponenteItem(cor, titulo, desc))
        story.append(Spacer(1, 1*mm))

    return story
