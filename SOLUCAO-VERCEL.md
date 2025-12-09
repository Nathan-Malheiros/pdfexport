# 🔧 Solução: Vercel dizendo que é uma função

## 🐛 Problema

O Vercel está reclamando que é uma função e não aceita o deploy.

## ✅ Soluções

### 1. Simplificar o `vercel.json`

O Vercel moderno detecta automaticamente funções Python na pasta `api/`. O `vercel.json` foi simplificado:

```json
{
  "functions": {
    "api/generate-pdf.py": {
      "maxDuration": 30
    }
  }
}
```

### 2. Verificar Estrutura de Pastas

Certifique-se de que a estrutura está assim:

```
pdfexport/              ← Root Directory (deixe vazio ou ".")
├── vercel.json
├── requirements.txt
├── api/
│   └── generate-pdf.py  ← Função serverless
└── art/
    └── logoPET.png
```

### 3. Configuração no Vercel Dashboard

**Root Directory:** Deixe **VAZIO** ou coloque **`.`**

**NÃO coloque:**
- ❌ `pdfexport`
- ❌ `api`
- ❌ Qualquer subpasta

### 4. Se ainda não funcionar

#### Opção A: Usar Vercel CLI

```bash
# Instalar CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel
```

#### Opção B: Verificar Logs

1. Vá em **Deployments** no Vercel
2. Clique no deploy que falhou
3. Veja os **Build Logs** e **Function Logs**
4. Procure por erros específicos

### 5. Erros Comuns

#### Erro: "No function found"
- ✅ Verifique se `api/generate-pdf.py` existe
- ✅ Verifique se o Root Directory está correto

#### Erro: "Module not found"
- ✅ Verifique se `requirements.txt` está na raiz
- ✅ Verifique se todas as dependências estão listadas

#### Erro: "Build failed"
- ✅ Verifique os logs de build
- ✅ Verifique se o Python está configurado corretamente

### 6. Testar Localmente com Vercel CLI

```bash
# Instalar Vercel CLI
npm install -g vercel

# Testar localmente
vercel dev
```

Isso vai simular o ambiente do Vercel localmente e mostrar erros antes do deploy.

---

## 📋 Checklist Final

Antes de fazer deploy, verifique:

- [ ] `vercel.json` está simplificado (sem "builds")
- [ ] `api/generate-pdf.py` existe e tem a função `handler`
- [ ] `requirements.txt` está na raiz
- [ ] `art/logoPET.png` existe
- [ ] Root Directory está **vazio** ou **`.`**
- [ ] Código está no repositório conectado

---

## 🆘 Se nada funcionar

1. **Copie a mensagem de erro completa** do Vercel
2. **Verifique os logs** de build e função
3. **Tente fazer deploy via CLI** (`vercel`) para ver mais detalhes
4. **Verifique se o repositório está conectado corretamente**

---

## 💡 Dica

O Vercel detecta automaticamente funções Python na pasta `api/`. Se você seguir a estrutura correta, não precisa de configuração complexa no `vercel.json`.

