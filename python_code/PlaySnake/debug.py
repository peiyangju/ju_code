import pygame
from pygame import Rect
from typing import Optional, Tuple


class Stream:
    """表示数据流的类"""

    def __init__(self, data: bytes):
        self.data = data
        self.position = 0

    def read(self, size: int) -> bytes:
        """从流中读取指定大小的数据"""
        if self.position >= len(self.data):
            return b''

        result = self.data[self.position:self.position + size]
        self.position += size
        return result

    def seek(self, position: int):
        """移动流的位置指针"""
        self.position = position


class Screen:
    """表示屏幕的类"""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.rect: Optional[Rect] = None
        self.surface = pygame.Surface((width, height))

    def set_rect(self, rect: Rect):
        """设置屏幕的矩形区域"""
        self.rect = rect

    def draw(self, surface: pygame.Surface, position: Tuple[int, int]):
        """将屏幕内容绘制到指定表面"""
        if self.rect:
            surface.blit(self.surface, position, self.rect)
        else:
            surface.blit(self.surface, position)


# 示例使用
if __name__ == "__main__":
    # 初始化Pygame
    pygame.init()

    # 创建主窗口
    main_surface = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Uniform Color Example")

    # 创建自定义屏幕 - 使用变量名 screen 替代 my_screen
    screen = Screen(400, 300)
    # 整个屏幕区域填充为纯蓝色
    screen.surface.fill((0, 0, 255))  # 纯蓝色填充

    # 设置矩形区域（可选）
    screen_rect = Rect(100, 50, 200, 200)
    screen.set_rect(screen_rect)

    # 主循环
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 清空主窗口为黑色背景
        main_surface.fill((0, 0, 0))

        # 绘制纯蓝色自定义屏幕到主窗口 - 使用变量名 screen
        screen.draw(main_surface, (200, 150))

        # 更新显示
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()