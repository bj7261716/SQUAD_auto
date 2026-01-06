import pyautogui
import time
import sys

print("=================================================")
print("🖱️  滑鼠座標偵測器")
print("=================================================")
print("請將滑鼠游標移到你想要偵測的位置...")
print("按 Ctrl+C 退出")
print("")

try:
    while True:
        x, y = pyautogui.position()
        # 清除同一行並印出新座標
        sys.stdout.write(f"\r當前座標: X={x}, Y={y}   ")
        sys.stdout.flush()
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n\n偵測結束。")
