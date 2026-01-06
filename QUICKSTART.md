# 🚀 快速啟動指南

## 第一次使用？跟著這個指南立即開始！

---

## ⚡ 5 分鐘快速啟動

### 📍 Step 1: 打開 PowerShell 並切換目錄

```powershell
cd D:\cheat\luck-raiders-ai-bot
```

### 📍 Step 2: 建立虛擬環境（建議）

```powershell
# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
.\venv\Scripts\activate

# 此時你的命令提示符應該會顯示 (venv)
```

### 📍 Step 3: 安裝 PyTorch (CUDA 支援)

```powershell
# 重要！必須先安裝 PyTorch CUDA 版本
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

⏱️ 預計時間: 2-5 分鐘（取決於網速）

### 📍 Step 4: 安裝其他套件

```powershell
pip install -r requirements.txt
```

⏱️ 預計時間: 2-3 分鐘

### 📍 Step 5: 驗證安裝

```powershell
python tests/test_cuda.py
```

✅ 如果看到「所有測試通過」，恭喜你完成了！

---

## 🎮 設定模擬器

### 下載並安裝 LDPlayer

1. 前往 [LDPlayer 官網](https://www.ldplayer.tw/)
2. 下載安裝程式
3. 安裝並啟動

### 設定模擬器

1. **設定解析度**: 1280x720 (建議)
   - 設定 → 顯示設定 → 解析度 → 1280x720

2. **啟用 ADB 除錯**:
   - 設定 → 關於平板電腦 → 版本號連點 7 次
   - 設定 → 開發人員選項 → USB 偵錯 (開啟)

3. **安裝遊戲**:
   - 打開 Google Play
   - 搜尋「運氣突擊隊」
   - 下載並安裝

### 連接 ADB

```powershell
# 下載 ADB (如果還沒有)
# https://developer.android.com/tools/releases/platform-tools

# 連接模擬器 (LDPlayer 預設埠是 5555)
adb connect 127.0.0.1:5555

# 驗證連接
adb devices
```

預期輸出:
```
List of devices attached
127.0.0.1:5555   device
```

---

## 📸 測試螢幕擷取

### 調整擷取區域

```powershell
# 執行區域擷取測試
python tests/test_screen_capture.py --region
```

這會：
1. 讓你輸入模擬器視窗的座標
2. 即時顯示擷取區域
3. 幫助你對齊遊戲畫面

### 更新配置檔案

根據測試結果，編輯 `configs/config.yaml`:

```yaml
capture:
  region:
    left: 100      # 調整為你的座標
    top: 100       # 調整為你的座標
    width: 1280
    height: 720
```

---

## ✅ 完成檢查清單

- [ ] Python 虛擬環境已建立
- [ ] PyTorch (CUDA) 已安裝
- [ ] 所有套件已安裝
- [ ] CUDA 測試通過
- [ ] 模擬器已安裝
- [ ] 遊戲已下載
- [ ] ADB 連接成功
- [ ] 螢幕擷取區域已調整

全部打勾？恭喜！你可以開始開發了！🎉

---

## 🐛 常見問題

### Q: PyTorch 無法使用 CUDA

**A**: 確認你安裝的是 CUDA 版本：

```powershell
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Q: ADB 連接失敗

**A**: 
1. 確認模擬器正在執行
2. 檢查埠號（可能不是 5555）
3. 嘗試重啟模擬器

查看模擬器的 ADB 埠號：
- LDPlayer: 通常是 5555, 5556, 5557...
- 設定 → 其他設定 → ADB 偵錯

### Q: 螢幕擷取顯示黑畫面

**A**:
1. 確認座標設定正確
2. 模擬器視窗必須可見（不能最小化）
3. 嘗試調整解析度

### Q: 記憶體不足錯誤

**A**: 編輯 `configs/config.yaml`，減少 batch size:

```yaml
vision:
  training:
    batch_size: 4  # 從 8 降到 4

ai:
  dqn:
    batch_size: 16  # 從 32 降到 16
```

---

## 📝 下一步

環境設定完成後，你可以：

### 1. 開始 Phase 2: 基礎自動化

學習如何：
- 自動點擊遊戲按鈕
- 識別戰鬥畫面
- 建立簡單的自動化腳本

### 2. 收集訓練資料

開始錄製遊戲畫面：
- 錄製 50+ 場戰鬥
- 截取不同情境的畫面
- 整理資料集

### 3. 學習 AI 技術

推薦教學：
- [PyTorch 60 分鐘快速入門](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)
- [YOLOv8 教學](https://docs.ultralytics.com/quickstart/)

---

## 💡 開發建議

### 循序漸進

不要一開始就想做完整的 AI 系統，建議順序：

1. ✅ **先做簡單的自動化** (1 週)
   - 固定位置點擊
   - 簡單的循環

2. ⬆️ **加入圖像識別** (2-3 週)
   - 訓練 YOLO 模型
   - 識別遊戲元素

3. 🧠 **最後才做 AI 學習** (4-6 週)
   - 強化學習訓練
   - 策略優化

### 保持耐心

- AI 訓練需要時間
- 可能需要多次調整參數
- 失敗是正常的，從錯誤中學習

### 記錄進度

使用 [PROGRESS.md](file:///D:/cheat/luck-raiders-ai-bot/PROGRESS.md) 追蹤你的進度：
- 完成的任務
- 遇到的問題
- 學到的經驗

---

## 🎯 立即行動

**現在就開始！**

```powershell
# 1. 切換目錄
cd D:\cheat\luck-raiders-ai-bot

# 2. 建立虛擬環境
python -m venv venv
.\venv\Scripts\activate

# 3. 執行安裝精靈
python setup.py
```

**或者直接手動安裝：**

```powershell
# 安裝 PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 安裝其他套件
pip install -r requirements.txt

# 測試 CUDA
python tests/test_cuda.py
```

---

**祝你開發順利！🚀**

有任何問題隨時問我！
