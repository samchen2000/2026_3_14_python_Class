# 2026_3_14_python_Class
## 樹莓派+Python 開發 Google Gemini AI 智慧應用實戰班

- 2026/3/14 09:00~12:00 樹莓派安裝和開發環境的配置  
- 2026/3/14 13:30~16:30 基本的 Linux 指令  
- 2026/3/21 09:00~12:00 設定虛擬環境和安裝程式庫   
- 2026/3/21 13:30~16:30 google gemini api  
- 2026/3/28 09:00~12:00 Python 基本語法  
- 2026/3/28 13:30~16:30 Python 資料結構  
- 2026/4/11 09:00~12:00 Python 套件  
- 2026/4/11 13:30~16:30 Python 物件導向  
- 2026/4/18 09:00~12:00 geminiAI 的純文字輸入內容產生文字  
- 2026/4/18 13:30~16:30 geminiAI 的文字和圖片輸入，產生文字   
- 2026/4/25 09:00~12:00 geminiAI 的產生文字串流，設定文字產生  
- 2026/4/25 13:30~16:30 geminiAI 的新增系統指示  

## 上課 Meet :

https://meet.google.com/nnj-tzex-mwj

## 上課 講義 :

https://github.com/roberthsu2003/LLMs_Raspberry

WiFi
SSID：A590301
PW：A590301AA

raspberry name : pi4Sam0216
user name : pi
password : raspberry

## 安裝raspberry pi imager

## 設定 機器帳號密碼
1. 使用Raspberry pi 4 的機器
2. Raspberry name : pi4Sam0216
3. user name : pi
4. password : raspberry

5. 使用 putty 選擇 SSH IP : pi@pi4Sam0216

6. 進入 Terminal 輸入 : sudo raspi-config  
7. 在畫面中先選第一項 "3. interface Options" enable VNC "13 VNC" 使用 "Tab" key 跳到 back 返回上一層.  
8. 選擇"5 Localisation Options" -> "L1 Locale" 選 en_GB.UTF-8 , en_US.UTF-8 , zh_TW.UTF-8 按 space key 打星號,然後 選擇 OK 更新語系  
9. 選擇"5 Localisation Options" -> "L2 TimeZone" 選 "Asia" -> "Taipei"  
10. 選擇 "8 Update" 之後 "Finish"  
11. 也可以先不用設定 8~10 項 , VNC enable 打開 可以使用 vnc Viewer, 或是接 microHDMI 連接螢幕設定. 在control center 裡面設定.
12. 使用電腦 wifi 作為熱點 :
    上課用 wifi 熱點名稱 : F602-08-wifi
                密碼    : raspberry
13. 安裝 kiro
📌 Vibe 模式開發
快速體驗 Vibe Coding 完成開發程式。
📌 Spec 模式：規格驅動開發（Spec-Driven）:
只要輸入簡單開發提示就可變成詳細的需求與架構，產生完整規格文件。
🤖 事件驅動代理（Agent Hooks）
可根據事件（如儲存檔案）自動觸發任務，像是產生文檔、測試、優化程式碼等。
🧭 代理指南（Agent Steering）
自訂每個專案的開發規範、語法命名等程式風格要求。
🧩 VS Code 基底，熟悉又升級的操作體驗
匯入你的設定檔與擴充套件，無需捨棄熟悉的開發環境。

14. 在 kiro 安裝延伸程式 " open remunt - SSH " " 繁體中文套件 "
