### **Python 程式碼**

# -*- coding: utf-8 -*-
# 這是為了確保檔案能正確處理中文註釋和其他多位元組字元編碼

# 導入必要的函式庫
# Pillow 函式庫是 Python 中處理影像最常用且功能強大的工具之一。
# 它允許我們開啟、操作和儲存各種影像格式。
from PIL import Image
import os # os 模組提供了與作業系統互動的功能，例如檢查檔案是否存在、處理檔案路徑等。

def convert_image_to_ascii(image_path, output_width=100, char_set=' .:-=+*#%@'):
    """
    將 JPG 圖片轉換為 ASCII 藝術文字檔。

    這個函式會讀取指定的圖片檔案，將其轉換為灰度圖像，然後縮放，
    最後根據每個像素的亮度值將其映射到預設的 ASCII 字元集，
    生成一個由這些字元組成的文字檔，模擬出原始圖片的視覺效果。

    Args:
        image_path (str): 欲轉換的圖片檔案路徑（例如 'my_photo.jpg'）。
        output_width (int, optional): 輸出 ASCII 藝術的目標寬度（字元數）。
                                     較大的值會產生更精細的輸出，但檔案也會更大。
                                     預設為 100 個字元寬。
        char_set (str, optional): 用於構成 ASCII 藝術的字元集合。
                                  字元應從亮度最低（最淺）到亮度最高（最深）排列。
                                  預設為 ' .:-=+*#%@'。
                                  例如：' ' (空白) 代表最亮，'@' 代表最暗。
    Returns:
        str: 如果轉換成功，則回傳輸出文字檔的路徑；如果失敗，則回傳錯誤訊息。
    """

    # --- 步驟 1: 檔案存在性檢查與開啟圖片 ---
    if not os.path.exists(image_path):
        return f"錯誤：找不到圖片檔案 '{image_path}'。請檢查路徑是否正確。"

    try:
        # 使用 Pillow 的 Image.open() 方法開啟圖片。
        # 'with' 語句確保在操作完成後，圖片檔案會被正確關閉，釋放資源。
        original_image = Image.open(image_path)
    except FileNotFoundError:
        return f"錯誤：無法開啟檔案 '{image_path}'。檔案可能不存在或路徑錯誤。"
    except Exception as e:
        # 捕捉其他可能的錯誤，例如檔案格式不支援等。
        return f"錯誤：處理圖片時發生未知錯誤 - {e}"

    print(f"成功開啟圖片：{image_path}")

    # --- 步驟 2: 轉換圖片為灰度模式 ---
    # ASCII 藝術主要是基於亮度來呈現的，顏色資訊在此處是不需要的。
    # 'L' 模式代表將圖片轉換為 8 位元像素的灰度圖（0-255，0 為黑，255 為白）。
    grayscale_image = original_image.convert('L')
    print("圖片已轉換為灰度模式。")

    # --- 步驟 3: 計算新的尺寸以符合目標寬度並保持長寬比 ---
    # 目標是讓輸出的 ASCII 藝術有指定的寬度，並根據原始圖片的長寬比來調整高度。
    # 這樣可以避免圖片被拉伸變形。
    width, height = grayscale_image.size
    aspect_ratio = height / width # 計算原始圖片的長寬比

    # 計算新的高度。為了讓 ASCII 藝術在終端機中看起來更自然（終端機字元通常高於寬），
    # 我們將高度乘以一個修正因子（例如 0.55）。您可以根據實際效果調整此值。
    new_height = int(output_width * aspect_ratio * 0.55)
    new_size = (output_width, new_height)
    print(f"原始尺寸：{width}x{height}，目標 ASCII 藝術尺寸：{new_size[0]}x{new_size[1]} (字元)。")

    # --- 步驟 4: 縮放圖片 ---
    # 使用 Image.resize() 方法將灰度圖縮放到新的尺寸。
    # Image.ANTIALIAS (或 Image.LANCZOS) 是一種高品質的縮放演算法，
    # 能夠在縮小時減少鋸齒，使結果更平滑。
    resized_image = grayscale_image.resize(new_size, Image.LANCZOS) # Image.ANTIALIAS 在較新版本中已更名為 Image.LANCZOS
    print("圖片已縮放。")

    # --- 步驟 5: 將像素亮度映射到 ASCII 字元 ---
    # 獲取縮放後圖片的所有像素數據。getdata() 會回傳一個序列，包含每個像素的亮度值。
    pixels = resized_image.getdata()

    # 計算每個 ASCII 字元對應的亮度範圍。
    # 例如，如果 char_set 有 10 個字元，亮度範圍 0-255，那麼每個字元對應 25.6 的亮度區間。
    # 亮度值越低，索引越靠近 char_set 的開頭（淺色字元）。
    # 亮度值越高，索引越靠近 char_set 的結尾（深色字元）。
    num_chars = len(char_set)
    # 除以 (256 // num_chars) 可以確保每個區間是等長的。
    # 例如，256 // 10 = 25。
    # 或者用浮點數除法 256 / num_chars 得到更精確的區間寬度。
    brightness_interval = 256 / num_chars

    ascii_characters = [] # 用來儲存轉換後的 ASCII 字元

    # 遍歷每個像素的亮度值
    for pixel_value in pixels:
        # 將像素亮度值映射到 char_set 中的索引。
        # int() 會向下取整。例如，亮度 0-24 會對應到索引 0。
        # min() 確保索引不會超出 char_set 的範圍（即使 pixel_value 是 255）。
        char_index = min(int(pixel_value / brightness_interval), num_chars - 1)
        ascii_characters.append(char_set[char_index])

    print("像素已映射到 ASCII 字元。")

    # --- 步驟 6: 組合 ASCII 字元並加入換行符號 ---
    # 將 ASCII 字元列表組合成一個字串，並在每行結束時加入換行符號。
    # 這樣才能形成多行的 ASCII 藝術。
    ascii_art_lines = []
    # 遍歷 ascii_characters 列表，每 output_width 個字元就切割一次，形成一行。
    for i in range(0, len(ascii_characters), output_width):
        line = "".join(ascii_characters[i:i + output_width])
        ascii_art_lines.append(line)

    # 用換行符號 '\n' 將所有行連接起來。
    final_ascii_art = "\n".join(ascii_art_lines)
    print("ASCII 藝術字串已生成。")

    # --- 步驟 7: 儲存 ASCII 藝術到文字檔 ---
    # 獲取原始檔案的名稱和擴展名
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_filename = f"{base_name}_ascii_art.txt"

    try:
        # 以寫入模式 ('w') 和 UTF-8 編碼打開新的文字檔。
        # UTF-8 編碼確保即使 char_set 中有非英文字元也能正確儲存。
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(final_ascii_art)
        print(f"ASCII 藝術文字檔已成功儲存為：'{output_filename}'")
        return output_filename
    except Exception as e:
        return f"錯誤：儲存文字檔時發生錯誤 - {e}"

