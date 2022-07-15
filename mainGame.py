# from termios import TAB0
import pygame
import random
import time

pygame.init()
running  = True
size = width, height = (900,800) # H and W of the screen
road_w = int(width/1.6) # Width of the road
roadMark_w = int(width/80)

screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption("Soumya's Car Game")
screen.fill((60, 200, 10)) # Color of the background

pygame.draw.rect(screen, (50, 50, 50), (width/2 - road_w/2, 0, road_w, height)) # Road
pygame.draw.rect(screen, (255, 255, 255), (width/2 - roadMark_w/2, 0, roadMark_w, height)) # Road Mark
pygame.draw.rect(screen, (0, 100, 0), (width/2 - road_w/2, 0, roadMark_w*2, height)) # Road - side (left)
pygame.draw.rect(screen, (0, 100, 0), (width/2 + road_w/2, 0, roadMark_w*2, height)) # Road - side (right)

pygame.display.update()

# Loading car images ->
enemy = pygame.image.load("assets/obstacle.png")
me = pygame.image.load("assets/myCar.png")
explosion = pygame.image.load("assets/blast.png")
pygame.mixer.music.load("assets/game_bgm.mp3")
pygame.mixer.music.play()
dead = True

# Checking for BGM ending ->
MUSIC_ENDING = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_ENDING)

# Fetching the loaction of the car images ->
enemy_loc = enemy.get_rect()
my_loc = me.get_rect()
enemy_loc.center = (width/2 + road_w/4, height*0.2)
my_loc.center = (width/2 - road_w/4, height*0.8)

# Restart button ->
smallfont = pygame.font.SysFont('Corbel',35)
resBtnText = smallfont.render("Restart", True, (255, 255, 255))
# mouse = pygame.mouse.get_pos()

def gameOver(score) :
    pygame.mixer.music.stop()
    pygame.mixer.music.load("assets/car_crash.mp3")
    pygame.mixer.music.play()
    global dead

    while dead:
        global width, height, road_w, roadMark_w
        width = screen.get_width()
        height = screen.get_height()
        road_w = int(width/1.6)
        roadMark_w = int(width/80)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
            # Restart button ->
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if resBtn_rect.collidepoint(mouse):
                    restart()
                    dead = False

        screen.fill((60, 200, 10)) # Color of the background

        pygame.draw.rect(screen, (50, 50, 50), (width/2 - road_w/2, 0, road_w, height)) # Road
        pygame.draw.rect(screen, (255, 255, 255), (width/2 - roadMark_w/2, 0, roadMark_w, height)) # Road Mark
        pygame.draw.rect(screen, (0, 100, 0), (width/2 - road_w/2, 0, roadMark_w*2, height)) # Road - side (left)
        pygame.draw.rect(screen, (0, 100, 0), (width/2 + road_w/2, 0, roadMark_w*2, height)) # Road - side (right)

        resBtn_rect = resBtnText.get_rect()
        pygame.draw.rect(screen, (255, 100, 100), (width - 70 - 1.2*resBtn_rect.width/2, 30 - 1.2*resBtn_rect.height/2, resBtn_rect.width*1.2, resBtn_rect.height*1.2))
        resBtn_rect.center = (width - 70, 30)

        font = pygame.font.SysFont("comicsansms", 100)
        text = font.render("Game Over !!!", True, (255, 10, 0))
        text_rect = text.get_rect()
        text_rect.center = (width/2, height/3)

        font1 = pygame.font.SysFont("comicsansms", 30)
        text1 = font1.render(f"Score : {score}", True, (25, 25, 25))
        text1_rect = text1.get_rect()
        text1_rect.center = (80, 25)
        screen.blit(text1, text1_rect)
        screen.blit(resBtnText, resBtn_rect)

        screen.blit(enemy, enemy_loc)
        screen.blit(me, my_loc)
        screen.blit(explosion, blast_loc)
        screen.blit(text, text_rect)
        pygame.display.update()

