# 程式流程詳細說明

這個程式是一個基於 Google Apps Script (GAS) 的 LINE Bot 應用程式，主要功能是作為個人 AI 助理，整合 Google Gemini API 來處理用戶訊息，並管理行程、待辦事項和備忘錄。程式使用 Google Sheets 作為數據存儲，並通過 LINE Messaging API 與用戶互動。以下是程式的整體流程說明。

## 1. 整體架構與初始化

### 技術棧：
- **Google Apps Script (GAS)**：運行在 Google Cloud 上，提供 Webhook 端點。
- **LINE Messaging API**：處理用戶訊息和回覆。
- **Google Gemini API**：用於自然語言處理和意圖分析。
- **Google Sheets**：作為數據庫，存儲用戶 ID、行程、待辦事項和備忘錄。

### 主要文件：
- `code.gs`：主要邏輯入口，處理 Webhook 和訊息路由。
- `lineAPI.gs`：LINE API 相關函數，回覆訊息和推送通知。
- `database.gs`：數據操作函數，與 Google Sheets 互動。
- `geminiAPI.gs`：Gemini API 調用邏輯（注意：此文件與 `database.gs` 中的 `callGemini` 函數重複，可能為備份或版本差異）。

### 初始化：
- 程式通過 `doPost(e)` 函數接收 LINE Webhook 請求。
- 使用 `PropertiesService.getScriptProperties()` 存儲敏感資訊，如 LINE Channel Access Token 和 Gemini API Key。
- 確保數據表存在（`ensureDataExists()`），包括 "用戶"、"行事曆"、"待辦清單"、"備忘錄" 等工作表。

## 2. 訊息處理流程

### Webhook 入口 (`doPost` in `code.gs`)：
- 解析 LINE 發送的 JSON 事件。
- 對於每個事件：
  - 如果是 `message` 類型且為文字，調用 `handleMessage(event)`。
  - 如果是 `follow` 類型（新用戶關注），調用 `handleNewUser(event)` 發送歡迎訊息。
- 回覆 "OK" 以確認接收。

### 新用戶處理 (`handleNewUser` in `code.gs`)：
- 儲存用戶 ID 到 "用戶" 工作表。
- 發送歡迎訊息，介紹功能。

### 訊息處理 (`handleMessage` in `code.gs`)：
- 提取用戶訊息和 ID。
- 檢查快速指令（無需 AI，直接處理）：
  - 行程相關：如 "今天"、"明天"、"本週" 等，查詢並回覆行程卡片。
  - 待辦相關：如 "待辦清單"，回覆待辦列表。
  - 備忘錄相關：如 "備忘錄"，回覆備忘錄列表。
  - 完成/刪除操作：如 "完成#1"、"刪除行程#2"，直接更新數據庫並回覆結果。
  - 幫助：顯示使用說明。
- 如果不是快速指令，調用 `callGemini(userMessage)` 進行 AI 分析。
- 根據 AI 返回的意圖（JSON 格式），執行相應動作：
  - `add_event`：新增單個行程。
  - `add_events`：新增多個行程。
  - `add_todo`：新增待辦事項。
  - `add_memo`：新增備忘錄。
  - `query_schedule`：查詢行程。
  - `complete_todo`：完成待辦。
  - `delete_event`：刪除行程。
  - `general_chat`：一般對話回覆。

## 3. AI 分析與意圖處理 (`callGemini` in `database.gs` or `geminiAPI.gs`)

### Gemini API 調用：
- 使用 `gemini-2.5-flash` 模型。
- 構造系統提示（System Prompt），包含當前時間、最近待辦和行程上下文。
- 提示要求 AI 以 JSON 格式返回意圖和參數。
- 意圖規則包括新增、查詢、完成等操作。

### 回應處理：
- 解析 AI 返回的 JSON。
- 如果解析失敗，回覆預設訊息。
- 根據意圖調用對應函數（如 `addEvent`、`addTodo` 等）。

## 4. 數據操作與回覆 (`database.gs` 和 `lineAPI.gs`)

### 數據存儲：
- 使用 Google Sheets 工作表：
  - "用戶"：存儲用戶 ID。
  - "行事曆"：行程數據（日期、時間、項目、狀態、提醒）。
  - "待辦清單"：待辦事項（項目、類別、狀態、完成時間）。
  - "備忘錄"：備忘錄內容。
- 函數如 `addEvent`、`getTodoList` 等操作 Sheets。

### 回覆機制：
- 使用 LINE Flex Message（卡片格式）回覆複雜內容，如行程列表或成功確認。
- 簡單文字回覆使用 `replyToLine`。
- 推送通知（如晨報、週報）使用 `pushToLine`。

## 5. 自動功能
- **提醒檢查** (`checkReminders`)：每 30 分鐘檢查即將到來的行程，推送提醒。
- **每日晨報** (`dailyReport`)：每天早上推送今日行程和待辦摘要。
- **週報** (`weeklyReport`)：每週推送待辦完成統計。
- 這些通過 GAS 觸發器（Triggers）自動執行。

## 6. 錯誤處理與日誌
- 使用 `Logger.log` 記錄錯誤和關鍵操作。
- API 調用失敗時，回覆友好訊息。

# 個人資料洩漏風險分析

根據程式內容，以下是潛在的個人資料洩漏問題評估。整體而言，程式設計相對安全，但用戶需注意配置和使用習慣：

## 正面方面（低風險）：
- **API 金鑰存儲**：LINE Access Token 和 Gemini API Key 存儲在 `PropertiesService.getScriptProperties()` 中，這是 GAS 的安全存儲方式，不會在程式碼中明文暴露。只有腳本擁有者能訪問。
- **數據本地化**：所有用戶數據（行程、待辦、備忘錄）存儲在 Google Sheets 中，位於用戶的 Google Drive。GAS 運行在 Google Cloud 上，數據不會傳送到第三方服務（除非用戶手動共享）。
- **用戶 ID 處理**：用戶 ID 僅用於推送通知和數據關聯，不會洩漏給外部。

## 潛在風險（需注意）：
- **Gemini API 數據傳輸**：用戶訊息內容會發送到 Google Gemini API 進行分析。這可能涉及隱私問題，因為訊息可能包含個人資訊（如電話號碼、行程細節）。Google 的隱私政策適用，但用戶應確保訊息不包含敏感數據，或考慮本地 AI 替代方案。
- **日誌記錄**：`Logger.log` 記錄的訊息可能包含用戶輸入或錯誤細節。如果腳本共享或被入侵，這些日誌可能洩漏資訊。建議在生產環境中移除詳細日誌。
- **Webhook 安全性**：LINE Webhook 端點是公開的（GAS 部署為 Web App）。雖然 LINE 驗證請求，但如果腳本配置錯誤（如允許匿名訪問），可能被濫用。確保 Web App 設置為 "Execute as: Me" 並限制訪問。
- **數據共享**：如果 Google Sheets 被意外共享，或腳本被複製到其他帳戶，數據可能洩漏。用戶應定期檢查權限。
- **無加密**：數據在 Sheets 中未加密存儲。如果帳戶被入侵，所有數據暴露。

## 建議：
- 使用強密碼保護 Google 帳戶，並啟用雙因素驗證。
- 避免在訊息中輸入高度敏感資訊（如銀行帳號）。
- 定期審查和清理日誌。
- 如果擔心隱私，考慮使用本地 AI 或加密數據存儲。