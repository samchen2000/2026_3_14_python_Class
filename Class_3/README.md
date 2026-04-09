# 2020/3/28 上課影片
## 2026/3/28 課程
### 2026_03_28_早上
https://www.youtube.com/watch?v=0Rz4UhiGn2k

### 2026_03_28_下午
https://www.youtube.com/watch?v=sSSUSdWo_30

## 3/28 上課筆記: (上午)
1. 安裝 Warp (Terminal)
2. 安裝 ollama , 安裝 LLM , 也可以安裝 Cloud 版本,但需要依照安裝後的LLM 提供的網址進入註冊.
3. 修改 raspberry /etc/default/locale 增加中文字形,避免輸出文字成為亂碼.
```
LANG=zh_TW.UTF-8
LC_ALL=zh_TW.UTF-8
LC_CTYPE=zh_TW.UTF-8
```
4. 安裝Docker , 先 update & upgrade
- 請參考
```
https://github.com/roberthsu2003/LLMs_Raspberry/blob/main/Docker/raspberry%E5%AE%89%E8%A3%9Ddocker.md
```
### 下載並執行 Docker 官方安裝腳本
```
# 下載安裝腳本
curl -fsSL https://get.docker.com -o get-docker.sh

# 執行安裝腳本
sudo sh get-docker.sh
```
### 將使用者加入 docker 群組
```
# 將目前使用者加入 docker 群組
sudo usermod -aG docker $USER

# 立即讓群組設定生效（執行後，無需登出即可讓 $USER 擁有 docker 權限）
newgrp docker
```


5. 安裝 OpenWebUI (是一個功能強大、介面友善的網頁UI，可以讓你與在本機（例如你的電腦或 Raspberry Pi）上運行的 Ollama 大型語言模型進行互動。)
- 請參考
安裝(適合raspberry)：連接到現有的 Ollama -> network:bridge
```
https://github.com/roberthsu2003/LLMs_Raspberry/blob/main/OpenWebUI/OpenWebUI%E7%B0%A1%E6%98%93%E5%AE%89%E8%A3%9D%E6%B5%81%E7%A8%8B%E8%AA%AA%E6%98%8E.md#section-4
```

## 3/28 上課筆記(下午)
1. 
```
# 檢查 Docker 系統資訊
docker system info

# 檢查 Docker 服務狀態
sudo systemctl status docker

# 檢查 Docker 是否正在執行
sudo systemctl is-active docker
```
2. open-webui 的建立
```

```
------------------------------------------------------------------------------------------

### Gemini: Python 針對 camera 的「指令」通常指的是使用 Python 程式庫來與攝影機互動的函數（functions）和方法（methods）。這些指令會根據你使用的攝影機類型和目的（例如，網路攝影機、IP 攝影機、DSLR、樹莓派攝影機、或用於即時串流、拍照）而有所不同。

以下是一些最常用且強大的 Python 程式庫及其核心「指令」：

---

### 1. 針對 USB 網路攝影機 (Webcam) 或內建攝影機 - 使用 `OpenCV` (最常用)

`OpenCV` (Open Source Computer Vision Library) 是處理影像和影片最流行的程式庫之一。

**安裝：**
```bash
pip install opencv-python numpy
```

**核心指令/操作：**

1.  **初始化攝影機：**
    *   `cv2.VideoCapture(0)`: 初始化預設攝影機 (通常是 USB 網路攝影機)。
        *   `0` 是攝影機的索引號，如果你有多個攝影機，可以是 `1`, `2` 等。
        *   也可以傳入影片檔案路徑 (`'video.mp4'`) 或網路串流位址 (`'rtsp://user:pass@ip:port/stream'`)。

2.  **檢查攝影機是否成功打開：**
    *   `cap.isOpened()`: 回傳 `True` 如果攝影機成功打開，否則為 `False`。

3.  **讀取影片幀 (frame)：**
    *   `ret, frame = cap.read()`: 讀取一幀。
        *   `ret` (boolean): 如果成功讀取幀，為 `True`。
        *   `frame` (numpy array): 讀取到的影像幀，以 NumPy 陣列表示。

4.  **顯示影像幀：**
    *   `cv2.imshow('視窗標題', frame)`: 在視窗中顯示影像幀。

