# 2020/4/18 上課影片
## 2026/4/18 課程
### 2026_04_18_早上
https://www.youtube.com/watch?v=wTmbvDS5nl8
### 2026_04_18_下午
https://www.youtube.com/watch?v=qnoOqfhAfwU
## 4/18 上課筆記: (上午)
1. 使用Notion 
2. 使用 python colab
## 4/18 上課筆記: (下午)
1. 申請telegram 
2. 申請後再telegram bot
3. 在 open-webui 設定函式 action
```
"""
title: Send to Telegram
author: Your Name
version: 0.1.0
requirements: requests, pydantic
"""

from pydantic import BaseModel, Field
from typing import Optional
import requests

class Action:
    class Valves(BaseModel):
        bot_token: str = Field(
            default="",
            description="Telegram Bot Token (從 @BotFather 取得)"
        )
        chat_id: str = Field(
            default="",
            description="你的 Telegram Chat ID (可向 @userinfobot 查詢)"
        )

    def __init__(self):
        self.valves = self.Valves()

    async def action(
        self,
        body: dict,
        __user__=None,
        __event_emitter__=None,
        __event_call__=None,
    ) -> Optional[dict]:
        """將訊息發送到 Telegram"""
        
        # 安全取得最後一句對話
        messages = body.get("messages", [])
        if not messages:
            return {"status": "empty"}
            
        last_message = messages[-1]
        message_content = last_message.get("content", "")
        
        if not self.valves.bot_token or not self.valves.chat_id:
            if __event_emitter__:
                await __event_emitter__({
                    "type": "message",
                    "data": {
                        "content": "❌ 未設定 Telegram 機器人 Token 或 Chat ID"
                    }
                })
            return {"status": "failed"}
        
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "description": "正在發送到 Telegram...",
                    "done": False
                }
            })
        
        try:
            # Telegram Bot API URL
            api_url = f"https://api.telegram.org/bot{self.valves.bot_token}/sendMessage"
            
            # 確保訊息不會超過 Telegram 的 4096 字元上限
            if len(message_content) > 4000:
                message_content = message_content[:4000] + "...\n\n(❗️字數過長，已截斷)"
            
            # 加入發送者名稱提示
            sender = __user__.get("name", "一般使用者") if __user__ else "使用者"
            formatted_msg = f"🔔 來自【{sender}】的備忘錄:\n\n{message_content}"
            
            payload = {
                "chat_id": self.valves.chat_id,
                "text": formatted_msg
                # ⚠️ 這裡刻意不使用 "parse_mode": "Markdown" 
                # 因為 AI 產生的內容常有未閉合的星號、底線等特殊符號，會導致 Telegram 解析失敗報錯
            }
            
            response = requests.post(api_url, json=payload, timeout=10)
            result = response.json()
            
            if __event_emitter__:
                if response.status_code == 200 and result.get("ok"):
                    await __event_emitter__({
                        "type": "message",
                        "data": {
                            "content": "✅ 訊息已經用小飛機 ✈️ 發送到 Telegram 囉！"
                        }
                    })
                else:
                    await __event_emitter__({
                        "type": "message",
                        "data": {
                            "content": f"❌ Telegram 發送失敗: {result.get('description', '未知錯誤')}"
                        }
                    })
        except Exception as e:
            if __event_emitter__:
                await __event_emitter__({
                    "type": "message",
                    "data": {
                        "content": f"❌ 系統發生錯誤: {str(e)}"
                    }
                })
        
        return {"status": "completed"}
```
