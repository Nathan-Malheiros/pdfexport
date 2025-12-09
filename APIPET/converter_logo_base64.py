"""
Script para converter o logo para base64
Útil para configurar no Vercel como variável de ambiente
"""

import base64
import os

# Caminho do logo (ajuste se necessário)
logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "art", "logoPET.png")

if os.path.exists(logo_path):
    with open(logo_path, 'rb') as f:
        logo_data = f.read()
        logo_base64 = base64.b64encode(logo_data).decode('utf-8')
    
    print("=" * 50)
    print("Logo convertido para base64!")
    print("=" * 50)
    print("\nCopie o valor abaixo e adicione como variável de ambiente LOGO_BASE64 no Vercel:")
    print("=" * 50)
    print(logo_base64)
    print("=" * 50)
    print(f"\nTamanho original: {len(logo_data)} bytes")
    print(f"Tamanho base64: {len(logo_base64)} caracteres")
else:
    print(f"❌ Logo não encontrado em: {logo_path}")