5.  **等待按鍵輸入 (用於控制更新或退出)：**
    *   `cv2.waitKey(delay)`: 等待指定毫秒數 (`delay`) 的按鍵輸入。
        *   如果 `delay` 為 `0`，則無限等待直到按鍵。
        *   回傳按鍵的 ASCII 值，如果沒有按鍵則回傳 `-1`。

6.  **設定攝影機屬性：**
    *   `cap.set(propId, value)`: 設定攝影機屬性。
        *   `propId` 是一些預定義的常數，例如：
            *   `cv2.CAP_PROP_FRAME_WIDTH`: 幀寬度
            *   `cv2.CAP_PROP_FRAME_HEIGHT`: 幀高度
            *   `cv2.CAP_PROP_FPS`: 幀率
            *   `cv2.CAP_PROP_BRIGHTNESS`: 亮度
            *   `cv2.CAP_PROP_CONTRAST`: 對比度
            *   `cv2.CAP_PROP_GAIN`: 增益
            *   `cv2.CAP_PROP_EXPOSURE`: 曝光
        *   `value`: 要設定的數值。

7.  **獲取攝影機屬性：**
    *   `cap.get(propId)`: 獲取攝影機屬性值。

8.  **釋放攝影機資源：**
    *   `cap.release()`: 釋放攝影機佔用的資源。

9.  **銷毀所有 OpenCV 視窗：**
    *   `cv2.destroyAllWindows()`: 關閉所有由 `cv2.imshow()` 創建的視窗。

**範例 (即時預覽)：**
```python
import cv2

# 初始化預設攝影機 (通常是索引 0)
cap = cv2.VideoCapture(0)

# 檢查攝影機是否成功打開
if not cap.isOpened():
    print("無法打開攝影機")
    exit()

# 嘗試設定解析度 (並非所有攝影機都支持任意解析度)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print(f"目前解析度: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}x{cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")

while True:
    # 逐幀捕獲
    ret, frame = cap.read()

    # 如果正確讀取幀，ret 為 True
    if not ret:
        print("無法接收幀 (串流結束?)。正在退出 ...")
        break

    # 在此可以對 `frame` 進行各種影像處理 (例如灰度轉換、邊緣檢測等)
    # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 顯示結果幀
    cv2.imshow('Camera Live Feed', frame)
    # cv2.imshow('Gray Frame', gray_frame) # 如果有處理，可以顯示處理後的幀

    # 按 'q' 鍵退出循環
    if cv2.waitKey(1) == ord('q'):
        break

# 釋放攝影機資源
cap.release()
# 銷毀所有 OpenCV 視窗
cv2.destroyAllWindows()
```

---

### 2. 針對 IP 攝影機 / 網路串流 - 依然使用 `OpenCV`

`OpenCV` 也能直接讀取網路串流，例如 RTSP (Real-Time Streaming Protocol) 或 HTTP MJPEG。

**核心指令：**
與 USB 攝影機相同，只是 `cv2.VideoCapture()` 的參數不同。

```python
import cv2

# IP 攝影機的 RTSP 串流位址
# 格式通常為 'rtsp://user:password@ip_address:port/stream_path'
# 請替換為你攝影機的實際位址和憑證
rtsp_url = 'rtsp://admin:password123@192.168.1.100:554/stream1'

cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print(f"無法打開 RTSP 串流: {rtsp_url}")
    exit()

print("成功連接 IP 攝影機，正在接收串流...")

while True:
    ret, frame = cap.read()

    if not ret:
        print("無法接收幀 (串流斷開?)。正在重新連接或退出 ...")
        # 可以嘗試重新連接，或者直接退出
        break

    cv2.imshow('IP Camera Feed', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

### 3. 針對樹莓派攝影機 (Raspberry Pi Camera)

樹莓派有專門的程式庫，分為舊版和新版。

#### a) 舊版攝影機模組 (V1/V2) - `picamera` (legacy)

**安裝：**
```bash
pip install picamera
```

**核心指令：**
*   `PiCamera()`: 初始化攝影機對象。
*   `camera.start_preview()`: 開始預覽。
*   `camera.capture('image.jpg')`: 拍照。
*   `camera.start_recording('video.h264')`: 開始錄影。
*   `camera.stop_recording()`: 停止錄影。
*   `camera.stop_preview()`: 停止預覽。
*   `camera.close()`: 關閉攝影機。
*   `camera.resolution = (width, height)`: 設定解析度。
*   `camera.framerate = fps`: 設定幀率。

**範例 (拍照)：**
```python
from picamera import PiCamera
from time import sleep

