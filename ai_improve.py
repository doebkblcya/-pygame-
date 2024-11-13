import pygame
import sys
import numpy as np
from pygame.locals import QUIT, KEYDOWN

# 初始化 pygame
pygame.init()

# 配置常量
BOARD_SIZE = 15
CELL_SIZE = 44
MARGIN = 27
SCREEN_SIZE = (670, 670)
LINE_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (0, 229, 238)
WIN_COLOR = (238, 48, 167)

# 创建游戏窗口
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("五子棋")

# 游戏状态变量
over_pos = []  # 已经落子的棋盘位置
tim = 0  # 按键延时
flag = False  # 延时控制标志
font = pygame.font.Font(None, 36)

# 棋盘二维数组
mp = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)


def draw_board():
    """绘制棋盘"""
    screen.fill([238, 154, 73])
    for i in range(MARGIN, SCREEN_SIZE[0] - MARGIN, CELL_SIZE):
        pygame.draw.line(screen, LINE_COLOR, [i, MARGIN], [i, SCREEN_SIZE[1] - MARGIN], 2)
        pygame.draw.line(screen, LINE_COLOR, [MARGIN, i], [SCREEN_SIZE[0] - MARGIN, i], 2)
    pygame.draw.circle(screen, LINE_COLOR, [MARGIN + CELL_SIZE * 7, MARGIN + CELL_SIZE * 7], 8)


def draw_pieces():
    """绘制棋盘上的棋子"""
    for pos, color in over_pos:
        pygame.draw.circle(screen, color, pos, 20)


def find_pos(x, y):
    """找到最近的格子位置"""
    for i in range(MARGIN, SCREEN_SIZE[0] - MARGIN, CELL_SIZE):
        for j in range(MARGIN, SCREEN_SIZE[1] - MARGIN, CELL_SIZE):
            if i - 22 <= x <= i + 22 and j - 22 <= y <= j + 22:
                return i, j
    return x, y


def check_win():
    """判断是否有五子连心"""
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if mp[i][j] != 0:
                # 横向、纵向、对角线判断
                for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                    count = 1
                    positions = [(i, j)]
                    for step in range(1, 5):
                        ni, nj = i + step * dx, j + step * dy
                        if 0 <= ni < BOARD_SIZE and 0 <= nj < BOARD_SIZE and mp[ni][nj] == mp[i][j]:
                            count += 1
                            positions.append((ni, nj))
                        else:
                            break
                    if count >= 5:
                        return mp[i][j], positions
    return 0, []


def handle_click():
    """处理点击事件，更新棋盘"""
    global tim, flag
    x, y = pygame.mouse.get_pos()
    x, y = find_pos(x, y)

    if is_valid_move(x, y) and tim == 0:
        color = WHITE if len(over_pos) % 2 else BLACK
        over_pos.append([(x, y), color])
        mp[(x - MARGIN) // CELL_SIZE][(y - MARGIN) // CELL_SIZE] = 2 if color == WHITE else 1
        flag = True


def is_valid_move(x, y):
    """检查当前位置是否可以落子"""
    for pos, _ in over_pos:
        if pos == (x, y):
            return False
    return True


def draw_highlight():
    """显示当前可落子的位置"""
    x, y = pygame.mouse.get_pos()
    x, y = find_pos(x, y)
    if is_valid_move(x, y):
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, [x - 22, y - 22, CELL_SIZE, CELL_SIZE], 2, 1)


def display_winner(winner):
    """显示游戏结束的赢家"""
    color = "黑棋" if winner == 1 else "白棋"
    text = font.render(f"胜利者：{color}", True, WIN_COLOR)
    screen.blit(text, (MARGIN, SCREEN_SIZE[1] - MARGIN - 50))


def main():
    global tim, flag
    while True:
        draw_board()
        draw_pieces()
        draw_highlight()

        # 检查是否有玩家获胜
        winner, positions = check_win()
        if winner:
            for pos in positions:
                pygame.draw.rect(screen, WIN_COLOR, [pos[0] * CELL_SIZE + MARGIN - 22, pos[1] * CELL_SIZE + MARGIN - 22, CELL_SIZE, CELL_SIZE], 2, 1)
            display_winner(winner)
            pygame.display.update()
            continue  # 游戏结束

        # 获取事件并响应
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_click()

        # 延时控制
        if flag:
            tim += 1
        if tim % 50 == 0:
            flag = False
            tim = 0

        pygame.display.update()


if __name__ == "__main__":
    main()
