"""
快速入門指南

這個腳本會引導你完成初始設定並驗證系統。
"""

import os
import sys
from pathlib import Path


def print_banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          運氣突擊隊 AI 自動戰鬥系統 v1.0                      ║
║          Luck Raiders AI Bot                                 ║
║                                                              ║
║          🤖 基於深度學習的遊戲 AI                            ║
║          🎮 自動學習最佳戰鬥策略                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")


def check_python_version():
    """檢查 Python 版本"""
    print("🔍 檢查 Python 版本...")
    major, minor = sys.version_info[:2]
    
    if major < 3 or (major == 3 and minor < 8):
        print(f"❌ Python 版本過舊: {major}.{minor}")
        print("   需要 Python 3.8 或更高版本")
        return False
    
    print(f"✅ Python {major}.{minor}.{sys.version_info.micro}")
    return True


def check_venv():
    """檢查是否在虛擬環境中"""
    print("\n🔍 檢查虛擬環境...")
    
    in_venv = sys.prefix != sys.base_prefix
    
    if not in_venv:
        print("⚠️  未偵測到虛擬環境")
        print("   建議使用虛擬環境以避免套件衝突")
        print("\n建立虛擬環境:")
        print("   python -m venv venv")
        print("   .\\venv\\Scripts\\activate")
        return False
    
    print("✅ 已在虛擬環境中")
    return True


def install_requirements():
    """安裝必要套件"""
    print("\n📦 安裝必要套件...")
    print("這可能需要幾分鐘時間...\n")
    
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("❌ requirements.txt 不存在")
        return False
    
    # 先安裝 PyTorch (CUDA 版本)
    print("⚡ 安裝 PyTorch (CUDA 支援)...")
    pytorch_cmd = "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118"
    
    response = input(f"\n執行指令: {pytorch_cmd}\n繼續? (y/n): ")
    if response.lower() == 'y':
        os.system(pytorch_cmd)
    
    # 安裝其他套件
    print("\n📦 安裝其他套件...")
    pip_cmd = f"pip install -r {requirements_file}"
    
    response = input(f"\n執行指令: {pip_cmd}\n繼續? (y/n): ")
    if response.lower() == 'y':
        os.system(pip_cmd)
        print("\n✅ 套件安裝完成")
        return True
    
    return False


def run_tests():
    """執行系統測試"""
    print("\n🧪 執行系統測試...\n")
    print("=" * 60)
    
    # 測試 CUDA
    print("\n1️⃣ 測試 GPU 和 CUDA...")
    response = input("執行 CUDA 測試? (y/n): ")
    if response.lower() == 'y':
        os.system("python tests/test_cuda.py")
    
    # 測試螢幕擷取
    print("\n2️⃣ 測試螢幕擷取...")
    response = input("執行螢幕擷取測試? (y/n): ")
    if response.lower() == 'y':
        os.system("python tests/test_screen_capture.py")


def main():
    print_banner()
    
    print("歡迎使用運氣突擊隊 AI 自動戰鬥系統！")
    print("這個安裝精靈將引導你完成初始設定。\n")
    print("=" * 60)
    
    # Step 1: 檢查 Python 版本
    if not check_python_version():
        print("\n❌ 環境檢查失敗，請先升級 Python")
        sys.exit(1)
    
    # Step 2: 檢查虛擬環境
    venv_ok = check_venv()
    if not venv_ok:
        response = input("\n是否繼續（不建議）? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)
    
    # Step 3: 安裝套件
    print("\n" + "=" * 60)
    response = input("\n是否安裝必要套件? (y/n): ")
    if response.lower() == 'y':
        install_requirements()
    
    # Step 4: 執行測試
    print("\n" + "=" * 60)
    response = input("\n是否執行系統測試? (y/n): ")
    if response.lower() == 'y':
        run_tests()
    
    # 完成
    print("\n" + "=" * 60)
    print("\n🎉 初始設定完成！\n")
    print("📝 下一步:")
    print("   1. 安裝並開啟 Android 模擬器（推薦 LDPlayer）")
    print("   2. 安裝「運氣突擊隊」遊戲")
    print("   3. 執行 python tests/test_screen_capture.py --region")
    print("   4. 調整 configs/config.yaml 中的擷取區域")
    print("\n詳細文件: README.md")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  安裝已取消")
        sys.exit(0)
