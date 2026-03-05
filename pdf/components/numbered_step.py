"""Flowable: círculo numerado + título + descrição (passos/etapas)."""
from reportlab.platypus.flowables import Flowable
from reportlab.lib.units import mm
from reportlab.lib.colors import white
from reportlab.platypus import Paragraph
from pdf.styles import FB, F, PASSO_TITULO, PASSO_DESC, AZUL


class NumberedStep(Flowable):
    """
    ●(N)  Título do Passo
           Descrição curta do passo aqui.
    """

    def __init__(self, numero, titulo, descricao,
                 cor_circulo=None, raio=6*mm,
                 espaco_apos=3*mm):
        super().__init__()
        self.numero = str(numero)
        self.titulo = titulo
        self.descricao = descricao
        self.cor_circulo = cor_circulo or AZUL
        self.raio = raio
        self.espaco_apos = espaco_apos
        self._titulo_p = None
        self._desc_p = None

    def wrap(self, available_width, available_height):
        self._larg = available_width
        r = self.raio
        texto_x = r * 2 + 4*mm
        texto_w = available_width - texto_x

        self._titulo_p = Paragraph(self.titulo, PASSO_TITULO)
        tw, th = self._titulo_p.wrap(texto_w, 999)

        self._desc_p = Paragraph(self.descricao, PASSO_DESC)
        dw, dh = self._desc_p.wrap(texto_w, 999)

        self._th = th
        self._dh = dh
        self._texto_x = texto_x
        total = max(r * 2, th + dh + 2*mm) + self.espaco_apos
        self._altura = total
        return (available_width, total)

    def draw(self):
        c = self.canv
        r = self.raio
        total_h = self._altura - self.espaco_apos

        # Círculo
        cx = r
        cy = total_h / 2
        c.setFillColor(self.cor_circulo)
        c.circle(cx, cy, r, fill=1, stroke=0)

        # Número
        c.setFillColor(white)
        c.setFont(FB, 11)
        c.drawCentredString(cx, cy - 4, self.numero)

        # Título e descrição
        text_y_base = total_h / 2 - (self._th + self._dh + 2*mm) / 2
        c.translate(self._texto_x, text_y_base + self._dh + 2*mm)
        self._titulo_p.drawOn(c, 0, 0)
        c.translate(0, -(self._dh + 2*mm))
        self._desc_p.drawOn(c, 0, 0)
