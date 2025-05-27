# 📊 Data Analysis Agent

Veri Tablolu Sorgulama ve Yorumlama için özelleştirilmiş AI Agent. Bu agent, CSV, Excel ve JSON formatındaki veri dosyalarını analiz ederek kullanıcı sorularını yanıtlar ve veri yorumlaması yapar.

## 🚀 Özellikler

- **Çoklu Format Desteği**: CSV, Excel (.xlsx, .xls) ve JSON dosyaları
- **Türkçe Dil Desteği**: Türkçe sorular ve yanıtlar
- **İstatistiksel Analiz**: Ortalama, medyan, toplam, min/max hesaplamaları
- **Veri Filtreleme**: Gelişmiş filtreleme kriterleri
- **Grup Analizi**: Kategorik verilere göre gruplama ve agregasyon
- **Otomatik Veri Tipi Tespiti**: Sayısal ve kategorik sütunların otomatik tanınması
- **Eksik Değer Analizi**: Null değerlerin tespiti ve raporlanması
- **Smithery MCP Entegrasyonu**: Model Context Protocol desteği

## 🔑 Smithery Konfigürasyonu

Bu agent Smithery MCP platformu ile entegre edilmiştir:

- **API Key**: `81c0c036-745e-42ae-9090-eebd33950d82`
- **Profile Key**: `probable-capybara-wWraCH`
- **Server Name**: `data-analysis-agent`
- **Version**: `1.0.0`

## 🛠️ Kurulum

### Smithery'ye Deploy

```bash
# 1. Otomatik deploy (Linux/Mac)
./deploy.sh

# 2. Manuel deploy
# https://smithery.ai adresine gidin
# API Key ve Profile Key'i girin
# smithery.yaml dosyasını upload edin
```

### Docker ile Çalıştırma

```bash
# Repository'yi klonlayın
git clone <repository-url>
cd DataAnalysisAgent

# Environment variables ayarlayın
export SMITHERY_API_KEY=81c0c036-745e-42ae-9090-eebd33950d82
export SMITHERY_PROFILE_KEY=probable-capybara-wWraCH

# Docker image'ını build edin
docker build -t data-analysis-agent .

# Container'ı çalıştırın
docker run -p 8000:8000 data-analysis-agent
```

### Manuel Kurulum

```bash
# Environment variables ayarlayın
export SMITHERY_API_KEY=81c0c036-745e-42ae-9090-eebd33950d82
export SMITHERY_PROFILE_KEY=probable-capybara-wWraCH

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# MCP Server'ı başlatın
python server.py

# Veya standalone uygulamayı çalıştırın
python app.py
```

## 📖 Kullanım

### Smithery MCP Client ile

```python
# Smithery MCP client ile bağlantı
import smithery

client = smithery.Client(
    api_key="81c0c036-745e-42ae-9090-eebd33950d82",
    profile_key="probable-capybara-wWraCH"
)

# Agent'a bağlan
agent = client.get_agent("data-analysis-agent")

# Veri yükleme
result = await agent.call_tool("load_data", {
    "file_path": "sales_data.csv"
})

# Analiz yapma
result = await agent.call_tool("analyze_data", {
    "query": "En çok satış yapan ürün hangisi?"
})
```

### MCP Server Olarak

```python
# MCP client ile bağlantı
from mcp.client import Client

client = Client("data-analysis-agent")

# Veri yükleme
result = await client.call_tool("load_data", {
    "file_path": "sales_data.csv"
})

# Analiz yapma
result = await client.call_tool("analyze_data", {
    "query": "En çok satış yapan ürün hangisi?"
})
```

### Standalone Uygulama Olarak

```bash
python app.py

# Veri yükleme
📊 Soru/Komut: load sales_data.csv

# Analiz soruları
📊 Soru/Komut: Bu tabloda en çok satış yapan ürün hangisi?
📊 Soru/Komut: 2023 yılına ait toplam geliri hesapla
📊 Soru/Komut: Müşteri memnuniyetine göre düşük puan alan ürünleri listele
```

## 🔧 Mevcut Araçlar (Tools)

