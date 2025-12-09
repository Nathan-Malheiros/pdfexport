from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
from datetime import datetime
from io import BytesIO
import os
import json
import uuid
import zipfile
import base64

# Imports para geração de PDF
import pandas as pd
from pandas import json_normalize
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, HRFlowable
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Caminho do logo (se disponível)
# No Vercel, podemos usar uma URL ou base64 do logo
LOGO_PATH = os.environ.get('LOGO_PATH', None)
LOGO_BASE64 = os.environ.get('LOGO_BASE64', None)


def preencher_faltantes_dict(paciente):
    """Preenche campos faltantes em um dicionário de paciente"""
    campos_padrao = {
        "sexo": " Campo não preenchido",
        "faixa_etaria": " Campo não preenchido",
        "tipo_usuario": " Campo não preenchido",
        "data_registro": " Campo não preenchido",
        "data_inicio_sintomas": " Campo não preenchido",
        "data_avc": " Campo não preenchido",
        "tipo_avc": " Campo não preenchido",
        "admissao_janela_terapeutica": " Campo não preenchido",
        "trombolise": " Campo não preenchido",
        "trombectomia": " Campo não preenchido",
        "medicamentos_utilizados": " Campo não preenchido",
        "ventilacao_mecanica": " Campo não preenchido",
        "tempo_ventilacao": " Campo não preenchido",
        "intubado": " Campo não preenchido",
        "traqueostomizado": " Campo não preenchido",
        "sequelas": " Campo não preenchido",
        "desfecho": " Campo não preenchido",
        "alta_medicamento": " Campo não preenchido",
        "alta_medicamento_qual": " Campo não preenchido",
        "grau_parentesco": " Campo não preenchido",
        "cuidador_externo": " Campo não preenchido",
        "tempo_chegada_hospital": " Campo não preenchido",
        "comorbidades": " Campo não preenchido",
        "historico_familiar": " Campo não preenchido",
        "medicamento_uso_diario": " Campo não preenchido",
        "medicamento_uso_diario_qual": " Campo não preenchido",
        "alimentacao": " Campo não preenchido",
        "atividade_fisica": " Campo não preenchido",
        "tabagismo": " Campo não preenchido",
        "alcool": " Campo não preenchido",
        "uso_medicamentos": " Campo não preenchido",
        "uso_medicamentos_qual": " Campo não preenchido"
    }
    
    paciente_completo = campos_padrao.copy()
    paciente_completo.update(paciente)
    return paciente_completo


