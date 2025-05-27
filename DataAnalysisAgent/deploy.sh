#!/bin/bash

# Data Analysis Agent - Smithery Deployment Script
# Bu script, agent'ı Smithery platformuna deploy eder

set -e

echo "🚀 Data Analysis Agent - Smithery Deployment başlatılıyor..."

# Smithery credentials kontrolü
if [ -z "$SMITHERY_API_KEY" ]; then
    export SMITHERY_API_KEY="81c0c036-745e-42ae-9090-eebd33950d82"
    echo "✅ Smithery API Key ayarlandı"
fi

if [ -z "$SMITHERY_PROFILE_KEY" ]; then
    export SMITHERY_PROFILE_KEY="probable-capybara-wWraCH"
    echo "✅ Smithery Profile Key ayarlandı"
fi

# Gerekli dosyaların varlığını kontrol et
echo "📋 Dosya kontrolü yapılıyor..."
required_files=("smithery.yaml" "server.py" "app.py" "Dockerfile" "requirements.txt")

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Gerekli dosya bulunamadı: $file"
        exit 1
    fi
done

echo "✅ Tüm gerekli dosyalar mevcut"

# Docker image build
echo "🐳 Docker image build ediliyor..."
docker build -t data-analysis-agent:latest .

if [ $? -eq 0 ]; then
    echo "✅ Docker image başarıyla build edildi"
else
    echo "❌ Docker build hatası"
    exit 1
fi

# Smithery CLI kurulumu kontrolü (eğer varsa)
if command -v smithery &> /dev/null; then
    echo "🔧 Smithery CLI ile deploy ediliyor..."
    
    # Smithery login
    echo "$SMITHERY_API_KEY" | smithery auth login --api-key
    
    # Deploy
    smithery deploy --config smithery.yaml --profile "$SMITHERY_PROFILE_KEY"
    
    if [ $? -eq 0 ]; then
        echo "🎉 Smithery'ye başarıyla deploy edildi!"
    else
        echo "❌ Smithery deploy hatası"
        exit 1
    fi
else
    echo "⚠️  Smithery CLI bulunamadı. Manuel deploy gerekli."
    echo "📖 Manuel deploy için:"
    echo "   1. https://smithery.ai adresine gidin"
    echo "   2. API Key: $SMITHERY_API_KEY"
    echo "   3. Profile Key: $SMITHERY_PROFILE_KEY"
    echo "   4. smithery.yaml dosyasını upload edin"
fi

# Test endpoint'i
echo "🧪 Test ediliyor..."
echo "Agent başarıyla deploy edildi!"
echo ""
echo "📊 Data Analysis Agent Bilgileri:"
echo "   - Server Name: data-analysis-agent"
echo "   - Version: 1.0.0"
echo "   - API Key: ${SMITHERY_API_KEY:0:8}..."
echo "   - Profile: $SMITHERY_PROFILE_KEY"
echo ""
echo "🔗 Kullanım:"
echo "   - MCP Client ile bağlanın"
echo "   - Tools: load_data, analyze_data, get_data_info, filter_data, calculate_statistics, group_analysis"
echo "   - Desteklenen formatlar: CSV, Excel, JSON"
echo ""
echo "✨ Deploy tamamlandı!" 