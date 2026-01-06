# 模板資料夾說明

這個資料夾用於存放遊戲 UI 元素的模板圖片，供模板匹配使用。

## 如何建立模板

### 步驟 1: 截取遊戲畫面

執行 `demo.py` 或 `tests/test_screen_capture.py`，在遊戲畫面中按 `s` 鍵截圖。

### 步驟 2: 裁切 UI 元素

使用圖片編輯工具（如小畫家、Photoshop、GIMP）：
1. 打開截圖
2. 裁切出你要識別的按鈕或圖標
3. 儲存為 PNG 格式

### 步驟 3: 命名規則

使用有意義的名稱，例如：
- `start_battle.png` - 開始戰鬥按鈕
- `claim_reward.png` - 領取獎勵按鈕
- `skill_1.png` - 技能 1 圖標
- `enemy_hp_full.png` - 敵人滿血血條
- `battle_end.png` - 戰鬥結束標誌

### 步驟 4: 放入此資料夾

將裁切好的圖片放入 `data/templates/` 目錄。

## 模板匹配使用範例

```python
from vision import TemplateMatcher

# 建立匹配器
matcher = TemplateMatcher(threshold=0.8)

# 載入模板
matcher.load_template('start_battle', 'data/templates/start_battle.png')

# 或載入整個資料夾
matcher.load_templates_from_dir('data/templates')

# 在螢幕上尋找
match = matcher.match(screen, 'start_battle')
if match:
    x, y, confidence = match
    print(f"找到按鈕在 ({x}, {y})，信心度 {confidence}")
```

## 注意事項

1. **圖片清晰度**: 確保模板圖片清晰，沒有模糊
2. **大小適中**: 不要太大也不要太小，建議 50x50 ~ 200x200 像素
3. **避免相似**: 不同模板要有明顯區別
4. **固定元素**: 模板匹配適合固定位置、固定外觀的 UI 元素
5. **光線變化**: 如果遊戲有光線變化，可能需要多個模板

## 推薦工具

- **Windows**: 小畫家、Paint.NET
- **跨平台**: GIMP
- **線上工具**: Photopea (https://www.photopea.com/)

## 範例模板結構

```
data/templates/
├── buttons/
│   ├── start_battle.png
│   ├── claim_reward.png
│   └── next.png
├── skills/
│   ├── skill_1.png
│   ├── skill_2.png
│   └── skill_3.png
└── icons/
    ├── gold_icon.png
    └── gem_icon.png
```

你可以建立子資料夾來組織模板，匹配器會遞迴載入所有 PNG 檔案。
