# 📋 GitHub Setup ve Smithery Deploy Talimatları

## 🔗 1. GitHub Repository Oluşturma

### GitHub'da yeni repository oluştur:
1. GitHub.com'a git
2. "New repository" butonuna tıkla
3. Repository adı: `dataagent-ai-system`
4. Description: `🤖 AI Veri Analizi Sistemi - MCP Server + Mastra Client`
5. Public/Private seç
6. **README, .gitignore, license ekleme** (zaten var)
7. "Create repository" tıkla

### 🚀 2. Local'den GitHub'a Push

```bash
# Remote repository ekle (GitHub'dan aldığın URL'yi kullan)
git remote add origin https://github.com/KULLANICI_ADI/dataagent-ai-system.git

# Ana branch'i main olarak ayarla
git branch -M main

# GitHub'a push et
git push -u origin main
```

## 🌐 3. Smithery Deploy Seçenekleri

### Seçenek A: Tek Repository (Önerilen)
```bash
# Sadece MCP Server'ı deploy et
cd DataAnalysisAgent
smithery deploy

# Mastra app ayrı platform'da deploy et
cd ../DataAgent-app
npm run build
# Vercel, Netlify, vs. deploy
```

### Seçenek B: Ayrı Repository'ler
```bash
# DataAnalysisAgent için ayrı repo
git subtree push --prefix=DataAnalysisAgent origin dataanalysis-server

# DataAgent-app için ayrı repo  
git subtree push --prefix=DataAgent-app origin dataagent-client
```

## 🔧 4. Smithery Deploy Adımları

### DataAnalysisAgent (MCP Server):
```bash
cd DataAnalysisAgent

# Smithery CLI kurulu mu kontrol et
smithery --version

# Login (eğer değilse)
smithery login

# Deploy
smithery deploy

# Status kontrol
smithery status
```

### Environment Variables:
```bash
# Smithery'de environment variables ayarla:
SMITHERY_API_KEY=81c0c036-745e-42ae-9090-eebd33950d82
SMITHERY_PROFILE_KEY=probable-capybara-wWraCH
```

## 📊 5. Deploy Sonrası Test

### MCP Server Test:
```bash
# Smithery dashboard'da tools kontrol et
# 6 tool görünmeli:
# - load_data
# - analyze_data  
# - get_data_info
# - filter_data
# - calculate_statistics
# - group_analysis
```

### Mastra Client Test:
```bash
cd DataAgent-app
npm run dev
# MCP server connection test
```

## 🎯 6. Production URLs

Deploy sonrası alacağın URL'ler:
- **MCP Server**: `https://your-smithery-url.smithery.ai`
- **Mastra App**: `https://your-app-url.vercel.app`

## 🔄 7. Update Workflow

```bash
# Code değişikliği sonrası:
git add .
git commit -m "Update: açıklama"
git push

# MCP Server update:
cd DataAnalysisAgent
smithery deploy

# Mastra App update:
cd DataAgent-app
npm run build
# Platform'a deploy
```

---
**Next Steps**: GitHub repo oluştur → Push et → Smithery deploy 