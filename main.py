import pygame, sys, random

pygame.init()

# MAIN WINDOW
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))

# COLORS
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# MOVEMENT VALUES
PLAYER_SPEED = 3
ENEMY_SPEED = 2
BULLET_SPEED = 4

# USER EVENTS
REMOVEBULLET = pygame.USEREVENT + 0
SPAWNENEMY = pygame.USEREVENT + 1

# PLAYER MOVEMENT
def player_movement():
    if keys_pressed[pygame.K_w]:
        if player.y > 4:
            player.y -= PLAYER_SPEED

    if keys_pressed[pygame.K_s]:
        if player.y < HEIGHT - 24:
            player.y += PLAYER_SPEED

    if keys_pressed[pygame.K_a]:
        if player.x > 3:
            player.x -= PLAYER_SPEED

    if keys_pressed[pygame.K_d]:
        if player.x < WIDTH - 24:
            player.x += PLAYER_SPEED


# BULLET
class Bullet(pygame.Rect):
    def __init__(self, left, top, width, heigth, targetdir):
        super().__init__(left, top, width, heigth)
        self.pos = pygame.math.Vector2((left, top))
        self.vel = BULLET_SPEED
        self.dir = pygame.math.Vector2(targetdir) - self.pos
        self.dir = self.dir.normalize()


# GAME SCENES
class Scenes():
    pygame.time.set_timer(SPAWNENEMY, 2000)

    def __init__(self):
        self.scene = 'scene_1'
        self.bullets = []
        self.enemies = []


    def scene_manager(self):
        if self.scene == 'scene_1':
            self.scene_1()

        elif self.scene == 'scene_2':
            self.scene_2()


    def scene_1(self):      
        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                self.bullets.append(Bullet(player.x, player.y, 10, 10, (mx, my)))
                
            if event.type == SPAWNENEMY:
                enemy = pygame.Rect(random.randint(1, 800), random.randint(1, 600), 20, 20)
                self.enemies.append(enemy)

        # PLAYER MOVEMENT
        player_movement()

        # CHECKS FOR SCENE SWITCH
        if keys_pressed[pygame.K_d] and player.x == 777:
            player.x = 6
            self.scene = 'scene_2'

        # DRAWING TO SCREEN
        win.fill(WHITE)

        pygame.draw.rect(win, GREEN, player)
        
        for enemy in self.enemies:
            pygame.draw.rect(win, RED, enemy)

        for bullet in self.bullets:
            pygame.draw.rect(win, YELLOW, bullet)

        pygame.display.update()
        
        # ENEMIES TRACKING PLAYER
        for enemy in self.enemies:

            if enemy.x < player.x:
                enemy.x += ENEMY_SPEED
            else:
                enemy.x -= ENEMY_SPEED

            if enemy.y < player.y:
                enemy.y += ENEMY_SPEED
            else:
                enemy.y -= ENEMY_SPEED

            if player.colliderect(enemy):
                print("You lost")
                sys.exit()

        # BULLET TRACKING
        for bullet in self.bullets:
            if bullet.x < WIDTH and bullet.x > 0 and bullet.y < HEIGHT and bullet.y > 0:
                bullet.pos += bullet.dir * bullet.vel
                bullet.x, bullet.y = (round(bullet.pos.x), round(bullet.pos.y))
            else:
                pygame.event.post(pygame.event.Event(REMOVEBULLET))
                self.bullets.remove(bullet)
                
            for enemy in self.enemies:
                if enemy.colliderect(bullet):
                    pygame.event.post(pygame.event.Event(REMOVEBULLET))
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)


    def scene_2(self):
        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # CHECKS FOR SCENE SWITCH
        if keys_pressed[pygame.K_a] and player.x == 3:
            player.x = 777
            self.scene = 'scene_1'
            self.bullets = []
            self.enemies = []

        # PLAYER MOVEMENT
        player_movement()

        # DRAWING TO SCREEN
        win.fill(WHITE)

        pygame.draw.rect(win, GREEN, player)

        pygame.display.update()


# PLAYER
player = pygame.Rect(30, 40, 20, 20)

# SCENE INSTANCE
current_scene = Scenes()

# MAIN LOOP
FPS = 60
clock = pygame.time.Clock()

while True:
    clock.tick(FPS)

    keys_pressed = pygame.key.get_pressed()

    # SCENE SWITCHING
    current_scene.scene_manager()


