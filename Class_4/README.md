# 2020/4/11 上課影片
## 2026/4/11 課程
### 2026_04_11_早上
https://www.youtube.com/watch?v=CqtZD3MlhpI
### 2026_04_11_下午
https://www.youtube.com/watch?v=zZJCgnm-yKQ

## 4/11 上課筆記: (上午)
在本機端安裝 claude code
```
https://docs.ollama.com/integrations/claude-code
```
### Install Claude Code:
```
#macOS / Linux
curl -fsSL https://claude.ai/install.sh | bash

#windows
irm https://claude.ai/install.ps1 | iex
```
### Quick setup
```
ollama launch claude
```
### Run directly with a model
```
ollama launch claude --model kimi-k2.5:cloud
```

## 4/11 上課筆記: (下午)
### Open-WebUI 介紹
- Open WebUI 是一個功能強大、可自託管且開源的 AI 前端介面，專為「離線運作」設計，常搭配 Ollama 執行本地 LLM。它以ChatGPT 般的UI界面提供了模型管理、RAG 知識庫、文件處理、多人聊天、語音互動等進階功能。通常使用 Docker 安裝。
### 快速安裝方式 (使用 Docker)
```
docker run -d \
--network=host \
-v open-webui:/app/backend/data \
-e OLLAMA_BASE_URL=http://127.0.0.1:11434 \
-e GEMINI_API_KEY=個人的API KEY \
--name open-webui \
--restart always \
ghcr.io/open-webui/open-webui:main
```
### 或是 (不使用 API key 而使用 Ollama 安裝的本地模型)
```
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main

```
- 這個命令做了哪些事情呢？

#### 1. Pull image: 先檢查本地有沒有安裝 ghcr.io/open-webui/open-webui:main 這個 image，如果沒有 Image 就從 docker hub 拉下來。image 是一個軟體包，包含程式碼、環境設定等等資訊，這些 image 通常會被放在 docker hub 上，如果說 Github 是程式碼的雲端；HuggingFace 是語言模型的雲端，那 docker hub 就是 image 的雲端。
#### 2. Create container: docker 會根據這個 image 創建一個容器
#### 3. Configure container: 根據命令的選項來設定。舉例來說： -d 表示在後台運行、-p 表示容器運行的 Port 設定，還有其他設定就請自己看文件吧！
#### 4. Start container: 啟動容器，因為我們的 port 設為 3000:8080 ，前面的數字表示本機的 port，後面則是容器的 port
- 開啟瀏覽器造訪 http://localhost:3000