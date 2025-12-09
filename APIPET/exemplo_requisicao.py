"""
Exemplo de como usar a API PET Saúde Digital
Execute este arquivo após iniciar o servidor (python app.py)
"""

import requests
import json

# URL da API
url = "http://localhost:5000/receber-json"

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
        print("Enviando dados para a API...")
        print(f"URL: {url}")
        print(f"Pacientes: {len(dados_paciente)}")
        
        # Enviar requisição POST
        response = requests.post(url, json=dados_paciente)
        
        # Verificar resposta
        if response.status_code == 200:
            resultado = response.json()
            print("\n✅ Sucesso!")
            print(f"Mensagem: {resultado['mensagem']}")
            print(f"Arquivo salvo: {resultado['arquivo']}")
            print(f"Pacientes processados: {resultado['pacientes']}")
        else:
            print(f"\n❌ Erro {response.status_code}")
            print(response.json())
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor.")
        print("Certifique-se de que o servidor está rodando (python app.py)")
    except Exception as e:
        print(f"❌ Erro: {e}")