camera = PiCamera()

try:
    camera.resolution = (1024, 768)
    camera.start_preview()
    sleep(2) # 給予攝影機暖機和自動白平衡的時間
    camera.capture('my_image.jpg')
    print("照片已儲存為 my_image.jpg")
except Exception as e:
    print(f"發生錯誤: {e}")
finally:
    camera.stop_preview()
    camera.close()
```

#### b) 新版攝影機模組 (Pi 3/4/5 with official camera modules) - `picamera2` (modern, 基於 `libcamera`)

`picamera2` 是 `libcamera` 框架的 Python 綁定，支援更新的樹莓派攝影機和功能。

**安裝：**
```bash
pip install picamera2
```

**核心指令：**
*   `Picamera2()`: 初始化攝影機對象。
*   `picam2.start()`: 開始攝影機串流。
*   `picam2.capture_array()`: 捕獲一個 NumPy 陣列的幀 (常用於與 OpenCV 結合)。
*   `picam2.capture_file('image.jpg')`: 拍照。
*   `picam2.create_video_encoder()`: 創建影片編碼器。
*   `picam2.start_recording()`: 開始錄影。
*   `picam2.stop_recording()`: 停止錄影。
*   `picam2.stop()`: 停止攝影機串流。
*   `picam2.close()`: 關閉攝影機。
*   `picam2.configure(config)`: 配置攝影機串流 (預覽、影片、靜態影像)。

**範例 (即時預覽並拍照)：**
```python
from picamera2 import Picamera2, Preview
import time
import cv2
import numpy as np

picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(preview_config)

picam2.start()
time.sleep(2) # 預留時間讓攝影機啟動

print("Press 'c' to capture image, 'q' to quit.")

while True:
    frame = picam2.capture_array() # 捕獲 NumPy 陣列
    cv2.imshow("PiCamera2 Live Feed", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"image_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Captured {filename}")
    elif key == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()
```

---

### 4. 針對專業相機 (DSLR, 無反相機) - `gphoto2-python`

對於在 Linux 或 macOS 上連接 DSLR 或一些無反相機，`gphoto2` 是一個強大的命令行工具。`gphoto2-python` 則是它的 Python 綁定。

**安裝 (首先需要安裝 gphoto2 工具本身，然後再安裝 Python 綁定)：**
```bash
# 在 Debian/Ubuntu:
sudo apt-get install gphoto2

# 然後安裝 Python 綁定:
pip install gphoto2-python
```

**核心指令：**
*   `gphoto2.Camera()`: 創建攝影機對象。
*   `camera.init()`: 初始化攝影機。
*   `camera.capture_image()`: 拍攝一張照片，並回傳照片路徑。
*   `camera.capture_preview()`: 捕獲預覽影像。
*   `camera.get_config()`: 獲取攝影機配置樹。
*   `camera.set_config_value(path, value)`: 設定配置值。
*   `camera.exit()`: 退出攝影機連線。

**範例 (拍照)：**
```python
import gphoto2 as gp
import os
import time

print("Connecting to camera...")
camera = gp.Camera()
camera.init()

print("Capturing image...")
file_path = camera.capture(gp.GP_CAPTURE_IMAGE)

print(f"Image captured: {file_path.name}")

# 將影像從攝影機下載到本地
target_path = os.path.join('/tmp', file_path.name)
camera_file = camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
camera_file.save(target_path)

print(f"Image saved to {target_path}")

camera.exit()
print("Camera disconnected.")
```

---

### 總結

「Python 針對 camera 的指令」的選擇完全取決於你的硬體、作業系統和需求。
*   **最常見且通用**：`OpenCV` (用於大多數網路攝影機、USB 攝影機和網路串流)。
*   **樹莓派專用**：`picamera` (舊版) 或 `picamera2` (新版)。
*   **專業相機**：`gphoto2-python` (多用於 Linux/macOS 的 DSLR)。

在開始之前，請務必確認你的攝影機驅動程式已正確安裝，並且 Python 環境中已安裝了所需的程式庫。
