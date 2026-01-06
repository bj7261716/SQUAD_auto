import cv2
import mss
import numpy as np
import yaml
import os
import sys

# 讀取設定
try:
    with open("configs/config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        region = config['capture']['region']
except Exception as e:
    print(f"❌ 無法讀取設定檔: {e}")
    sys.exit(1)

# 全域變數
drawing = False
ix, iy = -1, -1
roi_coords = None

def draw_rect(event, x, y, flags, param):
    global ix, iy, drawing, roi_coords, img_display

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = img_display.copy()
            cv2.rectangle(img_copy, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow('Crop Template', img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img_display, (ix, iy), (x, y), (0, 255, 0), 2)
        cv2.imshow('Crop Template', img_display)
        roi_coords = (min(ix, x), min(iy, y), abs(ix - x), abs(iy - y))
        print(f"已選取區域: {roi_coords}")

def main():
    global img_display
    
    # 確保目錄存在
    os.makedirs("data/templates", exist_ok=True)
    
    print("=" * 60)
    print("✂️  模板截取工具")
    print("=" * 60)
    print("1. 程式會抓取當前遊戲畫面")
    print("2. 請用滑鼠框選你要的區域")
    print("3. 按 's' 儲存")
    print("4. 按 'r' 重新抓取畫面")
    print("5. 按 'q' 退出")
    print()
    
    with mss.mss() as sct:
        while True:
            # 抓取畫面
            print("正在抓取畫面...")
            img = sct.grab(region)
            img_np = np.array(img)
            img_original = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)
            img_display = img_original.copy()
            
            cv2.namedWindow('Crop Template')
            cv2.setMouseCallback('Crop Template', draw_rect)
            cv2.imshow('Crop Template', img_display)
            
            print("等待操作... (s=儲存, r=重抓, q=退出)")
            
            while True:
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    print("👋 掰掰")
                    cv2.destroyAllWindows()
                    sys.exit(0)
                
                elif key == ord('r'):
                    print("🔄 重新抓取畫面...")
                    break  # 跳出內層迴圈，重新抓取
                
                elif key == ord('s'):
                    if roi_coords and roi_coords[2] > 0 and roi_coords[3] > 0:
                        x, y, w, h = roi_coords
                        crop_img = img_original[y:y+h, x:x+w]
                        
                        cv2.imshow('Preview', crop_img)
                        print("請輸入檔名 (例如: button_start): ", end='')
                        
                        # 簡單的 GUI 輸入有點難搞，我們先用 terminal 輸入
                        # 這裡暫時要把視窗 focus 移回 terminal
                        filename = input().strip()
                        
                        if filename:
                            if not filename.endswith('.png'):
                                filename += '.png'
                                
                            path = os.path.join("data/templates", filename)
                            cv2.imwrite(path, crop_img)
                            print(f"✅ 已儲存: {path}")
                            cv2.destroyWindow('Preview')
                        else:
                            print("❌ 未輸入檔名，取消儲存")
                    else:
                        print("❌ 請先框選區域！")

if __name__ == "__main__":
    main()
