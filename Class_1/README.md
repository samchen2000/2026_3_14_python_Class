# 2020/3/14 上課影片
## 2026/3/14 課程
### 2026_03_14_早上
https://www.youtube.com/watch?v=xCwNvjKsdBs

### 2026_03_14_下午
https://www.youtube.com/watch?v=QAB9R0uFqjM


## 上設需先預安裝軟體  :
1. 安裝 vscode , git , putty , vnc viewer , kiro
2. 進入 Github 網站登入
3. vscode or kiro 使用 terminal 輸入 : git config user.name " my name"  
                              git config user.email "my email"  
4. 要在 vscode 上傳 GitHub 需要輸入^^^^^^^^^^   
5. 


## 使用RaspBerry Pi
1. 先進入 respberry pi 的網站 進入 software software
2. 先安裝respberry 燒錄器 , 再選擇 DEVICE : respberry Pi5 -> 作業系統 : respberry Pi5 OS(64-bit) -> 插入SD card 執行下載安裝
3. 安裝 warp terminal
4. 目前使用需要有 wifi , 確認Pi5 有沒有連上主機
5. 在 warp terminal 輸入 : ssh pi@piSamchen01.local <-- pi5 一開始在燒錄中設定的主機名稱.
6. ~ ssh pi@piSamchen01.local pi@pisamchen01.local's password: <-- 輸入燒錄設定中設定的密碼 :
7. sudo raspi-config <--進入系統配置檔
8. 安裝 VNC viewer <-- 使用VNC Viewer 要確定 系統配置檔 VNC Enable
9. 進入 VNC 輸入主機名稱 pi@piSam0216.local
10. 可以用 VScode 載入 SSH , 需要在VS code 安裝 
```
Remote-SSH\           
```

## 在家測試心得
1. 使用 MINI HDMI 連接在螢幕 使用USB 鍵盤滑鼠接到 Pi5 上,新增一個家裡的無線網路.
2. 連接 EthernetHUB 將有線網路 連接到 Pi5 and 電腦 ,要確定可以上網,因為Pi5 需要RTC 時間透過 NTP 校準, 如果時間不準, 目前遇到的狀況 系統會停掉,但是應該有其他方式 鎖定RTC ,目前還沒有找到
3. 使用 Putty 也可以進入 SSH.
4. 已嘗試在VS code 連接 Pi5 並加入檔案.

