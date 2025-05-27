# 🚀 DataAgent Deployment Guide

## ✅ Deployment Status

### 1. MCP Server (DataAnalysisAgent)
- **Status**: ✅ DEPLOYED & RUNNING
- **Location**: `C:\Users\EmirTh\Desktop\DataAgent\DataAnalysisAgent\`
- **Command**: `python server.py`
- **Protocol**: stdio (MCP)
- **Tools**: 6 adet veri analizi aracı

### 2. Mastra Client (DataAgent-app)
- **Status**: ✅ DEPLOYED & RUNNING
- **Location**: `C:\Users\EmirTh\Desktop\DataAgent\DataAgent-app\`
- **Build**: ✅ Production build tamamlandı
- **Command**: `npm start`
- **Framework**: Mastra v0.10.0

### 3. Standalone App (DataAnalysisAgent)
- **Status**: ✅ READY
- **Location**: `C:\Users\EmirTh\Desktop\DataAgent\DataAnalysisAgent\`
- **Command**: `python app.py`
- **Interface**: Interactive CLI

## 🔧 Production Commands

### MCP Server Başlatma:
```bash
cd DataAnalysisAgent
python server.py
```

### Mastra App Başlatma:
```bash
cd DataAgent-app
npm start
```

### Standalone App Başlatma:
```bash
cd DataAnalysisAgent
python app.py
```

## 📊 Test Data

Test için `test_data.csv` dosyası oluşturuldu:
- 10 satır örnek veri
- Electronics ve Furniture kategorileri
- Sales, price, name sütunları

## 🎯 Kullanım Örnekleri

### Standalone App Test:
```
load test_data.csv
Bu tabloda en çok satış yapan ürün hangisi?
Kategori bazında toplam satışları göster
```

### MCP Tools Test:
```json
{
  "tool": "load_data",
  "args": {"file_path": "test_data.csv"}
}

{
  "tool": "analyze_data", 
  "args": {"query": "En yüksek fiyatlı ürün hangisi?"}
}
```

## 🌐 Production URLs

- **MCP Server**: stdio://localhost (process communication)
- **Mastra App**: Local Mastra instance
- **Standalone App**: CLI interface

## 📋 Health Check

Tüm servisler çalışıyor durumda:
- ✅ Python dependencies yüklü
- ✅ Node.js dependencies yüklü  
- ✅ MCP server aktif
- ✅ Mastra app production build
- ✅ Test data hazır

## 🔄 Restart Commands

```bash
# MCP Server restart
cd DataAnalysisAgent
python server.py

# Mastra App restart  
cd DataAgent-app
npm start

# Full system restart
# 1. Stop all processes
# 2. Run MCP server
# 3. Run Mastra app
```

## 📈 Monitoring

- MCP server logs: Console output
- Mastra app logs: Mastra CLI output
- Error handling: Built-in exception handling

---
**Deployment Date**: 2025-05-27
**Status**: ✅ PRODUCTION READY 