"""
Script para testar usando um arquivo JSON
Uso: python teste-com-json.py [caminho-do-json]
Exemplo: python teste-com-json.py jsons/entrada.json
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

# Simular requisição
class MockRequest:
    def __init__(self, method='POST', body=None):
        self.method = method
        self.body = json.dumps(body) if body else None
        self.json = body

if __name__ == "__main__":
    import io
    # Ajustar encoding para Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    # Pegar arquivo JSON do argumento ou usar padrão
    if len(sys.argv) > 1:
        arquivo_json = sys.argv[1]
    else:
        arquivo_json = "jsons/entrada.json"
    
    if not os.path.exists(arquivo_json):
        print(f"[ERRO] Arquivo não encontrado: {arquivo_json}")
        print(f"Uso: python teste-com-json.py [caminho-do-json]")
        sys.exit(1)
    
    print("=" * 60)
    print("TESTE COM ARQUIVO JSON")
    print("=" * 60)
    print(f"Arquivo: {arquivo_json}")
    print("-" * 60)
    
    # Carregar JSON
    try:
        with open(arquivo_json, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        if not isinstance(dados, list):
            dados = [dados]
        
        print(f"Pacientes encontrados: {len(dados)}")
        print("-" * 60)
        
        # Criar requisição mock
        req = MockRequest('POST', dados)
        
        # Chamar handler
        response = handler(req)
        
        print(f"Status Code: {response['statusCode']}")
        print("-" * 60)
        
        # Parse da resposta
        body = json.loads(response['body'])
        
        if body.get('success'):
            print(f"[OK] {body['message']}")
            print()
            for i, pdf in enumerate(body['pdfs'], 1):
                print(f"{i}. {pdf['nome']}")
                print(f"   Paciente: {pdf['paciente']}")
                print(f"   CPF: {pdf['cpf']}")
                print(f"   Salvo em: {pdf['caminho_relativo']}")
                
                # Verificar se arquivo existe
                if os.path.exists(pdf['caminho']):
                    tamanho = os.path.getsize(pdf['caminho'])
                    print(f"   Tamanho: {tamanho:,} bytes ({tamanho/1024:.2f} KB)")
                print()
            
            print(f"[OK] Todos os PDFs foram gerados e salvos!")
        else:
            print(f"[ERRO] {body.get('error', 'Erro desconhecido')}")
            if 'message' in body:
                print(f"   Detalhes: {body['message']}")
    
    except json.JSONDecodeError as e:
        print(f"[ERRO] Erro ao ler JSON: {e}")
    except Exception as e:
        print(f"[ERRO] Erro ao executar teste: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)

