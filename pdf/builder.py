"""Orquestrador: monta a story completa e chama multiBuild."""
from reportlab.platypus import NextPageTemplate, PageBreak
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from pdf.doc_template import PropostaTemplate
from pdf.styles import registrar_fontes, AZUL, FB
from pdf.pages import (p01_capa, p02_dados_specs, p03_como_funciona,
                        p04_fluxo_energia, p05_componentes, p06_sobre_empresa,
                        p07_investimento, p08_garantias, p09_faq_ambiental,
                        p10_etapas_termos)

_W, _H = A4


class NumberedCanvas(rl_canvas.Canvas):
    """Canvas que adiciona 'Página X de Y' em todas as páginas de conteúdo."""

    def __init__(self, *args, **kwargs):
        rl_canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            # Pagina 1 é a capa, sem numeração
            if self._pageNumber > 1:
                self._draw_page_number(num_pages)
            rl_canvas.Canvas.showPage(self)
        rl_canvas.Canvas.save(self)

    def _draw_page_number(self, total):
        self.saveState()
        self.setFont(FB, 8)
        self.setFillColor(AZUL)
        self.drawRightString(
            _W - 15*mm, 10*mm,
            f"Pagina {self._pageNumber} de {total}"
        )
        self.restoreState()


def build_proposal_pdf(buffer, dados: dict) -> None:
    """Gera o PDF completo e escreve em `buffer`."""
    registrar_fontes()

    doc = PropostaTemplate(buffer, dados)
    story = []

    # Página 1 — Capa (usa template sem margens)
    story += [NextPageTemplate("capa")]
    story += p01_capa.build(dados)

    # Páginas de conteúdo
    story += [PageBreak(), NextPageTemplate("conteudo")]
    story += p02_dados_specs.build(dados)

    story += [PageBreak()]
    story += p03_como_funciona.build(dados)

    story += [PageBreak()]
    story += p04_fluxo_energia.build(dados)

    story += [PageBreak()]
    story += p05_componentes.build(dados)

    story += [PageBreak()]
    story += p06_sobre_empresa.build(dados)

    story += [PageBreak()]
    story += p07_investimento.build(dados)

    story += [PageBreak()]
    story += p08_garantias.build(dados)

    story += [PageBreak()]
    story += p09_faq_ambiental.build(dados)

    story += [PageBreak()]
    story += p10_etapas_termos.build(dados)

    doc.multiBuild(story, canvasmaker=NumberedCanvas)
