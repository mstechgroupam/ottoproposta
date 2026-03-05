"""Flowable: barra colorida com título de seção."""
from reportlab.platypus.flowables import Flowable
from reportlab.lib.units import mm
from reportlab.lib.colors import white
from pdf.styles import FB


class SectionTitle(Flowable):
    """Barra horizontal colorida com texto branco em maiúsculas."""

    def __init__(self, texto, cor, altura=8*mm, font_size=11,
                 padding_left=5*mm, margem_top=4*mm):
        super().__init__()
        self.texto = texto
        self.cor = cor
        self.altura = altura
        self.font_size = font_size
        self.padding_left = padding_left
        self.margem_top = margem_top

    def wrap(self, available_width, available_height):
        self._larg = available_width
        return (available_width, self.altura + self.margem_top)

    def draw(self):
        c = self.canv
        # Empurra o bloco para baixo pelo margem_top
        y_base = 0
        # Fundo colorido
        c.setFillColor(self.cor)
        c.rect(0, y_base, self._larg, self.altura, fill=1, stroke=0)
        # Texto branco
        c.setFillColor(white)
        c.setFont(FB, self.font_size)
        y_text = y_base + (self.altura - self.font_size) / 2 + 1
        c.drawString(self.padding_left, y_text, self.texto)
