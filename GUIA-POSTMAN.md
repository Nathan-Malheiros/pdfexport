# 📮 Guia Completo - Testar API com Postman

## 🚀 Passo a Passo

### 1️⃣ Iniciar o Servidor Local

**Primeiro, abra um terminal e execute:**

```bash
python server-local.py
```

Você verá:
```
🚀 Servidor rodando em http://localhost:8000
📡 Endpoint: http://localhost:8000/api/generate-pdf
```

**Deixe este terminal aberto!**

---

### 2️⃣ Abrir o Postman

1. Abra o Postman (se não tiver, baixe em: https://www.postman.com/downloads/)
2. Clique em **"New"** → **"HTTP Request"**

---

### 3️⃣ Configurar a Requisição

#### Método e URL
- **Método:** Selecione **POST** no dropdown
- **URL:** Digite: `http://localhost:8000/api/generate-pdf`

#### Headers
1. Clique na aba **"Headers"**
2. Adicione:
   - **Key:** `Content-Type`
   - **Value:** `application/json`

#### Body
1. Clique na aba **"Body"**
2. Selecione **"raw"**
3. No dropdown ao lado, selecione **"JSON"**
4. Cole o JSON abaixo:

```json
[
  {
    "nome": "Maria Santos",
    "cpf": "111.222.333-44",
    "sexo": "Feminino",
    "faixa_etaria": "35-44",
    "tipo_usuario": "profissional",
    "data_registro": "2025-12-09 15:00:00",
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
]
```

---

### 4️⃣ Enviar a Requisição

1. Clique no botão **"Send"** (laranja)
2. Aguarde a resposta

---

### 5️⃣ Verificar a Resposta

Você verá algo assim:

```json
{
  "success": true,
  "message": "1 PDF(s) gerado(s) com sucesso",
  "pdfs": [
    {
      "nome": "Maria_Santos_11122233344.pdf",
      "paciente": "Maria Santos",
      "cpf": "111.222.333-44",
      "caminho": "C:\\...\\pdfexport\\PDF\\Maria_Santos_11122233344.pdf",
      "caminho_relativo": "PDF/Maria_Santos_11122233344.pdf",
      "pdf_base64": "..."
    }
  ]
}
```

---

### 6️⃣ Verificar o PDF Gerado

O PDF foi salvo automaticamente na pasta `PDF/` do projeto!

**Para verificar:**
- Abra a pasta `PDF/` no seu projeto
- Procure pelo arquivo: `Maria_Santos_11122233344.pdf`

---

## 📸 Visual do Postman

```
┌─────────────────────────────────────────────────┐
│ POST  http://localhost:8000/api/generate-pdf   │
├─────────────────────────────────────────────────┤
│ [Params] [Authorization] [Headers] [Body] [Pre-│
│                                                  │
│ Headers:                                        │
│ Content-Type: application/json                  │
│                                                  │
│ Body:                                           │
│ ○ none  ○ form-data  ○ x-www-form-urlencoded    │
│ ● raw   ○ binary     ○ GraphQL                 │
│                                                  │
│ [JSON ▼]                                        │
│                                                  │
│ [  {                                            │
│     "nome": "Maria Santos",                     │
│     "cpf": "111.222.333-44",                    │
│     ...                                         │
│   }                                             │
│ ]                                               │
│                                                  │
│                    [Send]                       │
└─────────────────────────────────────────────────┘
```

---

## 🎯 Testar Múltiplos Pacientes

Para gerar PDFs de vários pacientes de uma vez, envie um array com múltiplos objetos:

```json
[
  {
    "nome": "Paciente 1",
    "cpf": "111.111.111-11",
    ...
  },
  {
    "nome": "Paciente 2",
    "cpf": "222.222.222-22",
    ...
  },
  {
    "nome": "Paciente 3",
    "cpf": "333.333.333-33",
    ...
  }
]
```

---

## 💾 Salvar Requisição no Postman

Para não precisar configurar toda vez:

1. Clique em **"Save"** (ao lado de Send)
2. Dê um nome: `Gerar PDF - API Local`
3. Escolha uma Collection (ou crie uma nova)
4. Clique em **"Save"**

Agora você pode reutilizar essa requisição sempre que quiser!

---

## 🔧 Troubleshooting

### Erro: "Could not get any response"
- ✅ Verifique se o servidor está rodando (`python server-local.py`)
- ✅ Verifique se a URL está correta: `http://localhost:8000/api/generate-pdf`

### Erro: "JSON inválido"
- ✅ Verifique se selecionou **"raw"** e **"JSON"** no Body
- ✅ Verifique se o JSON está bem formatado (sem vírgulas extras, chaves fechadas, etc.)

### Status 405 (Method Not Allowed)
- ✅ Certifique-se de que o método está como **POST** (não GET)

### Status 400 (Bad Request)
- ✅ Verifique se o JSON tem pelo menos `nome` e `cpf`
- ✅ Verifique se todos os campos estão presentes (mesmo que vazios)

---

## 📋 Template Rápido (Copiar e Colar)

```json
[
  {
    "nome": "SEU NOME AQUI",
    "cpf": "000.000.000-00",
    "sexo": "Feminino",
    "faixa_etaria": "25-34",
    "tipo_usuario": "profissional",
    "data_registro": "2025-12-09 15:00:00",
    "data_inicio_sintomas": "2025-12-01",
    "data_avc": "2025-12-02",
    "tipo_avc": "Isquêmico",
    "admissao_janela_terapeutica": "Sim",
    "trombolise": "Sim",
    "trombectomia": "Não",
    "medicamentos_utilizados": "AAS",
    "ventilacao_mecanica": "Não",
    "tempo_ventilacao": "",
    "intubado": "Não",
    "traqueostomizado": "Não",
    "sequelas": "",
    "desfecho": "Alta",
    "alta_medicamento": "Sim",
    "alta_medicamento_qual": "AAS",
    "grau_parentesco": "",
    "cuidador_externo": "",
    "tempo_chegada_hospital": "",
    "comorbidades": "",
    "historico_familiar": "",
    "medicamento_uso_diario": "",
    "medicamento_uso_diario_qual": "",
    "alimentacao": "",
    "atividade_fisica": "",
    "tabagismo": "",
    "alcool": "",
    "uso_medicamentos": "",
    "uso_medicamentos_qual": ""
  }
]
```

---

## ✅ Checklist Rápido

Antes de enviar, verifique:

- [ ] Servidor rodando (`python server-local.py`)
- [ ] Método: **POST**
- [ ] URL: `http://localhost:8000/api/generate-pdf`
- [ ] Header: `Content-Type: application/json`
- [ ] Body: **raw** + **JSON**
- [ ] JSON válido (pelo menos `nome` e `cpf`)

---

## 🎉 Pronto!

Agora você pode testar quantos pacientes quiser pelo Postman!

**Dica:** Salve a requisição para usar sempre que precisar testar novos cadastros.

