## OpenClaw
- OpenClaw 是一款運行在使用者裝置上的個人人工智慧助理。它透過集中式網關將即時通訊服務（WhatsApp、Telegram、Slack、Discord、iMessage 等）與人工智慧編碼代理連接起來。

設定安裝
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

API key : 
進去 gemini AI studio 去創建一個 API key

