"""
Script para testar a API localmente
Execute: python test-local.py
"""
import json
import sys
import os

# Adicionar o diretório api ao path
api_path = os.path.join(os.path.dirname(__file__), 'api')
sys.path.insert(0, api_path)

# Importar o módulo (o arquivo tem hífen, então importamos diretamente)
import importlib.util
spec = importlib.util.spec_from_file_location("generate_pdf", os.path.join(api_path, "generate-pdf.py"))
generate_pdf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate_pdf)
handler = generate_pdf.handler

# Dados de teste
dados_teste = [
    {
        "nome": "Ana Silva",
        "cpf": "123.456.789-00",
        "sexo": "Feminino",
        "faixa_etaria": "25-34",
        "tipo_usuario": "profissional",
        "data_registro": "2025-11-01 10:30:00",
        "data_inicio_sintomas": "2025-10-28",
        "data_avc": "2025-10-29",
        "tipo_avc": "Isquêmico",
        "admissao_janela_terapeutica": "Sim",
        "trombolise": "Sim",
        "trombectomia": "Não",
        "medicamentos_utilizados": "AAS, Clopidogrel",
        "ventilacao_mecanica": "Não",
        "tempo_ventilacao": "",
        "intubado": "Não",
        "traqueostomizado": "Não",
        "sequelas": "Leve déficit motor braço direito",
        "desfecho": "Alta",
        "alta_medicamento": "Sim",
        "alta_medicamento_qual": "AAS",
        "grau_parentesco": "",
        "cuidador_externo": "",
        "tempo_chegada_hospital": "",
        "comorbidades": "Hipertensão",
        "historico_familiar": "Pai com AVC",
        "medicamento_uso_diario": "Sim",
        "medicamento_uso_diario_qual": "Losartana",
        "alimentacao": "Equilibrada",
        "atividade_fisica": "2x/semana",
        "tabagismo": "Não",
        "alcool": "Socialmente",
        "uso_medicamentos": "",
        "uso_medicamentos_qual": ""
    }
]

# Simular requisição
class MockRequest:
    def __init__(self, method='POST', body=None):
        self.method = method
        self.body = json.dumps(body) if body else None
        self.json = body

if __name__ == "__main__":
    import sys
    import io
    # Ajustar encoding para Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print("Testando API localmente...")
    print("-" * 50)
    
    # Criar requisição mock
    req = MockRequest('POST', dados_teste)
    
    # Chamar handler
    try:
        response = handler(req)
        
        print(f"Status Code: {response['statusCode']}")
        print(f"Headers: {response['headers']}")
        print("-" * 50)
        
        # Parse da resposta
        body = json.loads(response['body'])
        
        if body.get('success'):
            print(f"[OK] {body['message']}")
            print(f"PDFs gerados: {len(body['pdfs'])}")
            for pdf in body['pdfs']:
                print(f"   - {pdf['nome']} ({pdf['paciente']})")
                if 'caminho' in pdf:
                    print(f"     Salvo em: {pdf['caminho']}")
                if 'caminho_relativo' in pdf:
                    print(f"     Caminho relativo: {pdf['caminho_relativo']}")
                print(f"     Tamanho base64: {len(pdf['pdf_base64'])} caracteres")
        else:
            print(f"[ERRO] {body.get('error', 'Erro desconhecido')}")
            if 'message' in body:
                print(f"   Detalhes: {body['message']}")
    
    except Exception as e:
        print(f"[ERRO] Erro ao executar teste: {e}")
        import traceback
        traceback.print_exc()

