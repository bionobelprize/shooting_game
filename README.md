# Pixel-Style First-Person Shooter Game

一个使用Python和Pygame开发的像素风格第一人称射击游戏。
A pixel-style first-person shooter game developed with Python and Pygame.

## 功能特点 / Features

- 🎮 基于光线投射的3D渲染引擎 / Raycasting-based 3D rendering engine
- 🏃 流畅的第一人称移动和视角控制 / Smooth first-person movement and view control
- 🎯 射击系统与敌人目标 / Shooting system with enemy targets
- 🗺️ 2D小地图显示 / 2D minimap display
- 💚 生命值和弹药系统 / Health and ammo system
- 🎨 复古像素风格画面 / Retro pixel-style graphics

## 安装 / Installation

### 要求 / Requirements
- Python 3.7+
- Pygame 2.5.2
- NumPy 1.24.3

### 安装步骤 / Installation Steps

```bash
# 克隆仓库 / Clone repository
git clone https://github.com/bionobelprize/shooting_game.git
cd shooting_game

# 安装依赖 / Install dependencies
pip install -r requirements.txt
```

## 运行游戏 / Running the Game

```bash
python main.py
```

## 游戏控制 / Game Controls

### 菜单 / Menu
- **↑/↓** - 选择菜单项 / Select menu item
- **Enter** - 确认选择 / Confirm selection

### 游戏中 / In Game
- **W** - 前进 / Move forward
- **S** - 后退 / Move backward
- **A** - 左移 / Strafe left
- **D** - 右移 / Strafe right
- **←** - 左转 / Turn left
- **→** - 右转 / Turn right
- **Space** - 射击 / Shoot
- **ESC** - 返回菜单 / Return to menu

## 游戏目标 / Game Objective

消灭地图上的所有敌人（红色方块）即可获胜！
Eliminate all enemies (red squares) on the map to win!

## 游戏截图 / Screenshots

游戏包含以下元素：
The game includes:
- 3D第一人称视角 / 3D first-person perspective
- 准星瞄准系统 / Crosshair aiming system
- 左上角小地图 / Minimap in top-left corner
- 底部HUD显示生命值、弹药和敌人数量 / Bottom HUD showing health, ammo, and enemy count

## 技术实现 / Technical Implementation

- **渲染引擎**: 使用光线投射算法实现伪3D效果 / Raycasting algorithm for pseudo-3D rendering
- **碰撞检测**: 基于网格的碰撞检测系统 / Grid-based collision detection
- **游戏架构**: 模块化设计，易于扩展 / Modular design for easy extension

## 文件结构 / Project Structure

```
shooting_game/
├── main.py           # 游戏入口 / Game entry point
├── game.py           # 主游戏逻辑 / Main game logic
├── player.py         # 玩家类 / Player class
├── enemy.py          # 敌人类 / Enemy class
├── raycaster.py      # 光线投射引擎 / Raycasting engine
├── renderer.py       # 渲染工具 / Rendering utilities
├── config.py         # 游戏配置 / Game configuration
├── map_data.py       # 地图数据 / Map data
└── requirements.txt  # Python依赖 / Python dependencies
```

## 未来改进 / Future Improvements

- [ ] 添加更多武器类型 / Add more weapon types
- [ ] 实现敌人AI和移动 / Implement enemy AI and movement
- [ ] 添加音效和背景音乐 / Add sound effects and background music
- [ ] 创建更多关卡 / Create more levels
- [ ] 添加更多类型的敌人 / Add more enemy types
- [ ] 实现道具系统 / Implement item system

## 许可证 / License

MIT License