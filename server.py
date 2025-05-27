#!/usr/bin/env python3
"""
Data Analysis MCP Server
Model Context Protocol server implementasyonu - Doğrudan MCP client bağlantısı için
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional, Sequence

import pandas as pd
import numpy as np
from mcp.server import Server
from mcp.server.models import InitializationOptions, NotificationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
from pydantic import AnyUrl

# Logging konfigürasyonu
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("data-analysis-mcp")

# Global veri depolama
current_data: Optional[pd.DataFrame] = None
data_info: Dict[str, Any] = {}

# MCP Server oluştur
server = Server("data-analysis-agent")

@server.list_resources()
async def handle_list_resources() -> List[Resource]:
    """Mevcut kaynakları listele"""
    resources = []
    
    if current_data is not None:
        resources.append(
            Resource(
                uri=AnyUrl("data://current-dataset"),
                name="Current Dataset",
                description="Şu anda yüklü olan veri seti",
                mimeType="application/json"
            )
        )
        
        resources.append(
            Resource(
                uri=AnyUrl("data://data-summary"),
                name="Data Summary",
                description="Veri seti özet bilgileri",
                mimeType="text/plain"
            )
        )
    
    return resources

@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """Kaynak okuma"""
    if uri.scheme != "data":
        raise ValueError(f"Desteklenmeyen URI şeması: {uri.scheme}")
    
    if str(uri) == "data://current-dataset":
        if current_data is None:
            raise ValueError("Henüz veri yüklenmedi")
        return current_data.to_json(orient="records", indent=2)
    
    elif str(uri) == "data://data-summary":
        if current_data is None:
            raise ValueError("Henüz veri yüklenmedi")
        return generate_data_summary()
    
    else:
        raise ValueError(f"Bilinmeyen kaynak: {uri}")

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """Mevcut araçları listele"""
    return [
        Tool(
            name="load_data",
            description="CSV, Excel veya JSON formatında veri dosyası yükler",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Yüklenecek dosyanın yolu"
                    },
                    "file_content": {
                        "type": "string",
                        "description": "Dosya içeriği (base64 encoded)"
                    }
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="analyze_data",
            description="Yüklü veri üzerinde analiz yapar",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Analiz sorusu veya komutu"
                    },
                    "analysis_type": {
                        "type": "string",
                        "enum": ["summary", "statistics", "filter", "group", "trend", "visualization"],
                        "description": "Analiz türü"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_data_info",
            description="Yüklü verinin genel bilgilerini döndürür",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        ),
        Tool(
            name="filter_data",
            description="Veriyi belirli kriterlere göre filtreler",
            inputSchema={
                "type": "object",
                "properties": {
                    "column": {
                        "type": "string",
                        "description": "Filtrelenecek sütun adı"
                    },
                    "operator": {
                        "type": "string",
                        "enum": ["==", "!=", ">", "<", ">=", "<=", "contains", "startswith", "endswith"],
                        "description": "Filtreleme operatörü"
                    },
                    "value": {
                        "type": ["string", "number"],
                        "description": "Filtreleme değeri"
                    }
                },
                "required": ["column", "operator", "value"]
            }
        ),
        Tool(
            name="calculate_statistics",
            description="Sayısal sütunlar için istatistiksel hesaplamalar yapar",
            inputSchema={
                "type": "object",
                "properties": {
                    "columns": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "İstatistik hesaplanacak sütunlar"
                    },
                    "operation": {
                        "type": "string",
                        "enum": ["mean", "median", "sum", "min", "max", "std", "var", "count"],
                        "description": "İstatistiksel işlem"
                    }
                },
                "required": ["operation"]
            }
        ),
        Tool(
            name="group_analysis",
            description="Veriyi gruplara ayırarak analiz yapar",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_by": {
                        "type": "string",
                        "description": "Gruplama yapılacak sütun"
                    },
                    "agg_column": {
                        "type": "string",
                        "description": "Agregasyon yapılacak sütun"
                    },
                    "agg_function": {
                        "type": "string",
                        "enum": ["sum", "mean", "count", "min", "max"],
                        "description": "Agregasyon fonksiyonu"
                    }
                },
                "required": ["group_by"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Araç çağrılarını işle"""
    global current_data, data_info
    
    try:
        if name == "load_data":
            file_path = arguments.get("file_path", "")
            
            # Dosya yükleme
            try:
                file_extension = os.path.splitext(file_path)[1].lower()
                
                if file_extension == '.csv':
                    current_data = pd.read_csv(file_path)
                elif file_extension in ['.xlsx', '.xls']:
                    current_data = pd.read_excel(file_path)
                elif file_extension == '.json':
                    current_data = pd.read_json(file_path)
                else:
                    return [TextContent(
                        type="text",
                        text=f"❌ Desteklenmeyen dosya formatı: {file_extension}"
                    )]
                
                # Veri analizi
                analyze_data_structure()
                
                return [TextContent(
                    type="text",
                    text=f"✅ Veri başarıyla yüklendi!\n\n{generate_data_summary()}"
                )]
                
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"❌ Veri yükleme hatası: {str(e)}"
                )]
        
        elif name == "analyze_data":
            if current_data is None:
                return [TextContent(
                    type="text",
                    text="❌ Önce veri yüklemelisiniz!"
                )]
            
            query = arguments.get("query", "")
            analysis_type = arguments.get("analysis_type", "summary")
            
            result = analyze_query(query, analysis_type)
            
            return [TextContent(
                type="text",
                text=result
            )]
        
        elif name == "get_data_info":
            if current_data is None:
                return [TextContent(
                    type="text",
                    text="❌ Henüz veri yüklenmedi!"
                )]
            
            return [TextContent(
                type="text",
                text=generate_data_summary()
            )]
        
        elif name == "filter_data":
            if current_data is None:
                return [TextContent(
                    type="text",
                    text="❌ Önce veri yüklemelisiniz!"
                )]
            
            column = arguments.get("column")
            operator = arguments.get("operator")
            value = arguments.get("value")
            
            result = filter_data(column, operator, value)
            
            return [TextContent(
                type="text",
                text=result
            )]
        
        elif name == "calculate_statistics":
            if current_data is None:
                return [TextContent(
                    type="text",
                    text="❌ Önce veri yüklemelisiniz!"
                )]
            
            columns = arguments.get("columns", [])
            operation = arguments.get("operation")
            
            result = calculate_statistics(columns, operation)
            
            return [TextContent(
                type="text",
                text=result
            )]
        
        elif name == "group_analysis":
            if current_data is None:
                return [TextContent(
                    type="text",
                    text="❌ Önce veri yüklemelisiniz!"
                )]
            
            group_by = arguments.get("group_by")
            agg_column = arguments.get("agg_column")
            agg_function = arguments.get("agg_function", "count")
            
            result = group_analysis(group_by, agg_column, agg_function)
            
            return [TextContent(
                type="text",
                text=result
            )]
        
        else:
            return [TextContent(
                type="text",
                text=f"❌ Bilinmeyen araç: {name}"
            )]
    
    except Exception as e:
        logger.error(f"Araç çağrısı hatası: {str(e)}")
        return [TextContent(
            type="text",
            text=f"❌ Hata oluştu: {str(e)}"
        )]

