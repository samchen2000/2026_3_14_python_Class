import tkinter as tk
from tkinter import ttk


def calculate():
    try:
        # 讀取輸入（支援 0x 開頭或十進位）
        value_str = entry.get().strip()
        if value_str.startswith("0x") or value_str.startswith("0X"):
            line_count = int(value_str, 16)
        else:
            line_count = int(value_str)

        # 計算三段
        # reg_msb = (line_count >> 12) & 0x0F
        # reg_mid = (line_count >> 4) & 0xFF
        # reg_lsb = (line_count << 4) & 0xF0
        reg_msb = (line_count >> 12) & 0x0F
        reg_mid = (line_count >> 4) & 0xFF
        reg_lsb = (line_count >> 4) & 0xFF
        # 顯示結果（16進位）
        msb_var.set(f"0x{reg_msb:02X}")
        mid_var.set(f"0x{reg_mid:02X}")
        lsb_var.set(f"0x{reg_lsb:02X}")

    except ValueError:
        msb_var.set("Error")
        mid_var.set("Error")
        lsb_var.set("Error")


# 建立視窗
root = tk.Tk()
root.title("LineCount 計算工具")
root.geometry("320x240")

# 輸入欄位
ttk.Label(root, text="輸入 lineCount (十進位或0x):").pack(pady=5)
entry = ttk.Entry(root)
entry.pack(pady=5)

# 計算按鈕
ttk.Button(root, text="計算", command=calculate).pack(pady=10)

# 結果顯示
msb_var = tk.StringVar()
mid_var = tk.StringVar()
lsb_var = tk.StringVar()

ttk.Label(root, text="MSB (Addr-1):").pack()
ttk.Label(root, textvariable=msb_var).pack()

ttk.Label(root, text="MID (Addr+0):").pack()
ttk.Label(root, textvariable=mid_var).pack()

ttk.Label(root, text="LSB (Addr+1):").pack()
ttk.Label(root, textvariable=lsb_var).pack()

# 執行
root.mainloop()
