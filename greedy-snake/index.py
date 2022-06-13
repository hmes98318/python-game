import pygame
import sys
import random
from pygame.locals import *




WIDTH = 640  # 遊戲畫面的寬度
HEIGHT = 480  # 遊戲畫面的高度

RED = pygame.Color(255, 0, 0)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
GREY = pygame.Color(150, 150, 150)




def draw_text(font_name, display, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    display.blit(text_surface, text_rect)


def run(playSurface, fpsClock, STAT_FONT):
    snakePosition = [100, 100]
    snakeSegments = [[100, 100], [80, 100], [60, 100]]
    raspberryPosition = [300, 300]
    raspberrySpawned = 1
    direction = 'right'
    changeDirection = direction
    score = 0
    alive = 3

    playing = True
    while playing:
        # 檢測例如按鍵等pygame事件
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
               # 判斷鍵盤事件
                if event.key == K_RIGHT or event.key == ord('d'):
                    changeDirection = 'right'
                if event.key == K_LEFT or event.key == ord('a'):
                    changeDirection = 'left'
                if event.key == K_UP or event.key == ord('w'):
                    changeDirection = 'up'
                if event.key == K_DOWN or event.key == ord('s'):
                    changeDirection = 'down'
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))

        # 判斷是否輸入了反方向
        if changeDirection == 'right' and not direction == 'left':
            direction = changeDirection
        if changeDirection == 'left' and not direction == 'right':
            direction = changeDirection
        if changeDirection == 'up' and not direction == 'down':
            direction = changeDirection
        if changeDirection == 'down' and not direction == 'up':
            direction = changeDirection
        # 根據方向移動蛇頭的坐標
        if direction == 'right':
            snakePosition[0] += 20
        if direction == 'left':
            snakePosition[0] -= 20
        if direction == 'up':
            snakePosition[1] -= 20
        if direction == 'down':
            snakePosition[1] += 20

        # 增加蛇的長度
        snakeSegments.insert(0, list(snakePosition))
        # 判斷是否吃掉了樹莓
        if snakePosition[0] == raspberryPosition[0] and snakePosition[1] == raspberryPosition[1]:
            raspberrySpawned = 0
            score += 1
        else:
            snakeSegments.pop()
        # 如果吃掉樹莓，則重新生成樹莓
        if raspberrySpawned == 0:
            x = random.randrange(1, 32)
            y = random.randrange(1, 24)
            raspberryPosition = [int(x*20), int(y*20)]
            raspberrySpawned = 1
        # 繪製pygame顯示層
        playSurface.fill(BLACK)
        for position in snakeSegments:
            pygame.draw.rect(playSurface, WHITE, Rect(
                position[0], position[1], 20, 20))
            pygame.draw.rect(playSurface, RED, Rect(
                raspberryPosition[0], raspberryPosition[1], 20, 20))

        # 判斷是否死亡
        if snakePosition[0] > 620 or snakePosition[0] < 0 or snakePosition[1] > 460 or snakePosition[1] < 0:
            alive -= 1

            snakePosition = [100, 100]
            snakeSegments = [[100, 100], [80, 100], [60, 100]]
            raspberryPosition = [300, 300]
            raspberrySpawned = 1
            direction = 'right'
            changeDirection = direction
            score = 0


        score_label = STAT_FONT.render("Score: " + str(score), 1, WHITE)
        playSurface.blit(score_label, (5,5))

        alive_label = STAT_FONT.render("Alive: " + str(alive), 1, WHITE)
        playSurface.blit(alive_label, (WIDTH-100, 5))

        # 刷新pygame顯示層
        pygame.display.update()


        if alive < 1:
            playing = False
            gameOver(playSurface, fpsClock, STAT_FONT)

        # 控制游戲速度
        fpsClock.tick(8)


def gameOver(playSurface, fpsClock, STAT_FONT):
    fpsClock = pygame.time.Clock()  # 決定遊戲速度
    font_gameOver = pygame.font.match_font('comic.ttf')

    draw_text(font_gameOver, playSurface, "Game Over",90, WIDTH / 2, HEIGHT / 4)
    draw_text(font_gameOver, playSurface, "Press any key to restart!",64, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.update()

    # 按任意鍵重新開始
    waiting = True
    while waiting:
        fpsClock.tick(8)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False
                run(playSurface, fpsClock, STAT_FONT)




def main():

    pygame.init()  # pygame初始化
    pygame.display.set_caption('Greedy Snake Game')
    fpsClock = pygame.time.Clock()  # 決定遊戲速度
    playSurface = pygame.display.set_mode((WIDTH, HEIGHT))  # 決定遊戲畫面大小
    STAT_FONT = pygame.font.SysFont("comicsans", 20)


    # 開始畫面的文字
    font_name = pygame.font.match_font('comic.ttf')
    draw_text(font_name, playSurface, "Greedy Snake",90, WIDTH / 2, HEIGHT / 4)
    draw_text(font_name, playSurface, "Press any key to start!",64, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.update()



    # 按任意鍵遊戲開始
    waiting = True
    while waiting:
        fpsClock.tick(8)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False


    run(playSurface, fpsClock, STAT_FONT)




if __name__ == "__main__":
    main()