def analyze_data_structure():
    """Veri yapısını analiz eder"""
    global data_info
    
    if current_data is None:
        return
    
    data_info = {
        'shape': current_data.shape,
        'columns': list(current_data.columns),
        'dtypes': current_data.dtypes.to_dict(),
        'null_counts': current_data.isnull().sum().to_dict(),
        'memory_usage': current_data.memory_usage(deep=True).sum(),
        'numeric_columns': list(current_data.select_dtypes(include=[np.number]).columns),
        'categorical_columns': list(current_data.select_dtypes(include=['object']).columns),
        'summary_stats': current_data.describe().to_dict() if not current_data.empty else {}
    }

def generate_data_summary() -> str:
    """Veri özetini oluşturur"""
    if current_data is None or not data_info:
        return "Henüz veri yüklenmedi."
    
    summary = f"""
## 📊 Veri Özeti

**Boyut:** {data_info['shape'][0]:,} satır, {data_info['shape'][1]} sütun
**Bellek Kullanımı:** {data_info['memory_usage'] / 1024 / 1024:.2f} MB

### Sütunlar:
{', '.join(data_info['columns'])}

### Veri Tipleri:
"""
    
    for col, dtype in data_info['dtypes'].items():
        null_count = data_info['null_counts'][col]
        null_percent = (null_count / data_info['shape'][0]) * 100
        summary += f"- **{col}:** {dtype} (Eksik: {null_count} - %{null_percent:.1f})\n"
    
    if data_info['numeric_columns']:
        summary += f"\n### 🔢 Sayısal Sütunlar ({len(data_info['numeric_columns'])} adet):\n"
        summary += f"{', '.join(data_info['numeric_columns'])}\n"
    
    if data_info['categorical_columns']:
        summary += f"\n### 📝 Kategorik Sütunlar ({len(data_info['categorical_columns'])} adet):\n"
        summary += f"{', '.join(data_info['categorical_columns'])}\n"
    
    return summary

