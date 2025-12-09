from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
import json
import uuid

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# No Vercel, não podemos salvar arquivos localmente
# Vamos usar uma variável de ambiente para configurar webhook ou retornar dados processados
WEBHOOK_URL = os.environ.get('WEBHOOK_URL', None)


@app.route('/', methods=['GET'])
def home():
    """Endpoint de boas-vindas"""
    return jsonify({
        "mensagem": "API PET Saúde Digital",
        "status": "online",
        "endpoint": "/api/receber-json",
        "metodo": "POST",
        "plataforma": "Vercel"
    }), 200
#ola

@app.route('/api/receber-json', methods=['POST', 'OPTIONS'])
def receber_json():
    """
    Endpoint que recebe JSON e processa dados de pacientes
    
    Aceita:
    - JSON no body da requisição
    - Content-Type: application/json
    
    Retorna:
    - Status 200 se sucesso
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
        #h
        # Garantir que é um array (formato esperado pelo pdfexportv3.py)
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
        
        # Gerar nome único para o arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        id_unico = str(uuid.uuid4())[:8]
        nome_arquivo = f"entrada_{timestamp}_{id_unico}.json"
        num_pacientes = len(dados)
        
        # No Vercel serverless, não podemos salvar arquivos localmente
        # Retornamos os dados processados para que possam ser salvos pelo cliente
        # ou enviados via webhook
        
        resposta = {
            "mensagem": "JSON recebido e processado com sucesso",
            "arquivo_sugerido": nome_arquivo,
            "pacientes": num_pacientes,
            "timestamp": timestamp,
            "dados_processados": dados,
            "nota": "No ambiente Vercel serverless, os dados são retornados. Use um webhook ou salve localmente."
        }
        
        # Se houver webhook configurado, enviar dados (opcional)
        if WEBHOOK_URL:
            try:
                import requests
                requests.post(WEBHOOK_URL, json=dados, timeout=5)
                resposta["webhook_enviado"] = True
            except:
                resposta["webhook_enviado"] = False
        
        return jsonify(resposta), 200
        
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
        "nota": "Funções serverless não mantêm estado. Arquivos não podem ser salvos localmente."
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
