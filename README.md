# 運氣突擊隊 AI 自動戰鬥系統

## 📋 專案說明

這是一個基於圖像識別和強化學習的遊戲 AI 系統，能夠自動學習並優化「運氣突擊隊」的戰鬥策略。

---

## 🏗️ 專案結構

```
luck-raiders-ai-bot/
├── src/                    # 原始碼
│   ├── capture/           # 螢幕擷取模組
│   ├── vision/            # 圖像識別模組
│   ├── ai/                # AI 決策引擎
│   └── automation/        # 自動化操作模組
├── data/                   # 資料目錄
│   ├── screenshots/       # 遊戲截圖
│   ├── training/          # 訓練資料
│   └── models/            # 訓練好的模型
├── logs/                   # 日誌記錄
├── configs/               # 配置檔案
├── tests/                 # 測試腳本
└── requirements.txt       # Python 套件依賴
```

---

## 🚀 快速開始

### 1. 建立虛擬環境
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 2. 安裝依賴套件
```bash
pip install -r requirements.txt
```

### 3. 驗證 CUDA 是否可用
```bash
python tests/test_cuda.py
```

### 4. 執行第一個測試
```bash
python tests/test_screen_capture.py
```

---

## 📚 開發階段

- [x] Phase 0: 專案初始化
- [ ] Phase 1: 環境建置與驗證
- [ ] Phase 2: 基礎自動化
- [ ] Phase 3: 圖像識別
- [ ] Phase 4: AI 訓練
- [ ] Phase 5: 優化與測試

---

## 🔧 系統需求（已符合）

- ✅ CPU: AMD Ryzen 5 3600
- ✅ GPU: NVIDIA GTX 1650 (4GB)
- ✅ RAM: 16GB
- ✅ Python: 3.14.0
- ✅ CUDA: 支援

---

## ⚠️ 注意事項

> [!WARNING]
> 此工具僅供技術學習使用，請勿用於違反遊戲服務條款的行為。

---

## 📞 技術支援

詳細技術文件請參考：
- [技術規劃](../運氣突擊隊AI外掛技術規劃.md)
- [系統規格分析](../system_spec_analysis.md)

---

## 📅 開發時間表

預計開發時間：4 個月（2026/01 - 2026/04）

當前階段：**Phase 0 - 專案初始化** ✅
