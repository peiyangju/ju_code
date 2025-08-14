from pgzero.builtins import screen, Rect, keys
# 添加在最开头
import sys
import os
os.environ['PGZERO_MODE'] = 'auto'  # 防止图标加载问题

try:
    import pgzrun
    from pgzero.builtins import *
except ImportError as e:
    print(f"Required module missing: {e}")
    print("Please install with: pip install pgzero pygame")
    sys.exit(1)

# 原有代码保持不变...
from random import randint
from collections import deque
import time
from pygame import Rect


# 游戏设置
WIDTH = 800
HEIGHT = 600
TITLE = "Snake Game"
BG_COLOR = (0, 0, 0)  # 黑色背景

# 游戏状态
game_state = {
    "snake": deque(),
    "food": None,
    "direction": "right",
    "next_direction": "right",
    "score": 0,
    "game_speed": 10,  # 默认速度
    "game_over": False,
    "game_started": False,
    "buttons": [],
    "last_update": 0
}


# 蛇身方块类
class SnakeSegment:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20

    def draw(self):
        screen.draw.filled_rect(
            Rect((self.x, self.y), (self.size, self.size)),
            (0, 255, 0)  # 绿色蛇身
        )


# 食物类
class Food:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = 20
        self.respawn()

    def respawn(self):
        # 确保食物生成在网格上
        self.x = randint(0, (WIDTH - self.size) // self.size) * self.size
        self.y = randint(0, (HEIGHT - self.size) // self.size) * self.size

    def draw(self):
        screen.draw.filled_rect(
            Rect((self.x, self.y), (self.size, self.size)),
            (255, 0, 0)  # 红色食物
        )


# 按钮类
class Button:
    def __init__(self, x, y, width, height, text, color, text_color, action=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.text_color = text_color
        self.action = action
        self.rect = Rect((x, y), (width, height))

    def draw(self):
        screen.draw.filled_rect(self.rect, self.color)
        screen.draw.text(
            self.text,
            center=(self.x + self.width / 2, self.y + self.height / 2),
            color=self.text_color,
            fontsize=20
        )

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# 初始化游戏
def init_game():
    # 创建初始蛇身 (3个方块)
    head = SnakeSegment(WIDTH // 2, HEIGHT // 2)
    game_state["snake"] = deque([head])
    for i in range(1, 3):
        game_state["snake"].append(SnakeSegment(head.x - i * head.size, head.y))

    # 创建食物
    game_state["food"] = Food()

    # 重置游戏状态
    game_state["direction"] = "right"
    game_state["next_direction"] = "right"
    game_state["score"] = 0
    game_state["game_over"] = False
    game_state["game_started"] = True
    game_state["last_update"] = time.time()
    game_state["buttons"] = []


# 绘制开始菜单
def draw_start_menu():
    screen.fill(BG_COLOR)

    # 标题
    screen.draw.text(
        "Snake Game",
        center=(WIDTH // 2, 100),
        color=(255, 255, 255),
        fontsize=48
    )

    # 速度选择和微调按钮
    speed_x = WIDTH // 2 - 50
    speed_y = 200

    # 速度显示
    screen.draw.text(
        f"Speed: {game_state['game_speed']}",
        center=(speed_x, speed_y),
        color=(255, 255, 255),
        fontsize=24
    )

    # 微调按钮
    game_state["buttons"].append(
        Button(speed_x - 80, speed_y - 15, 40, 40, "-", (200, 200, 200), (0, 0, 0), decrease_speed)
    )
    game_state["buttons"].append(
        Button(speed_x + 80, speed_y - 15, 40, 40, "+", (200, 200, 200), (0, 0, 0), increase_speed)
    )

    # 主按钮
    game_state["buttons"].append(
        Button(WIDTH // 2 - 100, 350, 200, 60, "Start Game", (100, 255, 100), (255, 255, 255), init_game)
    )
    game_state["buttons"].append(
        Button(WIDTH // 2 - 100, 450, 200, 60, "Quit", (255, 0, 0), (255, 255, 255), quit_game)
    )


# 退出游戏
def quit_game():
    sys.exit()


# 调整速度
def decrease_speed():
    if game_state["game_speed"] > 1:
        game_state["game_speed"] -= 1


def increase_speed():
    if game_state["game_speed"] < 20:
        game_state["game_speed"] += 1


# 更新游戏状态
def update():
    if not game_state["game_started"] or game_state["game_over"]:
        return

    current_time = time.time()
    # 根据游戏速度控制更新频率
    if current_time - game_state["last_update"] < 1.0 / game_state["game_speed"]:
        return

    game_state["last_update"] = current_time

    # 更新方向
    game_state["direction"] = game_state["next_direction"]

    # 移动蛇
    head = game_state["snake"][0]
    new_head = SnakeSegment(head.x, head.y)

    if game_state["direction"] == "up":
        new_head.y -= new_head.size
    elif game_state["direction"] == "down":
        new_head.y += new_head.size
    elif game_state["direction"] == "left":
        new_head.x -= new_head.size
    elif game_state["direction"] == "right":
        new_head.x += new_head.size

    # 屏幕边缘传送
    if new_head.x < 0:
        new_head.x = WIDTH - new_head.size
    elif new_head.x >= WIDTH:
        new_head.x = 0
    elif new_head.y < 0:
        new_head.y = HEIGHT - new_head.size
    elif new_head.y >= HEIGHT:
        new_head.y = 0

    # 检查是否吃到自己
    for segment in game_state["snake"]:
        if new_head.x == segment.x and new_head.y == segment.y:
            game_state["game_over"] = True
            return

    # 添加新头部
    game_state["snake"].appendleft(new_head)

    # 检查是否吃到食物
    if (new_head.x == game_state["food"].x and
            new_head.y == game_state["food"].y):
        game_state["score"] += 1
        game_state["food"].respawn()
    else:
        # 没吃到食物则移除尾部
        game_state["snake"].pop()


# 绘制游戏
def draw():
    screen.fill(BG_COLOR)

    if not game_state["game_started"]:
        draw_start_menu()
    elif game_state["game_over"]:
        draw_game_over()
    else:
        # 绘制蛇
        for segment in game_state["snake"]:
            segment.draw()

        # 绘制食物
        game_state["food"].draw()

        # 绘制分数和速度
        screen.draw.text(
            f"Score: {game_state['score']}",
            topleft=(10, 10),
            color=(255, 255, 255),
            fontsize=24
        )
        screen.draw.text(
            f"Speed: {game_state['game_speed']}",
            topright=(WIDTH - 10, 10),
            color=(255, 255, 255),
            fontsize=24
        )

    # 绘制按钮
    for button in game_state["buttons"]:
        button.draw()


# 绘制游戏结束画面
def draw_game_over():
    screen.draw.text(
        "Game Over!",
        center=(WIDTH // 2, HEIGHT // 2 - 50),
        color=(255, 255, 255),
        fontsize=48
    )

    screen.draw.text(
        f"Final Score: {game_state['score']}",
        center=(WIDTH // 2, HEIGHT // 2 + 20),
        color=(255, 255, 255),
        fontsize=32
    )

    game_state["buttons"].append(
        Button(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 60, "Restart", (100, 255, 100), (255, 255, 255), init_game)
    )
    game_state["buttons"].append(
        Button(WIDTH // 2 - 100, HEIGHT // 2 + 180, 200, 60, "Quit", (255, 0, 0), (255, 255, 255), quit_game)
    )


# 键盘控制
def on_key_down(key):
    if game_state["game_over"]:
        if key == keys.R:  # 按R重新开始
            init_game()
        return

    if not game_state["game_started"]:
        return

    if key == keys.W and game_state["direction"] != "down":
        game_state["next_direction"] = "up"
    elif key == keys.S and game_state["direction"] != "up":
        game_state["next_direction"] = "down"
    elif key == keys.A and game_state["direction"] != "right":
        game_state["next_direction"] = "left"
    elif key == keys.D and game_state["direction"] != "left":
        game_state["next_direction"] = "right"
    elif key == keys.ESCAPE:  # ESC退出游戏
        quit_game()
    elif key == keys.PLUS or key == keys.EQUALS:  # +键加速
        increase_speed()
    elif key == keys.MINUS:  # -键减速
        decrease_speed()


# 鼠标点击事件
def on_mouse_down(pos):
    for button in game_state["buttons"]:
        if button.is_clicked(pos) and button.action:
            button.action()


# 运行游戏
pgzrun.go()