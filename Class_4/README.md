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

### 補充心得
1. 因為open-webui 有更新版本,所以依照網上安裝方式更新
- A. 停止並刪除當前容器  :  
**這將停止正在運行的容器並刪除它，但不會刪除儲存在 Docker 磁碟區中的資料。 （如果您的容器名稱不同，請在整個更新過程中將 open-webui 替換為您的容器名稱。）.**
```
docker rm -f open-webui
```
- B. 拉取最新的 Docker 映像 ：  
**這將更新 Docker 映像，但不會更新正在運行的容器或其資料。**
``` 
docker pull ghcr.io/open-webui/open-webui:main
```
- C. 使用更新的鏡像和附加的現有磁碟區重新啟動容器 ：  
**如果您沒有刪除現有數據，這將使用更新的鏡像和現有數據啟動容器。如果您刪除了現有數據，這將使用更新的鏡像和新的空卷啟動容器。 對於 Nvidia GPU 支持，請在 docker run 命令中新增 --gpus all.**
```
docker run -d -p 3000:8080 -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main
```

2. 自己依照步驟更新後就無法進入 open-webui ,
 重新關閉Docker stop open-webui ,
 再打開 Docker start open-webui 還是沒有辦法打開,所以重新執行
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