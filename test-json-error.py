"""
Teste para verificar o tratamento de JSON com dados extras
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

# Simular requisição com JSON malformado (com dados extras)
class MockRequest:
    def __init__(self, method='POST', body=None):
        self.method = method
        self.body = body if isinstance(body, str) else json.dumps(body) if body else None
        self.json = body if not isinstance(body, str) else None

# Teste 1: JSON válido
print("Teste 1: JSON válido")
print("-" * 50)
dados_validos = [{"nome": "Teste", "cpf": "123.456.789-00", "sexo": "Feminino"}]
req1 = MockRequest('POST', json.dumps(dados_validos))
response1 = handler(req1)
print(f"Status: {response1['statusCode']}")
body1 = json.loads(response1['body'])
print(f"Resultado: {body1.get('success', body1.get('error'))}")
print()

# Teste 2: JSON com dados extras (simulando o erro)
print("Teste 2: JSON com dados extras")
print("-" * 50)
json_com_extras = json.dumps(dados_validos) + "\n{\"extra\": \"dados\"}"
req2 = MockRequest('POST', json_com_extras)
response2 = handler(req2)
print(f"Status: {response2['statusCode']}")
body2 = json.loads(response2['body'])
print(f"Resultado: {body2.get('error', body2.get('success'))}")
if 'message' in body2:
    print(f"Mensagem: {body2['message']}")
print()

# Teste 3: JSON com múltiplos objetos separados
print("Teste 3: Múltiplos objetos JSON")
print("-" * 50)
json_multiplo = json.dumps(dados_validos) + json.dumps([{"nome": "Outro", "cpf": "999.999.999-99"}])
req3 = MockRequest('POST', json_multiplo)
response3 = handler(req3)
print(f"Status: {response3['statusCode']}")
body3 = json.loads(response3['body'])
print(f"Resultado: {body3.get('error', body3.get('success'))}")
if 'message' in body3:
    print(f"Mensagem: {body3['message']}")

