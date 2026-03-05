"""Página 8 — Garantias, manutenção e monitoramento do sistema."""
from reportlab.platypus import (Paragraph, Spacer, Table, TableStyle,
                                 HRFlowable)
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from pdf.styles import (AZUL, LARANJA, VERDE, CINZA, CINZA_BORDA, BRANCO,
                         FB, F, CORPO, LABEL, VALOR, SUBSEC, BULLET,
                         GAR_NOME, GAR_DESC, GAR_PRAZO)
from pdf.components.section_title import SectionTitle

GARANTIAS = [
    ("Painéis Solares", "25 anos",
     "Garantia de eficiência mínima de 80% após 25 anos de uso."),
    ("Inversor", "5 anos",
     "Possibilidade de extensão para até 10 anos mediante contrato."),
    ("Estruturas de Fixação", "10 anos",
     "Garantia contra corrosão e defeitos de fabricação."),
    ("Mão de Obra", "2 anos",
     "Garantia da instalação realizada pela equipe Otto Energia Solar."),
]

MANUTENCAO = [
    "Limpeza dos painéis a cada 6 meses (pode variar conforme clima e localização)",
    "Inspeção visual anual das conexões e estruturas",
    "Verificação do inversor e sistema de monitoramento",
    "Limpeza com água limpa, sem produtos abrasivos",
]

MONITORAMENTO = [
    "Sistema de monitoramento em tempo real via aplicativo",
    "Acompanhamento da geração de energia diária, mensal e anual",
    "Alertas automáticos em caso de queda de desempenho",
    "Histórico completo de produção de energia",
    "Comparativo de economia na conta de luz",
    "Acesso remoto de qualquer lugar via smartphone ou computador",
]


def build(dados: dict) -> list:
    story = []

    story.append(SectionTitle("GARANTIAS DO SISTEMA", VERDE))
    story.append(Spacer(1, 4*mm))

    # Tabela de garantias
    for nome, prazo, desc in GARANTIAS:
        row = [
            [Paragraph(nome, GAR_NOME),
             Paragraph(f"Garantia: {prazo}", GAR_PRAZO)],
            [Paragraph(desc, GAR_DESC), ""],
        ]
        t = Table(row, colWidths=["65%", "35%"])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), HexColor("#F9F9FB")),
            ("BOX",           (0, 0), (-1, -1), 0.5, CINZA_BORDA),
            ("TOPPADDING",    (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING",   (0, 0), (-1, -1), 6),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
            ("SPAN",          (0, 1), (1, 1)),
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(t)
        story.append(Spacer(1, 2*mm))

    story.append(Spacer(1, 3*mm))

    # ── Manutenção ────────────────────────────────────────────────────
    story.append(SectionTitle("MANUTENÇÃO DO SISTEMA", AZUL))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph(
        "O sistema fotovoltaico requer manutenção mínima:", CORPO))

    for item in MANUTENCAO:
        story.append(Paragraph(f"• {item}", BULLET))

    story.append(Paragraph(
        "A Otto Energia Solar oferece planos de manutenção preventiva opcionais, "
        "garantindo o máximo desempenho do seu sistema ao longo dos anos.", CORPO))

    story.append(Spacer(1, 3*mm))

    # ── Monitoramento ─────────────────────────────────────────────────
    story.append(SectionTitle("MONITORAMENTO DE DESEMPENHO", LARANJA))
    story.append(Spacer(1, 3*mm))

    for item in MONITORAMENTO:
        story.append(Paragraph(f"• {item}", BULLET))

    return story
