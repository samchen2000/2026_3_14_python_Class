import tkinter as tk
from tkinter import messagebox
import google.generativeai as genai
import os

# 設置 API 金鑰（同時支援 GEMINI_API_KEY 和 GOOGLE_API_KEY）
API_KEY = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
if not API_KEY:
    messagebox.showerror("錯誤", "請設置 GEMINI_API_KEY 或 GOOGLE_API_KEY 環境變數。")
    exit(1)

genai.configure(api_key=API_KEY)
# gemini-pro 可能在當前 v1beta 版本無法使用，請改用可用模型名稱
# 可透過 `genai.list_models()` 查詢來獲得最新名稱
model = genai.GenerativeModel('models/gemini-2.5-flash')
model_list = genai.list_models()

def send_question():
    question = entry.get()
    style = style_var.get()
    if not question.strip():
        messagebox.showwarning("警告", "請輸入問題。")
        return

    try:
        prompt = f"請用{style}風格回答以下問題，並用繁體中文：{question}"
        response = model.generate_content(prompt)
        text_area.insert(tk.END, f"Sam 問: {question}\n")
        text_area.insert(tk.END, f"Gemini 小幫手 ({style}): {response.text}\n\n")
        entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("錯誤", f"發生錯誤: {str(e)}")

# 創建主視窗
root = tk.Tk()
root.title("Gemini 小幫手")
root.geometry("500x400")

# 風格選擇
style_var = tk.StringVar(value="友好")
style_label = tk.Label(root, text="選擇AI風格:")
style_label.pack(pady=5)
style_menu = tk.OptionMenu(root, style_var, "友好", "專業", "幽默", "簡潔", "詳細")
style_menu.pack(pady=5)

# 輸入框
entry = tk.Entry(root, width=50)
entry.pack(pady=10)

# 發送按鈕
send_button = tk.Button(root, text="發送", command=send_question)
send_button.pack()

# 文本區域顯示對話
text_area = tk.Text(root, height=15, width=60, wrap="word", font=("微軟正黑體", 12))
text_area.pack(pady=10)

# 運行 GUI
root.mainloop()