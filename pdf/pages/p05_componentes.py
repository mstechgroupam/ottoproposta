"""Página 5 — Componentes do painel solar + Processo de instalação."""
import os
from reportlab.platypus import (Paragraph, Spacer, Image, Table,
                                 TableStyle, HRFlowable)
from reportlab.lib.units import mm
from config import IMG_COMPONENTES
from pdf.styles import (AZUL, LARANJA, VERDE, CINZA, CINZA_BORDA, BRANCO,
                         FB, F, CORPO, LABEL, SUBSEC, BULLET)
from pdf.components.section_title import SectionTitle
from pdf.components.numbered_step import NumberedStep

CAMADAS = [
    ("Vidro Temperado",
     "Proteção frontal resistente a impactos e intempéries."),
    ("EVA (Acetato de Vinila)",
     "Camada encapsulante que protege as células solares."),
    ("Células Fotovoltaicas",
     "Núcleo do painel onde ocorre a conversão de luz em eletricidade."),
    ("Backsheet",
     "Camada traseira isolante que protege contra umidade."),
    ("Moldura de Alumínio",
     "Estrutura que dá rigidez e facilita a instalação."),
]

INSTALACAO = [
    (1, "Visita Técnica",     "Análise completa do local e do telhado."),
    (2, "Projeto Executivo",  "Elaboração do projeto elétrico detalhado."),
    (3, "Documentação",       "Aprovação junto à concessionária de energia."),
    (4, "Instalação",         "Montagem do sistema fotovoltaico no telhado."),
    (5, "Conexão e Ativação", "Ligação à rede e ativação do monitoramento."),
]


def build(dados: dict) -> list:
    story = []

    story.append(SectionTitle("3. COMPONENTES DO PAINEL SOLAR", LARANJA))
    story.append(Spacer(1, 3*mm))

    if os.path.exists(IMG_COMPONENTES):
        try:
            img = Image(IMG_COMPONENTES, width=140*mm, height=60*mm)
            img.hAlign = "CENTER"
            story.append(img)
        except Exception:
            pass

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Estrutura Interna do Painel:", SUBSEC))
    story.append(Spacer(1, 2*mm))

    for titulo, desc in CAMADAS:
        row = [[Paragraph(f"• {titulo}", LABEL),
                Paragraph(desc, CORPO)]]
        t = Table(row, colWidths=[55*mm, None])
        t.setStyle(TableStyle([
            ("TOPPADDING",    (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING",   (0, 0), (-1, -1), 3),
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(t)

    story.append(Spacer(1, 5*mm))
    story.append(SectionTitle("4. PROCESSO DE INSTALAÇÃO", AZUL))
    story.append(Spacer(1, 4*mm))

    cores = [AZUL, LARANJA, VERDE, AZUL, LARANJA]
    for i, (num, titulo, desc) in enumerate(INSTALACAO):
        story.append(NumberedStep(num, titulo, desc,
                                   cor_circulo=cores[i % len(cores)],
                                   raio=5*mm))
        story.append(HRFlowable(width="100%", thickness=0.3,
                                 color=CINZA_BORDA, spaceAfter=2*mm))

    return story
