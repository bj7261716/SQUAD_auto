import cv2
import sys
import os
import yaml
from pathlib import Path

# 添加 src 到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from capture import ScreenCapture
from vision import TemplateMatcher

def test_vision():
    print("=" * 60)
    print("👁️  視覺辨識單元測試")
    print("=" * 60)
    
    # 載入 config
    try:
        with open("configs/config.yaml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            region = config['capture']['region']
            # 確保 resize 是 None (如果 config 裡被註解掉或是 null)
            resize = config['capture'].get('resize')
            if resize:
                resize = tuple(resize)
            print(f"配置: Region={region}, Resize={resize}")
    except Exception as e:
        print(f"❌ 無法讀取配置: {e}")
        return

    # 初始化
    capturer = ScreenCapture(region=region, resize=resize)
    matcher = TemplateMatcher(threshold=0.6)  # 先用寬鬆一點的閾值看看
    
    # 載入模板
    templates_dir = Path("data/templates")
    count = matcher.load_templates_from_dir(str(templates_dir))
    print(f"已載入 {count} 個模板: {matcher.get_template_names()}")
    
    if count == 0:
        print("❌ 沒有模板可測試！請先建立模板。")
        return

    print("\n📸 正在截取螢幕...")
    frame = capturer.capture()
    
    # 保存當前畫面以便除錯
    debug_path = "debug_vision_test.png"
    cv2.imwrite(debug_path, frame)
    print(f"已保存當前畫面為: {debug_path}")
    
    print("\n🔍 開始匹配...")
    found_any = False
    
    for name in matcher.get_template_names():
        match = matcher.match(frame, name)
        if match:
            x, y, conf = match
            print(f"✅ 找到 [{name}]: Confidence = {conf:.4f} at ({x}, {y})")
            
            # 畫框框
            h, w = matcher.templates[name].shape[:2]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{name}:{conf:.2f}", (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
            found_any = True
        else:
            # 雖然沒找到，但也印出最佳分數以便除錯
            # TemplateMatcher.match 只回傳 None，所以我們得稍微改寫或是信任 log
            # 這裡我們只印出未找到
            print(f"❌ 未找到 [{name}]")

    if found_any:
        result_path = "debug_vision_result.png"
        cv2.imwrite(result_path, frame)
        print(f"\n已保存結果圖片為: {result_path}")
        print("請打開圖片檢查框選位置是否正確。")
    else:
        print("\n⚠️  完全沒找到任何東西。請檢查 debug_vision_test.png 是否包含目標。")

if __name__ == "__main__":
    test_vision()
