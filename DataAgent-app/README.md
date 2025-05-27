# 📊 DataAgent App - Mastra Framework

Veri Tablolu Sorgulama ve Yorumlama AI Agent'ı - Mastra Framework ile geliştirilmiş, MCP Server entegrasyonu bulunan modern veri analizi uygulaması.

## 🚀 Özellikler

- **Mastra Framework**: Modern AI agent framework'ü ile geliştirilmiş
- **MCP Server Entegrasyonu**: Model Context Protocol ile veri analizi server'ına bağlantı
- **Türkçe Dil Desteği**: Doğal Türkçe konuşma ve analiz
- **Çoklu Format Desteği**: CSV, Excel, JSON dosya formatları
- **Akıllı Analiz**: GPT-4o-mini ile güçlendirilmiş veri yorumlama
- **Smithery Platform**: MCP araçları için bulut entegrasyonu

## 🔧 Kurulum

### Gereksinimler
- Node.js >= 20.9.0
- npm veya yarn
- MCP Server (DataAnalysisAgent klasöründe)

### Kurulum Adımları

```bash
# Bağımlılıkları yükle
npm install

# Development modunda çalıştır
npm run dev

# Production build
npm run build

# Production'da çalıştır
npm start
```

## 🔗 MCP Server Bağlantısı

Bu uygulama, ayrı bir MCP server'a bağlanarak veri analizi yapar:

### Server Bilgileri
- **Server Name**: data-analysis-agent
- **Port**: 8000
- **Protocol**: HTTP
- **Location**: ../DataAnalysisAgent/

### Smithery Entegrasyonu
- **API Key**: `81c0c036-745e-42ae-9090-eebd33950d82`
- **Profile Key**: `probable-capybara-wWraCH`

### MCP Server'ı Başlatma

```bash
# DataAnalysisAgent klasörüne git
cd ../DataAnalysisAgent

# MCP Server'ı başlat
python server.py

# Veya Docker ile
docker run -p 8000:8000 data-analysis-agent
```

## 🛠️ Kullanım

### Agent ile Konuşma

```typescript
import { mastra } from './src/mastra';

// Agent'ı al
const agent = mastra.getAgent('dataAnalysisAgent');

// Veri analizi yap
const response = await agent.generate([
  {
    role: 'user',
    content: 'Bu CSV dosyasındaki satış verilerini analiz et'
  }
]);
```

### Örnek Sorular

```
"Bu tabloda en çok satış yapan ürün hangisi?"
"2023 yılına ait toplam geliri hesapla"
"Müşteri memnuniyetine göre düşük puan alan ürünleri listele"
"Aylık değişimleri grafik olarak açıklayabilir misin?"
"Bu veriye göre hangi kategori dikkat çekiyor?"
```

## 📊 MCP Tools

Agent aşağıdaki MCP araçlarını kullanabilir:

### 1. `load_data`
Veri dosyası yükler
```json
{
  "file_path": "data.csv",
  "file_type": "csv",
  "encoding": "utf-8"
}
```

### 2. `analyze_data`
Genel veri analizi yapar
```json
{
  "query": "En yüksek satış değeri nedir?",
  "analysis_type": "statistics"
}
```

### 3. `get_data_info`
Veri seti bilgilerini döndürür
```json
{}
```

### 4. `filter_data`
Veriyi filtreler
```json
{
  "column": "sales",
  "operator": ">",
  "value": 1000
}
```

### 5. `calculate_statistics`
İstatistik hesaplar
```json
{
  "columns": ["sales", "profit"],
  "operation": "mean"
}
```

### 6. `group_analysis`
Grup analizi yapar
```json
{
  "group_by": "category",
  "agg_column": "sales",
  "agg_function": "sum"
}
```

## 🏗️ Proje Yapısı

```
DataAgent-app/
├── src/
│   └── mastra/
│       ├── agents/
│       │   └── data-analysis-agent.ts    # Ana AI agent
│       ├── config/
│       │   └── mcp-config.ts            # MCP server konfigürasyonu
│       └── index.ts                     # Mastra instance
├── package.json
└── README.md
```

## ⚙️ Konfigürasyon

### Environment Variables

```bash
# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key

# MCP Server
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8000

# Smithery
SMITHERY_API_KEY=81c0c036-745e-42ae-9090-eebd33950d82
SMITHERY_PROFILE_KEY=probable-capybara-wWraCH
```

### MCP Server Konfigürasyonu

`src/mastra/config/mcp-config.ts` dosyasında MCP server bağlantı ayarları bulunur.

## 🔄 Workflow

1. **Agent Başlatma**: Mastra framework ile agent başlatılır
2. **MCP Bağlantısı**: Agent, MCP server'a bağlanır
3. **Veri Yükleme**: Kullanıcı veri dosyası yükler
4. **Analiz**: Agent, MCP tools kullanarak analiz yapar
5. **Yorumlama**: Sonuçlar Türkçe olarak yorumlanır
6. **Yanıt**: Kullanıcıya anlaşılır şekilde sunulur

## 🚀 Deployment

### Development
```bash
npm run dev
```

### Production
```bash
npm run build
npm start
```

### Docker (MCP Server ile birlikte)
```bash
# MCP Server'ı başlat
cd ../DataAnalysisAgent
docker build -t data-analysis-agent .
docker run -d -p 8000:8000 data-analysis-agent

# Mastra App'i başlat
cd ../DataAgent-app
npm run build
npm start
```

## 🤝 Katkıda Bulunma

1. Repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🆘 Destek

- GitHub Issues açın
- Mastra dokümantasyonunu kontrol edin
- MCP server loglarını inceleyin
- Smithery community'ye katılın 