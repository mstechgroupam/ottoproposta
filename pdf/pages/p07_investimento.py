"""Página 7 — Investimento, retorno, projeção de economia e benefícios."""
from reportlab.platypus import (Paragraph, Spacer, Table, TableStyle,
                                 HRFlowable)
from reportlab.platypus.flowables import Flowable
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from pdf.styles import (AZUL, LARANJA, VERDE, CINZA, CINZA_BORDA, BRANCO,
                         FB, F, LABEL, VALOR, CORPO, SUBSEC, BULLET,
                         LABEL_GRANDE)
from pdf.components.section_title import SectionTitle


def _fmt(valor: float) -> str:
    """Formata valor em reais → R$ 27.000,00"""
    s = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {s}"


# ── Flowable canvas para card KPI ─────────────────────────────────────────────
class KPICard(Flowable):
    """Card colorido com título (pequeno) e valor (grande) via canvas direto.
    Não usa Paragraph, então evita qualquer problema com caracteres especiais."""

    def __init__(self, titulo, valor, cor, altura=22*mm):
        super().__init__()
        self.titulo = titulo.upper()
        self.valor  = valor
        self.cor    = cor
        self.altura = altura

    def wrap(self, available_width, available_height):
        self._larg = available_width
        return (available_width, self.altura)

    def draw(self):
        c = self.canv
        h = self.altura
        # Fundo colorido
        c.setFillColor(self.cor)
        c.roundRect(0, 0, self._larg, h, 3*mm, fill=1, stroke=0)

        # Título (topo)
        c.setFillColor(white)
        c.setFont(FB, 8)
        c.drawCentredString(self._larg / 2, h - 6*mm, self.titulo)

        # Linha divisória sutil
        c.setStrokeColor(HexColor("#FFFFFF44") if False else
                         white)
        c.setLineWidth(0.3)
        c.line(4*mm, h - 8*mm, self._larg - 4*mm, h - 8*mm)

        # Valor (grande, auto-size)
        c.setFillColor(white)
        tam = 18
        while tam >= 10:
            c.setFont(FB, tam)
            if c.stringWidth(self.valor, FB, tam) <= self._larg - 6*mm:
                break
            tam -= 1
        # Centraliza verticalmente na área inferior
        meio_y = (h - 8*mm) / 2 - tam * 0.35
        c.drawCentredString(self._larg / 2, meio_y, self.valor)


def build(dados: dict) -> list:
    story = []

    inv = dados.get("investimento_total", 0)
    eco = dados.get("economia_mensal", 0)
    pay = dados.get("payback_meses", 0)
    pay_anos  = pay // 12
    pay_resto = pay % 12
    pagamento = dados.get("forma_pagamento", "À vista")

    if pay_anos and pay_resto:
        pay_str = f"{pay} meses ({pay_anos}a {pay_resto}m)"
    elif pay_anos:
        pay_str = f"{pay} meses ({pay_anos} anos)"
    else:
        pay_str = f"{pay} meses"

    story.append(SectionTitle("INVESTIMENTO E RETORNO", VERDE))
    story.append(Spacer(1, 5*mm))

    # ── Cards KPI (3 colunas) ─────────────────────────────────────────
    kpi_row = [
        KPICard("Investimento Total",        _fmt(inv),    AZUL),
        KPICard("Economia Mensal",           _fmt(eco),    VERDE),
        KPICard("Retorno do Investimento",   pay_str,      LARANJA),
    ]
    t_kpi = Table([kpi_row], colWidths=["32%", "32%", "32%"],
                   hAlign="CENTER", spaceAfter=5*mm)
    t_kpi.setStyle(TableStyle([
        ("LEFTPADDING",   (0, 0), (-1, -1), 2),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 2),
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(t_kpi)
    story.append(Spacer(1, 4*mm))

    # ── Projeção de economia ──────────────────────────────────────────
    story.append(SectionTitle("PROJEÇÃO DE ECONOMIA", AZUL))
    story.append(Spacer(1, 4*mm))

    proj = [
        ("1 Ano",   eco * 12),
        ("5 Anos",  eco * 12 * 5),
        ("10 Anos", eco * 12 * 10),
        ("25 Anos", eco * 12 * 25),
    ]
    row1 = [_proj_card(p[0], _fmt(p[1])) for p in proj[:2]]
    row2 = [_proj_card(p[0], _fmt(p[1])) for p in proj[2:]]

    t_proj = Table([row1, row2], colWidths=["49%", "49%"],
                    hAlign="CENTER", spaceAfter=5*mm)
    t_proj.setStyle(TableStyle([
        ("LEFTPADDING",   (0, 0), (-1, -1), 2),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 2),
        ("TOPPADDING",    (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(t_proj)
    story.append(Spacer(1, 4*mm))

    # ── Condições de pagamento ────────────────────────────────────────
    cond_data = [
        [Paragraph("CONDIÇÕES DE PAGAMENTO", LABEL)],
        [Paragraph(f"Forma de Pagamento: {pagamento}", VALOR)],
    ]
    t_cond = Table(cond_data, colWidths=["100%"])
    t_cond.setStyle(TableStyle([
        ("BOX",           (0, 0), (-1, -1), 0.5, CINZA_BORDA),
        ("BACKGROUND",    (0, 0), (-1, -1), HexColor("#F9F9FB")),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
    ]))
    story.append(t_cond)
    story.append(Spacer(1, 5*mm))

    # ── Benefícios ────────────────────────────────────────────────────
    story.append(SectionTitle("BENEFÍCIOS DO SISTEMA SOLAR", LARANJA))
    story.append(Spacer(1, 3*mm))

    beneficios = [
        "Economia de até 95% na conta de luz",
        "Valorização do imóvel em até 30%",
        "Energia 100% limpa e renovável",
        "Proteção contra aumentos na tarifa de energia",
        "Baixíssima necessidade de manutenção",
        "Garantia de 25 anos nos painéis solares",
        "Sistema totalmente silencioso",
    ]
    # Grid 2 colunas de benefícios
    pares = []
    for i in range(0, len(beneficios), 2):
        esq = Paragraph(f"\u2714 {beneficios[i]}", BULLET)
        dir_ = Paragraph(f"\u2714 {beneficios[i+1]}", BULLET) if i+1 < len(beneficios) else Paragraph("", BULLET)
        pares.append([esq, dir_])

    t_ben = Table(pares, colWidths=["50%", "50%"])
    t_ben.setStyle(TableStyle([
        ("TOPPADDING",    (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(t_ben)

    return story


def _proj_card(periodo, valor):
    conteudo = [
        [Paragraph(periodo, LABEL)],
        [Paragraph(valor, LABEL_GRANDE)],
    ]
    t = Table(conteudo, colWidths=["100%"])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), HexColor("#F0F4FF")),
        ("BOX",           (0, 0), (-1, -1), 0.5, CINZA_BORDA),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t
