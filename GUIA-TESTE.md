# 🧪 Guia de Teste - API PDF Export

Este guia mostra como testar a API com novos cadastros de pacientes.

## 📋 Índice

1. [Teste Local Rápido](#teste-local-rápido)
2. [Teste com Servidor Local](#teste-com-servidor-local)
3. [Teste com Arquivo JSON](#teste-com-arquivo-json)
4. [Teste com cURL](#teste-com-curl)
5. [Teste com JavaScript/Fetch](#teste-com-javascriptfetch)
6. [Teste com Postman](#teste-com-postman)
7. [Estrutura do JSON](#estrutura-do-json)

---

## 🚀 Teste Local Rápido

A forma mais simples de testar:

```bash
python test-local.py
```

Isso usa dados de exemplo pré-configurados.

---

## 🌐 Teste com Servidor Local

Para testar como uma API real:

### 1. Iniciar o servidor

```bash
python server-local.py
```

Você verá:
```
🚀 Servidor rodando em http://localhost:8000
📡 Endpoint: http://localhost:8000/api/generate-pdf
```

### 2. Fazer requisições

Agora você pode fazer requisições para `http://localhost:8000/api/generate-pdf`

---

## 📄 Teste com Arquivo JSON

### Criar um arquivo de teste

Crie um arquivo `teste-paciente.json`:

```json
[
  {
    "nome": "João da Silva",
    "cpf": "111.222.333-44",
    "sexo": "Masculino",
    "faixa_etaria": "35-44",
    "tipo_usuario": "profissional",
    "data_registro": "2025-12-09 10:00:00",
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
    "sequelas": "Nenhuma",
    "desfecho": "Alta",
    "alta_medicamento": "Sim",
    "alta_medicamento_qual": "AAS",
    "grau_parentesco": "",
    "cuidador_externo": "",
    "tempo_chegada_hospital": "",
    "comorbidades": "Hipertensão",
    "historico_familiar": "",
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

### Enviar com cURL (Windows PowerShell)

```powershell
$body = Get-Content teste-paciente.json -Raw
Invoke-RestMethod -Uri http://localhost:8000/api/generate-pdf -Method POST -Body $body -ContentType "application/json" | ConvertTo-Json
```

### Enviar com cURL (Linux/Mac)

```bash
curl -X POST http://localhost:8000/api/generate-pdf \
  -H "Content-Type: application/json" \
  -d @teste-paciente.json
```

---

## 🔧 Teste com cURL

### Exemplo básico

```bash
curl -X POST http://localhost:8000/api/generate-pdf \
  -H "Content-Type: application/json" \
  -d '[
    {
      "nome": "Maria Santos",
      "cpf": "999.888.777-66",
      "sexo": "Feminino",
      "faixa_etaria": "45-54",
      "tipo_usuario": "parente",
      "data_registro": "2025-12-09 11:00:00",
      "data_inicio_sintomas": "2025-12-03",
      "data_avc": "2025-12-04",
      "tipo_avc": "Hemorrágico",
      "admissao_janela_terapeutica": "Não",
      "trombolise": "Não",
      "trombectomia": "Sim",
      "medicamentos_utilizados": "Nimodipina",
      "ventilacao_mecanica": "Sim",
      "tempo_ventilacao": "12 horas",
      "intubado": "Sim",
      "traqueostomizado": "Não",
      "sequelas": "Déficit motor leve",
      "desfecho": "Internado",
      "alta_medicamento": "Não",
      "alta_medicamento_qual": "",
      "grau_parentesco": "Filha",
      "cuidador_externo": "Sim",
      "tempo_chegada_hospital": "1 hora",
      "comorbidades": "Diabetes",
      "historico_familiar": "Mãe com AVC",
      "medicamento_uso_diario": "Sim",
      "medicamento_uso_diario_qual": "Metformina",
      "alimentacao": "Rica em sódio",
      "atividade_fisica": "1x/semana",
      "tabagismo": "Ex-fumante",
      "alcool": "Ocasionalmente",
      "uso_medicamentos": "Sim",
      "uso_medicamentos_qual": "Anticoagulante"
    }
  ]'
```

---

## 💻 Teste com JavaScript/Fetch

### No navegador (Console do DevTools)

```javascript
// Dados do paciente
const paciente = {
  "nome": "Pedro Oliveira",
  "cpf": "555.444.333-22",
  "sexo": "Masculino",
  "faixa_etaria": "55-64",
  "tipo_usuario": "profissional",
  "data_registro": "2025-12-09 12:00:00",
  "data_inicio_sintomas": "2025-12-05",
  "data_avc": "2025-12-06",
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
  "comorbidades": "Hipertensão, Dislipidemia",
  "historico_familiar": "Pai com AVC",
  "medicamento_uso_diario": "Sim",
  "medicamento_uso_diario_qual": "Losartana",
  "alimentacao": "Equilibrada",
  "atividade_fisica": "2x/semana",
  "tabagismo": "Não",
  "alcool": "Socialmente",
  "uso_medicamentos": "",
  "uso_medicamentos_qual": ""
};

// Fazer requisição
fetch('http://localhost:8000/api/generate-pdf', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify([paciente])
})
.then(response => response.json())
.then(data => {
  console.log('✅ Sucesso!', data);
  console.log(`📄 PDF gerado: ${data.pdfs[0].nome}`);
  console.log(`💾 Salvo em: ${data.pdfs[0].caminho_relativo}`);
})
.catch(error => {
  console.error('❌ Erro:', error);
});
```

### Múltiplos pacientes

```javascript
const pacientes = [
  {
    "nome": "Paciente 1",
    "cpf": "111.111.111-11",
    // ... outros campos
  },
  {
    "nome": "Paciente 2",
    "cpf": "222.222.222-22",
    // ... outros campos
  }
];

fetch('http://localhost:8000/api/generate-pdf', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(pacientes)
})
.then(response => response.json())
.then(data => {
  console.log(`✅ ${data.message}`);
  data.pdfs.forEach(pdf => {
    console.log(`📄 ${pdf.nome} - ${pdf.paciente}`);
  });
});
```

---

## 📮 Teste com Postman

### Configuração

1. **Método:** POST
2. **URL:** `http://localhost:8000/api/generate-pdf`
3. **Headers:**
   - `Content-Type: application/json`
4. **Body:** Selecione "raw" e "JSON", depois cole:

```json
[
  {
    "nome": "Teste Postman",
    "cpf": "123.456.789-00",
    "sexo": "Feminino",
    "faixa_etaria": "25-34",
    "tipo_usuario": "profissional",
    "data_registro": "2025-12-09 13:00:00",
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
    "sequelas": "Nenhuma",
    "desfecho": "Alta",
    "alta_medicamento": "Sim",
    "alta_medicamento_qual": "AAS",
    "grau_parentesco": "",
    "cuidador_externo": "",
    "tempo_chegada_hospital": "",
    "comorbidades": "Hipertensão",
    "historico_familiar": "",
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

5. Clique em **Send**

---

## 📋 Estrutura do JSON

### Campos Obrigatórios

- `nome` - Nome completo do paciente
- `cpf` - CPF do paciente

### Campos Opcionais (podem ser vazios "")

Todos os outros campos podem ser strings vazias se não aplicáveis.

### Exemplo Mínimo

```json
[
  {
    "nome": "Paciente Teste",
    "cpf": "123.456.789-00",
    "sexo": "",
    "faixa_etaria": "",
    "tipo_usuario": "",
    "data_registro": "",
    "data_inicio_sintomas": "",
    "data_avc": "",
    "tipo_avc": "",
    "admissao_janela_terapeutica": "",
    "trombolise": "",
    "trombectomia": "",
    "medicamentos_utilizados": "",
    "ventilacao_mecanica": "",
    "tempo_ventilacao": "",
    "intubado": "",
    "traqueostomizado": "",
    "sequelas": "",
    "desfecho": "",
    "alta_medicamento": "",
    "alta_medicamento_qual": "",
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

## ✅ Verificar Resultado

### Resposta de Sucesso

```json
{
  "success": true,
  "message": "1 PDF(s) gerado(s) com sucesso",
  "pdfs": [
    {
      "nome": "Joao_da_Silva_11122233344.pdf",
      "paciente": "João da Silva",
      "cpf": "111.222.333-44",
      "caminho": "C:\\...\\pdfexport\\PDF\\Joao_da_Silva_11122233344.pdf",
      "caminho_relativo": "PDF/Joao_da_Silva_11122233344.pdf",
      "pdf_base64": "..."
    }
  ]
}
```

### Verificar Arquivo Salvo

Os PDFs são salvos automaticamente na pasta `PDF/`:

```bash
# Windows PowerShell
Get-ChildItem PDF

# Linux/Mac
ls PDF/
```

---

## 🔍 Dicas

1. **Múltiplos pacientes:** Envie um array com vários objetos
2. **Campos vazios:** Use `""` para campos não preenchidos
3. **Nomes duplicados:** A API adiciona timestamp automaticamente
4. **Teste local primeiro:** Use `server-local.py` antes de fazer deploy
5. **Verifique os PDFs:** Sempre confira se os PDFs foram gerados corretamente na pasta `PDF/`

---

## 🐛 Troubleshooting

### Erro: "Connection refused"
- Certifique-se de que o servidor está rodando (`python server-local.py`)

### Erro: "JSON inválido"
- Verifique se o JSON está bem formatado
- Use um validador JSON online

### PDF não aparece na pasta
- Verifique se a pasta `PDF/` existe
- Verifique permissões de escrita

### Erro: "ModuleNotFoundError"
- Execute: `pip install -r requirements.txt`

