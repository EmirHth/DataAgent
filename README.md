[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/emirhth-dataagent-badge.png)](https://mseep.ai/app/emirhth-dataagent)

# 🤖 DataAgent - AI Veri Analizi Sistemi

Bu proje, MCP (Model Context Protocol) tabanlı veri analizi AI agent'ı içerir.

## 📁 Proje Yapısı

```
DataAgent/
├── DataAnalysisAgent/     # MCP Server (Pure MCP Tools)
│   ├── server.py         # MCP Server Implementation
│   ├── app.py           # Standalone CLI App
│   ├── requirements.txt # Python Dependencies
│   └── smithery.yaml    # Smithery MCP Config
│
└── DataAgent-app/        # Mastra Client (AI Agent)
    ├── src/             # Mastra Agent Implementation
    ├── package.json     # Node.js Dependencies
    └── mastra.config.ts # Mastra Configuration
```

## 🚀 Smithery Deployment

### 1. MCP Server Deploy (DataAnalysisAgent)
```bash
cd DataAnalysisAgent
smithery deploy
```

### 2. Mastra App Deploy (DataAgent-app)
```bash
cd DataAgent-app
npm run build
# Deploy to your preferred platform
```

## 🔧 Local Development

### MCP Server:
```bash
cd DataAnalysisAgent
pip install -r requirements.txt
python server.py
```

### Mastra Client:
```bash
cd DataAgent-app
npm install
npm run dev
```

## 📊 Özellikler

- **6 MCP Tool**: load_data, analyze_data, get_data_info, filter_data, calculate_statistics, group_analysis
- **Multi-format Support**: CSV, Excel, JSON
- **Turkish Language**: Türkçe dil desteği
- **Statistical Analysis**: İstatistiksel analiz araçları
- **Data Filtering**: Gelişmiş veri filtreleme
- **Group Analysis**: Kategori bazında analiz

## 🌐 Smithery Integration

Bu proje Smithery MCP platformu ile entegre edilmiştir:
- MCP Server: `DataAnalysisAgent/smithery.yaml`
- Authentication: API Key tabanlı
- Tools: 6 adet veri analizi aracı

## 📋 Requirements

- Python 3.11+
- Node.js 18+
- Smithery CLI
- Git

---
**Version**: 1.0.0  
**License**: MIT  
**Author**: DataAgent Team 