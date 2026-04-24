## Claude Code 概述
### - Claude Code 是一個代理編碼工具，可以讀取您的程式碼庫、編輯檔案、執行命令，並與您的開發工具整合。可在您的終端機、IDE、桌面應用程式和瀏覽器中使用。

### - Claude Code 是一個由 AI 驅動的編碼助手，可幫助您建立功能、修復錯誤和自動化開發任務。它理解您的整個程式碼庫，並可以跨多個檔案和工具工作以完成任務。

### 在VS CODE 中使用 Claude code
### 🔧 一、安裝步驟
- 在 VS Code 中按下 Cmd+Shift+X（Mac）或 Ctrl+Shift+X（Windows/Linux）開啟擴充套件市集，搜尋 "Claude Code"，點選由 Anthropic 發布的官方套件，再按 Install。   
- 安裝完成後，VS Code 右上角的編輯器工具列會出現一個 Spark（⚡）圖示。若沒看到，請確認 VS Code 版本是否符合需求。  
### 🔑 二、申請與設定帳號
### - 訂閱需求  
Claude Code 至少需要 Pro 訂閱方案（每月 $20 美元），免費方案無法使用 Claude Code。 Braincuber
### - 登入流程  
第一次開啟面板時，會出現登入畫面。點選 Sign in，完成瀏覽器授權即可。如果你在終端機設定了 ANTHROPIC_API_KEY 環境變數，但仍出現登入提示，建議從終端機用 code . 指令啟動 VS Code，這樣它才能繼承你的環境變數設定。  
### - 登入後
登入後會顯示「Learn Claude Code」引導清單，點選每個項目的 Show me 可逐步了解功能，或點 X 關閉。若想之後重新開啟，可在 VS Code 設定的「Extensions → Claude Code」中取消勾選「Hide Onboarding」。  
### 🖥️ 三、介面說明
- Claude Code 的 Spark（⚡）圖示會出現在三個地方：

    編輯器工具列（右上角）：最快速的開啟方式，需要有檔案開啟才會顯示  
    活動列（左側邊欄）：點擊可開啟對話清單，隨時可見，不需要開啟檔案
    狀態列（右下角）：顯示「✱ Claude Code」，即使沒有開啟檔案也能使用 Claude

- 提示輸入框功能
    VS Code 擴充套件提供了一個專用側邊欄面板，可即時透過 Inline Diff（行內差異）查看 Claude 的修改內容。 Anthropic
    Claude Code 支援兩種權限模式，可透過提示框底部的模式按鈕切換：  
        一般模式（Normal）：每次操作前都會向你請求確認  
        計畫模式（Plan Mode）：先讓你審查並編輯 Claude 的計畫再執行 Claude  

- 審查修改  
當 Claude 想要編輯檔案時，會顯示**並排差異比較（Side-by-side Diff）**，讓你在授權前看清楚原始內容與建議修改的對比。你可以直接接受、拒絕，或告訴 Claude 要改什麼。  
### ⚙️ 四、操作流程
- 基本流程
    1. 開啟 Claude 面板：點擊 Spark 圖示，或按 Cmd+Shift+P → 輸入「Claude Code」  
    2. 輸入你的問題或指令：例如「幫我解釋這段程式碼」、「找出這個函式的 bug」
    3. @-提及檔案或程式碼：Claude 會自動看到你選取的文字；按 Option+K（Mac）/ Alt+K（Windows/Linux）可將選取範圍插入為 @file.ts#5-10 形式的參照
    4. 審查並接受修改：在 Diff 畫面中確認 Claude 的建議，按接受或拒絕  
- 多對話管理  
可用 Cmd+N（Mac）或 Ctrl+N（Windows）開啟新對話，支援在不同分頁或視窗中同時執行多個對話，每個工作區各自維護獨立的 context。 Claude Fast
- Checkpoint 回滾  
Claude Code 有**自動存檔（Checkpoint）**功能，在每次修改前自動儲存程式碼狀態，可隨時按兩下 Esc 或執行 /rewind 指令，回到先前的程式碼狀態。   
- Plugin 管理  
在提示框中輸入 /plugins 可開啟 Manage Plugins 介面，安裝或關閉各種擴充功能，也可以管理 Marketplace 來源。  
### 📋 快速鍵總整理
| 功能 | Mac | Windows/Linux|
| --- | ---- | ----|  
| 開啟擴充套件市集 | Cmd+Shift+X | Ctrl+Shift+X |
| 指令面板 | Cmd+Shift+P | Ctrl+Shift+P |
| 插入 @-提及 | Option+K | Alt+K | 
| 新對話 | Cmd+N | Ctrl+N | 
| 回滾程式碼 | 按兩下 Esc 或 /rewind | 同左 |  
