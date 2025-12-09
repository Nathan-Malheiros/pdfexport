import json
import os
import sys
from datetime import datetime
import pandas as pd
from pandas import json_normalize
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, HRFlowable
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import base64
import io

# Caminho do logo (ajustar para Vercel)
logo_path = os.path.join(os.path.dirname(__file__), "..", "art", "logoPET.png")
# Caminho da pasta PDF
pasta_pdf_base = os.path.join(os.path.dirname(__file__), "..", "PDF")

def preencher_faltantes(df):
    for coluna in df.columns:
        df[coluna] = df[coluna].fillna(" Campo não preenchido")
    return df

def gerar_pdf_formulario(paciente, logo_path):
    """Gera PDF em memória e retorna como base64"""
    buffer = io.BytesIO()
    
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
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
        "Sexo": paciente.get("sexo", ""),
        "Faixa Etária": paciente.get("faixa_etaria", ""),
        "Tipo de Usuário": paciente.get("tipo_usuario", ""),
        "Data de Registro": paciente.get("data_registro", "")
    })

    bloco("Dados Clínicos Gerais", {
        "Data Início Sintomas": paciente.get("data_inicio_sintomas", ""),
        "Data AVC": paciente.get("data_avc", ""),
        "Tipo de AVC": paciente.get("tipo_avc", ""),
        "Admissão Janela Terapêutica": paciente.get("admissao_janela_terapeutica", ""),
        "Trombolise": paciente.get("trombolise", ""),
        "Trombectomia": paciente.get("trombectomia", "")
    })

    bloco("Medicamentos e Intervenções", {
        "Medicamentos Utilizados": paciente.get("medicamentos_utilizados", ""),
        "Ventilação Mecânica": paciente.get("ventilacao_mecanica", ""),
        "Tempo de Ventilação": paciente.get("tempo_ventilacao", ""),
        "Intubado": paciente.get("intubado", ""),
        "Traqueostomizado": paciente.get("traqueostomizado", "")
    })

    bloco("Sequelas e Desfecho", {
        "Sequelas": paciente.get("sequelas", ""),
        "Desfecho": paciente.get("desfecho", ""),
        "Alta com Medicamento": paciente.get("alta_medicamento", ""),
        "Qual Medicamento": paciente.get("alta_medicamento_qual", "")
    })

    bloco("Parente / Acompanhante", {
        "Grau de Parentesco": paciente.get("grau_parentesco", ""),
        "Cuidador Externo": paciente.get("cuidador_externo", ""),
        "Tempo Chegada ao Hospital": paciente.get("tempo_chegada_hospital", "")
    })

    bloco("Fatores de Risco e Comorbidades", {
        "Comorbidades": paciente.get("comorbidades", ""),
        "Histórico Familiar": paciente.get("historico_familiar", ""),
        "Medicamento de Uso Diário": paciente.get("medicamento_uso_diario", ""),
        "Qual Medicamento": paciente.get("medicamento_uso_diario_qual", "")
    })

    bloco("Hábitos Alimentares e Estilo de Vida", {
        "Alimentação": paciente.get("alimentacao", ""),
        "Atividade Física": paciente.get("atividade_fisica", ""),
        "Tabagismo": paciente.get("tabagismo", ""),
        "Álcool": paciente.get("alcool", ""),
        "Uso de Medicamentos (Acompanhante)": paciente.get("uso_medicamentos", ""),
        "Quais Medicamentos": paciente.get("uso_medicamentos_qual", "")
    })

    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1F497D"), spaceBefore=12, spaceAfter=6, hAlign='CENTER'))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Relatório gerado automaticamente pelo PET Saúde Digital.", styles["Normal"]))

    doc.build(story)
    buffer.seek(0)
    return buffer

def parse_json_safely(json_str):
    """
    Tenta parsear JSON de forma segura, lidando com dados extras
    """
    if not json_str or not isinstance(json_str, str):
        return None
    
    json_str = json_str.strip()
    if not json_str:
        return None
    
    # Tentativa 1: Parse direto
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        # Tentativa 2: Se houver erro de posição, tentar até a posição do erro
        if e.pos:
            try:
                # Pegar até onde o JSON é válido
                partial = json_str[:e.pos].strip()
                # Remover caracteres extras no final
                while partial and partial[-1] in [',', '\n', '\r', ' ', '\t']:
                    partial = partial[:-1]
                # Tentar parsear novamente
                if partial:
                    return json.loads(partial)
            except:
                pass
        
        # Tentativa 3: Procurar por arrays ou objetos JSON completos
        # Se começar com [, procurar o ] correspondente
        if json_str.startswith('['):
            try:
                bracket_count = 0
                for i, char in enumerate(json_str):
                    if char == '[':
                        bracket_count += 1
                    elif char == ']':
                        bracket_count -= 1
                        if bracket_count == 0:
                            return json.loads(json_str[:i+1])
            except:
                pass
        
        # Tentativa 4: Se começar com {, procurar o } correspondente
        if json_str.startswith('{'):
            try:
                brace_count = 0
                for i, char in enumerate(json_str):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            # Se for um objeto único, converter para array
                            obj = json.loads(json_str[:i+1])
                            return [obj] if isinstance(obj, dict) else obj
            except:
                pass
        
        # Se nada funcionou, relançar o erro original
        raise e

