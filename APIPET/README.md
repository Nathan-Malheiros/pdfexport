# API PET Saúde Digital

API Flask que recebe dados JSON de pacientes e salva na pasta `jsons/` para processamento automático pelo `pdfexportv3.py`.

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como usar

### 1. Iniciar o servidor

```bash
python app.py
```

O servidor será iniciado em `http://localhost:5000`

### 2. Enviar dados JSON

#### Usando cURL:
```bash
curl -X POST http://localhost:5000/receber-json \
  -H "Content-Type: application/json" \
  -d @seu_arquivo.json
```

#### Usando Python (requests):
```python
import requests

url = "http://localhost:5000/receber-json"
dados = [
    {
        "nome": "João Silva",
        "cpf": "123.456.789-00",
        "sexo": "Masculino",
        # ... outros campos
    }
]

response = requests.post(url, json=dados)
print(response.json())
```

#### Usando JavaScript (fetch):
```javascript
fetch('http://localhost:5000/receber-json', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify([
    {
      nome: "João Silva",
      cpf: "123.456.789-00",
      // ... outros campos
    }
  ])
})
.then(response => response.json())
.then(data => console.log(data));
```

## Endpoints

### `GET /`
Retorna informações sobre a API.

### `POST /receber-json`
Recebe dados JSON e salva na pasta `jsons/`.

**Body:** JSON (array ou objeto)
```json
[
  {
    "nome": "João Silva",
    "cpf": "123.456.789-00",
    "sexo": "Masculino",
    ...
  }
]
```

**Resposta de sucesso (200):**
```json
{
  "mensagem": "JSON recebido e salvo com sucesso",
  "arquivo": "entrada_20251209_164530_a1b2c3d4.json",
  "caminho": "C:\\...\\jsons\\entrada_20251209_164530_a1b2c3d4.json",
  "pacientes": 1,
  "timestamp": "20251209_164530"
}
```

### `GET /status`
Verifica o status da API e lista arquivos na pasta `jsons/`.

## Fluxo completo

1. API recebe JSON via POST
2. JSON é salvo na pasta `jsons/` com nome único
3. `pdfexportv3.py` detecta o novo arquivo (se estiver rodando)
4. PDFs são gerados automaticamente na pasta `pdf/{data}/`

## Notas

- A API aceita tanto objetos únicos quanto arrays de pacientes
- Arquivos são salvos com timestamp e UUID para evitar conflitos
- O formato do JSON deve seguir a estrutura esperada pelo `pdfexportv3.py`

