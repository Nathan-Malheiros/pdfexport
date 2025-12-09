"""
Script para testar com um novo paciente
Modifique os dados abaixo e execute: python teste-novo-paciente.py
"""
import json
import sys
import os
import importlib.util

# Adicionar o diretório api ao path
api_path = os.path.join(os.path.dirname(__file__), 'api')
sys.path.insert(0, api_path)

# Importar o módulo
spec = importlib.util.spec_from_file_location("generate_pdf", os.path.join(api_path, "generate-pdf.py"))
generate_pdf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate_pdf)
handler = generate_pdf.handler

# ============================================
# MODIFIQUE OS DADOS AQUI PARA TESTAR
# ============================================
novo_paciente = {
    "nome": "Seu Nome Aqui",
    "cpf": "000.000.000-00",
    "sexo": "Feminino",
    "faixa_etaria": "25-34",
    "tipo_usuario": "profissional",
    "data_registro": "2025-12-09 14:00:00",
    "data_inicio_sintomas": "2025-12-01",
    "data_avc": "2025-12-02",
    "tipo_avc": "Isquêmico",
    "admissao_janela_terapeutica": "Sim",
    "trombolise": "Sim",
    "trombectomia": "Não",
    "medicamentos_utilizados": "AAS, Clopidogrel",
    "ventilacao_mecanica": "Não",
    "tempo_ventilacao": "",
    "intubado": "Não",
    "traqueostomizado": "Não",
    "sequelas": "Nenhuma",
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
    "atividade_fisica": "3x/semana",
    "tabagismo": "Não",
    "alcool": "Socialmente",
    "uso_medicamentos": "",
    "uso_medicamentos_qual": ""
}

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
    
    print("=" * 60)
    print("TESTE DE NOVO PACIENTE")
    print("=" * 60)
    print(f"Paciente: {novo_paciente['nome']}")
    print(f"CPF: {novo_paciente['cpf']}")
    print("-" * 60)
    
    # Criar requisição mock
    req = MockRequest('POST', [novo_paciente])
    
    # Chamar handler
    try:
        response = handler(req)
        
        print(f"Status Code: {response['statusCode']}")
        print("-" * 60)
        
        # Parse da resposta
        body = json.loads(response['body'])
        
        if body.get('success'):
            print(f"[OK] {body['message']}")
            print()
            for pdf in body['pdfs']:
                print(f"PDF Gerado:")
                print(f"  Nome: {pdf['nome']}")
                print(f"  Paciente: {pdf['paciente']}")
                print(f"  CPF: {pdf['cpf']}")
                print(f"  Caminho: {pdf['caminho']}")
                print(f"  Caminho Relativo: {pdf['caminho_relativo']}")
                print()
            
            # Verificar se arquivo existe
            caminho_pdf = body['pdfs'][0]['caminho']
            if os.path.exists(caminho_pdf):
                tamanho = os.path.getsize(caminho_pdf)
                print(f"[OK] Arquivo salvo com sucesso!")
                print(f"     Tamanho: {tamanho:,} bytes ({tamanho/1024:.2f} KB)")
            else:
                print(f"[AVISO] Arquivo não encontrado em: {caminho_pdf}")
        else:
            print(f"[ERRO] {body.get('error', 'Erro desconhecido')}")
            if 'message' in body:
                print(f"   Detalhes: {body['message']}")
    
    except Exception as e:
        print(f"[ERRO] Erro ao executar teste: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)

