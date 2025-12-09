# 🚀 Guia de Deploy no Vercel

## 📋 Configuração do Root Directory

### ✅ Root Directory no Vercel

**Deixe em branco** ou coloque: **`.`** (ponto)

Isso significa que a raiz do projeto é onde está o arquivo `vercel.json`.

---

## 🔧 Passo a Passo no Vercel Dashboard

### 1. Importar Projeto

1. Acesse: https://vercel.com/dashboard
2. Clique em **"Add New..."** → **"Project"**
3. Conecte seu repositório (GitHub, GitLab, etc.)

### 2. Configurar Projeto

Na tela de configuração:

- **Framework Preset:** Deixe como está (ou selecione "Other")
- **Root Directory:** 
  - ✅ **Deixe vazio** ou coloque **`.`**
  - ❌ NÃO coloque `pdfexport` ou qualquer subpasta

- **Build Command:** Deixe vazio (não precisa)
- **Output Directory:** Deixe vazio (não precisa)

### 3. Environment Variables

Não precisa configurar nenhuma variável de ambiente por enquanto.

### 4. Deploy

Clique em **"Deploy"**

---

## 📁 Estrutura Esperada pelo Vercel

O Vercel espera encontrar na raiz:

```
pdfexport/                    ← Root Directory (.)
├── vercel.json              ← Configuração do Vercel
├── requirements.txt         ← Dependências Python
├── api/
│   └── generate-pdf.py      ← Função serverless
├── art/
│   └── logoPET.png          ← Logo (usado nos PDFs)
└── PDF/                     ← Pasta para PDFs (criada automaticamente)
```

---

## ⚠️ Importante: Pasta PDF no Vercel

**Atenção:** No Vercel, a pasta `PDF/` é **temporária** (ephemeral storage). 

Os PDFs são salvos durante a execução da função, mas **não persistem** entre execuções.

### Soluções Alternativas:

1. **Retornar apenas base64** (já está fazendo isso)
2. **Usar storage externo** (S3, Google Cloud Storage, etc.)
3. **Fazer download direto** do base64 no frontend

---

## 🔍 Verificar Deploy

Após o deploy, você receberá uma URL como:

```
https://seu-projeto.vercel.app/api/generate-pdf
```

### Testar a API

```bash
curl -X POST https://seu-projeto.vercel.app/api/generate-pdf \
  -H "Content-Type: application/json" \
  -d '[{"nome": "Teste", "cpf": "123.456.789-00", ...}]'
```

---

## 🐛 Troubleshooting

### Erro: "Build failed"
- ✅ Verifique se `requirements.txt` está na raiz
- ✅ Verifique se todas as dependências estão listadas

### Erro: "Function not found"
- ✅ Verifique se `api/generate-pdf.py` existe
- ✅ Verifique se `vercel.json` está correto

### Erro: "Module not found"
- ✅ Verifique se `requirements.txt` tem todas as dependências
- ✅ Verifique se os caminhos dos arquivos estão corretos

---

## 📝 Checklist de Deploy

Antes de fazer deploy, verifique:

- [ ] `vercel.json` está na raiz
- [ ] `requirements.txt` está na raiz
- [ ] `api/generate-pdf.py` existe
- [ ] `art/logoPET.png` existe
- [ ] Root Directory está vazio ou como `.`
- [ ] Código está no repositório conectado

---

## 🎯 Resumo

**Root Directory:** Deixe **vazio** ou coloque **`.`**

Isso é tudo que você precisa configurar!

