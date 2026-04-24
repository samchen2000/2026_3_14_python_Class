## 關於 Godot Engine
- Godot Engine 是一款功能齊全、跨平台的遊戲引擎，能以統一介面製作 2D 與 3D 遊戲。它提供完整的常用工具組，讓使用者能專注在做遊戲，而不必重造輪子。遊戲可一鍵匯出至多種平台，包含主流桌面平台（Linux、macOS、Windows）、行動平台（Android、iOS），以及網頁平台與遊戲主機。

- Godot 完全自由且開源，採用 寬鬆的 MIT 授權。沒有附帶條款、沒有權利金，沒有任何額外要求。即便到引擎的最後一行程式碼為止，使用者的遊戲都完全屬於使用者。Godot 的開發完全獨立且由社群驅動，讓使用者能一起塑造引擎，使其符合預期。它由非營利組織 Godot Foundation 支持。

## 安裝設定
1.  下載 Godot 4  
前往官方網站下載 Godot 4（免安裝，解壓縮即可使用）。
2. 選擇版本  
選擇「Standard」版本（含 .NET/C# 需另下載 .NET SDK）。建議新手選 Standard。
3. 解壓並執行  
解壓縮後，直接雙擊執行檔即可啟動。無需安裝程序。  
4. 建立第一個專案  
在專案管理員點擊「新建專案」，選擇資料夾與渲染器（建議 Forward+）。  

## 核心概念
#### 🌳Scene（場景）
- Godot 的一切都是場景。場景可以是玩家、敵人、關卡、UI——任何東西。場景可以嵌套在其他場景中，形成樹狀結構。.tscn 為場景檔格式。
#### 🔵Node（節點）
- 場景由 Node 組成。每個 Node 有特定功能（如 Sprite2D 顯示圖片、CollisionShape2D 處理碰撞）。Node 形成父子層級，子節點跟隨父節點移動/縮放。 
#### 📡Signal（訊號）
- Signal 是 Godot 的事件系統（類似其他引擎的事件/回調）。節點發出訊號，其他節點監聽並做出反應。例如 button.pressed 訊號在按鈕被點擊時發出。

#### 常用節點類型
- Node2D :  2D 場景的基礎節點，有位置/旋轉/縮放屬性。
- CharacterBody2D : 用於玩家/NPC 角色控制，內建 move_and_slide()。
- Area2D : 偵測重疊/進入區域，適合傷害判定、道具拾取。
- Camera2D : 2D 攝影機，可跟隨玩家、設定邊界。

## GDScript 範例
**GDScript 基礎語法**
```
extends CharacterBody2D

# 常數與變數
const SPEED = 200.0
const JUMP_VELOCITY = -400.0
var health = 100

# _ready() 在節點載入場景時執行一次
func _ready():
    print("玩家已準備好！")

# _process(delta) 每幀呼叫，delta = 幀時間
func _process(delta):
    if Input.is_action_pressed("ui_accept"):
        print("按下確認鍵")
```
### 玩家移動範例（2D 平台遊戲）
```
extends CharacterBody2D

const SPEED = 200.0
const JUMP_VELOCITY = -400.0

func _physics_process(delta):
    # 加入重力
    if not is_on_floor():
        velocity += get_gravity() * delta

    # 跳躍
    if Input.is_action_just_pressed("ui_accept") and is_on_floor():
        velocity.y = JUMP_VELOCITY

    # 左右移動
    var direction = Input.get_axis("ui_left", "ui_right")
    if direction:
        velocity.x = direction * SPEED
    else:
        velocity.x = move_toward(velocity.x, 0, SPEED)

    move_and_slide()
```
### Signal 使用範例
```
extends Node

# 定義自訂訊號
signal player_died(player_name)

func _ready():
    # 連接內建訊號（按鈕點擊）
    $Button.pressed.connect(_on_button_pressed)

func _on_button_pressed():
    print("按鈕被按下！")
    # 發出自訂訊號
    player_died.emit("Player1")
```
### 場景切換 / 節點取得
```
# 取得子節點
var sprite = $Sprite2D
var player = get_node("Player")

# 切換場景
func go_to_next_level():
    get_tree().change_scene_to_file("res://levels/level2.tscn")

# 實例化場景（動態生成敵人）
var enemy_scene = preload("res://enemy.tscn")
func spawn_enemy(pos: Vector2):
    var enemy = enemy_scene.instantiate()
    enemy.position = pos
    add_child(enemy)
```
*GDScript 語法類似 Python，使用縮排分隔區塊。型別是動態的，但可加型別標註（如 var speed: float = 200.0）提升效能與可讀性。*
## 第一個專案
製作你的第一個 2D 遊戲：步驟流程  
### 1. 建立專案與場景  
新建專案 → 建立主場景（Node2D）→ 儲存為 main.tscn  
### 2. 建立玩家場景  
新建場景 → 根節點選 CharacterBody2D → 加入 Sprite2D（圖片）、CollisionShape2D（碰撞）  
### 3. 加入 GDScript 腳本  
選取根節點 → 點擊「新增腳本」→ 撰寫移動邏輯（參考左側 GDScript 範例頁）  
### 4. 設定輸入映射  
專案 → 專案設定 → 輸入映射，定義 "move_left"、"move_right"、"jump" 等動作鍵  
### 5. 加入地形（TileMap）   
主場景加入 TileMapLayer 節點 → 載入 Tileset → 繪製地板與障礙物  
### 6. 加入 UI 與音效  
CanvasLayer → Label（分數顯示）、ProgressBar（血條）；AudioStreamPlayer 播放音效  
### 7. 匯出遊戲  
專案 → 匯出 → 選擇平台（Windows/Web/Android）→ 下載對應匯出範本 → 匯出
## 學習資源
### 官方文件（正體中文）
- 📘Godot 4 官方文件 — 正體中文（台灣）  
docs.godotengine.org/zh-tw/4.x  
- 🪜Step by Step — 入門逐步教學   
官方推薦新手第一課  
- 📝GDScript 基礎語法參考  
官方 GDScript 完整說明文件  
### 社群教學（中文）  
- 🎮巴哈姆特 Godot 教學系列（繁中）   
從安裝到製作第一個 2D 射擊遊戲  
- 🏘️Godot 新手村（簡中)  
多人連線、AI、狀態機深度教學  
### 推薦 YouTube 頻道  
- ▶️GDQuest（英文，高品質）  
社群最推薦的 Godot 入門影片教學  
- ▶️Brackeys（英文）  
製作 Godot 新手第一款遊戲系列  
### 資產庫
- 🗂️Godot Asset Library — 官方資源庫
免費插件、範例專案、素材