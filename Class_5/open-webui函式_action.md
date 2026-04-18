# Open-WebUI 函式 Action 範例解釋

這個文件 `open-webui函式_action.py` 是一個 Open-WebUI 平台的 Action 範例程式碼。Open-WebUI 是一個開源的 Web UI 框架，用於建構聊天機器人或對話系統的擴充功能。這個腳本示範了如何建立一個簡單的 Action，用來分析對話訊息的長度並將結果附加到訊息中。

## 檔案結構與基本資訊

```python
"""
title: 基礎 Action 範例
author: YourName
version: 1.0
"""
```

- **Docstring**：這是檔案的文檔字串，包含標題、作者和版本資訊。
- **用途**：用來描述這個 Action 的基本資訊，方便識別和維護。

## 類別定義

```python
from typing import Optional, Callable, Any

class Action:
    def __init__(self):
        pass
```

- **匯入模組**：
  - `typing`：用於型別提示，提供 `Optional`、`Callable`、`Any` 等型別註解。
- **Action 類別**：
  - 這是主要的類別，繼承自 `object`（預設）。
  - `__init__` 方法：建構函式，目前是空的，表示沒有初始化邏輯。

## Action 方法

```python
async def action(
    self,
    body: dict,
    __user__: Optional[dict] = None,
    __event_emitter__: Optional[Callable[..., Any]] = None,
) -> Optional[dict]:
```

- **方法簽章**：
  - `async def`：這是一個異步方法，使用 `async` 關鍵字，表示可以在非同步環境中執行。
  - **參數**：
    - `self`：類別實例的參考。
    - `body: dict`：主要的輸入資料，通常包含對話訊息等資訊。
    - `__user__: Optional[dict] = None`：可選的用戶資訊字典。
    - `__event_emitter__: Optional[Callable[..., Any]] = None`：可選的事件發射器函式，用於發送事件（例如 SSE 串流）。
  - **回傳型別**：`Optional[dict]`，表示可能回傳一個字典或 `None`。

## 方法邏輯

```python
# 取得所有對話
messages = body.get("messages", [])
if not messages:
    return body

# 取得最後點擊欲處理的那則訊息
last_message = messages[-1]
message_content = last_message.get("content", "")
message_len = len(message_content)

# ⚠️ 由於目前前端接收 Action 的 SSE 串流時易發生 JSON 解析錯誤
# 最穩定相容的做法是直接將結果附加在對話內容中並回傳 body
last_message["content"] += f"\n\n*(系統分析：這則訊息的長度是 {message_len} 個字)*"

# 回傳變更後的 body 讓前端更新畫面
return body
```

- **取得對話訊息**：
  - `messages = body.get("messages", [])`：從 `body` 字典中提取 `messages` 鍵的值，如果不存在則預設為空列表。
  - `if not messages: return body`：如果沒有訊息，直接回傳原始的 `body`，避免進一步處理。

- **處理最後一條訊息**：
  - `last_message = messages[-1]`：取得列表中的最後一條訊息（通常是最新或被點擊的訊息）。
  - `message_content = last_message.get("content", "")`：提取訊息的內容，如果沒有內容則預設為空字串。
  - `message_len = len(message_content)`：計算訊息內容的字元長度。

- **附加分析結果**：
  - 註釋說明：由於前端在接收 SSE（Server-Sent Events）串流時可能發生 JSON 解析錯誤，因此選擇將結果直接附加到訊息內容中，而不是使用事件發射器。
  - `last_message["content"] += f"\n\n*(系統分析：這則訊息的長度是 {message_len} 個字)*"`：將分析結果以 Markdown 格式附加到訊息內容的末尾。格式為斜體文字，顯示訊息長度。

- **回傳結果**：
  - `return body`：回傳修改後的 `body` 字典，讓前端更新對話畫面。

## 整體功能與用途

- **功能**：這個 Action 會分析對話中最後一條訊息的字元長度，並將結果以系統分析的形式附加到訊息中。
- **應用場景**：可用於聊天機器人中，提供訊息長度的統計資訊，或作為更複雜分析的基礎。
- **注意事項**：
  - 由於前端 SSE 串流的限制，目前採用直接修改訊息內容的方式，而不是發送獨立事件。
  - 這個範例是基礎的，可以擴充為更複雜的邏輯，例如情感分析或關鍵字提取。

## 潛在改進

- **錯誤處理**：可以加入檢查 `body` 或 `messages` 的型別驗證。
- **事件發射**：如果前端支援更好的 SSE，可以使用 `__event_emitter__` 發送事件而不是修改內容。
- **多語言支援**：目前訊息是中文，可以根據用戶語言調整。

這個腳本展示了 Open-WebUI Action 的基本結構和異步處理方式，適合用於擴充聊天系統的功能。