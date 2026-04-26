#!/usr/bin/env python3
"""
YouBike 2.0 海山捷運站周邊即時監控視窗版
每 10 秒自動抓取一次新北市 YouBike 開放資料 API，
顯示海山站附近各站點的腳踏車可借數量。
"""

import math
import requests
import threading
import time
from datetime import datetime

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    raise ImportError("此程式需要 tkinter 模組，請確認 Python 已安裝 tkinter。")

# ── 海山捷運站座標 ──────────────────────────────────────────────
HAISHAN_LAT = 24.9778   # 緯度
HAISHAN_LON = 121.4647  # 經度
SEARCH_RADIUS_KM = 8.0  # 搜尋半徑（公里）
REFRESH_INTERVAL = 10   # 抓取間隔（秒）

# ── 新北市 YouBike 2.0 API ─────────────────────────────────────
API_URL = (
    "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
)

# 備用 API（若主要 API 失效可切換）
API_URL_BACKUP = (
    "https://data.ntpc.gov.tw/api/datasets/"
    "010e5b15-3823-4b20-b401-b1cf000550c5/json"
)


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    return R * 2 * math.asin(math.sqrt(a))


def fetch_ubike_data():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
        )
    }
    try:
        resp = requests.get(API_URL, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException:
        try:
            resp = requests.get(API_URL_BACKUP, headers=headers, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException:
            return None


def parse_station(raw):
    try:
        lat = float(
            raw.get("latitude") or raw.get("lat") or raw.get("StationPosition", {}).get("PositionLat", 0)
        )
        lon = float(
            raw.get("longitude") or raw.get("lng") or raw.get("StationPosition", {}).get("PositionLon", 0)
        )

        available_bikes = int(
            raw.get("available_rent_bikes")
            or raw.get("AvailableRentBikes")
            or raw.get("sbi")
            or 0
        )
        available_returns = int(
            raw.get("available_return_bikes")
            or raw.get("AvailableReturnBikes")
            or raw.get("bemp")
            or 0
        )
        total = int(
            raw.get("total")
            or raw.get("capacity")
            or raw.get("tot")
            or (available_bikes + available_returns)
        )

        name_zh = (
            raw.get("station_name")
            or raw.get("ar")
            or raw.get("StationName", {}).get("Zh_tw", "")
            or raw.get("sna", "")
            or "未知站點"
        )

        act = raw.get("act") or raw.get("ServiceStatus") or 1

        return {
            "name": name_zh,
            "lat": lat,
            "lon": lon,
            "available": available_bikes,
            "empty_slots": available_returns,
            "total": total,
            "active": str(act) in ("1", "true", "True", "NORMAL"),
        }
    except (TypeError, ValueError, KeyError):
        return None


def filter_nearby_stations(data, radius_km=SEARCH_RADIUS_KM):
    nearby = []
    if not isinstance(data, list):
        return nearby
    for raw in data:
        station = parse_station(raw)
        if not station:
            continue
        dist = haversine(HAISHAN_LAT, HAISHAN_LON, station["lat"], station["lon"])
        if dist <= radius_km:
            station["distance_m"] = int(dist * 1000)
            nearby.append(station)
    nearby.sort(key=lambda s: s["distance_m"])
    return nearby


def bike_status_symbol(available, total):
    if total <= 0:
        ratio = 0
    else:
        ratio = available / total
    if ratio >= 0.5:
        return "🟢"
    if ratio >= 0.2:
        return "🟡"
    if available > 0:
        return "🟠"
    return "🔴"


class YouBikeMonitorApp:
    def __init__(self):
        self.attempt = 0
        self.running = True
        self.root = tk.Tk()
        self.root.title("YouBike 2.0 海山捷運站即時監控")
        self.root.geometry("900x560")
        self.root.resizable(False, False)

        self.create_widgets()
        self.schedule_update(initial=True)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def create_widgets(self):
        header = tk.Label(
            self.root,
            text="🚲 YouBike 2.0 海山捷運站周邊即時監控",
            font=("Helvetica", 16, "bold"),
            pady=10,
        )
        header.pack()

        info_frame = tk.Frame(self.root)
        info_frame.pack(fill="x", padx=12)

        self.summary_label = tk.Label(info_frame, text="正在初始化資料…", anchor="w", font=("Helvetica", 11))
        self.summary_label.pack(side="left", padx=(0, 12))

        self.status_label = tk.Label(info_frame, text="尚未更新", anchor="w", font=("Helvetica", 11), fg="#333333")
        self.status_label.pack(side="left")

        self.error_label = tk.Label(self.root, text="", fg="#b00020", font=("Helvetica", 10, "bold"))
        self.error_label.pack(fill="x", padx=12, pady=(2, 10))

        columns = ("name", "distance", "available", "empty", "total", "status")
        self.tree = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings",
            height=18,
        )

        headings = {
            "name": ("站名", 320),
            "distance": ("距離", 80),
            "available": ("可借", 80),
            "empty": ("空位", 80),
            "total": ("總格", 80),
            "status": ("狀態", 190),
        }

        for col, (title, width) in headings.items():
            self.tree.heading(col, text=title)
            self.tree.column(col, width=width, anchor="center")

        self.tree.pack(fill="both", padx=12)

        style = ttk.Style(self.root)
        style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))
        style.configure("Treeview", rowheight=28, font=("Helvetica", 11))

        self.tree.tag_configure("green", background="#e8f5e9")
        self.tree.tag_configure("yellow", background="#fffde7")
        self.tree.tag_configure("orange", background="#fff3e0")
        self.tree.tag_configure("red", background="#ffebee")

        footer = tk.Frame(self.root)
        footer.pack(fill="x", padx=12, pady=10)

        self.next_label = tk.Label(footer, text=f"下次自動更新：{REFRESH_INTERVAL} 秒後", font=("Helvetica", 10))
        self.next_label.pack(side="left")

        refresh_button = tk.Button(
            footer,
            text="立即更新",
            command=self.run_fetch,
            width=12,
            bg="#1976d2",
            fg="white",
            font=("Helvetica", 10, "bold"),
        )
        refresh_button.pack(side="right")

    def schedule_update(self, initial=False):
        if not self.running:
            return
        delay = 100 if initial else REFRESH_INTERVAL * 1000
        self.root.after(delay, self.run_fetch)

    def run_fetch(self):
        if not self.running:
            return
        self.attempt += 1
        self.status_label.config(text=f"第 {self.attempt} 次更新：抓取資料中...", fg="#0d47a1")
        self.error_label.config(text="")

        thread = threading.Thread(target=self.fetch_data_thread, daemon=True)
        thread.start()

    def fetch_data_thread(self):
        t0 = time.time()
        data = fetch_ubike_data()
        elapsed_ms = int((time.time() - t0) * 1000)
        now = datetime.now()
        stations = filter_nearby_stations(data) if data else []
        self.root.after(0, lambda: self.update_ui(stations, data, now, elapsed_ms))

    def update_ui(self, stations, data, now, elapsed_ms):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if data is None:
            self.summary_label.config(text="目前無法取得資料，請檢查網路連線。")
            self.status_label.config(
                text=f"{now.strftime('%Y-%m-%d %H:%M:%S')} | 第 {self.attempt} 次更新失敗 | {elapsed_ms} ms",
                fg="#b00020",
            )
            self.error_label.config(text="❌ 無法連線至 API，將於稍後自動重試。")
            self.next_label.config(text=f"下次自動更新：{REFRESH_INTERVAL} 秒後")
            self.schedule_update()
            return

        total_available = sum(s["available"] for s in stations)
        total_slots = sum(s["empty_slots"] for s in stations)
        total_bikes = sum(s["total"] for s in stations)
        active_count = sum(1 for s in stations if s["active"])

        summary = (
            f"搜尋範圍：海山站半徑 {int(SEARCH_RADIUS_KM * 1000)} 公尺  |  "
            f"共 {len(stations)} 站（{active_count} 站正常營運）  |  "
            f"可借 {total_available} 輛  空位 {total_slots} 格  總格 {total_bikes}"
        )
        self.summary_label.config(text=summary)
        self.status_label.config(
            text=f"{now.strftime('%Y-%m-%d %H:%M:%S')} | {elapsed_ms} ms | 第 {self.attempt} 次更新",
            fg="#1b5e20",
        )
        self.error_label.config(text="")

        for station in stations:
            status = bike_status_symbol(station["available"], station["total"])
            tag = self.status_tag(station["available"], station["total"])
            self.tree.insert(
                "",
                "end",
                values=(
                    station["name"],
                    f"{station['distance_m']} m",
                    station["available"],
                    station["empty_slots"],
                    station["total"],
                    status + (" (停用)" if not station["active"] else ""),
                ),
                tags=(tag,),
            )

        self.next_label.config(text=f"下次自動更新：{REFRESH_INTERVAL} 秒後")
        self.schedule_update()

    @staticmethod
    def status_tag(available, total):
        if total <= 0:
            return "red"
        ratio = available / total
        if ratio >= 0.5:
            return "green"
        if ratio >= 0.2:
            return "yellow"
        if available > 0:
            return "orange"
        return "red"

    def on_close(self):
        self.running = False
        self.root.destroy()


if __name__ == "__main__":
    YouBikeMonitorApp()
