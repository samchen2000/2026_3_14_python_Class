# lesson3_1.py 說明文件

## 這個程式是什麼？

這是一個 **Open WebUI Filter（過濾器）** 的範例程式。

Open WebUI 是一個可以在本地端運行大型語言模型（LLM）的網頁介面。Filter 是它的插件機制，讓你可以在使用者送出訊息「之前」或 AI 回應「之後」，插入自訂的處理邏輯。

---

## 程式架構說明

### 1. 元資料（檔案頂部的註解）

```python
"""
title: Example Filter
author: open-webui
version: 0.1
"""
```

這些是 Open WebUI 用來識別這個插件的基本資訊，顯示在管理介面上。

---

### 2. `Valves`（管理員設定）

```python
class Valves(BaseModel):
    priority: int = Field(default=0, ...)
    max_turns: int = Field(default=8, ...)
```

- `Valves` 是給**管理員**設定的參數，透過 Open WebUI 後台介面調整。
- `priority`：當有多個 Filter 同時存在時，決定執行順序（數字越小越先執行）。
- `max_turns`：整個系統允許的最大對話輪數上限，預設 8 輪。

---

### 3. `UserValves`（使用者設定）

```python
class UserValves(BaseModel):
    max_turns: int = Field(default=4, ...)
```

- `UserValves` 是給**一般使用者**自己調整的參數。
- `max_turns`：使用者自己設定的對話輪數上限，預設 4 輪。

---

### 4. `inlet`（入口過濾器）

```python
def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
```

- 在使用者的訊息**送到 AI 之前**執行。
- 這裡的邏輯是：取 `UserValves.max_turns` 和 `Valves.max_turns` 兩者的**最小值**作為實際上限。
- 如果目前對話的訊息數量超過上限，就拋出例外（錯誤），阻止這次請求繼續。

```python
max_turns = min(__user__["valves"].max_turns, self.valves.max_turns)
if len(messages) > max_turns:
    raise Exception(f"Conversation turn limit exceeded. Max turns: {max_turns}")
```

簡單說：**超過對話輪數就擋下來，不讓 AI 繼續回應。**

---

### 5. `outlet`（出口過濾器）

```python
def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
```

- 在 AI 回應**回傳給使用者之前**執行。
- 這個範例只有印出 log，沒有做額外處理，直接回傳原始 body。
- 你可以在這裡修改 AI 的回應內容，例如過濾敏感詞、加上格式等。

---

## 資料流示意圖

```
使用者輸入訊息
      ↓
  [ inlet() ]  ← 可在這裡檢查、修改、或拒絕請求
      ↓
   AI 模型處理
      ↓
  [ outlet() ] ← 可在這裡修改或分析 AI 的回應
      ↓
使用者看到回應
```

---

## 如何使用

### 部署到 Open WebUI

1. 開啟 Open WebUI 管理介面。
2. 進入「工作區（Workspace）」→「函式（Functions）」。
3. 點擊「新增函式（Add Function）」。
4. 將 `lesson3_1.py` 的內容貼上，儲存。
5. 啟用這個 Filter，它就會自動套用到對話流程中。

### 調整參數

- 管理員可以在後台調整 `max_turns`（系統上限）。
- 使用者可以在自己的設定頁面調整個人的 `max_turns`。
- 實際生效的上限 = `min(使用者設定, 管理員設定)`，確保使用者無法超過管理員設定的上限。

### 擴充這個 Filter

你可以在 `inlet` 加入更多邏輯，例如：
- 關鍵字過濾
- 注入系統提示（system prompt）
- 記錄使用者行為

也可以在 `outlet` 加入：
- 過濾 AI 回應中的敏感內容
- 格式化輸出
- 統計 token 用量

---

## 重點整理

| 元件 | 角色 | 說明 |
|------|------|------|
| `Valves` | 管理員設定 | 系統層級的參數，後台調整 |
| `UserValves` | 使用者設定 | 個人層級的參數，使用者自行調整 |
| `inlet()` | 前處理 | 訊息送出前攔截，可修改或拒絕 |
| `outlet()` | 後處理 | AI 回應後攔截，可修改或分析 |