# --- 主程式執行區塊 ---
# 只有當這個腳本被直接執行時，才會執行下面的程式碼。
# 如果這個腳本被作為模組導入到其他程式中，則不會執行。
if __name__ == "__main__":
    print("--- JPG 圖片轉 ASCII 藝術文字檔工具 ---")
    print("請輸入您要轉換的 JPG 圖片檔案路徑。")
    print("範例：'image.jpg' 或 'C:\\Users\\YourName\\Pictures\\photo.jpg'")
    
    # 讓使用者輸入圖片路徑
    input_image_path = input("請輸入 JPG 圖片路徑：")

    # 您也可以在這裡設定其他的參數，例如輸出寬度或字元集
    # output_width = 150 # 如果您想要更寬的輸出
    # custom_char_set = ' .-=+*#%@' # 如果您想使用不同的字元集

    # 呼叫轉換函式
    result = convert_image_to_ascii(input_image_path) # 使用預設參數
    # result = convert_image_to_ascii(input_image_path, output_width=150) # 使用自定義寬度
    # result = convert_image_to_ascii(input_image_path, char_set=' _-=+*#%@') # 使用自定義字元集

    print("\n--- 轉換結果 ---")
    if result.startswith("錯誤"):
        print(result)
    else:
        print(f"程式執行完成。您可以在 '{result}' 檔案中查看結果。")
        print("建議使用純文字編輯器開啟，並調整視窗大小以獲得最佳視覺效果。")
        print("在某些終端機或編輯器中，您可能需要縮放文字來看到效果。")

```