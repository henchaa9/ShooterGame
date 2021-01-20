import pygame, sys, random

pygame.init()

width, height = 800, 600
win = pygame.display.set_mode((width, height))

# COLORS
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

# MOVEMENT VALUES
player_speed = 3
enemy_speed = 2
bullet_speed = 4

# USER EVENTS
REMOVEBULLET = pygame.USEREVENT + 0
SPAWNENEMY = pygame.USEREVENT + 1

pygame.time.set_timer(SPAWNENEMY, 2000)


def draw(*args):
    win.fill(white)

    pygame.draw.rect(win, green, player)
    
    for enemy in enemies:
        pygame.draw.rect(win, red, enemy)

    for bullet in bullets:
        pygame.draw.rect(win, yellow, bullet)

    pygame.display.update()


def move_player(keys_pressed, player):

    if keys_pressed[pygame.K_w]:
        if player.y > 4:
            player.y -= player_speed

    if keys_pressed[pygame.K_s]:
        if player.y < height - 24:
            player.y += player_speed

    if keys_pressed[pygame.K_a]:
        if player.x > 3:
            player.x -= player_speed

    if keys_pressed[pygame.K_d]:
        if player.x < width - 24:
            player.x += player_speed
    

def enemy_attack(player):

    for enemy in enemies:

        if enemy.x < player.x:
            enemy.x += enemy_speed
        else:
            enemy.x -= enemy_speed

        if enemy.y < player.y:
            enemy.y += enemy_speed
        else:
            enemy.y -= enemy_speed

        if player.colliderect(enemy):
            print("You lost")
            sys.exit()


class Bullet(pygame.Rect):
    def __init__(self, left, top, width, heigth, targetdir):
        super().__init__(left, top, width, heigth)
        self.pos = pygame.math.Vector2((left, top))
        self.vel = bullet_speed
        self.dir = pygame.math.Vector2(targetdir) - self.pos
        self.dir = self.dir.normalize()
        self.collisions = 0


def shoot(bullets):

    for bullet in bullets:

        if bullet.x < width and bullet.x > 0 and bullet.y < height and bullet.y > 0:
            bullet.pos += bullet.dir * bullet.vel
            bullet.x, bullet.y = (round(bullet.pos.x), round(bullet.pos.y))
        else:
            pygame.event.post(pygame.event.Event(REMOVEBULLET))
            bullets.remove(bullet)
            
        for enemy in enemies:

            if enemy.colliderect(bullet):
                pygame.event.post(pygame.event.Event(REMOVEBULLET))
                bullets.remove(bullet)
                enemies.remove(enemy)

                
def spawn_enemy():
    enemy = pygame.Rect(random.randint(1, 800), random.randint(1, 600), 20, 20)
    enemies.append(enemy)


fps = 60
clock = pygame.time.Clock()

player = pygame.Rect(30, 40, 20, 20)

bullets = []
enemies = []


while True:
    clock.tick(fps)
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            bullets.append(Bullet(player.x, player.y, 10, 10, (mx, my)))
            
        if event.type == SPAWNENEMY:
            spawn_enemy()

    keys_pressed = pygame.key.get_pressed() 

    draw(player)
    move_player(keys_pressed, player)
    enemy_attack(player)
    shoot(bullets)
