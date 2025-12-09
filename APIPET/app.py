from flask import Flask, request, jsonify
from datetime import datetime
import os
import json
import uuid

app = Flask(__name__)

# Caminho relativo para a pasta jsons (um nível acima)
PASTA_JSONS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "jsons")

# Garantir que a pasta jsons existe
os.makedirs(PASTA_JSONS, exist_ok=True)


@app.route('/', methods=['GET'])
def home():
    """Endpoint de boas-vindas"""
    return jsonify({
        "mensagem": "API PET Saúde Digital",
        "status": "online",
        "endpoint": "/receber-json",
        "metodo": "POST"
    }), 200
#ola

@app.route('/receber-json', methods=['POST'])
def receber_json():
    """
    Endpoint que recebe JSON e salva na pasta jsons
    
    Aceita:
    - JSON no body da requisição
    - Content-Type: application/json
    
    Retorna:
    - Status 200 se sucesso
    - Status 400 se erro
    """
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
        
        # Garantir que é um array (formato esperado pelo pdfexportv3.py)
        if isinstance(dados, dict):
            dados = [dados]
        
        # Gerar nome único para o arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        id_unico = str(uuid.uuid4())[:8]
        nome_arquivo = f"entrada_{timestamp}_{id_unico}.json"
        caminho_arquivo = os.path.join(PASTA_JSONS, nome_arquivo)
        
        # Salvar JSON no arquivo
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        
        # Contar quantos pacientes foram recebidos
        num_pacientes = len(dados)
        
        return jsonify({
            "mensagem": "JSON recebido e salvo com sucesso",
            "arquivo": nome_arquivo,
            "caminho": caminho_arquivo,
            "pacientes": num_pacientes,
            "timestamp": timestamp
        }), 200
        
    except json.JSONDecodeError:
        return jsonify({
            "erro": "JSON inválido"
        }), 400
    except Exception as e:
        return jsonify({
            "erro": f"Erro ao processar requisição: {str(e)}"
        }), 500


@app.route('/status', methods=['GET'])
def status():
    """Endpoint para verificar status da API e pasta jsons"""
    try:
        arquivos_json = [f for f in os.listdir(PASTA_JSONS) if f.endswith('.json')]
        return jsonify({
            "status": "online",
            "pasta_jsons": PASTA_JSONS,
            "pasta_existe": os.path.exists(PASTA_JSONS),
            "arquivos_json": len(arquivos_json),
            "ultimos_arquivos": arquivos_json[-5:] if len(arquivos_json) > 0 else []
        }), 200
    except Exception as e:
        return jsonify({
            "erro": f"Erro ao verificar status: {str(e)}"
        }), 500


if __name__ == '__main__':
    print("=" * 50)
    print("API PET Saúde Digital")
    print("=" * 50)
    print(f"Pasta de destino: {PASTA_JSONS}")
    print(f"Endpoint: http://localhost:5000/receber-json")
    print(f"Status: http://localhost:5000/status")
    print("=" * 50)
    print("Servidor iniciando...")
    app.run(host='0.0.0.0', port=5000, debug=True)

