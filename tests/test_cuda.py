"""
CUDA 和 GPU 驗證測試腳本

檢查系統是否正確安裝 PyTorch 和 CUDA，並顯示 GPU 資訊。
"""

import sys


def test_cuda():
    print("=" * 60)
    print("🔍 CUDA 和 GPU 驗證測試")
    print("=" * 60)
    print()
    
    # 測試 PyTorch 安裝
    try:
        import torch
        print("✅ PyTorch 已成功安裝")
        print(f"   版本: {torch.__version__}")
    except ImportError:
        print("❌ PyTorch 未安裝")
        print("   請執行: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
        return False
    
    print()
    
    # 測試 CUDA 可用性
    if torch.cuda.is_available():
        print("✅ CUDA 可用")
        print(f"   CUDA 版本: {torch.version.cuda}")
        print(f"   cuDNN 版本: {torch.backends.cudnn.version()}")
    else:
        print("❌ CUDA 不可用")
        print("   請確認:")
        print("   1. 已安裝 NVIDIA 驅動程式")
        print("   2. 已安裝對應版本的 CUDA Toolkit")
        print("   3. 安裝的是 PyTorch CUDA 版本")
        return False
    
    print()
    
    # GPU 資訊
    num_gpus = torch.cuda.device_count()
    print(f"🎮 偵測到 {num_gpus} 個 GPU:")
    print()
    
    for i in range(num_gpus):
        props = torch.cuda.get_device_properties(i)
        print(f"   GPU {i}: {props.name}")
        print(f"   ├─ 總記憶體: {props.total_memory / 1e9:.2f} GB")
        print(f"   ├─ 多處理器數量: {props.multi_processor_count}")
        print(f"   ├─ CUDA 能力: {props.major}.{props.minor}")
        if hasattr(props, 'maxThreadsPerBlock'):
            print(f"   └─ 最大線程/塊: {props.maxThreadsPerBlock}")
        elif hasattr(props, 'max_threads_per_block'): # Backwards compatibility
             print(f"   └─ 最大線程/塊: {props.max_threads_per_block}")
        print()
    
    # 測試 GPU 運算
    print("🧪 測試 GPU 運算能力...")
    try:
        # 建立測試張量
        x = torch.randn(1000, 1000).cuda()
        y = torch.randn(1000, 1000).cuda()
        
        # GPU 運算
        import time
        start = time.time()
        z = torch.matmul(x, y)
        torch.cuda.synchronize()
        gpu_time = time.time() - start
        
        # CPU 運算（比較用）
        x_cpu = x.cpu()
        y_cpu = y.cpu()
        start = time.time()
        z_cpu = torch.matmul(x_cpu, y_cpu)
        cpu_time = time.time() - start
        
        print(f"   ✅ GPU 矩陣運算時間: {gpu_time*1000:.2f} ms")
        print(f"   ℹ️  CPU 矩陣運算時間: {cpu_time*1000:.2f} ms")
        print(f"   ⚡ GPU 加速倍數: {cpu_time/gpu_time:.2f}x")
        print()
        
    except Exception as e:
        print(f"   ❌ GPU 運算測試失敗: {e}")
        return False
    
    # 記憶體資訊
    print("💾 GPU 記憶體狀態:")
    for i in range(num_gpus):
        allocated = torch.cuda.memory_allocated(i) / 1e9
        reserved = torch.cuda.memory_reserved(i) / 1e9
        total = torch.cuda.get_device_properties(i).total_memory / 1e9
        
        print(f"   GPU {i}:")
        print(f"   ├─ 已分配: {allocated:.2f} GB")
        print(f"   ├─ 已保留: {reserved:.2f} GB")
        print(f"   └─ 總容量: {total:.2f} GB")
    
    print()
    print("=" * 60)
    print("✅ 所有測試通過！你的系統已準備好進行 AI 訓練。")
    print("=" * 60)
    
    return True


def test_other_libraries():
    """測試其他必要的函式庫"""
    print()
    print("=" * 60)
    print("📚 測試其他必要函式庫")
    print("=" * 60)
    print()
    
    libraries = {
        "OpenCV": "cv2",
        "NumPy": "numpy",
        "PIL (Pillow)": "PIL",
        "MSS": "mss",
        "PyAutoGUI": "pyautogui",
        "Ultralytics (YOLOv8)": "ultralytics",
    }
    
    all_installed = True
    
    for name, module in libraries.items():
        try:
            lib = __import__(module)
            version = getattr(lib, "__version__", "未知版本")
            print(f"✅ {name:20s} - {version}")
        except ImportError:
            print(f"❌ {name:20s} - 未安裝")
            all_installed = False
    
    print()
    
    if all_installed:
        print("✅ 所有必要函式庫已安裝")
    else:
        print("⚠️  部分函式庫未安裝，請執行:")
        print("   pip install -r requirements.txt")
    
    print("=" * 60)
    
    return all_installed


if __name__ == "__main__":
    success = test_cuda()
    libs_ok = test_other_libraries()
    
    if success and libs_ok:
        print()
        print("🎉 恭喜！你的開發環境已完全準備好！")
        print("📝 下一步: 執行 python tests/test_screen_capture.py")
        sys.exit(0)
    else:
        print()
        print("⚠️  請先解決上述問題，再繼續開發。")
        sys.exit(1)