def handler(req):
    """Handler principal da API serverless para Vercel"""
    try:
        # Verificar método HTTP
        method = req.method if hasattr(req, 'method') else req.get('httpMethod', 'GET')
        
        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': ''
            }
        
        if method != 'POST':
            return {
                'statusCode': 405,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({
                    'error': 'Método não permitido. Use POST.'
                })
            }

        # Obter dados do body
        body = {}
        try:
            if hasattr(req, 'json') and req.json:
                body = req.json
            elif hasattr(req, 'body'):
                if isinstance(req.body, str):
                    body = parse_json_safely(req.body)
                else:
                    body = req.body
            elif isinstance(req, dict) and 'body' in req:
                if isinstance(req['body'], str):
                    body = parse_json_safely(req['body'])
                else:
                    body = req['body']
        except json.JSONDecodeError as e:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'JSON inválido',
                    'message': f'Erro ao parsear JSON: {str(e)}',
                    'dica': 'Verifique se o JSON está bem formatado. Se houver múltiplos objetos JSON, envie como um array único.'
                }, ensure_ascii=False)
            }
        except Exception as e:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Erro ao processar body',
                    'message': str(e)
                }, ensure_ascii=False)
            }

        if not body:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'JSON inválido ou vazio'
                })
            }

        # Converter para DataFrame
        if isinstance(body, list):
            df = pd.DataFrame(body)
        elif isinstance(body, dict):
            df = pd.DataFrame([body])
        else:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Formato de dados inválido. Esperado array ou objeto JSON.'
                })
            }

        # Preencher campos faltantes
        df = preencher_faltantes(df)

        # Criar pasta PDF se não existir
        pasta_pdf = os.path.abspath(pasta_pdf_base)
        os.makedirs(pasta_pdf, exist_ok=True)

        # Gerar PDFs para cada paciente
        pdfs_gerados = []
        for _, paciente in df.iterrows():
            pdf_buffer = gerar_pdf_formulario(paciente.to_dict(), logo_path)
            
            # Nome do arquivo
            nome_pdf = f"{paciente['nome'].replace(' ', '_')}_{paciente['cpf'].replace('.', '').replace('-', '')}.pdf"
            
            # Caminho completo do arquivo
            caminho_pdf = os.path.join(pasta_pdf, nome_pdf)
            
            # Se o arquivo já existir, adicionar timestamp
            if os.path.exists(caminho_pdf):
                hora_atual = datetime.now().strftime("%H%M%S")
                nome_base = f"{paciente['nome'].replace(' ', '_')}_{paciente['cpf'].replace('.', '').replace('-', '')}"
                nome_pdf = f"{nome_base}_{hora_atual}.pdf"
                caminho_pdf = os.path.join(pasta_pdf, nome_pdf)
            
            # Salvar PDF em arquivo
            pdf_buffer.seek(0)
            with open(caminho_pdf, 'wb') as f:
                f.write(pdf_buffer.read())
            
            # Converter para base64 também (para manter compatibilidade)
            pdf_buffer.seek(0)
            pdf_base64 = base64.b64encode(pdf_buffer.read()).decode('utf-8')
            
            pdfs_gerados.append({
                'nome': nome_pdf,
                'paciente': paciente['nome'],
                'cpf': paciente['cpf'],
                'caminho': caminho_pdf,
                'caminho_relativo': os.path.join('PDF', nome_pdf),
                'pdf_base64': pdf_base64
            })

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': True,
                'message': f'{len(pdfs_gerados)} PDF(s) gerado(s) com sucesso',
                'pdfs': pdfs_gerados
            }, ensure_ascii=False)
        }

    except Exception as e:
        import traceback
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Erro ao processar requisição',
                'message': str(e),
                'traceback': traceback.format_exc()
            }, ensure_ascii=False)
        }

