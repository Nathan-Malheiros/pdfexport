# 🚀 Como Rodar a API

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

1. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

## 🧪 Opção 1: Teste Rápido (Sem Servidor)

Teste direto sem precisar de servidor HTTP:

```bash
python test-local.py
```

Isso vai:
- ✅ Processar dados de teste
- ✅ Gerar PDF em memória
- ✅ Mostrar resultado no console

## 🌐 Opção 2: Servidor Local (Recomendado)

Para testar como uma API real:

```bash
python server-local.py
```

O servidor vai iniciar em: **http://localhost:8000**

### Testar a API

**Com curl:**
```bash
curl -X POST http://localhost:8000/api/generate-pdf \
  -H "Content-Type: application/json" \
  -d @jsons/entrada.json
```

**Com PowerShell (Windows):**
```powershell
$body = Get-Content jsons/entrada.json -Raw
Invoke-RestMethod -Uri http://localhost:8000/api/generate-pdf -Method POST -Body $body -ContentType "application/json"
```

**Com JavaScript (no navegador):**
```javascript
fetch('http://localhost:8000/api/generate-pdf', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify([{
    "nome": "Ana Silva",
    "cpf": "123.456.789-00",
    // ... outros campos
  }])
})
.then(res => res.json())
.then(data => console.log(data));
```

## ☁️ Opção 3: Deploy no Vercel

### Passo a passo:

1. **Instale o Vercel CLI:**
```bash
npm install -g vercel
```

2. **Faça login:**
```bash
vercel login
```

3. **No diretório do projeto, execute:**
```bash
vercel
```

4. **Siga as instruções:**
   - Escolha o projeto (ou crie um novo)
   - Confirme as configurações
   - Aguarde o deploy

5. **Você receberá uma URL como:**
   ```
   https://seu-projeto.vercel.app/api/generate-pdf
   ```

### Deploy Automático (GitHub)

1. Crie um repositório no GitHub
2. Faça push do código
3. No Vercel Dashboard, conecte o repositório
4. O deploy será automático a cada push!

## 📝 Exemplo de Uso

### Requisição:
```json
POST /api/generate-pdf
Content-Type: application/json

[
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
```

### Resposta:
```json
{
  "success": true,
  "message": "1 PDF(s) gerado(s) com sucesso",
  "pdfs": [
    {
      "nome": "Ana_Silva_12345678900.pdf",
      "paciente": "Ana Silva",
      "cpf": "123.456.789-00",
      "pdf_base64": "JVBERi0xLjQKJeLjz9MKMy..."
    }
  ]
}
```

## ❓ Problemas Comuns

### Erro: "ModuleNotFoundError"
**Solução:** Instale as dependências:
```bash
pip install -r requirements.txt
```

### Erro: "Port already in use"
**Solução:** Mude a porta no `server-local.py` (linha com `port = 8000`)

### Erro no Vercel: "Build failed"
**Solução:** Verifique se o `requirements.txt` está correto e todas as dependências estão listadas.

## 🎯 Próximos Passos

1. Teste localmente com `server-local.py`
2. Teste com seus dados reais
3. Faça deploy no Vercel
4. Use a URL da API em outras aplicações!

