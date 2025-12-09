# API PET Saúde Digital

API Flask que recebe dados JSON de pacientes e **gera PDF automaticamente**!

## 🚀 Funcionalidades

- ✅ Recebe JSON via POST
- ✅ Valida dados do paciente
- ✅ Gera PDF automaticamente no mesmo formato do `pdfexportv3.py`
- ✅ Retorna PDF único ou ZIP com múltiplos PDFs
- ✅ Funciona localmente e no Vercel

## 📦 Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🎯 Como usar

### 1. Iniciar o servidor local

```bash
python app.py
```

O servidor será iniciado em `http://localhost:5000`

### 2. Enviar dados JSON e receber PDF

#### Usando Python (requests):
```python
import requests

url = "http://localhost:5000/api/receber-json"
dados = [
    {
        "nome": "João Silva",
        "cpf": "123.456.789-00",
        "sexo": "Masculino",
        "faixa_etaria": "30-39 anos",
        # ... outros campos
    }
]

response = requests.post(url, json=dados)

# Salvar PDF recebido
if response.status_code == 200:
    with open('paciente.pdf', 'wb') as f:
        f.write(response.content)
    print("PDF salvo com sucesso!")
```

#### Usando cURL:
```bash
curl -X POST http://localhost:5000/api/receber-json \
  -H "Content-Type: application/json" \
  -d @seu_arquivo.json \
  --output paciente.pdf
```

#### Usando JavaScript (fetch):
```javascript
fetch('http://localhost:5000/api/receber-json', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify([
    {
      nome: "João Silva",
      cpf: "123.456.789-00",
      sexo: "Masculino",
      // ... outros campos
    }
  ])
})
.then(response => response.blob())
.then(blob => {
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'paciente.pdf';
  a.click();
});
```

## 📡 Endpoints

### `GET /`
Retorna informações sobre a API.

### `POST /api/receber-json`
Recebe dados JSON e gera PDF automaticamente.

**Body:** JSON (array ou objeto)
```json
[
  {
    "nome": "João Silva",
    "cpf": "123.456.789-00",
    "sexo": "Masculino",
    "faixa_etaria": "30-39 anos",
    "tipo_usuario": "Paciente",
    "data_registro": "2025-12-09",
    ...
  }
]
```

**Resposta:**
- **1 paciente:** Retorna PDF diretamente (Content-Type: application/pdf)
- **Múltiplos pacientes:** Retorna ZIP com todos os PDFs (Content-Type: application/zip)

### `GET /api/status`
Verifica o status da API.

## 🎨 Configurar Logo

Para incluir o logo do PET nos PDFs:

### Opção 1: Variável de ambiente (Vercel)
1. Execute `python converter_logo_base64.py` para obter o base64 do logo
2. No Vercel, adicione variável de ambiente: `LOGO_BASE64` = (valor base64)

### Opção 2: Caminho local
Se rodando localmente, coloque o logo em `../art/logoPET.png` ou configure `LOGO_PATH` no código.

## 🌐 Deploy no Vercel

Veja o arquivo `DEPLOY_VERCEL.md` para instruções detalhadas.

**URL após deploy:** `https://pdfexport-ten.vercel.app/api/receber-json`

## 📋 Campos do JSON

### Obrigatórios:
- `nome` - Nome do paciente
- `cpf` - CPF do paciente

### Opcionais (serão preenchidos com " Campo não preenchido" se ausentes):
- `sexo`, `faixa_etaria`, `tipo_usuario`, `data_registro`
- `data_inicio_sintomas`, `data_avc`, `tipo_avc`
- `admissao_janela_terapeutica`, `trombolise`, `trombectomia`
- `medicamentos_utilizados`, `ventilacao_mecanica`, `tempo_ventilacao`
- `intubado`, `traqueostomizado`
- `sequelas`, `desfecho`, `alta_medicamento`, `alta_medicamento_qual`
- `grau_parentesco`, `cuidador_externo`, `tempo_chegada_hospital`
- `comorbidades`, `historico_familiar`
- `medicamento_uso_diario`, `medicamento_uso_diario_qual`
- `alimentacao`, `atividade_fisica`, `tabagismo`, `alcool`
- `uso_medicamentos`, `uso_medicamentos_qual`

## 🔄 Diferenças do pdfexportv3.py

- ✅ **Geração instantânea:** PDF é gerado imediatamente ao receber JSON
- ✅ **Sem monitoramento:** Não precisa de watchdog ou pasta monitorada
- ✅ **Resposta direta:** PDF retornado na resposta HTTP
- ✅ **Múltiplos pacientes:** ZIP automático quando há vários pacientes
- ✅ **Serverless:** Funciona no Vercel sem salvar arquivos localmente

## 📝 Exemplo Completo

Veja `exemplo_requisicao.py` para um exemplo completo de uso.
