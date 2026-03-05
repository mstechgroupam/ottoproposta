"""Canvas callbacks: cabeçalho e rodapé de cada página de conteúdo."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from config import IMG_LOGO_HEADER, EMPRESA
from pdf.styles import AZUL, LARANJA, CINZA_BORDA, F, FB

_W, _H = A4
_BAR_H = 13*mm  # altura da barra azul do cabeçalho


def desenhar_cabecalho_conteudo(canvas, doc):
    """Barra azul no topo + logo + número da proposta."""
    canvas.saveState()
    dados = getattr(doc, "dados", {})

    # Barra azul
    canvas.setFillColor(AZUL)
    canvas.rect(0, _H - _BAR_H, _W, _BAR_H, fill=1, stroke=0)

    # Linha laranja na base da barra
    canvas.setFillColor(LARANJA)
    canvas.rect(0, _H - _BAR_H - 1.5*mm, _W, 1.5*mm, fill=1, stroke=0)

    # Logo (lado esquerdo)
    if os.path.exists(IMG_LOGO_HEADER):
        try:
            canvas.drawImage(IMG_LOGO_HEADER,
                             5*mm, _H - _BAR_H + 0.5*mm,
                             width=24*mm, height=10*mm,
                             preserveAspectRatio=True, mask="auto")
        except Exception:
            pass

    # Número da proposta (lado direito)
    numero = dados.get("numero", "")
    canvas.setFont(FB, 9)
    canvas.setFillColor(HexColor("#FFFFFF"))
    canvas.drawRightString(_W - 6*mm, _H - _BAR_H + 4*mm,
                           f"Proposta OTTO-{numero}")

    canvas.restoreState()


def desenhar_rodape(canvas, doc):
    """Rodapé com linha, endereço e número de página."""
    canvas.saveState()

    # Linha divisória
    canvas.setStrokeColor(CINZA_BORDA)
    canvas.setLineWidth(0.4)
    canvas.line(15*mm, 15*mm, _W - 15*mm, 15*mm)

    # Endereço
    canvas.setFont(F, 7.5)
    canvas.setFillColor(HexColor("#999999"))
    canvas.drawCentredString(_W/2, 11*mm, EMPRESA["endereco"])
    canvas.drawCentredString(_W/2, 7.5*mm,
                             f"Telefone: {EMPRESA['telefone']} | {EMPRESA['site']}")

    canvas.restoreState()


def decorar_pagina_conteudo(canvas, doc):
    desenhar_cabecalho_conteudo(canvas, doc)
    desenhar_rodape(canvas, doc)
