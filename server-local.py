"""
Servidor local simples para testar a API
Execute: python server-local.py
Acesse: http://localhost:8000/api/generate-pdf
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
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

class APIHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/generate-pdf':
            # Ler body
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            
            # Criar objeto request mock
            class Request:
                def __init__(self, method, body_data):
                    self.method = method
                    try:
                        self.body = body_data.decode('utf-8')
                        self.json = json.loads(self.body)
                    except:
                        self.body = body_data.decode('utf-8')
                        self.json = {}
            
            req = Request('POST', body)
            
            # Processar
            try:
                response = handler(req)
                
                # Enviar resposta
                self.send_response(response['statusCode'])
                for key, value in response['headers'].items():
                    self.send_header(key, value)
                self.end_headers()
                self.wfile.write(response['body'].encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = json.dumps({
                    'error': 'Erro interno do servidor',
                    'message': str(e)
                })
                self.wfile.write(error_response.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {format % args}")

if __name__ == "__main__":
    port = 8000
    server = HTTPServer(('localhost', port), APIHandler)
    print(f"🚀 Servidor rodando em http://localhost:{port}")
    print(f"📡 Endpoint: http://localhost:{port}/api/generate-pdf")
    print("Pressione Ctrl+C para parar")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor parado")
        server.shutdown()

