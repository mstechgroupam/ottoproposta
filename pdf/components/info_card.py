"""Flowable: card com fundo colorido e borda arredondada."""
from reportlab.platypus.flowables import Flowable
from reportlab.platypus import Paragraph
from reportlab.lib.units import mm
from pdf.styles import CINZA, CINZA_BORDA, BRANCO


class InfoCard(Flowable):
    """Card com fundo e texto interno."""

    def __init__(self, conteudo_flowables, cor_fundo=None,
                 cor_borda=None, padding=4*mm, raio=2*mm,
                 margem_apos=3*mm):
        super().__init__()
        self.flowables = conteudo_flowables
        self.cor_fundo = cor_fundo or CINZA
        self.cor_borda = cor_borda or CINZA_BORDA
        self.padding = padding
        self.raio = raio
        self.margem_apos = margem_apos

    def wrap(self, available_width, available_height):
        self._larg = available_width
        inner_w = available_width - 2 * self.padding
        total_h = self.padding

        self._wrapped = []
        for fl in self.flowables:
            w, h = fl.wrap(inner_w, 9999)
            self._wrapped.append((fl, w, h))
            total_h += h + 1.5*mm

        total_h += self.padding
        self._inner_h = total_h
        return (available_width, total_h + self.margem_apos)

    def draw(self):
        c = self.canv
        h = self._inner_h
        # Fundo
        c.setFillColor(self.cor_fundo)
        c.setStrokeColor(self.cor_borda)
        c.setLineWidth(0.5)
        c.roundRect(0, 0, self._larg, h, self.raio, fill=1, stroke=1)

        # Conteúdo interno
        y = h - self.padding
        for fl, w, fh in self._wrapped:
            y -= fh
            c.saveState()
            c.translate(self.padding, y)
            fl.drawOn(c, 0, 0)
            c.restoreState()
            y -= 1.5*mm
