"""Página 4 — Fluxo de energia: do sol até sua casa (5 passos)."""
import os
from reportlab.platypus import Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.units import mm
from config import IMG_FLUXO
from pdf.styles import (AZUL, LARANJA, VERDE, CINZA, CINZA_BORDA,
                         FB, F, CORPO, SUBSEC)
from pdf.components.section_title import SectionTitle
from pdf.components.numbered_step import NumberedStep


PASSOS = [
    (1, "Captação da Luz Solar",
     "Os painéis solares captam a radiação solar através de células fotovoltaicas. "
     "Cada célula é composta de materiais semicondutores (silício) que geram corrente "
     "elétrica quando expostos à luz."),
    (2, "Geração de Energia",
     "A luz solar excita os elétrons nas células fotovoltaicas, criando corrente elétrica "
     "contínua (CC). Quanto maior a intensidade de luz, maior a geração de energia."),
    (3, "Conversão da Energia",
     "O inversor solar converte a corrente contínua (CC) gerada pelos painéis em corrente "
     "alternada (CA), compatível com os equipamentos elétricos da sua residência e com a "
     "rede da concessionária."),
    (4, "Utilização da Energia",
     "A energia convertida é enviada ao quadro de distribuição e utilizada imediatamente "
     "pelos equipamentos ligados. Você consome primeiro a energia solar gerada."),
    (5, "Energia Excedente",
     "Se gerar mais energia do que consome, o excedente é automaticamente injetado na rede "
     "da concessionária, gerando créditos que podem ser utilizados à noite ou em dias nublados."),
]

CORES_PASSOS = [AZUL, LARANJA, VERDE, AZUL, LARANJA]


def build(dados: dict) -> list:
    story = []

    story.append(SectionTitle("2. FLUXO DE ENERGIA — DO SOL ATÉ SUA CASA", LARANJA))
    story.append(Spacer(1, 4*mm))

    # Imagem do diagrama de fluxo
    if os.path.exists(IMG_FLUXO):
        try:
            img = Image(IMG_FLUXO, width=130*mm, height=55*mm)
            img.hAlign = "CENTER"
            story.append(img)
        except Exception:
            pass

    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("Passo a Passo do Funcionamento:", SUBSEC))
    story.append(Spacer(1, 2*mm))

    for i, (num, titulo, desc) in enumerate(PASSOS):
        cor = CORES_PASSOS[i % len(CORES_PASSOS)]
        step = NumberedStep(num, titulo, desc, cor_circulo=cor)
        story.append(step)

        # Separador sutil entre passos
        story.append(Spacer(1, 1*mm))
        from reportlab.platypus import HRFlowable
        story.append(HRFlowable(width="100%", thickness=0.3,
                                 color=CINZA_BORDA, spaceAfter=2*mm))

    return story
