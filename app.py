"""App Flask — Gerador de Propostas Comerciais Otto Energia Solar."""
import io
import re
from datetime import date, timedelta

from flask import Flask, render_template, request, send_file, jsonify

from pdf.builder import build_proposal_pdf

app = Flask(__name__)


# ── Rotas ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    hoje = date.today()
    validade = hoje + timedelta(days=30)
    defaults = {
        "numero": "001",
        "data_emissao": hoje.strftime("%Y-%m-%d"),
        "data_validade": validade.strftime("%Y-%m-%d"),
        "tipo_cliente": "Residencial",
    }
    return render_template("form.html", defaults=defaults)


@app.route("/gerar-pdf", methods=["POST"])
def gerar_pdf():
    dados = _extrair_dados(request.form)
    dados = _calcular_ambiental(dados)

    buffer = io.BytesIO()
    build_proposal_pdf(buffer, dados)
    buffer.seek(0)

    slug = re.sub(r"[^a-zA-Z0-9]", "_", dados.get("nome_cliente", "cliente"))
    nome_arquivo = f"Proposta_OTTO-{dados['numero']}_{slug}.pdf"

    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=nome_arquivo,
    )


@app.route("/calcular", methods=["POST"])
def calcular():
    """Retorna campos calculados para preview ao vivo no formulário."""
    try:
        kwp = float(request.form.get("potencia_kwp", 0))
        eco = float(request.form.get("economia_mensal", 0))
        inv = float(request.form.get("investimento_total", 0))
        dados = {"potencia_kwp": kwp, "economia_mensal": eco,
                 "investimento_total": inv}
        dados = _calcular_ambiental(dados)
        return jsonify({
            "geracao_kwh_ano": int(dados["geracao_kwh_ano"]),
            "co2_ano": dados["co2_ano"],
            "arvores": int(dados["arvores"]),
            "projecao_1":  _fmt(eco * 12),
            "projecao_5":  _fmt(eco * 12 * 5),
            "projecao_10": _fmt(eco * 12 * 10),
            "projecao_25": _fmt(eco * 12 * 25),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ── Auxiliares ────────────────────────────────────────────────────────────────

def _extrair_dados(form) -> dict:
    def _float(k, default=0.0):
        try:
            return float(form.get(k, default) or default)
        except (ValueError, TypeError):
            return float(default)

    def _int(k, default=0):
        try:
            return int(form.get(k, default) or default)
        except (ValueError, TypeError):
            return int(default)

    # Formata datas de YYYY-MM-DD para DD/MM/YYYY
    def _fmt_data(k):
        raw = form.get(k, "")
        try:
            d = date.fromisoformat(raw)
            return d.strftime("%d/%m/%Y")
        except Exception:
            return raw

    return {
        # Metadados
        "numero":         form.get("numero", "001").zfill(4),
        "data_emissao":   _fmt_data("data_emissao"),
        "data_validade":  _fmt_data("data_validade"),
        # Cliente
        "nome_cliente":   (form.get("nome_cliente") or "").upper().strip(),
        "endereco":       form.get("endereco", ""),
        "telefone":       form.get("telefone", ""),
        "email":          form.get("email", ""),
        "tipo_cliente":   form.get("tipo_cliente", "Residencial"),
        # Sistema
        "consumo_kwh":    _float("consumo_kwh"),
        "potencia_kwp":   _float("potencia_kwp"),
        "qtd_paineis":    _int("qtd_paineis"),
        "modelo_painel":  form.get("modelo_painel", ""),
        "modelo_inversor": form.get("modelo_inversor", ""),
        # Financeiro
        "investimento_total": _float("investimento_total"),
        "economia_mensal":    _float("economia_mensal"),
        "payback_meses":      _int("payback_meses"),
        "forma_pagamento":    form.get("forma_pagamento", "À vista"),
    }


def _calcular_ambiental(dados: dict) -> dict:
    """Calcula CO₂ evitado, árvores equivalentes e geração anual."""
    kwp = dados.get("potencia_kwp", 0)
    geracao_ano = kwp * 4.5 * 0.80 * 365          # kWh/ano
    co2_ano     = geracao_ano * 0.0817 / 1000     # toneladas (fator MCTIC)
    arvores     = co2_ano * 1000 / 22             # cada árvore absorve ~22 kg/ano

    dados["geracao_kwh_ano"] = round(geracao_ano, 0)
    dados["co2_ano"]         = round(co2_ano, 2)
    dados["arvores"]         = round(arvores, 0)
    return dados


def _fmt(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
