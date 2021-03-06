import os
import sys
import random
import pygame




WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)

BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "background.png")), (500, 400))
BIRD_IMGS = [
                pygame.transform.scale(pygame.image.load(os.path.join("imgs", "bird1.png")), (50, 50)), 
                pygame.transform.scale(pygame.image.load(os.path.join("imgs", "bird2.png")), (50, 50)), 
                pygame.transform.scale(pygame.image.load(os.path.join("imgs", "bird3.png")), (50, 50))
            ]
WALL_UP_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "wall.png")), (40, 120))
WALL_DOWN_IMG = WALL_UP_IMG




pygame.font.init()
mainWindow = pygame.display.set_mode((500, 400))
pygame.display.set_caption('Flappy Bird')

upper_wall = pygame.Rect(400, 0, 40, 120)
lower_wall = pygame.Rect(400, 280, 40, 120)
bird = pygame.Rect(130, 150, 50, 50)

score_file = open("best_score.txt","r")
best_score = int(score_file.read())
score_file.close()
score = 0


clock = pygame.time.Clock()
v_wall = 5
v_bird = 0
a_bird = 1
bird_images_index = 0
bird_images_ratio = 5


my_font = pygame.font.SysFont("Jokerman Regular", 50)
gameover_text = my_font.render("Game Over", True, RED)
pause_text = my_font.render("Pause", True, RED)

my_font = pygame.font.SysFont("Jokerman Regular", 30)
play_again_text = my_font.render("Press 'SPACE' to play again or 'ESC' to exit", True, RED)

my_font = pygame.font.SysFont("Jokerman Regular", 35)
score_text = my_font.render("Your Score: " + str(score), True, RED)
best_score_text = my_font.render("Best Score: " + str(best_score), True, RED)
score_renderer = my_font.render("0", True, RED)




state = "starting"
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    mainWindow.blit(BG_IMG, (0,0))
    mainWindow.blit(WALL_UP_IMG, (upper_wall.x, upper_wall.y))
    mainWindow.blit(WALL_DOWN_IMG, (lower_wall.x, lower_wall.y))
    mainWindow.blit(BIRD_IMGS[bird_images_index // bird_images_ratio], (bird.x, bird.y))
    mainWindow.blit(score_renderer, (30, 30))


    if state == "starting":
        mainWindow.blit(best_score_text, (160, 100))

        keypressed = pygame.key.get_pressed()
        if keypressed[pygame.K_SPACE]:
            state = "playing"

    if state == "playing":
        bird_images_index += 1
        if bird_images_index >= (bird_images_ratio * len(BIRD_IMGS)):
            bird_images_index = 0

        upper_wall.x -= v_wall
        lower_wall.x -= v_wall

        v_bird += a_bird
        bird.y += v_bird

        keypressed = pygame.key.get_pressed()
        if keypressed[pygame.K_SPACE]:
            v_bird = -7
        if keypressed[pygame.K_p]:
            state = "pause"
        
        if upper_wall.x <= -40:
            upper_wall.x = 500
            lower_wall.x = 500

            upper_wall.h = random.randint(40, 200)
            WALL_UP_IMG = pygame.transform.scale(WALL_UP_IMG, (40, upper_wall.h))
            lower_wall.h = 240 - upper_wall.h
            lower_wall.y = 400 - lower_wall.h
            WALL_DOWN_IMG = pygame.transform.scale(WALL_DOWN_IMG, (40, lower_wall.h))

        if bird.colliderect(upper_wall) or bird.colliderect(lower_wall) or bird.y < -30 or bird.y > 400:
            state = "game over"

        if bird.x == lower_wall.x + lower_wall.w :
            score += 1
            score_renderer = my_font.render(str(score), True, (255, 0, 0))


    if state == "pause":
        mainWindow.blit(pause_text, (200, 150))

        keypressed = pygame.key.get_pressed()
        if keypressed[pygame.K_SPACE]:
            state = "playing"

        
    if state == "game over":

        if score > best_score:
            best_score = score
            best_score_file = open("best_score.txt", "w")
            best_score_file.write(str(best_score))
            best_score_file.close()
            
        
        mainWindow.blit(gameover_text, (160, 100))
        mainWindow.blit(play_again_text, (25, 300))

        score_text = my_font.render("Your Score: " + str(score), True, (255, 0, 0))
        mainWindow.blit(score_text, (180, 160))

        best_score_text = my_font.render("Best Score: " + str(best_score), True, (255, 0, 0))
        mainWindow.blit(best_score_text, (180, 200))

        keypressed = pygame.key.get_pressed()
        if keypressed[pygame.K_SPACE]:
            bird.x = 130
            bird.y = 150
            upper_wall.x = 400
            lower_wall.x = 400
            score = 0
            score_renderer = my_font.render(str(score), True, (255, 0, 0))
            state = "playing"
        if keypressed[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        

    clock.tick(30)
    pygame.display.update()