"""Configurações da empresa Otto Energia Solar."""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminhos de recursos estáticos
STATIC_DIR   = os.path.join(BASE_DIR, "static")
FONTS_DIR    = os.path.join(STATIC_DIR, "fonts")
IMG_DIR      = os.path.join(STATIC_DIR, "img")

FONT_REGULAR = os.path.join(FONTS_DIR, "DejaVuSans.ttf")
FONT_BOLD    = os.path.join(FONTS_DIR, "DejaVuSans-Bold.ttf")

IMG_LOGO_HEADER    = os.path.join(IMG_DIR, "logo_otto.png")
IMG_LOGO_CAPA      = os.path.join(IMG_DIR, "logo_capa.png")
IMG_PAINEIS_FOTO   = os.path.join(IMG_DIR, "paineis_foto.jpg")
IMG_DIAGRAMA       = os.path.join(IMG_DIR, "diagrama_sistema.png")
IMG_FLUXO          = os.path.join(IMG_DIR, "fluxo_energia.png")
IMG_COMPONENTES    = os.path.join(IMG_DIR, "componentes_painel.jpg")

# Dados fixos da empresa
EMPRESA = {
    "nome":     "OTTO ENERGIA SOLAR",
    "endereco": "R. David José Tadros, 134 - Conj. Res. Jardim Belvedere - Planalto, Manaus - AM - CEP 69044-090",
    "telefone": "(92) 99333-7677",
    "site":     "www.ottoenergiasolar.com.br",
    "email":    "contato@ottoenergiasolar.com.br",
}
