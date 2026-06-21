#!/bin/bash

# تلوين المخرجات في التيرمنال
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting NETGITS Quiz Setup Process...${NC}"

# 1. التحقق من وجود بايثون
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}📦 Python3 is not installed. Trying to install...${NC}"
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install python3 python3-pip python3-venv -y
    else
        echo -e "${RED}❌ Could not install Python automatically. Please install Python 3.8+ manually.${NC}"
        exit 1
    fi
fi

# 2. إنشاء البيئة الوهمية (Virtual Environment)
echo -e "${BLUE}📦 Creating Python Virtual Environment (venv)...${NC}"
python3 -m venv venv

# 3. تفعيل البيئة الوهمية
source venv/bin/activate

# 4. تحديث pip وتثبيت المتطلبات
echo -e "${BLUE}⚙️ Installing required dependencies (PyQt6)...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# 5. تشغيل التطبيق بنجاح
echo -e "${GREEN}✅ Setup complete! Launching NETGITS Quiz (source.py)...${NC}"
python3 source.py
