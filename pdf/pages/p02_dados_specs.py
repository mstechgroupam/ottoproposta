"""Página 2 — Dados do cliente + Especificações técnicas do sistema."""
import os
from reportlab.platypus import (Paragraph, Spacer, Table, TableStyle,
                                 Image, KeepTogether)
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from config import IMG_PAINEIS_FOTO
from pdf.styles import (AZUL, LARANJA, VERDE, CINZA, CINZA_BORDA, BRANCO,
                         FB, F,
                         LABEL, VALOR, CORPO, SUBSEC)
from pdf.components.section_title import SectionTitle

_CINZA_HEADER = HexColor("#F0F4FF")


def build(dados: dict) -> list:
    story = []

    # ── DADOS DO CLIENTE ─────────────────────────────────────────────
    story.append(SectionTitle("DADOS DO CLIENTE", AZUL))
    story.append(Spacer(1, 4*mm))

    campos_cliente = [
        ("Nome:",     dados.get("nome_cliente", "")),
        ("Endereço:", dados.get("endereco", "")),
        ("Telefone:", dados.get("telefone", "")),
        ("E-mail:",   dados.get("email", "")),
        ("Tipo:",     dados.get("tipo_cliente", "")),
    ]

    data_cliente = [
        [Paragraph(label, LABEL), Paragraph(valor, VALOR)]
        for label, valor in campos_cliente
    ]

    t_cliente = Table(data_cliente, colWidths=[35*mm, None])
    t_cliente.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CINZA),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [BRANCO, _CINZA_HEADER]),
        ("GRID",       (0, 0), (-1, -1), 0.3, CINZA_BORDA),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",  (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(t_cliente)
    story.append(Spacer(1, 6*mm))

    # ── ESPECIFICAÇÕES TÉCNICAS ───────────────────────────────────────
    story.append(SectionTitle("ESPECIFICAÇÕES TÉCNICAS DO SISTEMA", LARANJA))
    story.append(Spacer(1, 4*mm))

    consumo = f"{dados.get('consumo_kwh', 0):.0f} kWh"
    potencia = f"{dados.get('potencia_kwp', 0):.1f} kWp"
    qtd = f"{dados.get('qtd_paineis', 0)} unidades"
    painel = dados.get("modelo_painel", "—")
    inversor = dados.get("modelo_inversor", "—")

    campos_tech = [
        ("Consumo Médio Mensal:",  consumo),
        ("Potência do Sistema:",   potencia),
        ("Quantidade de Painéis:", qtd),
        ("Modelo do Painel:",      painel),
        ("Modelo do Inversor:",    inversor),
    ]

    data_tech = [
        [Paragraph(label, LABEL), Paragraph(valor, VALOR)]
        for label, valor in campos_tech
    ]

    t_tech = Table(data_tech, colWidths=[55*mm, None])
    t_tech.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [BRANCO, _CINZA_HEADER]),
        ("GRID",           (0, 0), (-1, -1), 0.3, CINZA_BORDA),
        ("TOPPADDING",     (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 4),
        ("LEFTPADDING",    (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 5),
        ("VALIGN",         (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 6*mm))

    # ── FOTO DOS PAINÉIS ──────────────────────────────────────────────
    if os.path.exists(IMG_PAINEIS_FOTO):
        try:
            img = Image(IMG_PAINEIS_FOTO, width=130*mm, height=65*mm)
            img.hAlign = "CENTER"
            story.append(img)
        except Exception:
            pass

    return story
