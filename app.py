#!/usr/bin/env python3
"""
Data Analysis Agent - Veri Tablolu Sorgulama ve Yorumlama AI Agent'ı
Smithery MCP entegrasyonu ile birlikte çalışır.
"""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd
import numpy as np
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Smithery Configuration
SMITHERY_API_KEY = os.getenv("SMITHERY_API_KEY", "81c0c036-745e-42ae-9090-eebd33950d82")
SMITHERY_PROFILE_KEY = os.getenv("SMITHERY_PROFILE_KEY", "probable-capybara-wWraCH")

def get_smithery_config() -> Dict[str, str]:
    """Smithery konfigürasyonunu döndürür"""
    return {
        "api_key": SMITHERY_API_KEY,
        "profile_key": SMITHERY_PROFILE_KEY,
        "server_name": "data-analysis-agent",
        "version": "1.0.0"
    }

class DataAnalysisAgent:
    """
    Veri Analisti AI Agent'ı
    
    Bu agent, kullanıcı tarafından verilen tabloları analiz ederek
    soruları yanıtlar ve veri yorumlaması yapar.
    """
    
    def __init__(self):
        self.current_data: Optional[pd.DataFrame] = None
        self.data_info: Dict[str, Any] = {}
        self.analysis_history: List[Dict[str, Any]] = []
        self.smithery_config = get_smithery_config()
        
        # Smithery bağlantı bilgilerini logla
        logger.info(f"Smithery API Key: {SMITHERY_API_KEY[:8]}...")
        logger.info(f"Smithery Profile Key: {SMITHERY_PROFILE_KEY}")
        
    def load_data(self, file_path: str) -> bool:
        """
        Veri dosyasını yükler (CSV, Excel, JSON)
        
        Args:
            file_path: Dosya yolu
            
        Returns:
            bool: Yükleme başarılı mı
        """
        try:
            file_extension = Path(file_path).suffix.lower()
            
            if file_extension == '.csv':
                self.current_data = pd.read_csv(file_path)
            elif file_extension in ['.xlsx', '.xls']:
                self.current_data = pd.read_excel(file_path)
            elif file_extension == '.json':
                self.current_data = pd.read_json(file_path)
            else:
                logger.error(f"Desteklenmeyen dosya formatı: {file_extension}")
                return False
                
            self._analyze_data_structure()
            logger.info(f"Veri başarıyla yüklendi: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Veri yükleme hatası: {str(e)}")
            return False
    
    def _analyze_data_structure(self):
        """Veri yapısını analiz eder"""
        if self.current_data is None:
            return
            
        self.data_info = {
            'shape': self.current_data.shape,
            'columns': list(self.current_data.columns),
            'dtypes': self.current_data.dtypes.to_dict(),
            'null_counts': self.current_data.isnull().sum().to_dict(),
            'memory_usage': self.current_data.memory_usage(deep=True).sum(),
            'numeric_columns': list(self.current_data.select_dtypes(include=[np.number]).columns),
            'categorical_columns': list(self.current_data.select_dtypes(include=['object']).columns),
            'summary_stats': self.current_data.describe().to_dict() if not self.current_data.empty else {}
        }
    
    def get_data_summary(self) -> str:
        """Veri özetini döndürür"""
        if self.current_data is None:
            return "Henüz veri yüklenmedi."
            
        summary = f"""
## Veri Özeti

**Boyut:** {self.data_info['shape'][0]} satır, {self.data_info['shape'][1]} sütun

**Sütunlar:**
{', '.join(self.data_info['columns'])}

**Veri Tipleri:**
"""
        for col, dtype in self.data_info['dtypes'].items():
            null_count = self.data_info['null_counts'][col]
            summary += f"- {col}: {dtype} (Eksik değer: {null_count})\n"
            
        if self.data_info['numeric_columns']:
            summary += f"\n**Sayısal Sütunlar:** {', '.join(self.data_info['numeric_columns'])}"
            
        if self.data_info['categorical_columns']:
            summary += f"\n**Kategorik Sütunlar:** {', '.join(self.data_info['categorical_columns'])}"
            
        return summary
    
    def analyze_query(self, query: str) -> str:
        """
        Kullanıcı sorgusunu analiz eder ve yanıtlar
        
        Args:
            query: Kullanıcı sorusu
            
        Returns:
            str: Analiz sonucu
        """
        if self.current_data is None:
            return "Lütfen önce bir veri dosyası yükleyin."
            
        query_lower = query.lower()
        
        try:
            # Farklı sorgu tiplerini analiz et
            if any(word in query_lower for word in ['özet', 'summary', 'genel', 'bilgi']):
                return self.get_data_summary()
                
            elif any(word in query_lower for word in ['en çok', 'en yüksek', 'maksimum', 'max']):
                return self._find_maximum_values(query)
                
            elif any(word in query_lower for word in ['en az', 'en düşük', 'minimum', 'min']):
                return self._find_minimum_values(query)
                
            elif any(word in query_lower for word in ['toplam', 'sum', 'total']):
                return self._calculate_totals(query)
                
            elif any(word in query_lower for word in ['ortalama', 'average', 'mean']):
                return self._calculate_averages(query)
                
            elif any(word in query_lower for word in ['filtrele', 'filter', 'şart', 'koşul']):
                return self._filter_data(query)
                
            elif any(word in query_lower for word in ['grup', 'group', 'kategori']):
                return self._group_analysis(query)
                
            elif any(word in query_lower for word in ['trend', 'değişim', 'zaman']):
                return self._trend_analysis(query)
                
            elif any(word in query_lower for word in ['görselleştir', 'grafik', 'chart']):
                return self._visualization_suggestions(query)
                
            else:
                return self._general_analysis(query)
                
        except Exception as e:
            logger.error(f"Sorgu analiz hatası: {str(e)}")
            return f"Sorgu analiz edilirken hata oluştu: {str(e)}"
    
    def _find_maximum_values(self, query: str) -> str:
        """En yüksek değerleri bulur"""
        numeric_cols = self.data_info['numeric_columns']
        if not numeric_cols:
            return "Veri setinde sayısal sütun bulunamadı."
            
        result = "## En Yüksek Değerler\n\n"
        for col in numeric_cols:
            max_val = self.current_data[col].max()
            max_idx = self.current_data[col].idxmax()
            result += f"**{col}:** {max_val} (Satır: {max_idx + 1})\n"
            
        return result
    
    def _find_minimum_values(self, query: str) -> str:
        """En düşük değerleri bulur"""
        numeric_cols = self.data_info['numeric_columns']
        if not numeric_cols:
            return "Veri setinde sayısal sütun bulunamadı."
            
        result = "## En Düşük Değerler\n\n"
        for col in numeric_cols:
            min_val = self.current_data[col].min()
            min_idx = self.current_data[col].idxmin()
            result += f"**{col}:** {min_val} (Satır: {min_idx + 1})\n"
            
        return result
    
    def _calculate_totals(self, query: str) -> str:
        """Toplam değerleri hesaplar"""
        numeric_cols = self.data_info['numeric_columns']
        if not numeric_cols:
            return "Veri setinde sayısal sütun bulunamadı."
            
        result = "## Toplam Değerler\n\n"
        for col in numeric_cols:
            total = self.current_data[col].sum()
            result += f"**{col}:** {total:,.2f}\n"
            
        return result
    
    def _calculate_averages(self, query: str) -> str:
        """Ortalama değerleri hesaplar"""
        numeric_cols = self.data_info['numeric_columns']
        if not numeric_cols:
            return "Veri setinde sayısal sütun bulunamadı."
            
        result = "## Ortalama Değerler\n\n"
        for col in numeric_cols:
            avg = self.current_data[col].mean()
            result += f"**{col}:** {avg:.2f}\n"
            
        return result
    
    def _filter_data(self, query: str) -> str:
        """Veri filtreleme önerileri"""
        return """
## Veri Filtreleme Önerileri

Veri filtrelemek için şu formatları kullanabilirsiniz:
- "X sütununda Y değerinden büyük olanları göster"
- "Z kategorisindeki kayıtları listele"
- "Belirli tarih aralığındaki verileri filtrele"

Lütfen daha spesifik bir filtreleme kriteri belirtin.
"""
    
    def _group_analysis(self, query: str) -> str:
        """Grup analizi yapar"""
        categorical_cols = self.data_info['categorical_columns']
        if not categorical_cols:
            return "Veri setinde kategorik sütun bulunamadı."
            
        result = "## Kategori Analizi\n\n"
        for col in categorical_cols[:3]:  # İlk 3 kategorik sütun
            value_counts = self.current_data[col].value_counts().head(5)
            result += f"**{col} Dağılımı:**\n"
            for value, count in value_counts.items():
                result += f"- {value}: {count} adet\n"
            result += "\n"
            
        return result
    
    def _trend_analysis(self, query: str) -> str:
        """Trend analizi önerileri"""
        return """
## Trend Analizi Önerileri

Trend analizi için:
1. Zaman serisi verileriniz varsa tarih sütununu belirtin
2. Hangi metriğin trendini görmek istediğinizi söyleyin
3. Dönemsel analiz (aylık, yıllık) tercihlerinizi belirtin

Örnek: "2023 yılındaki aylık satış trendini göster"
"""
    
    def _visualization_suggestions(self, query: str) -> str:
        """Görselleştirme önerileri"""
        suggestions = "## Görselleştirme Önerileri\n\n"
        
        if self.data_info['numeric_columns']:
            suggestions += "**Sayısal Veriler için:**\n"
            suggestions += "- Histogram: Dağılım analizi\n"
            suggestions += "- Box Plot: Aykırı değer tespiti\n"
            suggestions += "- Scatter Plot: İlişki analizi\n\n"
            
        if self.data_info['categorical_columns']:
            suggestions += "**Kategorik Veriler için:**\n"
            suggestions += "- Bar Chart: Kategori karşılaştırması\n"
            suggestions += "- Pie Chart: Oran analizi\n\n"
            
        suggestions += "Hangi tür grafik istediğinizi belirtin."
        return suggestions
    
    def _general_analysis(self, query: str) -> str:
        """Genel analiz"""
        return f"""
## Genel Veri Analizi

Sorunuz için daha spesifik bilgi verebilmem için lütfen şunları belirtin:

1. Hangi sütun(lar) ile ilgili analiz istiyorsunuz?
2. Nasıl bir analiz türü? (özet, karşılaştırma, trend, vb.)
3. Belirli bir filtreleme kriteri var mı?

**Mevcut Sütunlar:** {', '.join(self.data_info['columns'])}

Örnek sorular:
- "Satış sütunundaki en yüksek değer nedir?"
- "Kategori bazında ortalama fiyatları göster"
- "2023 verilerini filtrele"
"""

async def main():
    """Ana uygulama fonksiyonu"""
    agent = DataAnalysisAgent()
    
    print("🔍 Data Analysis Agent başlatıldı!")
    print("Veri dosyası yüklemek için 'load <dosya_yolu>' komutunu kullanın.")
    print("Çıkmak için 'quit' yazın.\n")
    
    while True:
        try:
            user_input = input("📊 Soru/Komut: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'çık']:
                print("👋 Data Analysis Agent kapatılıyor...")
                break
                
            elif user_input.lower().startswith('load '):
                file_path = user_input[5:].strip()
                if agent.load_data(file_path):
                    print("✅ Veri başarıyla yüklendi!")
                    print(agent.get_data_summary())
                else:
                    print("❌ Veri yüklenemedi!")
                    
            elif user_input:
                response = agent.analyze_query(user_input)
                print(f"\n📈 Analiz Sonucu:\n{response}\n")
                
        except KeyboardInterrupt:
            print("\n👋 Data Analysis Agent kapatılıyor...")
            break
        except Exception as e:
            logger.error(f"Uygulama hatası: {str(e)}")
            print(f"❌ Hata oluştu: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 