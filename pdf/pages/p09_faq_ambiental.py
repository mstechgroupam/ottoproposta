"""Página 9 — Perguntas frequentes + Impacto ambiental."""
from reportlab.platypus import (Paragraph, Spacer, Table, TableStyle)
from reportlab.platypus.flowables import Flowable
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from pdf.styles import (AZUL, LARANJA, VERDE, CINZA_BORDA,
                         FB, F, CORPO, BULLET,
                         FAQ_P, FAQ_R)
from pdf.components.section_title import SectionTitle

FAQS = [
    ("O sistema funciona à noite ou em dias nublados?",
     "O sistema gera energia durante o dia. A energia excedente é injetada na rede da "
     "concessionária, gerando créditos que podem ser utilizados à noite ou em dias nublados."),
    ("Quanto tempo dura a instalação?",
     "A instalação típica leva de 2 a 5 dias úteis, dependendo do tamanho do sistema "
     "e complexidade do local."),
    ("Preciso de autorização da concessionária?",
     "Sim, mas a Otto cuida de toda a documentação e processo de aprovação junto à concessionária."),
    ("O sistema requer muita manutenção?",
     "Não, a manutenção é mínima. Recomenda-se apenas limpeza periódica dos painéis e inspeção anual."),
    ("E se eu produzir mais energia do que consumo?",
     "Os créditos de energia são acumulados e podem ser utilizados em até 60 meses, "
     "conforme regras da ANEEL."),
]


class ImpactoCard(Flowable):
    """Card verde com número grande e label, via canvas."""

    def __init__(self, numero, label, altura=20*mm):
        super().__init__()
        self.numero = numero
        self.label  = label
        self.altura = altura

    def wrap(self, available_width, available_height):
        self._larg = available_width
        return (available_width, self.altura)

    def draw(self):
        c = self.canv
        h = self.altura
        # Fundo verde claro
        c.setFillColor(HexColor("#F0FFF4"))
        c.setStrokeColor(VERDE)
        c.setLineWidth(0.8)
        c.roundRect(0, 0, self._larg, h, 3*mm, fill=1, stroke=1)

        # Número grande (auto-size)
        tam = 20
        while tam >= 12:
            c.setFont(FB, tam)
            if c.stringWidth(self.numero, FB, tam) <= self._larg - 6*mm:
                break
            tam -= 1
        c.setFillColor(VERDE)
        c.drawCentredString(self._larg / 2, h * 0.52, self.numero)

        # Label
        c.setFont(F, 7.5)
        c.setFillColor(HexColor("#555555"))
        linhas = self.label.split("\n")
        y = h * 0.25
        for linha in reversed(linhas):
            c.drawCentredString(self._larg / 2, y, linha)
            y += 9


def build(dados: dict) -> list:
    story = []

    story.append(SectionTitle("PERGUNTAS FREQUENTES", AZUL))
    story.append(Spacer(1, 3*mm))

    for pergunta, resposta in FAQS:
        t_faq = Table(
            [[Paragraph(f"P: {pergunta}", FAQ_P)],
             [Paragraph(f"R: {resposta}", FAQ_R)]],
            colWidths=["100%"]
        )
        t_faq.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), HexColor("#F9F9FB")),
            ("BOX",           (0, 0), (-1, -1), 0.5, CINZA_BORDA),
            ("TOPPADDING",    (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING",   (0, 0), (-1, -1), 6),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
        ]))
        story.append(t_faq)
        story.append(Spacer(1, 2*mm))

    story.append(Spacer(1, 3*mm))
    story.append(SectionTitle("IMPACTO AMBIENTAL", VERDE))
    story.append(Spacer(1, 3*mm))

    story.append(Paragraph(
        "Com este sistema, você estará contribuindo para um planeta mais sustentável:", CORPO))
    story.append(Spacer(1, 4*mm))

    co2  = dados.get("co2_ano", 0)
    arv  = int(dados.get("arvores", 0))
    kwh  = int(dados.get("geracao_kwh_ano", 0))

    co2_str = f"{co2:.1f}".replace(".", ",")
    kwh_str = f"{kwh:,}".replace(",", ".")

    cards_row = [
        ImpactoCard(co2_str, "toneladas de CO2\nevitadas por ano"),
        ImpactoCard(str(arv),  "árvores equivalentes\nplantadas por ano"),
        ImpactoCard(kwh_str,   "kWh de energia\nlimpa gerada/ano"),
    ]
    t_imp = Table([cards_row], colWidths=["33%", "33%", "33%"],
                   hAlign="CENTER", spaceAfter=4*mm)
    t_imp.setStyle(TableStyle([
        ("LEFTPADDING",   (0, 0), (-1, -1), 2),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 2),
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(t_imp)
    story.append(Spacer(1, 4*mm))

    bullets = [
        "Redução da dependência de combustíveis fósseis",
        "Contribuição ativa para o combate às mudanças climáticas",
        "Geração local de energia sem emissão de poluentes",
    ]
    for b in bullets:
        story.append(Paragraph(f"\u25cf  {b}", BULLET))

    return story
