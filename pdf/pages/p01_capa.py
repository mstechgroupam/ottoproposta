"""Página 1 — Capa da proposta (design premium)."""
import os
from reportlab.platypus.flowables import Flowable
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from config import IMG_LOGO_HEADER, EMPRESA
from pdf.styles import AZUL, LARANJA, CINZA_BORDA, BRANCO, FB, F

_W, _H = A4

_ZONA_AZUL_H  = _H * 0.42
_ZONA_LARANJA = 3*mm
_RODAPE_H     = 20*mm


class CapaPage(Flowable):
    def __init__(self, dados: dict):
        super().__init__()
        self.dados = dados

    def wrap(self, available_width, available_height):
        return (_W, _H)

    def draw(self):
        _draw_capa(self.canv, self.dados)


def _draw_capa(c, d):
    # Fundo branco total
    c.setFillColor(BRANCO)
    c.rect(0, 0, _W, _H, fill=1, stroke=0)

    # Zona azul superior
    topo_y = _H - _ZONA_AZUL_H
    c.setFillColor(AZUL)
    c.rect(0, topo_y, _W, _ZONA_AZUL_H, fill=1, stroke=0)

    # Tira laranja no alto
    c.setFillColor(LARANJA)
    c.rect(0, _H - 4*mm, _W, 4*mm, fill=1, stroke=0)

    # Logo OTTO centralizado na zona azul
    logo_w, logo_h = 80*mm, 50*mm
    logo_x = (_W - logo_w) / 2
    logo_y = topo_y + (_ZONA_AZUL_H - logo_h) / 2 + 4*mm
    if os.path.exists(IMG_LOGO_HEADER):
        try:
            c.drawImage(IMG_LOGO_HEADER, logo_x, logo_y,
                        width=logo_w, height=logo_h,
                        preserveAspectRatio=True, mask="auto")
        except Exception:
            c.setFillColor(BRANCO)
            c.setFont(FB, 26)
            c.drawCentredString(_W/2, topo_y + _ZONA_AZUL_H/2, "OTTO ENERGIA SOLAR")

    # Barra laranja separadora
    barra_y = topo_y - _ZONA_LARANJA
    c.setFillColor(LARANJA)
    c.rect(0, barra_y, _W, _ZONA_LARANJA, fill=1, stroke=0)

    # Título
    content_y = barra_y - 9*mm
    c.setFillColor(AZUL)
    c.setFont(FB, 30)
    c.drawCentredString(_W/2, content_y - 10*mm, "PROPOSTA COMERCIAL")

    # Box laranja — subtítulo
    sub_bx, sub_bw, sub_bh = 30*mm, _W - 60*mm, 9*mm
    sub_by = content_y - 25*mm
    c.setFillColor(LARANJA)
    c.roundRect(sub_bx, sub_by, sub_bw, sub_bh, 3*mm, fill=1, stroke=0)
    c.setFillColor(BRANCO)
    c.setFont(FB, 11)
    c.drawCentredString(_W/2, sub_by + (sub_bh - 11)/2 + 1,
                        "Sistema de Energia Solar Fotovoltaica")

    # Box info da proposta
    numero        = d.get("numero", "001")
    data_emissao  = d.get("data_emissao", "")
    data_validade = d.get("data_validade", "")

    box_x = _W/2 - 52*mm
    box_w, box_h = 104*mm, 38*mm
    box_y = sub_by - 14*mm - box_h
    c.setFillColor(HexColor("#F7F9FF"))
    c.setStrokeColor(CINZA_BORDA)
    c.setLineWidth(0.8)
    c.roundRect(box_x, box_y, box_w, box_h, 4*mm, fill=1, stroke=1)
    # Acento laranja no topo do box
    c.setFillColor(LARANJA)
    c.rect(box_x + 2*mm, box_y + box_h - 2.5*mm, box_w - 4*mm, 2.5*mm,
           fill=1, stroke=0)

    cx = _W / 2
    c.setFillColor(AZUL)
    c.setFont(FB, 12)
    c.drawCentredString(cx, box_y + box_h - 12*mm,
                        f"PROPOSTA N\u00ba OTTO-{numero}")
    c.setFillColor(HexColor("#444444"))
    c.setFont(F, 10)
    c.drawCentredString(cx, box_y + box_h - 21*mm,
                        f"Data de Emiss\u00e3o: {data_emissao}")
    c.drawCentredString(cx, box_y + box_h - 30*mm,
                        f"V\u00e1lido at\u00e9: {data_validade}")

    # "Preparado para:"
    prep_y = box_y - 12*mm
    c.setFillColor(AZUL)
    c.setFont(FB, 11)
    c.drawCentredString(_W/2, prep_y, "Preparado para:")

    # Box laranja — nome do cliente
    nome = d.get("nome_cliente", "").upper()
    cx_bx, cx_bw, cx_bh = 18*mm, _W - 36*mm, 14*mm
    cx_by = prep_y - 4*mm - cx_bh
    c.setFillColor(LARANJA)
    c.roundRect(cx_bx, cx_by, cx_bw, cx_bh, 4*mm, fill=1, stroke=0)
    c.setFillColor(BRANCO)
    _draw_text_fit(c, nome, _W/2, cx_by + (cx_bh - 13)/2 + 1,
                   cx_bw - 10*mm, FB, 13)

    # Rodapé cinza
    c.setFillColor(HexColor("#F0F2F5"))
    c.rect(0, 0, _W, _RODAPE_H, fill=1, stroke=0)
    c.setFillColor(HexColor("#777777"))
    c.setFont(F, 8)
    c.drawCentredString(_W/2, _RODAPE_H - 7*mm, EMPRESA["endereco"])
    c.drawCentredString(_W/2, _RODAPE_H - 13*mm,
                        f"Telefone: {EMPRESA['telefone']}  |  {EMPRESA['site']}")


def _draw_text_fit(canvas, texto, cx, y, max_w, fonte, tam):
    while tam >= 8:
        canvas.setFont(fonte, tam)
        if canvas.stringWidth(texto, fonte, tam) <= max_w:
            break
        tam -= 1
    canvas.drawCentredString(cx, y, texto)


def build(dados: dict) -> list:
    return [CapaPage(dados)]
