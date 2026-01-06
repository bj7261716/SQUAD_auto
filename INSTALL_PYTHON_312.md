# 🚀 Python 3.12 安裝與環境重建指南

## 📥 Step 1: 安裝 Python 3.12.8

### 下載已開始
**下載連結**: https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe

檔案應該正在下載到你的「下載」資料夾。

### 安裝步驟

1. **找到下載的檔案**
   - 檔案名稱: `python-3.12.8-amd64.exe`
   - 通常位置: `C:\Users\你的使用者名\Downloads\`

2. **執行安裝程式**
   - 雙擊 `python-3.12.8-amd64.exe`

3. **重要！安裝選項**
   - ✅ **勾選「Add python.exe to PATH」**（非常重要！）
   - ✅ 選擇「Install Now」（建議選項）
   
   或者使用自訂安裝：
   - ✅ 勾選「pip」
   - ✅ 勾選「tcl/tk and IDLE」
   - ✅ 勾選「Python test suite」
   - ✅ 勾選「py launcher」（可以同時管理多個 Python 版本）
   - ✅ 勾選「for all users」（選用）

4. **等待安裝完成**
   - 大約需要 2-3 分鐘

5. **驗證安裝**
   - 打開新的 PowerShell（**必須是新的！**）
   - 執行: `py -3.12 --version`
   - 應該顯示: `Python 3.12.8`

---

## 🔄 Step 2: 重建虛擬環境（自動化腳本）

安裝完成後，執行以下指令來自動重建環境：

### 方案 A：手動執行（推薦）

```powershell
# 1. 切換到專案目錄
cd D:\cheat\luck-raiders-ai-bot

# 2. 刪除舊的虛擬環境
Remove-Item -Recurse -Force venv

# 3. 使用 Python 3.12 建立新環境
py -3.12 -m venv venv

# 4. 啟動虛擬環境
.\venv\Scripts\activate

# 5. 升級 pip
python -m pip install --upgrade pip

# 6. 安裝基礎套件
pip install numpy opencv-python opencv-contrib-python pillow mss pyautogui pyyaml tqdm loguru

# 7. 安裝 PyTorch (CUDA 12.6) ⭐ 重要！
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

# 8. 安裝 AI 相關套件
pip install ultralytics stable-baselines3 gymnasium matplotlib seaborn tensorboard plotly

# 9. 安裝其他工具
pip install pandas scipy

# 10. 測試 CUDA
python tests/test_cuda.py
```

### 方案 B：使用自動化腳本

我已為你準備好自動化腳本 `rebuild_env.ps1`，安裝完 Python 3.12 後執行：

```powershell
cd D:\cheat\luck-raiders-ai-bot
.\rebuild_env.ps1
```

---

## ✅ Step 3: 驗證安裝

執行以下測試腳本：

```powershell
# 確保虛擬環境已啟動
.\venv\Scripts\activate

# 測試 CUDA
python tests/test_cuda.py
```

### 預期結果

```
============================================================
🔍 CUDA 和 GPU 驗證測試
============================================================

✅ PyTorch 已成功安裝
   版本: 2.9.1+cu126

✅ CUDA 可用
   CUDA 版本: 12.6
   cuDNN 版本: 90400

🎮 偵測到 1 個 GPU:

   GPU 0: NVIDIA GeForce GTX 1650
   ├─ 總記憶體: 4.00 GB
   ├─ 多處理器數量: 14
   ├─ CUDA 能力: 7.5
   └─ 最大線程/塊: 1024

🧪 測試 GPU 運算能力...
   ✅ GPU 矩陣運算時間: 2.15 ms
   ℹ️  CPU 矩陣運算時間: 45.32 ms
   ⚡ GPU 加速倍數: 21.08x

💾 GPU 記憶體狀態:
   GPU 0:
   ├─ 已分配: 0.00 GB
   ├─ 已保留: 0.00 GB
   └─ 總容量: 4.00 GB

============================================================
✅ 所有測試通過！你的系統已準備好進行 AI 訓練。
============================================================
```

---

## 📦 完整套件清單

安裝完成後，你將擁有以下套件：

### 核心框架
- ✅ `torch 2.9.1+cu126` - PyTorch (CUDA 12.6)
- ✅ `torchvision` - 電腦視覺
- ✅ `torchaudio` - 音訊處理

### 圖像處理
- ✅ `opencv-python` - OpenCV 核心
- ✅ `opencv-contrib-python` - OpenCV 擴展模組
- ✅ `pillow` - PIL 圖像處理
- ✅ `ultralytics` - YOLOv8

### 強化學習
- ✅ `stable-baselines3` - RL 演算法庫
- ✅ `gymnasium` - 環境框架

### 螢幕擷取與自動化
- ✅ `mss` - 螢幕擷取
- ✅ `pyautogui` - 自動化操作

### 資料處理與視覺化
- ✅ `numpy` - 數值運算
- ✅ `pandas` - 資料分析
- ✅ `matplotlib` - 繪圖
- ✅ `seaborn` - 統計視覺化
- ✅ `tensorboard` - 訓練監控

### 工具
- ✅ `pyyaml` - YAML 配置
- ✅ `tqdm` - 進度條
- ✅ `loguru` - 日誌記錄

---

## 🐛 常見問題

### Q1: 安裝時找不到 `py` 指令

**A**: 檢查是否勾選了「Add python.exe to PATH」，如果沒有：
1. 重新執行安裝程式
2. 選擇「Modify」
3. 勾選「Add Python to environment variables」

### Q2: `pip` 安裝 PyTorch 時出現 timeout

**A**: 網路問題，可以：
1. 重試安裝
2. 使用清華大學鏡像:
```powershell
pip install torch torchvision torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple --index-url https://download.pytorch.org/whl/cu126
```

### Q3: CUDA 測試失敗

**A**: 檢查：
1. 是否安裝了正確的 PyTorch 版本（應該是 `+cu126`）
2. NVIDIA 驅動是否更新（建議 >= 545.84）
3. 重新執行: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126`

### Q4: 想保留 Python 3.14 怎麼辦？

**A**: 沒問題！Python launcher (`py`) 可以管理多個版本：
- Python 3.12: `py -3.12`
- Python 3.14: `py -3.14`

---

## 📅 安裝後的下一步

1. ✅ 執行 `python demo.py` 測試系統整合
2. ✅ 安裝並設定 Android 模擬器
3. ✅ 下載「運氣突擊隊」遊戲
4. ✅ 測試 ADB 連接
5. ✅ 開始 Phase 2 開發

---

## 💡 提示

- **虛擬環境**: 每次開發前記得啟動 `.\venv\Scripts\activate`
- **套件更新**: 定期執行 `pip list --outdated` 檢查更新
- **CUDA 驅動**: 確保 NVIDIA 驅動是最新的

---

**準備好了嗎？** 🚀

安裝完 Python 3.12 後，告訴我「已安裝」，我會立即幫你執行自動化腳本！
