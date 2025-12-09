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
    
    # Garantir que todos os valores são strings e tratar None/vazios
    for key, value in paciente_completo.items():
        if value is None:
            paciente_completo[key] = " Campo não preenchido"
        elif not isinstance(value, str):
            paciente_completo[key] = str(value) if value else " Campo não preenchido"
        elif value.strip() == "":
            paciente_completo[key] = " Campo não preenchido"
    
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
    if LOGO_PATH and isinstance(LOGO_PATH, str) and os.path.exists(LOGO_PATH):
        try:
            img = Image(LOGO_PATH)
            img.drawHeight = 80
            img.drawWidth = 80
            img.hAlign = "CENTER"
            story.append(img)
            story.append(Spacer(1, 12))
        except Exception as e:
            # Logo não pôde ser carregado, continuar sem logo
            print(f"Aviso: Não foi possível carregar logo de {LOGO_PATH}: {e}")
    elif LOGO_BASE64 and isinstance(LOGO_BASE64, str):
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
        except Exception as e:
            # Logo base64 não pôde ser decodificado, continuar sem logo
            print(f"Aviso: Não foi possível decodificar logo base64: {e}")
    
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
    
    # Nome e CPF (garantir que são strings)
    nome = str(paciente.get('nome', 'Nome não informado'))
    cpf = str(paciente.get('cpf', 'CPF não informado'))
    story.append(Paragraph(f"<b>Nome:</b> {nome}", styles["Normal"]))
    story.append(Paragraph(f"<b>CPF:</b> {cpf}", styles["Normal"]))
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
    
    # Blocos de informações (garantir que todos os valores são strings)
    def get_str_value(key, default=" Campo não preenchido"):
        value = paciente.get(key, default)
        if value is None:
            return default
        return str(value) if value else default
    
    bloco("Identificação Básica", {
        "Sexo": get_str_value("sexo"),
        "Faixa Etária": get_str_value("faixa_etaria"),
        "Tipo de Usuário": get_str_value("tipo_usuario"),
        "Data de Registro": get_str_value("data_registro")
    })
    
    bloco("Dados Clínicos Gerais", {
        "Data Início Sintomas": get_str_value("data_inicio_sintomas"),
        "Data AVC": get_str_value("data_avc"),
        "Tipo de AVC": get_str_value("tipo_avc"),
        "Admissão Janela Terapêutica": get_str_value("admissao_janela_terapeutica"),
        "Trombolise": get_str_value("trombolise"),
        "Trombectomia": get_str_value("trombectomia")
    })
    
    bloco("Medicamentos e Intervenções", {
        "Medicamentos Utilizados": get_str_value("medicamentos_utilizados"),
        "Ventilação Mecânica": get_str_value("ventilacao_mecanica"),
        "Tempo de Ventilação": get_str_value("tempo_ventilacao"),
        "Intubado": get_str_value("intubado"),
        "Traqueostomizado": get_str_value("traqueostomizado")
    })
    
    bloco("Sequelas e Desfecho", {
        "Sequelas": get_str_value("sequelas"),
        "Desfecho": get_str_value("desfecho"),
        "Alta com Medicamento": get_str_value("alta_medicamento"),
        "Qual Medicamento": get_str_value("alta_medicamento_qual")
    })
    
    bloco("Parente / Acompanhante", {
        "Grau de Parentesco": get_str_value("grau_parentesco"),
        "Cuidador Externo": get_str_value("cuidador_externo"),
        "Tempo Chegada ao Hospital": get_str_value("tempo_chegada_hospital")
    })
    
    bloco("Fatores de Risco e Comorbidades", {
        "Comorbidades": get_str_value("comorbidades"),
        "Histórico Familiar": get_str_value("historico_familiar"),
        "Medicamento de Uso Diário": get_str_value("medicamento_uso_diario"),
        "Qual Medicamento": get_str_value("medicamento_uso_diario_qual")
    })
    
    bloco("Hábitos Alimentares e Estilo de Vida", {
        "Alimentação": get_str_value("alimentacao"),
        "Atividade Física": get_str_value("atividade_fisica"),
        "Tabagismo": get_str_value("tabagismo"),
        "Álcool": get_str_value("alcool"),
        "Uso de Medicamentos (Acompanhante)": get_str_value("uso_medicamentos"),
        "Quais Medicamentos": get_str_value("uso_medicamentos_qual")
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
                
                # Nome do arquivo (sanitizar para evitar caracteres inválidos)
                nome_paciente = str(paciente.get('nome', 'Paciente')).replace(' ', '_').replace('/', '_').replace('\\', '_')
                cpf_paciente = str(paciente.get('cpf', '00000000000')).replace('.', '').replace('-', '').replace(' ', '')
                nome_pdf = f"{nome_paciente}_{cpf_paciente}.pdf"
                
                pdfs_gerados.append({
                    "nome": nome_pdf,
                    "bytes": pdf_bytes,
                    "paciente": str(paciente.get('nome', 'Paciente'))
                })
            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                return jsonify({
                    "erro": f"Erro ao gerar PDF para {paciente.get('nome', 'paciente desconhecido')}: {str(e)}",
                    "detalhes": error_details if os.environ.get("DEBUG", "False") == "True" else None
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
        
    except json.JSONDecodeError as e:
        return jsonify({
            "erro": f"JSON inválido: {str(e)}"
        }), 400
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return jsonify({
            "erro": f"Erro ao processar requisição: {str(e)}",
            "detalhes": error_details if os.environ.get("DEBUG", "False") == "True" else None
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