def gerar_pdf_formulario_memoria(paciente):
    """
    Gera PDF do formulário do paciente em memória
    Retorna bytes do PDF
    """
    # Preencher campos faltantes
    paciente = preencher_faltantes_dict(paciente)
    
    # Criar buffer em memória
    buffer = BytesIO()
    
    # Criar documento PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    styles = getSampleStyleSheet()
    story = []
    
    # Adicionar logo se disponível
    if LOGO_PATH and os.path.exists(LOGO_PATH):
        try:
            img = Image(LOGO_PATH)
            img.drawHeight = 80
            img.drawWidth = 80
            img.hAlign = "CENTER"
            story.append(img)
            story.append(Spacer(1, 12))
        except:
            pass
    elif LOGO_BASE64:
        try:
            # Decodificar logo base64
            logo_data = base64.b64decode(LOGO_BASE64)
            logo_buffer = BytesIO(logo_data)
            img = Image(logo_buffer)
            img.drawHeight = 80
            img.drawWidth = 80
            img.hAlign = "CENTER"
            story.append(img)
            story.append(Spacer(1, 12))
        except:
            pass
    
    # Título principal
    titulo_principal = Paragraph(
        "<b>PET Saúde Digital - Ficha do Paciente</b>",
        ParagraphStyle(
            name="TituloPrincipal",
            fontSize=18,
            alignment=1,
            textColor=colors.HexColor("#1583c9"),
            spaceAfter=12
        )
    )
    story.append(titulo_principal)
    
    # Nome e CPF
    story.append(Paragraph(f"<b>Nome:</b> {paciente['nome']}", styles["Normal"]))
    story.append(Paragraph(f"<b>CPF:</b> {paciente['cpf']}", styles["Normal"]))
    story.append(Spacer(1, 12))
    
    # Estilos
    secao_style = ParagraphStyle(
        name="secao",
        fontSize=12,
        leading=14,
        spaceAfter=6,
        textColor=colors.HexColor("#1583c9")
    )
    campo_style = ParagraphStyle(
        name="campo",
        fontSize=10,
        leading=12,
        spaceAfter=4
    )
    
    def bloco(titulo, campos):
        story.append(HRFlowable(
            width="100%",
            thickness=1,
            color=colors.HexColor("#1583c9"),
            spaceBefore=6,
            spaceAfter=6,
            hAlign='CENTER'
        ))
        story.append(Paragraph(f"<b>{titulo}</b>", secao_style))
        story.append(Spacer(1, 2))
        for label, valor in campos.items():
            story.append(Paragraph(f"<b>{label}:</b> {valor}", campo_style))
        story.append(Spacer(1, 8))
    
    # Blocos de informações
    bloco("Identificação Básica", {
        "Sexo": paciente.get("sexo", " Campo não preenchido"),
        "Faixa Etária": paciente.get("faixa_etaria", " Campo não preenchido"),
        "Tipo de Usuário": paciente.get("tipo_usuario", " Campo não preenchido"),
        "Data de Registro": paciente.get("data_registro", " Campo não preenchido")
    })
    
    bloco("Dados Clínicos Gerais", {
        "Data Início Sintomas": paciente.get("data_inicio_sintomas", " Campo não preenchido"),
        "Data AVC": paciente.get("data_avc", " Campo não preenchido"),
        "Tipo de AVC": paciente.get("tipo_avc", " Campo não preenchido"),
        "Admissão Janela Terapêutica": paciente.get("admissao_janela_terapeutica", " Campo não preenchido"),
        "Trombolise": paciente.get("trombolise", " Campo não preenchido"),
        "Trombectomia": paciente.get("trombectomia", " Campo não preenchido")
    })
    
    bloco("Medicamentos e Intervenções", {
        "Medicamentos Utilizados": paciente.get("medicamentos_utilizados", " Campo não preenchido"),
        "Ventilação Mecânica": paciente.get("ventilacao_mecanica", " Campo não preenchido"),
        "Tempo de Ventilação": paciente.get("tempo_ventilacao", " Campo não preenchido"),
        "Intubado": paciente.get("intubado", " Campo não preenchido"),
        "Traqueostomizado": paciente.get("traqueostomizado", " Campo não preenchido")
    })
    
    bloco("Sequelas e Desfecho", {
        "Sequelas": paciente.get("sequelas", " Campo não preenchido"),
        "Desfecho": paciente.get("desfecho", " Campo não preenchido"),
        "Alta com Medicamento": paciente.get("alta_medicamento", " Campo não preenchido"),
        "Qual Medicamento": paciente.get("alta_medicamento_qual", " Campo não preenchido")
    })
    
    bloco("Parente / Acompanhante", {
        "Grau de Parentesco": paciente.get("grau_parentesco", " Campo não preenchido"),
        "Cuidador Externo": paciente.get("cuidador_externo", " Campo não preenchido"),
        "Tempo Chegada ao Hospital": paciente.get("tempo_chegada_hospital", " Campo não preenchido")
    })
    
    bloco("Fatores de Risco e Comorbidades", {
        "Comorbidades": paciente.get("comorbidades", " Campo não preenchido"),
        "Histórico Familiar": paciente.get("historico_familiar", " Campo não preenchido"),
        "Medicamento de Uso Diário": paciente.get("medicamento_uso_diario", " Campo não preenchido"),
        "Qual Medicamento": paciente.get("medicamento_uso_diario_qual", " Campo não preenchido")
    })
    
    bloco("Hábitos Alimentares e Estilo de Vida", {
        "Alimentação": paciente.get("alimentacao", " Campo não preenchido"),
        "Atividade Física": paciente.get("atividade_fisica", " Campo não preenchido"),
        "Tabagismo": paciente.get("tabagismo", " Campo não preenchido"),
        "Álcool": paciente.get("alcool", " Campo não preenchido"),
        "Uso de Medicamentos (Acompanhante)": paciente.get("uso_medicamentos", " Campo não preenchido"),
        "Quais Medicamentos": paciente.get("uso_medicamentos_qual", " Campo não preenchido")
    })
    
    # Rodapé
    story.append(HRFlowable(
        width="100%",
        thickness=1,
        color=colors.HexColor("#1F497D"),
        spaceBefore=12,
        spaceAfter=6,
        hAlign='CENTER'
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Relatório gerado automaticamente pelo PET Saúde Digital.", styles["Normal"]))
    
    # Construir PDF
    doc.build(story)
    
    # Obter bytes do PDF
    buffer.seek(0)
    return buffer.getvalue()


@app.route('/', methods=['GET'])
def home():
    """Endpoint de boas-vindas"""
    return jsonify({
        "mensagem": "API PET Saúde Digital",
        "status": "online",
        "endpoint": "/api/receber-json",
        "metodo": "POST",
        "plataforma": "Vercel",
        "funcionalidade": "Recebe JSON e gera PDF automaticamente"
    }), 200


@app.route('/api/receber-json', methods=['POST', 'OPTIONS'])
def receber_json():
    """
    Endpoint que recebe JSON e gera PDF automaticamente
    
    Aceita:
    - JSON no body da requisição
    - Content-Type: application/json
    
    Retorna:
    - PDF único se um paciente
    - ZIP com múltiplos PDFs se vários pacientes
    - Status 400 se erro
    """
    # Tratar OPTIONS (preflight CORS)
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        # Verificar se há dados JSON no request
        if not request.is_json:
            return jsonify({
                "erro": "Content-Type deve ser application/json"
            }), 400
        
        # Obter dados JSON
        dados = request.get_json()
        
        if not dados:
            return jsonify({
                "erro": "Nenhum dado JSON foi enviado"
            }), 400
        
        # Validar se é um array ou objeto
        if not isinstance(dados, (list, dict)):
            return jsonify({
                "erro": "JSON deve ser um objeto ou array"
            }), 400
        
        # Garantir que é um array
        if isinstance(dados, dict):
            dados = [dados]
        
        # Validar campos obrigatórios
        for paciente in dados:
            if not isinstance(paciente, dict):
                return jsonify({
                    "erro": "Cada item do array deve ser um objeto"
                }), 400
            if "nome" not in paciente or "cpf" not in paciente:
                return jsonify({
                    "erro": "Campos 'nome' e 'cpf' são obrigatórios"
                }), 400
        
        # Gerar PDFs para cada paciente
        pdfs_gerados = []
        
        for paciente in dados:
            try:
                # Gerar PDF em memória
                pdf_bytes = gerar_pdf_formulario_memoria(paciente)
                
                # Nome do arquivo
                nome_pdf = f"{paciente['nome'].replace(' ', '_')}_{paciente['cpf'].replace('.', '').replace('-', '')}.pdf"
                
                pdfs_gerados.append({
                    "nome": nome_pdf,
                    "bytes": pdf_bytes,
                    "paciente": paciente['nome']
                })
            except Exception as e:
                return jsonify({
                    "erro": f"Erro ao gerar PDF para {paciente.get('nome', 'paciente desconhecido')}: {str(e)}"
                }), 500
        
        # Se houver apenas um PDF, retornar diretamente
        if len(pdfs_gerados) == 1:
            pdf_data = pdfs_gerados[0]
            return Response(
                pdf_data["bytes"],
                mimetype='application/pdf',
                headers={
                    'Content-Disposition': f'attachment; filename="{pdf_data["nome"]}"',
                    'Access-Control-Allow-Origin': '*'
                }
            )
        
        # Se houver múltiplos PDFs, criar ZIP
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for pdf_data in pdfs_gerados:
                zip_file.writestr(pdf_data["nome"], pdf_data["bytes"])
        
        zip_buffer.seek(0)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_nome = f"pacientes_{timestamp}.zip"
        
        return Response(
            zip_buffer.getvalue(),
            mimetype='application/zip',
            headers={
                'Content-Disposition': f'attachment; filename="{zip_nome}"',
                'Access-Control-Allow-Origin': '*'
            }
        )
        
    except json.JSONDecodeError:
        return jsonify({
            "erro": "JSON inválido"
        }), 400
    except Exception as e:
        return jsonify({
            "erro": f"Erro ao processar requisição: {str(e)}"
        }), 500


@app.route('/api/status', methods=['GET'])
def status():
    """Endpoint para verificar status da API"""
    return jsonify({
        "status": "online",
        "plataforma": "Vercel Serverless",
        "ambiente": os.environ.get("VERCEL_ENV", "production"),
        "funcionalidade": "Geração automática de PDFs a partir de JSON"
    }), 200


if __name__ == '__main__':
    print("=" * 50)
    print("API PET Saúde Digital")
    print("=" * 50)
    print(f"Endpoint: http://localhost:5000/api/receber-json")
    print(f"Status: http://localhost:5000/api/status")
    print("=" * 50)
    print("Servidor iniciando...")
    app.run(host='0.0.0.0', port=5000, debug=True)
