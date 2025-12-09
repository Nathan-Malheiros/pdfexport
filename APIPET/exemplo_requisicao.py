"""
Exemplo de como usar a API PET Saúde Digital
Execute este arquivo após iniciar o servidor (python app.py)
A API agora gera PDF automaticamente!
"""

import requests
import json
import os

# URL da API (local ou Vercel)
url_local = "http://localhost:5000/api/receber-json"
url_vercel = "https://pdfexport-ten.vercel.app/api/receber-json"

# Escolha qual URL usar
url = url_local  # Mude para url_vercel para testar no Vercel

# Dados de exemplo (um paciente)
dados_paciente = [
    {
        "nome": "Maria Silva",
        "cpf": "123.456.789-00",
        "sexo": "Feminino",
        "faixa_etaria": "30-39 anos",
        "tipo_usuario": "Paciente",
        "data_registro": "2025-12-09",
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
        "alta_medicamento_qual": "AAS 100mg",
        "grau_parentesco": "Esposa",
        "cuidador_externo": "Sim",
        "tempo_chegada_hospital": "1 hora",
        "comorbidades": "Hipertensão",
        "historico_familiar": "Pai com AVC",
        "medicamento_uso_diario": "Sim",
        "medicamento_uso_diario_qual": "Losartana",
        "alimentacao": "Equilibrada",
        "atividade_fisica": "3x/semana",
        "tabagismo": "Não",
        "alcool": "Socialmente",
        "uso_medicamentos": "Não",
        "uso_medicamentos_qual": ""
    }
]

if __name__ == "__main__":
    try:
        print("=" * 50)
        print("Enviando dados para a API...")
        print(f"URL: {url}")
        print(f"Pacientes: {len(dados_paciente)}")
        print("=" * 50)
        
        # Enviar requisição POST
        response = requests.post(url, json=dados_paciente)
        
        # Verificar resposta
        if response.status_code == 200:
            # Verificar se é PDF ou ZIP
            content_type = response.headers.get('Content-Type', '')
            
            if 'application/pdf' in content_type:
                # É um PDF único
                nome_arquivo = response.headers.get('Content-Disposition', '').split('filename=')[-1].strip('"')
                if not nome_arquivo:
                    nome_arquivo = f"paciente_{dados_paciente[0]['nome'].replace(' ', '_')}.pdf"
                
                # Criar pasta de saída
                pasta_saida = "pdfs_gerados"
                os.makedirs(pasta_saida, exist_ok=True)
                caminho_arquivo = os.path.join(pasta_saida, nome_arquivo)
                
                # Salvar PDF
                with open(caminho_arquivo, 'wb') as f:
                    f.write(response.content)
                
                print("\n✅ PDF gerado com sucesso!")
                print(f"Arquivo salvo: {caminho_arquivo}")
                print(f"Tamanho: {len(response.content)} bytes")
                
            elif 'application/zip' in content_type:
                # É um ZIP com múltiplos PDFs
                nome_arquivo = response.headers.get('Content-Disposition', '').split('filename=')[-1].strip('"')
                if not nome_arquivo:
                    nome_arquivo = "pacientes.zip"
                
                # Criar pasta de saída
                pasta_saida = "pdfs_gerados"
                os.makedirs(pasta_saida, exist_ok=True)
                caminho_arquivo = os.path.join(pasta_saida, nome_arquivo)
                
                # Salvar ZIP
                with open(caminho_arquivo, 'wb') as f:
                    f.write(response.content)
                
                print("\n✅ ZIP com PDFs gerado com sucesso!")
                print(f"Arquivo salvo: {caminho_arquivo}")
                print(f"Tamanho: {len(response.content)} bytes")
                print(f"Contém {len(dados_paciente)} PDF(s)")
            else:
                # Resposta JSON (erro ou formato inesperado)
                try:
                    resultado = response.json()
                    print("\n✅ Sucesso!")
                    print(json.dumps(resultado, indent=2, ensure_ascii=False))
                except:
                    print("\n✅ Resposta recebida (formato não reconhecido)")
                    print(f"Content-Type: {content_type}")
                    print(f"Tamanho: {len(response.content)} bytes")
        else:
            print(f"\n❌ Erro {response.status_code}")
            try:
                erro = response.json()
                print(json.dumps(erro, indent=2, ensure_ascii=False))
            except:
                print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor.")
        print("Certifique-se de que o servidor está rodando (python app.py)")
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
