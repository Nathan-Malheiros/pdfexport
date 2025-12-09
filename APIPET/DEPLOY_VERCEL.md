# Como fazer Deploy no Vercel

## Passo a Passo

### 1. Instalar Vercel CLI (se ainda não tiver)
```bash
npm install -g vercel
```

### 2. Fazer login no Vercel
```bash
vercel login
```

### 3. Navegar para a pasta APIPET
```bash
cd pdfexport/APIPET
```

### 4. Fazer deploy
```bash
vercel
```

Siga as instruções:
- **Set up and deploy?** → Y
- **Which scope?** → Selecione sua conta
- **Link to existing project?** → N (primeira vez) ou Y (se já tiver projeto)
- **Project name?** → pdfexport (ou o nome que preferir)
- **Directory?** → ./ (pasta atual)

### 5. Deploy em produção
```bash
vercel --prod
```

## Estrutura de Arquivos Necessária

Certifique-se de que os seguintes arquivos estão na pasta `APIPET`:

```
APIPET/
├── app.py              # Aplicação Flask principal
├── vercel.json         # Configuração do Vercel
├── requirements.txt    # Dependências Python
└── README.md           # Documentação
```

## Endpoints Disponíveis

Após o deploy, seus endpoints estarão disponíveis em:
- `https://pdfexport-ten.vercel.app/` - Página inicial
- `https://pdfexport-ten.vercel.app/api/receber-json` - POST para receber JSON
- `https://pdfexport-ten.vercel.app/api/status` - GET para status

## Importante: Limitações do Vercel Serverless

⚠️ **O Vercel é um ambiente serverless que NÃO permite salvar arquivos localmente.**

A API retorna os dados processados no response. Você tem duas opções:

### Opção 1: Cliente salva os dados
O cliente que chama a API recebe os dados processados e pode salvá-los localmente.

### Opção 2: Usar Webhook
Configure uma variável de ambiente `WEBHOOK_URL` no Vercel para enviar os dados automaticamente para outro serviço.

## Configurar Variável de Ambiente (Webhook)

1. Acesse o dashboard do Vercel
2. Vá em Settings → Environment Variables
3. Adicione: `WEBHOOK_URL` = URL do seu webhook
4. Faça redeploy

## Testar Localmente

Antes de fazer deploy, teste localmente:

```bash
vercel dev
```

Isso iniciará um servidor local que simula o ambiente do Vercel.

## Troubleshooting

### Erro 500 - FUNCTION_INVOCATION_FAILED
- Verifique se todas as dependências estão no `requirements.txt`
- Verifique os logs no dashboard do Vercel
- Certifique-se de que o `vercel.json` está correto

### CORS Errors
- A API já está configurada com CORS habilitado
- Se ainda tiver problemas, verifique os headers da requisição

### JSON não está sendo recebido
- Certifique-se de enviar `Content-Type: application/json`
- Verifique se o body da requisição está em formato JSON válido