def analyze_query(query: str, analysis_type: str = "summary") -> str:
    """Sorgu analizi yapar"""
    query_lower = query.lower()
    
    if analysis_type == "summary" or any(word in query_lower for word in ['özet', 'summary', 'genel']):
        return generate_data_summary()
    
    elif analysis_type == "statistics" or any(word in query_lower for word in ['istatistik', 'statistics']):
        return generate_statistics_summary()
    
    elif any(word in query_lower for word in ['en çok', 'en yüksek', 'maksimum', 'max']):
        return find_maximum_values()
    
    elif any(word in query_lower for word in ['en az', 'en düşük', 'minimum', 'min']):
        return find_minimum_values()
    
    elif any(word in query_lower for word in ['toplam', 'sum', 'total']):
        return calculate_totals()
    
    elif any(word in query_lower for word in ['ortalama', 'average', 'mean']):
        return calculate_averages()
    
    else:
        return f"""
## 🤔 Sorgu Analizi

Sorunuz: "{query}"

Bu sorgu için daha spesifik bilgi verebilmem için lütfen şunları belirtin:

1. **Hangi sütun(lar)** ile ilgili analiz istiyorsunuz?
2. **Nasıl bir analiz türü?** (özet, karşılaştırma, trend, vb.)
3. **Belirli bir filtreleme kriteri** var mı?

**Mevcut Sütunlar:** {', '.join(data_info['columns'])}

### Örnek Sorular:
- "Satış sütunundaki en yüksek değer nedir?"
- "Kategori bazında ortalama fiyatları göster"
- "2023 verilerini filtrele"
"""

def filter_data(column: str, operator: str, value: Any) -> str:
    """Veri filtreleme"""
    try:
        if column not in current_data.columns:
            return f"❌ '{column}' sütunu bulunamadı!"
        
        if operator == "==":
            filtered_data = current_data[current_data[column] == value]
        elif operator == "!=":
            filtered_data = current_data[current_data[column] != value]
        elif operator == ">":
            filtered_data = current_data[current_data[column] > value]
        elif operator == "<":
            filtered_data = current_data[current_data[column] < value]
        elif operator == ">=":
            filtered_data = current_data[current_data[column] >= value]
        elif operator == "<=":
            filtered_data = current_data[current_data[column] <= value]
        elif operator == "contains":
            filtered_data = current_data[current_data[column].astype(str).str.contains(str(value), na=False)]
        elif operator == "startswith":
            filtered_data = current_data[current_data[column].astype(str).str.startswith(str(value), na=False)]
        elif operator == "endswith":
            filtered_data = current_data[current_data[column].astype(str).str.endswith(str(value), na=False)]
        else:
            return f"❌ Desteklenmeyen operatör: {operator}"
        
        result = f"""
## 🔍 Filtreleme Sonucu

**Filtre:** {column} {operator} {value}
**Sonuç:** {len(filtered_data)} satır bulundu (Toplam: {len(current_data)})

### İlk 10 Sonuç:
"""
        
        if len(filtered_data) > 0:
            result += filtered_data.head(10).to_string(index=False)
        else:
            result += "Hiç sonuç bulunamadı."
        
        return result
        
    except Exception as e:
        return f"❌ Filtreleme hatası: {str(e)}"

def calculate_statistics(columns: List[str], operation: str) -> str:
    """İstatistik hesaplama"""
    try:
        if not columns:
            columns = data_info['numeric_columns']
        
        if not columns:
            return "❌ Sayısal sütun bulunamadı!"
        
        result = f"## 📈 İstatistik Sonuçları ({operation.upper()})\n\n"
        
        for col in columns:
            if col not in current_data.columns:
                result += f"❌ '{col}' sütunu bulunamadı!\n"
                continue
            
            if col not in data_info['numeric_columns']:
                result += f"⚠️ '{col}' sayısal bir sütun değil!\n"
                continue
            
            if operation == "mean":
                value = current_data[col].mean()
            elif operation == "median":
                value = current_data[col].median()
            elif operation == "sum":
                value = current_data[col].sum()
            elif operation == "min":
                value = current_data[col].min()
            elif operation == "max":
                value = current_data[col].max()
            elif operation == "std":
                value = current_data[col].std()
            elif operation == "var":
                value = current_data[col].var()
            elif operation == "count":
                value = current_data[col].count()
            else:
                result += f"❌ Desteklenmeyen işlem: {operation}\n"
                continue
            
            result += f"**{col}:** {value:,.2f}\n"
        
        return result
        
    except Exception as e:
        return f"❌ İstatistik hesaplama hatası: {str(e)}"

