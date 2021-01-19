import pygame, sys


width, height = 800, 600
win = pygame.display.set_mode((width, height))

#COLORS
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

#MOVEMENT VALUES
player_speed = 3
enemy_speed = 2
bullet_speed = 5


def draw(*args):
    win.fill(white)

    pygame.draw.rect(win, green, player)
    pygame.draw.rect(win, red, enemy)

    for bullet in bullets:
        pygame.draw.rect(win, yellow, bullet)

    pygame.display.update()


def move_player(keys_pressed, player):

    if keys_pressed[pygame.K_w]:
        if player.y > 1:
            player.y -= player_speed

    if keys_pressed[pygame.K_s]:
        if player.y < height - 11:
            player.y += player_speed

    if keys_pressed[pygame.K_a]:
        if player.x > 3:
            player.x -= player_speed

    if keys_pressed[pygame.K_d]:
        if player.x < width - 11:
            player.x += player_speed
    

def enemy_attack(player, enemy):

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


def shoot(bullets):

    for bullet in bullets:

        if bullet.x < 800 and bullet.x > 0 and bullet.y < 600 and bullet.y > 0:
            bullet.pos += bullet.dir * bullet.vel
            bullet.x, bullet.y = (round(bullet.pos.x), round(bullet.pos.y))
        else:
            bullets.remove(bullet)

        if bullet.colliderect(enemy):
            bullets.remove(bullet)
            print('hit')


fps = 60
clock = pygame.time.Clock()

player = pygame.Rect(30, 40, 20, 20)
enemy = pygame.Rect(300, 300, 20, 20)

bullets = []
bullet_pos = []


while True:
    clock.tick(fps)
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            bullets.append(Bullet(player.x, player.y, 10, 10, (mx, my)))
            
    keys_pressed = pygame.key.get_pressed() 

    draw(player, enemy)
    move_player(keys_pressed, player)
    enemy_attack(player, enemy)
    shoot(bullets)
