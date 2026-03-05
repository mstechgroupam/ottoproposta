"""Página 6 — Sobre a Otto Energia Solar + Diferenciais + Certificações."""
from reportlab.platypus import (Paragraph, Spacer, Table, TableStyle,
                                 HRFlowable)
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from pdf.styles import (AZUL, LARANJA, VERDE, CINZA, CINZA_BORDA, BRANCO,
                         FB, F, CORPO, LABEL, SUBSEC, DIF_TITULO, DIF_DESC,
                         BULLET)
from pdf.components.section_title import SectionTitle

DIFERENCIAIS = [
    ("Experiência Comprovada",
     "Anos de atuação no mercado de energia solar em Manaus e região."),
    ("Equipamentos de Qualidade",
     "Trabalhamos apenas com marcas líderes do mercado global."),
    ("Equipe Certificada",
     "Profissionais qualificados e em constante atualização técnica."),
    ("Acompanhamento Total",
     "Suporte completo durante e após a instalação do sistema."),
    ("Garantias Estendidas",
     "Garantia de 25 anos nos painéis e 5 anos nos inversores."),
    ("Melhor Custo-Benefício",
     "Preços competitivos sem abrir mão da qualidade e do prazo."),
]

CERTIFICACOES = [
    "Equipe com certificação NR35 (Trabalho em Altura)",
    "Certificação NR10 (Segurança em Instalações Elétricas)",
    "Parceiros autorizados de fabricantes renomados",
    "Projetos aprovados pela concessionária local",
    "Instalações conforme normas ABNT e ANEEL",
]


def build(dados: dict) -> list:
    story = []

    story.append(SectionTitle("SOBRE A OTTO ENERGIA SOLAR", LARANJA))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph(
        "A Otto Energia Solar é uma empresa especializada em soluções completas de "
        "energia solar fotovoltaica, atuando no mercado de Manaus e região. Nossa missão "
        "é proporcionar economia, sustentabilidade e independência energética para nossos clientes.",
        CORPO))

    story.append(Paragraph(
        "Com equipe técnica qualificada e certificada, utilizamos equipamentos de primeira "
        "linha e oferecemos garantia total em nossos serviços. Acompanhamos cada projeto "
        "desde o planejamento até a instalação e pós-venda, garantindo total satisfação.",
        CORPO))

    story.append(Spacer(1, 3*mm))
    story.append(SectionTitle("NOSSOS DIFERENCIAIS", AZUL))
    story.append(Spacer(1, 4*mm))

    # Grid 2 colunas de diferenciais
    _CINZA_CARD = HexColor("#F0F4FF")
    rows = []
    for i in range(0, len(DIFERENCIAIS), 2):
        esq = _card_dif(*DIFERENCIAIS[i])
        dir_ = _card_dif(*DIFERENCIAIS[i+1]) if i+1 < len(DIFERENCIAIS) else ""
        rows.append([esq, dir_])

    t = Table(rows, colWidths=["49%", "49%"],
              hAlign="CENTER", spaceBefore=0, spaceAfter=0)
    t.setStyle(TableStyle([
        ("LEFTPADDING",   (0, 0), (-1, -1), 3),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 3),
        ("TOPPADDING",    (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(t)
    story.append(Spacer(1, 5*mm))

    story.append(SectionTitle("CERTIFICAÇÕES E QUALIFICAÇÕES", VERDE))
    story.append(Spacer(1, 4*mm))

    for cert in CERTIFICACOES:
        story.append(Paragraph(f"• {cert}", BULLET))

    return story


def _card_dif(titulo, desc):
    from reportlab.platypus import Table, TableStyle
    from pdf.styles import CINZA, CINZA_BORDA
    conteudo = [
        [Paragraph(titulo, DIF_TITULO)],
        [Paragraph(desc, DIF_DESC)],
    ]
    t = Table(conteudo, colWidths=["100%"])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), CINZA),
        ("BOX",           (0, 0), (-1, -1), 0.5, CINZA_BORDA),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ]))
    return t
