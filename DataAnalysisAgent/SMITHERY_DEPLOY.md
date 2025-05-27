# 🚀 Smithery Deploy Talimatları

## ❌ Sorun: Repository Gözükmüyor

Smithery CLI sadece **mevcut server'ları install** etmek için kullanılır. Kendi server'ımızı deploy etmek için farklı yöntemler var.

## ✅ Çözüm Seçenekleri

### 1. Smithery Web Dashboard (Önerilen)

1. **Smithery.ai'ye git**: https://smithery.ai/
2. **Login ol** (API Key ile)
3. **"Deploy Server"** butonuna tıkla
4. **GitHub Repository** seç: `https://github.com/EmirHth/DataAgent`
5. **Subfolder** belirt: `DataAnalysisAgent`
6. **smithery.yaml** otomatik algılanacak

### 2. GitHub Actions ile Deploy

```yaml
# .github/workflows/smithery-deploy.yml
name: Deploy to Smithery
on:
  push:
    branches: [main]
    paths: ['DataAnalysisAgent/**']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Smithery
        env:
          SMITHERY_API_KEY: ${{ secrets.SMITHERY_API_KEY }}
        run: |
          cd DataAnalysisAgent
          curl -X POST https://api.smithery.ai/deploy \
            -H "Authorization: Bearer $SMITHERY_API_KEY" \
            -H "Content-Type: application/json" \
            -d '{
              "repository": "https://github.com/EmirHth/DataAgent",
              "path": "DataAnalysisAgent",
              "config": "smithery.yaml"
            }'
```

### 3. Manual Upload

1. **ZIP dosyası oluştur**: DataAnalysisAgent klasörünü zip'le
2. **Smithery Dashboard**: Manual upload seçeneği
3. **smithery.yaml** dosyasını kontrol et

## 🔧 Alternatif: Docker Deploy

```bash
# Docker image oluştur
cd DataAnalysisAgent
docker build -t dataagent-mcp .

# Docker Hub'a push et
docker tag dataagent-mcp your-username/dataagent-mcp
docker push your-username/dataagent-mcp

# Smithery'de Docker image kullan
```

## 📋 Gerekli Bilgiler

- **Repository**: https://github.com/EmirHth/DataAgent
- **Path**: DataAnalysisAgent
- **Config**: smithery.yaml
- **API Key**: 81c0c036-745e-42ae-9090-eebd33950d82
- **Profile**: probable-capybara-wWraCH

## 🎯 Sıradaki Adımlar

1. **Smithery.ai'ye git**
2. **Login ol**
3. **"Deploy Server"** tıkla
4. **GitHub repo seç**
5. **DataAnalysisAgent** klasörünü belirt
6. **Deploy** et

## 🔍 Troubleshooting

### Repository Gözükmüyorsa:
- GitHub repo public mi?
- smithery.yaml dosyası var mı?
- Repository URL doğru mu?

### Deploy Başarısızsa:
- requirements.txt kontrol et
- server.py syntax hatası var mı?
- Environment variables doğru mu?

---
**Next**: Smithery web dashboard kullan! 