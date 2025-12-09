import pandas as pd
from pandas import json_normalize
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, HRFlowable
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import os
import json
import time


pasta_entrada = r"jsons"
logo_path = r"art/logoPET.png"


def carregar_dados(arquivo):
    extensao = os.path.splitext(arquivo)[1].lower()
    if extensao == ".csv":
        df = pd.read_csv(arquivo)
    elif extensao == ".json":
        try:
            df = pd.read_json(arquivo)
        except ValueError:
            with open(arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
            df = json_normalize(dados)
    else:
        raise ValueError("Formato não suportado. Use CSV ou JSON.")
    return df

def preencher_faltantes(df):
    for coluna in df.columns:
        df[coluna] = df[coluna].fillna(" Campo não preenchido")
    return df

def gerar_pdf_formulario(paciente, pasta_saida, logo_path):
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    nome_pdf_base = f"{paciente['nome'].replace(' ', '_')}_{paciente['cpf'].replace('.', '').replace('-', '')}.pdf"
    caminho_pdf = os.path.join(pasta_saida, nome_pdf_base)

    if os.path.exists(caminho_pdf):
        hora_atual = datetime.now().strftime("%H%M%S")
        nome_pdf_base = f"{paciente['nome'].replace(' ', '_')}_{paciente['cpf'].replace('.', '').replace('-', '')}_{hora_atual}.pdf"
        caminho_pdf = os.path.join(pasta_saida, nome_pdf_base)

    doc = SimpleDocTemplate(caminho_pdf, pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
    styles = getSampleStyleSheet()
    story = []

    if os.path.exists(logo_path):
        img = Image(logo_path)
        img.drawHeight = 80
        img.drawWidth = 80
        img.hAlign = "CENTER"
        story.append(img)
        story.append(Spacer(1, 12))

    titulo_principal = Paragraph("<b>PET Saúde Digital - Ficha do Paciente</b>", ParagraphStyle(
        name="TituloPrincipal", fontSize=18, alignment=1, textColor=colors.HexColor("#1583c9"), spaceAfter=12))
    story.append(titulo_principal)

    story.append(Paragraph(f"<b>Nome:</b> {paciente['nome']}", styles["Normal"]))
    story.append(Paragraph(f"<b>CPF:</b> {paciente['cpf']}", styles["Normal"]))
    story.append(Spacer(1, 12))

    secao_style = ParagraphStyle(name="secao", fontSize=12, leading=14, spaceAfter=6, textColor=colors.HexColor("#1583c9"))
    campo_style = ParagraphStyle(name="campo", fontSize=10, leading=12, spaceAfter=4)

    def bloco(titulo, campos):
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1583c9"), spaceBefore=6, spaceAfter=6, hAlign='CENTER'))
        story.append(Paragraph(f"<b>{titulo}</b>", secao_style))
        story.append(Spacer(1, 2))
        for label, valor in campos.items():
            story.append(Paragraph(f"<b>{label}:</b> {valor}", campo_style))
        story.append(Spacer(1, 8))

    bloco("Identificação Básica", {
        "Sexo": paciente["sexo"],
        "Faixa Etária": paciente["faixa_etaria"],
        "Tipo de Usuário": paciente["tipo_usuario"],
        "Data de Registro": paciente["data_registro"]
    })

    bloco("Dados Clínicos Gerais", {
        "Data Início Sintomas": paciente["data_inicio_sintomas"],
        "Data AVC": paciente["data_avc"],
        "Tipo de AVC": paciente["tipo_avc"],
        "Admissão Janela Terapêutica": paciente["admissao_janela_terapeutica"],
        "Trombolise": paciente["trombolise"],
        "Trombectomia": paciente["trombectomia"]
    })

    bloco("Medicamentos e Intervenções", {
        "Medicamentos Utilizados": paciente["medicamentos_utilizados"],
        "Ventilação Mecânica": paciente["ventilacao_mecanica"],
        "Tempo de Ventilação": paciente["tempo_ventilacao"],
        "Intubado": paciente["intubado"],
        "Traqueostomizado": paciente["traqueostomizado"]
    })

    bloco("Sequelas e Desfecho", {
        "Sequelas": paciente["sequelas"],
        "Desfecho": paciente["desfecho"],
        "Alta com Medicamento": paciente["alta_medicamento"],
        "Qual Medicamento": paciente["alta_medicamento_qual"]
    })

    bloco("Parente / Acompanhante", {
        "Grau de Parentesco": paciente["grau_parentesco"],
        "Cuidador Externo": paciente["cuidador_externo"],
        "Tempo Chegada ao Hospital": paciente["tempo_chegada_hospital"]
    })

    bloco("Fatores de Risco e Comorbidades", {
        "Comorbidades": paciente["comorbidades"],
        "Histórico Familiar": paciente["historico_familiar"],
        "Medicamento de Uso Diário": paciente["medicamento_uso_diario"],
        "Qual Medicamento": paciente["medicamento_uso_diario_qual"]
    })

    bloco("Hábitos Alimentares e Estilo de Vida", {
        "Alimentação": paciente["alimentacao"],
        "Atividade Física": paciente["atividade_fisica"],
        "Tabagismo": paciente["tabagismo"],
        "Álcool": paciente["alcool"],
        "Uso de Medicamentos (Acompanhante)": paciente["uso_medicamentos"],
        "Quais Medicamentos": paciente["uso_medicamentos_qual"]
    })

    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1F497D"), spaceBefore=12, spaceAfter=6, hAlign='CENTER'))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Relatório gerado automaticamente pelo PET Saúde Digital.", styles["Normal"]))

    doc.build(story)
    print(f"PDF gerado: {caminho_pdf}")


class NovoArquivoHandler(FileSystemEventHandler):
    def __init__(self, pasta_saida):
        self.pasta_saida = pasta_saida

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".json"):
            arquivo = event.src_path
            print(f"\nNovo arquivo detectado: {arquivo}")
            try:
                df = carregar_dados(arquivo)
                df = preencher_faltantes(df)
                for _, paciente in df.iterrows():
                    gerar_pdf_formulario(paciente, self.pasta_saida, logo_path)
            except Exception as e:
                print(f"Erro ao processar {arquivo}: {e}")


if __name__ == "__main__":
    os.makedirs(pasta_entrada, exist_ok=True)
    data_atual = datetime.now().strftime("%Y-%m-%d")
    pasta_saida = os.path.join("pdf", data_atual)
    os.makedirs(pasta_saida, exist_ok=True)

    print(f"Monitorando a pasta '{pasta_entrada}' para novos arquivos JSON...\n")

    event_handler = NovoArquivoHandler(pasta_saida)
    observer = Observer()
    observer.schedule(event_handler, pasta_entrada, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nMonitoramento encerrado.")

    observer.join()