### 1. `load_data`
Veri dosyası yükler ve analiz için hazırlar.

**Parametreler:**
- `file_path` (string): Dosya yolu

### 2. `analyze_data`
Genel veri analizi yapar ve soruları yanıtlar.

**Parametreler:**
- `query` (string): Analiz sorusu
- `analysis_type` (string, opsiyonel): Analiz türü

### 3. `get_data_info`
Yüklü verinin genel bilgilerini döndürür.

### 4. `filter_data`
Veriyi belirli kriterlere göre filtreler.

**Parametreler:**
- `column` (string): Sütun adı
- `operator` (string): Operatör (==, !=, >, <, >=, <=, contains, startswith, endswith)
- `value` (string/number): Filtreleme değeri

### 5. `calculate_statistics`
İstatistiksel hesaplamalar yapar.

**Parametreler:**
- `columns` (array, opsiyonel): Sütun listesi
- `operation` (string): İşlem türü (mean, median, sum, min, max, std, var, count)

### 6. `group_analysis`
Grup analizi yapar.

**Parametreler:**
- `group_by` (string): Gruplama sütunu
- `agg_column` (string, opsiyonel): Agregasyon sütunu
- `agg_function` (string): Agregasyon fonksiyonu

## 📊 Örnek Senaryolar

### Satış Analizi
```
"Bu tabloda en çok satış yapan ürün hangisi?"
"Kategori bazında toplam satışları göster"
"Aylık satış trendini analiz et"
```

### İstatistiksel Analiz
```
"Tüm sayısal sütunların ortalamasını hesapla"
"Fiyat sütunundaki en yüksek ve en düşük değerleri bul"
"Müşteri yaşlarının standart sapmasını hesapla"
```

### Filtreleme ve Gruplama
```
"2023 yılındaki verileri filtrele"
"Fiyatı 100 TL'den yüksek ürünleri listele"
"Şehir bazında müşteri sayılarını göster"
```

## 🔒 Güvenlik

- Veriler geçici olarak bellekte tutulur
- Hassas bilgiler loglanmaz
- Kullanıcı verileri üçüncü taraflarla paylaşılmaz
- Dosya erişimi kontrollü şekilde yapılır
- Smithery API anahtarları güvenli şekilde saklanır

## 🌐 Environment Variables

```bash
# Smithery Configuration
SMITHERY_API_KEY=81c0c036-745e-42ae-9090-eebd33950d82
SMITHERY_PROFILE_KEY=probable-capybara-wWraCH

# Application Configuration
PYTHONPATH=/app
LOG_LEVEL=INFO
PORT=8000

# Data Analysis Configuration
MAX_FILE_SIZE=100MB
SUPPORTED_FORMATS=csv,xlsx,xls,json
DEFAULT_ENCODING=utf-8
```

## 🚀 Deployment

### Smithery Platform

1. **Otomatik Deploy**:
   ```bash
   ./deploy.sh
   ```

2. **Manuel Deploy**:
   - https://smithery.ai adresine gidin
   - API Key: `81c0c036-745e-42ae-9090-eebd33950d82`
   - Profile Key: `probable-capybara-wWraCH`
   - `smithery.yaml` dosyasını upload edin

### Docker Deployment

```bash
# Build
docker build -t data-analysis-agent .

# Run
docker run -p 8000:8000 \
  -e SMITHERY_API_KEY=81c0c036-745e-42ae-9090-eebd33950d82 \
  -e SMITHERY_PROFILE_KEY=probable-capybara-wWraCH \
  data-analysis-agent
```

## 🤝 Katkıda Bulunma

1. Repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 🆘 Destek

Sorularınız için:
- GitHub Issues açın
- Dokümantasyonu kontrol edin
- Örnek kullanımları inceleyin
- Smithery community'ye katılın

## 🔄 Sürüm Geçmişi

### v1.0.0
- İlk sürüm
- CSV, Excel, JSON desteği
- Temel istatistiksel analizler
- MCP entegrasyonu
- Türkçe dil desteği
- Smithery platform entegrasyonu 