import pygame
import os # importing operating system to identify the location of something

pygame.font.init() # in order to display font in the surface
pygame.mixer.init() # adds sound effects



WIDTH, HEIGHT = 900, 500 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Space Wars')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('Arial', 200)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

bg_color = (150, 150, 150) # 0-255...numbers for color...3 element for R G B
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

FPS = 60 # creating frames: 60 frames per second
VEL = 2
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

BULLET_VEL = 6
MAX_BULLET = 2

YELLOW_HIT = pygame.USEREVENT + 1 # creating a new event
RED_HIT = pygame.USEREVENT + 2

spaceship_width, spaceship_height = 45, 50

SPACESHIP_YELLOW = pygame.image.load(os.path.join('Assets', 'spaceship_red.png' ))
SPACESHIP_RED = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png' ))

background = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

# to resize
SPACESHIP_YELLOW = pygame.transform.scale(SPACESHIP_YELLOW, (spaceship_width, spaceship_height))
SPACESHIP_RED = pygame.transform.scale(SPACESHIP_RED, (spaceship_width, spaceship_height))

# to rotate
SPACESHIP_YELLOW2 = pygame.transform.rotate(SPACESHIP_YELLOW, 90)
SPACESHIP_RED2 = pygame.transform.rotate(SPACESHIP_RED, 270)


def draw_window(red, yellow, yellow_bullets, red_bullets, red_health, yellow_health):
    # WIN.fill(bg_color)
    WIN.blit(background, (0, 0))
    
    red_heath_text = HEALTH_FONT.render('Heath: '+str(red_health), 1, WHITE) # to render some text on screen..here 1 is for anti ailiasing
    yellow_heath_text = HEALTH_FONT.render('Heath: '+str(yellow_health), 1, WHITE) # render(what , anti ailiaising , color)

    WIN.blit(red_heath_text, (10, 10))
    WIN.blit(yellow_heath_text, (WIDTH - yellow_heath_text.get_width() - 10, 10)) # blit(what, (x, y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    # border_background = pygame.transform.scale(background, (10, HEIGHT))
    pygame.draw.rect(WIN, BLACK, BORDER) # drawing rect(where, color, what = rect)
    
    WIN.blit(SPACESHIP_YELLOW2, (yellow.x, yellow.y)) # position of the target in co ordinate system--> (225, 250)
    WIN.blit(SPACESHIP_RED2, (red.x, red.y)) # there is no point defining the co ordinate of the image if we use Rect 
    # blit is only for any types of imported surface

    pygame.display.update() # to update the changes

def handle_collision(yellow_bullets, red_bullets, red, yellow):
        for bullet in yellow_bullets:
            bullet.x -= BULLET_VEL # ?
            if red.colliderect(bullet): # for cheacking collision one rect with another
                pygame.event.post(pygame.event.Event(RED_HIT))
                yellow_bullets.remove(bullet)
            elif bullet.x < 0:
                yellow_bullets.remove(bullet)

        for bullet in red_bullets:
            bullet.x += BULLET_VEL
            if yellow.colliderect(bullet): # for cheacking collision one rect with another
                pygame.event.post(pygame.event.Event(YELLOW_HIT))
                red_bullets.remove(bullet)
            elif bullet.x > WIDTH:
                red_bullets.remove(bullet)


def draw_winner_text(winner_text):
    x = WINNER_FONT.render(winner_text, 1, WHITE)
    WIN.blit(x, (WIDTH // 2 - (x.get_width() // 2), HEIGHT // 2 - (x.get_height() // 2)))
    pygame.display.update()
    pygame.time.delay(5000) # 5000 milisecond delay 

def movement(keys_pressed, red, yellow):
    if keys_pressed[pygame.K_a] and red.x - VEL > 0:
            red.x -= VEL
    if keys_pressed[pygame.K_d] and red.x + VEL < BORDER.x - red.width:
            red.x += VEL
    if keys_pressed[pygame.K_w] and red.y - VEL > 0:
            red.y -= VEL
    if keys_pressed[pygame.K_s] and red.y + VEL < HEIGHT - red.height:
            red.y += VEL
    if keys_pressed[pygame.K_UP] and yellow.y - VEL > 0:
            yellow.y -= VEL
    if keys_pressed[pygame.K_DOWN] and yellow.y + VEL < HEIGHT - yellow.height:
            yellow.y += VEL
    if keys_pressed[pygame.K_LEFT] and yellow.x - VEL > BORDER.x :
            yellow.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and yellow.x + VEL < WIDTH - yellow.width:
            yellow.x += VEL


def main():
    yellow = pygame.Rect(675, 250, spaceship_width, spaceship_height) # Rect(x, y, width, height)
    red = pygame.Rect(225, 250, spaceship_width, spaceship_height) 
    
    red_health = 10
    yellow_health = 10

    red_bullets = []
    yellow_bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:    # for individual key pressed
                if event.key == pygame.K_SPACE and len(red_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(red.x + red.width, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(yellow_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(yellow.x,  yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
                
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ''
        # if red_health <= 0 and yellow_health <= 0:
        #     winner_text = 'Draw'

        if yellow_health <= 0:
            winner_text = 'RED Wins'
            

        if red_health <= 0:
            winner_text = 'Yellow Wins'
            

        if winner_text != '':
            draw_winner_text(winner_text)
            break
                     

        # red. x += 1
        # yellow.x += 1

        keys_pressed = pygame.key.get_pressed() # keys that are currently pressed 
        movement(keys_pressed, red, yellow)     # for multiple key pressed 

        handle_collision(yellow_bullets, red_bullets, red, yellow)
        
        draw_window(yellow, red, yellow_bullets, red_bullets, red_health, yellow_health)

    main()   
        



if __name__ == '__main__': # this is for determinig that this game is completely running directly
    main()
