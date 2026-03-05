"""Página 10 — Etapas do projeto + Termos e condições + Assinaturas."""
from reportlab.platypus import (Paragraph, Spacer, HRFlowable)
from reportlab.platypus.flowables import Flowable
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from pdf.styles import (AZUL, LARANJA, VERDE, CINZA_BORDA,
                         FB, F, SUBSEC, TERMOS)
from pdf.components.section_title import SectionTitle
from pdf.components.numbered_step import NumberedStep
from config import EMPRESA

ETAPAS = [
    (1, "Visita Técnica",     "Análise completa do local de instalação."),
    (2, "Projeto Executivo",  "Elaboração do projeto elétrico detalhado."),
    (3, "Documentação",       "Aprovação junto à concessionária de energia."),
    (4, "Instalação",         "Montagem do sistema fotovoltaico."),
    (5, "Conexão e Ativação", "Ligação à rede elétrica e ativação do sistema."),
]

CORES_ETAPAS = [AZUL, LARANJA, VERDE, AZUL, LARANJA]


class AssinaturaFlowable(Flowable):
    """Área de assinaturas com linhas desenhadas e labels abaixo."""

    def __init__(self, label_esq, label_dir, altura=28*mm):
        super().__init__()
        self.label_esq = label_esq
        self.label_dir = label_dir
        self.altura    = altura

    def wrap(self, available_width, available_height):
        self._larg = available_width
        return (available_width, self.altura)

    def draw(self):
        c = self.canv
        h = self.altura
        metade = self._larg / 2
        pad = 12*mm

        # Linhas de assinatura
        c.setStrokeColor(AZUL)
        c.setLineWidth(0.8)
        c.line(pad, h * 0.55, metade - pad, h * 0.55)
        c.line(metade + pad, h * 0.55, self._larg - pad, h * 0.55)

        # Labels principais
        c.setFont(FB, 9)
        c.setFillColor(AZUL)
        c.drawCentredString(metade / 2, h * 0.38, self.label_esq)
        c.drawCentredString(metade + metade / 2, h * 0.38, self.label_dir)

        # Sub-labels
        c.setFont(F, 7.5)
        c.setFillColor(HexColor("#888888"))
        c.drawCentredString(metade / 2, h * 0.22, "Nome / Assinatura")
        c.drawCentredString(metade + metade / 2, h * 0.22, "Representante Legal")


class CTABox(Flowable):
    """Box de destaque azul para contato final."""

    def __init__(self, altura=22*mm):
        super().__init__()
        self.altura = altura

    def wrap(self, available_width, available_height):
        self._larg = available_width
        return (available_width, self.altura)

    def draw(self):
        c = self.canv
        h = self.altura

        # Fundo azul
        c.setFillColor(AZUL)
        c.roundRect(0, 0, self._larg, h, 3*mm, fill=1, stroke=0)
        # Acento laranja no topo
        c.setFillColor(LARANJA)
        c.rect(3*mm, h - 2.5*mm, self._larg - 6*mm, 2.5*mm, fill=1, stroke=0)

        # Chamada
        c.setFillColor(white)
        c.setFont(FB, 11)
        c.drawCentredString(self._larg / 2, h * 0.60, "Entre em contato conosco!")

        # Telefone e site
        c.setFont(F, 9)
        c.setFillColor(HexColor("#CCDDFF"))
        c.drawCentredString(
            self._larg / 2, h * 0.32,
            f"{EMPRESA['telefone']}   |   {EMPRESA['site']}"
        )


def build(dados: dict) -> list:
    story = []

    story.append(SectionTitle("ETAPAS DO PROJETO", AZUL))
    story.append(Spacer(1, 4*mm))

    for i, (num, titulo, desc) in enumerate(ETAPAS):
        story.append(NumberedStep(num, titulo, desc,
                                   cor_circulo=CORES_ETAPAS[i],
                                   raio=5.5*mm))
        story.append(HRFlowable(width="100%", thickness=0.3,
                                 color=CINZA_BORDA, spaceAfter=2*mm))

    story.append(Spacer(1, 4*mm))

    # ── Termos e condições ────────────────────────────────────────────
    story.append(Paragraph("TERMOS E CONDIÇÕES", SUBSEC))
    story.append(Spacer(1, 2*mm))

    data_val = dados.get("data_validade", "—")

    termos = [
        f"Esta proposta tem validade até {data_val}.",
        "Os valores apresentados são estimativas baseadas nas informações fornecidas.",
        "A proposta final será elaborada após visita técnica ao local.",
        "Os equipamentos podem sofrer alterações conforme disponibilidade de estoque.",
        "Garantia de 25 anos para os painéis solares e 5 anos para inversores.",
        "Instalação realizada por equipe especializada e certificada.",
    ]
    for termo in termos:
        story.append(Paragraph(f"• {termo}", TERMOS))

    story.append(Spacer(1, 8*mm))

    # ── Área de assinaturas ───────────────────────────────────────────
    story.append(AssinaturaFlowable("CLIENTE", "OTTO ENERGIA SOLAR"))
    story.append(Spacer(1, 5*mm))

    # ── CTA de contato ────────────────────────────────────────────────
    story.append(CTABox())

    return story
