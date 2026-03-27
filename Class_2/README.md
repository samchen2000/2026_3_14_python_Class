# 2020/3/21 上課影片
## 2026/3/21 課程
### 2026_03_21_早上
https://www.youtube.com/watch?v=evIGCpBdhvU

### 2026_03_21_下午
https://www.youtube.com/watch?v=_JEWTw_UG8M

## 3/21 上課筆記:
1. 如果 Kiro 無法使用 就使用VSCode
2. 設定 Wifi Dongle 熱點 
   Wifi name : F602-08-wifi
   密碼 : raspberry 
3. 如果 kiro 無法連線 raspberry 可以將 本機端的 .ssh or .kiro 刪除再連線 raspberry pi.
4. 程式中呼叫
```     
   "google-genai>=1.68.0",
   "python-dotenv>=1.2.2",
```
需要安裝 :  
```
pip install google-genai
pip inatall python-dotenv
```           
---
## 5. 安裝 uv (現代化的 Python 套件管理與虛擬環境工具)         
### - Linux 安裝  
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
### - 在已有的專案
```
uv init --python 3.10
uv venv
uv sync
```
### - 建立新專案
```
uv init my-project
cd my-project
uv sync
```
### - 建立虛擬環境
```
uv venv
```
### - 啟用虛擬環境
```
source .venv/bin/activate  # macOS/Linux
```
## 設定 API 金鑰
- 將 API 金鑰設為環境變數 `GEMINI_API_KEY` 在本地增加 `.env`檔案 將 GEMINI_API_KEY=xxxxxxxxxx 填入.
- 增加 `.gitignore`檔案 將.venv/ , .env 寫入, 避免將 檔案上傳到 github.
- 提供使用

## 回家作業
1. 在 raspberry pi 安裝 ollima 

### 安裝 ollama：
```
curl -fsSL https://ollama.com/install.sh  | sh
```
### 安裝 ollama 後：
```
ollama run tinydolphin
```

## 在家測試心得
1. 要在 google AI studio 申請一個 API Key , 可以透過 程式呼叫 gemini AI 進行問題詢問.
2. 安裝完 選擇安裝模型, 可以參考下面推薦清單  

| 模型          |	參數大小       |	 特色	                  |  適合場景	                   |  下載指令                |  
| ------------- | ------------- | ------------------------- |------------------------   | ------------------------ |
| llama3.2      | 1B / 3B       | Meta 最新輕量模型，速度快   | 快速問答、文字摘要、入門測試 |	ollama pull llama3.2    |
| llama3.1:8b	 | 8B	           | 品質與速度的平衡點     	  | 日常對話、內容撰寫、翻譯	   | ollama pull llama3.1:8b |
| mistral	    |7B     	     | 歐洲團隊開發，推理能力不錯   |	分析、摘要、邏輯推理	      | ollama pull mistral     |
| gemma2	       |2B / 9B / 27B  | Google 開源，多種大小可選   | 研究、實驗、多語言任務	      | ollama pull gemma2     |
| qwen2.5	    | 0.5B – 72B    |	中文表現突出，多種大小可選 | 中文對話、中文內容生成	    | ollama pull qwen2.5    |
| codellama	    |7B / 13B / 34B |	Meta 程式碼專用模型	     | 程式碼生成、程式碼解釋	      | ollama pull codellama  |

