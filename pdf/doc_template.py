"""BaseDocTemplate com PageTemplates para capa e páginas de conteúdo."""
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from pdf.components.header_footer import decorar_pagina_conteudo

_W, _H = A4

MAR_ESQ = 18*mm
MAR_DIR = 18*mm
MAR_SUP = 19*mm   # barra azul 13mm + acento 1.5mm + gap 4.5mm
MAR_INF = 22*mm   # espaço para o rodapé


class PropostaTemplate(BaseDocTemplate):
    def __init__(self, buffer, dados: dict):
        super().__init__(
            buffer,
            pagesize=A4,
            leftMargin=MAR_ESQ,
            rightMargin=MAR_DIR,
            topMargin=MAR_SUP,
            bottomMargin=MAR_INF,
        )
        self.dados = dados
        self._setup_templates()

    def _setup_templates(self):
        # Frame para a capa (sem margens — conteúdo desenhado manualmente no canvas)
        frame_capa = Frame(
            0, 0, _W, _H,
            leftPadding=0, rightPadding=0,
            topPadding=0, bottomPadding=0,
            id="capa"
        )
        # Frame padrão para as páginas de conteúdo
        frame_conteudo = Frame(
            MAR_ESQ,
            MAR_INF,
            _W - MAR_ESQ - MAR_DIR,
            _H - MAR_SUP - MAR_INF,
            leftPadding=0, rightPadding=0,
            topPadding=0, bottomPadding=0,
            id="conteudo"
        )
        self.addPageTemplates([
            PageTemplate(id="capa",     frames=[frame_capa],
                         onPage=self._on_capa),
            PageTemplate(id="conteudo", frames=[frame_conteudo],
                         onPage=decorar_pagina_conteudo),
        ])

    def _on_capa(self, canvas, doc):
        """Callback da capa — desenho feito dentro do flowable CapaPage."""
        pass
