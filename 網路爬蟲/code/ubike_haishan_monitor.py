#!/usr/bin/env python3
"""
YouBike 2.0 海山捷運站周邊即時監控程式
每 10 秒自動抓取一次新北市 YouBike 開放資料 API，
顯示海山站附近各站點的腳踏車可借數量。

資料來源：新北市政府 YouBike 2.0 開放資料 API
"""

import requests
import time
import math
import os
from datetime import datetime

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


def clear_screen():
    """清除終端畫面"""
    os.system("cls" if os.name == "nt" else "clear")


def haversine(lat1, lon1, lat2, lon2):
    """
    計算兩個 GPS 座標間的距離（公里）
    使用 Haversine 公式
    """
    R = 6371  # 地球半徑（公里）
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
    """
    從新北市開放資料 API 抓取 YouBike 即時資料
    回傳原始 JSON 列表，失敗回傳 None
    """
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
    except requests.RequestException as e:
        # 嘗試備用 API
        try:
            resp = requests.get(API_URL_BACKUP, headers=headers, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException:
            return None


def parse_station(raw):
    """
    統一解析站點資料（相容多種 API 格式）
    回傳標準化 dict 或 None（無法解析時）
    """
    try:
        # 嘗試取得座標（不同 API 欄位名稱不同）
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
    """篩選出距離海山站指定半徑內的站點，並依距離排序"""
    nearby = []
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


def bike_bar(available, total, width=20):
    """產生 ASCII 進度條顯示可借車輛比例"""
    if total <= 0:
        ratio = 0
    else:
        ratio = available / total
    filled = int(ratio * width)
    bar = "█" * filled + "░" * (width - filled)

    if ratio >= 0.5:
        status = "🟢"
    elif ratio >= 0.2:
        status = "🟡"
    elif available > 0:
        status = "🟠"
    else:
        status = "🔴"

    return f"{status} [{bar}]"


def display(stations, fetch_time, elapsed_ms, attempt):
    """清屏並輸出完整的監控畫面"""
    clear_screen()

    # ── 標題區 ────────────────────────────────────────────────
    print("=" * 70)
    print("  🚲  YouBike 2.0 即時監控  ──  捷運海山站周邊")
    print("=" * 70)
    print(f"  📍 搜尋範圍：海山站半徑 {SEARCH_RADIUS_KM * 1000:.0f} 公尺")
    print(f"  🕒 更新時間：{fetch_time.strftime('%Y-%m-%d  %H:%M:%S')}")
    print(f"  ⚡ 回應速度：{elapsed_ms} ms   |   第 {attempt} 次更新")
    print(f"  🔄 下次更新：{REFRESH_INTERVAL} 秒後")
    print("-" * 70)

    if not stations:
        print("\n  ⚠️  目前範圍內找不到站點，請確認網路連線或放大搜尋半徑。\n")
        print("=" * 70)
        return

    # ── 統計摘要 ──────────────────────────────────────────────
    total_available = sum(s["available"] for s in stations)
    total_slots = sum(s["empty_slots"] for s in stations)
    total_bikes = sum(s["total"] for s in stations)
    active_count = sum(1 for s in stations if s["active"])

    print(
        f"  📊 共 {len(stations)} 站（{active_count} 站正常營運）"
        f"  |  可借：{total_available} 輛  |  空位：{total_slots} 格  |  總車格：{total_bikes}"
    )
    print("=" * 70)

    # ── 表頭 ──────────────────────────────────────────────────
    print(
        f"  {'站名':<22} {'距離':>5}  {'可借':>4}  {'空位':>4}  {'總格':>4}  {'狀態'}"
    )
    print("  " + "-" * 66)

    # ── 各站點資料列 ──────────────────────────────────────────
    for s in stations:
        active_tag = "" if s["active"] else " ⛔停用"
        bar = bike_bar(s["available"], s["total"])
        name = s["name"]
        if len(name) > 20:
            name = name[:19] + "…"

        print(
            f"  {name:<22} {s['distance_m']:>4}m"
            f"  {s['available']:>4}  {s['empty_slots']:>4}  {s['total']:>4}"
            f"  {bar}{active_tag}"
        )

    print("=" * 70)
    print("  💡 圖示說明：🟢 充足（≥50%）  🟡 尚有（20-49%）  🟠 偏少（1-19%）  🔴 無車")
    print("  ⌨️  按 Ctrl+C 結束程式")
    print("=" * 70)


def main():
    """主迴圈：每 10 秒抓取一次並顯示"""
    attempt = 0
    print("🚲 YouBike 海山站監控程式啟動中，請稍候…")
    time.sleep(1)

    while True:
        attempt += 1
        t0 = time.time()
        data = fetch_ubike_data()
        elapsed_ms = int((time.time() - t0) * 1000)
        now = datetime.now()

        if data is None:
            clear_screen()
            print("=" * 70)
            print("  ❌ 無法取得資料，請確認網路連線，將在 10 秒後重試…")
            print(f"  🕒 {now.strftime('%Y-%m-%d %H:%M:%S')}  |  第 {attempt} 次嘗試")
            print("=" * 70)
        else:
            stations = filter_nearby_stations(data)
            display(stations, now, elapsed_ms, attempt)

        time.sleep(REFRESH_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  👋 程式已結束，感謝使用！\n")