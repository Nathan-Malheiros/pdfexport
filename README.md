# API PDF Export - PET Saúde Digital

API serverless para geração de PDFs a partir de dados JSON de pacientes.

## Como usar

### Endpoint
```
POST /api/generate-pdf
```

### Exemplo de requisição

```javascript
fetch('https://seu-dominio.vercel.app/api/generate-pdf', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify([
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
  ])
})
.then(response => response.json())
.then(data => {
  console.log(data);
  // data.pdfs[0].pdf_base64 contém o PDF em base64
});
```

### Resposta de sucesso

```json
{
  "success": true,
  "message": "1 PDF(s) gerado(s) com sucesso",
  "pdfs": [
    {
      "nome": "Ana_Silva_12345678900.pdf",
      "paciente": "Ana Silva",
      "cpf": "123.456.789-00",
      "caminho": "C:\\caminho\\completo\\PDF\\Ana_Silva_12345678900.pdf",
      "caminho_relativo": "PDF/Ana_Silva_12345678900.pdf",
      "pdf_base64": "JVBERi0xLjQKJeLjz9MKMy..."
    }
  ]
}
```

**Nota:** Os PDFs são automaticamente salvos na pasta `PDF/` do projeto. Se um arquivo com o mesmo nome já existir, será adicionado um timestamp ao nome.

### Resposta de erro

```json
{
  "error": "Erro ao processar requisição",
  "message": "Descrição do erro"
}
```

## Como rodar

### Opção 1: Teste Local Simples

Teste rápido sem servidor:

```bash
python test-local.py
```

### Opção 2: Servidor Local (Recomendado)

Para testar como se fosse uma API real:

1. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

2. **Execute o servidor:**
```bash
python server-local.py
```

3. **Teste com curl ou Postman:**
```bash
curl -X POST http://localhost:8000/api/generate-pdf \
  -H "Content-Type: application/json" \
  -d @jsons/entrada.json
```

Ou use o arquivo `example-request.js` no navegador (ajustando a URL para `http://localhost:8000/api/generate-pdf`)

### Opção 3: Deploy no Vercel

1. **Instale o Vercel CLI:**
```bash
npm i -g vercel
```

2. **Faça login:**
```bash
vercel login
```

3. **Deploy:**
```bash
vercel
```

4. **Ou conecte seu repositório GitHub ao Vercel** para deploy automático.

Após o deploy, você receberá uma URL como: `https://seu-projeto.vercel.app/api/generate-pdf`

## Estrutura do projeto

```
pdfexport/
├── api/
│   └── generate-pdf.py    # Endpoint da API
├── art/
│   └── logoPET.png        # Logo usado nos PDFs
├── PDF/                    # Pasta onde os PDFs são salvos
│   └── *.pdf              # PDFs gerados
├── requirements.txt        # Dependências Python
├── vercel.json            # Configuração do Vercel
└── README.md              # Este arquivo
```

## Dependências

- pandas
- reportlab
- openpyxl

