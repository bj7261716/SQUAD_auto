# Python 3.12 環境自動重建腳本
# 此腳本會自動刪除舊環境並建立新的 Python 3.12 環境

Write-Host "=" * 60
Write-Host "🔄 Python 3.12 環境重建腳本"
Write-Host "=" * 60
Write-Host ""

# 檢查 Python 3.12 是否已安裝
Write-Host "檢查 Python 3.12..."
try {
    $pythonVersion = & py -3.12 --version 2>&1
    Write-Host "✅ 找到: $pythonVersion"
} catch {
    Write-Host "❌ Python 3.12 未安裝！"
    Write-Host ""
    Write-Host "請先安裝 Python 3.12.8:"
    Write-Host "https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe"
    Write-Host ""
    Read-Host "按 Enter 鍵退出"
    exit 1
}

Write-Host ""

# 刪除舊的虛擬環境
Write-Host "刪除舊的虛擬環境..."
if (Test-Path "venv") {
    Remove-Item -Recurse -Force venv
    Write-Host "✅ 舊環境已刪除"
} else {
    Write-Host "ℹ️  沒有找到舊環境"
}

Write-Host ""

# 建立新的虛擬環境
Write-Host "建立新的 Python 3.12 虛擬環境..."
& py -3.12 -m venv venv

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 虛擬環境建立成功"
} else {
    Write-Host "❌ 虛擬環境建立失敗"
    Read-Host "按 Enter 鍵退出"
    exit 1
}

Write-Host ""

# 啟動虛擬環境並安裝套件
Write-Host "啟動虛擬環境並安裝套件..."
Write-Host ""

# 升級 pip
Write-Host "📦 升級 pip..."
& .\venv\Scripts\python.exe -m pip install --upgrade pip

Write-Host ""

# 安裝基礎套件
Write-Host "📦 安裝基礎套件..."
& .\venv\Scripts\pip.exe install numpy opencv-python opencv-contrib-python pillow mss pyautogui pyyaml tqdm loguru

Write-Host ""

# 安裝 PyTorch (CUDA 12.6)
Write-Host "⚡ 安裝 PyTorch (CUDA 12.6) - 這可能需要幾分鐘..."
& .\venv\Scripts\pip.exe install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

Write-Host ""

# 安裝 AI 相關套件
Write-Host "🤖 安裝 AI 相關套件..."
& .\venv\Scripts\pip.exe install ultralytics stable-baselines3 gymnasium matplotlib seaborn tensorboard plotly pandas scipy

Write-Host ""
Write-Host "=" * 60
Write-Host "✅ 安裝完成！"
Write-Host "=" * 60
Write-Host ""

# 測試 CUDA
Write-Host "🧪 測試 CUDA 支援..."
Write-Host ""

& .\venv\Scripts\python.exe tests\test_cuda.py

Write-Host ""
Write-Host "=" * 60
Write-Host "🎉 環境準備完成！"
Write-Host "=" * 60
Write-Host ""
Write-Host "下一步："
Write-Host "1. 檢查上方的 CUDA 測試結果"
Write-Host "2. 確認 GPU 可用"
Write-Host "3. 開始開發！"
Write-Host ""

Read-Host "按 Enter 鍵退出"