def group_analysis(group_by: str, agg_column: str = None, agg_function: str = "count") -> str:
    """Grup analizi"""
    try:
        if group_by not in current_data.columns:
            return f"❌ '{group_by}' sütunu bulunamadı!"
        
        if agg_column and agg_column not in current_data.columns:
            return f"❌ '{agg_column}' sütunu bulunamadı!"
        
        if agg_column:
            if agg_function == "sum":
                grouped = current_data.groupby(group_by)[agg_column].sum()
            elif agg_function == "mean":
                grouped = current_data.groupby(group_by)[agg_column].mean()
            elif agg_function == "count":
                grouped = current_data.groupby(group_by)[agg_column].count()
            elif agg_function == "min":
                grouped = current_data.groupby(group_by)[agg_column].min()
            elif agg_function == "max":
                grouped = current_data.groupby(group_by)[agg_column].max()
            else:
                return f"❌ Desteklenmeyen agregasyon fonksiyonu: {agg_function}"
        else:
            grouped = current_data.groupby(group_by).size()
            agg_function = "count"
        
        result = f"""
## 📊 Grup Analizi

**Gruplama:** {group_by}
**Agregasyon:** {agg_function}
{f"**Sütun:** {agg_column}" if agg_column else ""}

### Sonuçlar:
"""
        
        for group, value in grouped.head(20).items():
            result += f"- **{group}:** {value:,.2f}\n"
        
        if len(grouped) > 20:
            result += f"\n... ve {len(grouped) - 20} grup daha"
        
        return result
        
    except Exception as e:
        return f"❌ Grup analizi hatası: {str(e)}"

def generate_statistics_summary() -> str:
    """İstatistik özeti"""
    if not data_info['numeric_columns']:
        return "❌ Sayısal sütun bulunamadı!"
    
    result = "## 📈 İstatistiksel Özet\n\n"
    
    for col in data_info['numeric_columns']:
        stats = current_data[col].describe()
        result += f"### {col}\n"
        result += f"- **Ortalama:** {stats['mean']:.2f}\n"
        result += f"- **Medyan:** {stats['50%']:.2f}\n"
        result += f"- **Standart Sapma:** {stats['std']:.2f}\n"
        result += f"- **Min:** {stats['min']:.2f}\n"
        result += f"- **Max:** {stats['max']:.2f}\n\n"
    
    return result

def find_maximum_values() -> str:
    """En yüksek değerleri bulur"""
    if not data_info['numeric_columns']:
        return "❌ Sayısal sütun bulunamadı!"
    
    result = "## 🔝 En Yüksek Değerler\n\n"
    for col in data_info['numeric_columns']:
        max_val = current_data[col].max()
        max_idx = current_data[col].idxmax()
        result += f"**{col}:** {max_val:,.2f} (Satır: {max_idx + 1})\n"
    
    return result

def find_minimum_values() -> str:
    """En düşük değerleri bulur"""
    if not data_info['numeric_columns']:
        return "❌ Sayısal sütun bulunamadı!"
    
    result = "## 🔻 En Düşük Değerler\n\n"
    for col in data_info['numeric_columns']:
        min_val = current_data[col].min()
        min_idx = current_data[col].idxmin()
        result += f"**{col}:** {min_val:,.2f} (Satır: {min_idx + 1})\n"
    
    return result

def calculate_totals() -> str:
    """Toplam değerleri hesaplar"""
    if not data_info['numeric_columns']:
        return "❌ Sayısal sütun bulunamadı!"
    
    result = "## ➕ Toplam Değerler\n\n"
    for col in data_info['numeric_columns']:
        total = current_data[col].sum()
        result += f"**{col}:** {total:,.2f}\n"
    
    return result

def calculate_averages() -> str:
    """Ortalama değerleri hesaplar"""
    if not data_info['numeric_columns']:
        return "❌ Sayısal sütun bulunamadı!"
    
    result = "## 📊 Ortalama Değerler\n\n"
    for col in data_info['numeric_columns']:
        avg = current_data[col].mean()
        result += f"**{col}:** {avg:.2f}\n"
    
    return result

async def main():
    """Ana server fonksiyonu"""
    # Server'ı stdio ile başlat
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="data-analysis-agent",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(
                        tools_changed=False,
                        resources_changed=False
                    ),
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main()) 