# RESTART ->
def restart() :
    print('restart')
    pygame.mixer.music.stop()
    pygame.mixer.music.load("assets/game_bgm.mp3")
    pygame.mixer.music.play()
    global running, score, my_loc, enemy_loc, speed, t0
    running = True
    score = 0
    my_loc.center = (width/2 - road_w/4, height*0.8)
    speed = 1
    enemy_loc[1] = -169
    t0 = time.time()

# EvenListenter for game collapse
speed = 1
t0 = time.time()
score = 0

while running :
    # print('running')
    enemy_loc[1] += speed

    my_loc[0] = (my_loc[0] / width) * screen.get_width()
    width = screen.get_width()
    height = screen.get_height()
    road_w = int(width/1.6)
    roadMark_w = int(width/80)
    # my_loc[0] = my_loc[0] * width

    if enemy_loc[1] > height :
        val = random.choice(['left', 'right'])
        enemy_loc[1] = -169
        if val == 'left' :
            enemy_loc[0] = width/2 - road_w/4 + random.randint(int(-1*road_w/8), int(road_w/8))
        else :
            enemy_loc[0] = width/2 + road_w/4 - random.randint(int(-1*road_w/8), int(road_w/8))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == MUSIC_ENDING:
            pygame.mixer.music.load("assets/game_bgm.mp3")
            pygame.mixer.music.play()

        # Logic for the car movement ->

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_a, pygame.K_LEFT] and my_loc.left > (width/2 - road_w/2.5):
                my_loc = my_loc.move([-road_w/8, 0])
            if event.key in [pygame.K_RIGHT, pygame.K_d] and my_loc.right < (width/2 + road_w/2.5):
                my_loc = my_loc.move([road_w/8, 0])
            if event.key in [pygame.K_UP, pygame.K_w] and my_loc.top > 0:
                my_loc = my_loc.move([0, -20])
            if event.key in [pygame.K_DOWN, pygame.K_s] and my_loc.bottom < height:
                my_loc = my_loc.move([0, 20])

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if resBtn_rect.collidepoint(mouse):
                restart()

    # Updating the location of the car images ->
    screen.fill((60, 200, 10)) # Color of the background

    pygame.draw.rect(screen, (50, 50, 50), (width/2 - road_w/2, 0, road_w, height)) # Road
    pygame.draw.rect(screen, (255, 255, 255), (width/2 - roadMark_w/2, 0, roadMark_w, height)) # Road Mark
    pygame.draw.rect(screen, (0, 100, 0), (width/2 - road_w/2, 0, roadMark_w*2, height)) # Road - side (left)
    pygame.draw.rect(screen, (0, 100, 0), (width/2 + road_w/2, 0, roadMark_w*2, height)) # Road - side (right)

    font = pygame.font.SysFont("comicsansms", 30)
    text = font.render(f"Score : {score}", True, (25, 25, 25))
    text_rect = text.get_rect()
    text_rect.center = (85, 25)
    screen.blit(text, text_rect)

    resBtn_rect = resBtnText.get_rect()
    pygame.draw.rect(screen, (255, 100, 100), (width - 70 - 1.2*resBtn_rect.width/2, 30 - 1.2*resBtn_rect.height/2, resBtn_rect.width*1.2, resBtn_rect.height*1.2))
    resBtn_rect.center = (width - 70, 30)

    screen.blit(enemy, enemy_loc)
    screen.blit(me, my_loc)
    screen.blit(resBtnText, resBtn_rect)
    pygame.display.update()

    # Collision Detection ->
    if enemy_loc.colliderect(my_loc):
        collide_loc = ((enemy_loc.centerx + my_loc.centerx)/2, (enemy_loc.centery + my_loc.centery)/2)
        blast_loc = explosion.get_rect()
        blast_loc.center = collide_loc

        print(collide_loc)
        # running = False
        dead = True
        gameOver(score)

    t1 = time.time() - t0
    if t1 >= 2:
        speed = speed + 0.1
        t1 = 0
        score += 10
        t0 = time.time()
          

pygame.quit()