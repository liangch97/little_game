import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
GROUND_COLOR = (139, 69, 19)
BRICK_COLOR = (200, 100, 50)
COIN_COLOR = (255, 215, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 40
        self.height = 50
        self.image = pygame.Surface((self.width, self.height))
        self.draw_mario()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.jump_power = -15
        self.gravity = 0.8
        self.speed = 5
        self.facing_right = True
        self.lives = 3
        self.invincible = False
        self.invincible_timer = 0
        
    def draw_mario(self):
        self.image.fill((255, 0, 255))
        self.image.set_colorkey((255, 0, 255))
        
        pygame.draw.circle(self.image, (255, 218, 185), (20, 15), 12)
        
        hat_points = [(8, 15), (32, 15), (30, 8), (10, 8)]
        pygame.draw.polygon(self.image, RED, hat_points)
        pygame.draw.rect(self.image, RED, (12, 12, 16, 6))
        
        pygame.draw.circle(self.image, BLACK, (16, 14), 2)
        pygame.draw.circle(self.image, BLACK, (24, 14), 2)
        
        pygame.draw.rect(self.image, (139, 69, 19), (15, 18, 10, 3))
        
        pygame.draw.rect(self.image, BLUE, (10, 25, 20, 15))
        
        pygame.draw.rect(self.image, (255, 218, 185), (8, 28, 6, 12))
        pygame.draw.rect(self.image, (255, 218, 185), (26, 28, 6, 12))
        
        pygame.draw.rect(self.image, BLUE, (12, 40, 7, 10))
        pygame.draw.rect(self.image, BLUE, (21, 40, 7, 10))
        
        pygame.draw.rect(self.image, (101, 67, 33), (12, 47, 7, 3))
        pygame.draw.rect(self.image, (101, 67, 33), (21, 47, 7, 3))
        
    def update(self, platforms, enemies, coins, powerups):
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
        
        self.vel_x = 0
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.vel_x = -self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.vel_x = self.speed
            self.facing_right = True
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
        
        self.vel_y += self.gravity
        if self.vel_y > 15:
            self.vel_y = 15
        
        self.rect.x += self.vel_x
        self.check_collision_x(platforms)
        
        self.rect.y += self.vel_y
        self.on_ground = False
        self.check_collision_y(platforms)
        
        if self.rect.bottom > SCREEN_HEIGHT:
            self.lives -= 1
            self.rect.x = 50
            self.rect.y = SCREEN_HEIGHT - 150
            self.vel_y = 0
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        
        coin_hits = pygame.sprite.spritecollide(self, coins, True)
        
        if not self.invincible:
            enemy_hits = pygame.sprite.spritecollide(self, enemies, False)
            for enemy in enemy_hits:
                if self.vel_y > 0 and self.rect.bottom - 10 < enemy.rect.top:
                    enemy.kill()
                    self.vel_y = -8
                else:
                    self.lives -= 1
                    self.invincible = True
                    self.invincible_timer = 60
                    self.rect.x -= 50 if self.facing_right else -50
        
        powerup_hits = pygame.sprite.spritecollide(self, powerups, True)
        for powerup in powerup_hits:
            if powerup.type == 'life':
                self.lives += 1
            elif powerup.type == 'star':
                self.invincible = True
                self.invincible_timer = 300
        
        return len(coin_hits)
    
    def check_collision_x(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_x > 0:
                    self.rect.right = platform.rect.left
                elif self.vel_x < 0:
                    self.rect.left = platform.rect.right
    
    def check_collision_y(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
                    if hasattr(platform, 'hit'):
                        platform.hit()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=GROUND_COLOR, platform_type='ground'):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = platform_type
        self.draw_platform(color, platform_type)
        
    def draw_platform(self, color, platform_type):
        if platform_type == 'brick':
            brick_width = 40
            brick_height = 20
            for i in range(0, self.width, brick_width):
                for j in range(0, self.height, brick_height):
                    pygame.draw.rect(self.image, BRICK_COLOR, (i, j, brick_width-2, brick_height-2))
                    pygame.draw.rect(self.image, (150, 75, 40), (i, j, brick_width-2, brick_height-2), 2)
        elif platform_type == 'mystery':
            self.image.fill((255, 215, 0))
            pygame.draw.rect(self.image, (200, 170, 0), (0, 0, self.width, self.height), 3)
            font = pygame.font.Font(None, 36)
            text = font.render('?', True, (255, 100, 0))
            text_rect = text.get_rect(center=(self.width//2, self.height//2))
            self.image.blit(text, text_rect)
            self.has_item = True
        else:
            self.image.fill(color)
            for i in range(0, self.width, 30):
                pygame.draw.line(self.image, (100, 50, 20), (i, 0), (i, self.height), 2)
    
    def hit(self):
        if self.type == 'mystery' and self.has_item:
            self.has_item = False
            self.image.fill((150, 150, 150))
            pygame.draw.rect(self.image, (100, 100, 100), (0, 0, self.width, self.height), 3)
            return True
        return False

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type='goomba'):
        super().__init__()
        self.type = enemy_type
        if enemy_type == 'goomba':
            self.width = 35
            self.height = 35
        else:
            self.width = 40
            self.height = 40
        
        self.image = pygame.Surface((self.width, self.height))
        self.draw_enemy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = -2
        self.vel_y = 0
        self.gravity = 0.8
        
    def draw_enemy(self):
        self.image.fill((255, 0, 255))
        self.image.set_colorkey((255, 0, 255))
        
        if self.type == 'goomba':
            pygame.draw.ellipse(self.image, (139, 69, 19), (5, 10, 25, 25))
            
            pygame.draw.circle(self.image, WHITE, (12, 15), 4)
            pygame.draw.circle(self.image, WHITE, (22, 15), 4)
            pygame.draw.circle(self.image, BLACK, (12, 15), 2)
            pygame.draw.circle(self.image, BLACK, (22, 15), 2)
            
            pygame.draw.rect(self.image, (101, 67, 33), (8, 28, 8, 7))
            pygame.draw.rect(self.image, (101, 67, 33), (19, 28, 8, 7))
        else:
            shell_color = GREEN if random.random() > 0.5 else RED
            pygame.draw.ellipse(self.image, shell_color, (0, 10, 40, 30))
            pygame.draw.ellipse(self.image, (100, 200, 100), (5, 15, 30, 20))
            
            pygame.draw.circle(self.image, (150, 255, 150), (20, 8), 8)
            pygame.draw.circle(self.image, BLACK, (18, 6), 2)
            pygame.draw.circle(self.image, BLACK, (22, 6), 2)
    
    def update(self, platforms):
        self.vel_y += self.gravity
        if self.vel_y > 15:
            self.vel_y = 15
        
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
        
        if self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
            self.vel_x *= -1
        
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 20
        self.height = 25
        self.image = pygame.Surface((self.width, self.height))
        self.draw_coin()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animation_timer = 0
        
    def draw_coin(self):
        self.image.fill((255, 0, 255))
        self.image.set_colorkey((255, 0, 255))
        pygame.draw.ellipse(self.image, COIN_COLOR, (2, 2, 16, 21))
        pygame.draw.ellipse(self.image, (255, 255, 0), (5, 5, 10, 15))
        
    def update(self):
        self.animation_timer += 1
        if self.animation_timer % 20 < 10:
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((255, 0, 255))
            self.image.set_colorkey((255, 0, 255))
            pygame.draw.ellipse(self.image, COIN_COLOR, (2, 2, 16, 21))
            pygame.draw.ellipse(self.image, (255, 255, 0), (5, 5, 10, 15))
        else:
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((255, 0, 255))
            self.image.set_colorkey((255, 0, 255))
            pygame.draw.ellipse(self.image, COIN_COLOR, (7, 2, 6, 21))

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, powerup_type='life'):
        super().__init__()
        self.type = powerup_type
        self.width = 30
        self.height = 30
        self.image = pygame.Surface((self.width, self.height))
        self.draw_powerup()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def draw_powerup(self):
        self.image.fill((255, 0, 255))
        self.image.set_colorkey((255, 0, 255))
        
        if self.type == 'life':
            pygame.draw.polygon(self.image, RED, [
                (15, 8), (20, 3), (25, 8), (15, 20), (5, 8), (10, 3)
            ])
        else:
            points = []
            for i in range(5):
                angle = i * 144 - 90
                x = 15 + 12 * pygame.math.Vector2(1, 0).rotate(angle).x
                y = 15 + 12 * pygame.math.Vector2(1, 0).rotate(angle).y
                points.append((x, y))
            pygame.draw.polygon(self.image, (255, 255, 100), points)
            pygame.draw.circle(self.image, (255, 255, 200), (15, 15), 6)

class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 50
        self.height = 200
        self.image = pygame.Surface((self.width, self.height))
        self.draw_flag()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def draw_flag(self):
        self.image.fill((255, 0, 255))
        self.image.set_colorkey((255, 0, 255))
        
        pygame.draw.rect(self.image, BLACK, (5, 0, 5, 200))
        
        flag_points = [(10, 10), (45, 25), (10, 40)]
        pygame.draw.polygon(self.image, GREEN, flag_points)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Super Mario Game - 超级马里奥")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_level = 1
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.load_level(self.current_level)
        
    def load_level(self, level):
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.flags = pygame.sprite.Group()
        
        self.player = Player(50, SCREEN_HEIGHT - 150)
        self.all_sprites.add(self.player)
        
        if level == 1:
            self.create_level_1()
        elif level == 2:
            self.create_level_2()
        elif level == 3:
            self.create_level_3()
        else:
            self.create_level_4()
    
    def create_level_1(self):
        ground = Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50, GROUND_COLOR, 'ground')
        self.platforms.add(ground)
        self.all_sprites.add(ground)
        
        platforms_data = [
            (200, 450, 100, 20, 'brick'),
            (350, 400, 100, 20, 'brick'),
            (500, 350, 100, 20, 'brick'),
            (300, 300, 40, 40, 'mystery'),
            (600, 450, 80, 20, 'brick'),
        ]
        
        for x, y, w, h, ptype in platforms_data:
            platform = Platform(x, y, w, h, BRICK_COLOR, ptype)
            self.platforms.add(platform)
            self.all_sprites.add(platform)
        
        coins_positions = [
            (220, 420), (250, 420), (280, 420),
            (370, 370), (400, 370), (430, 370),
            (520, 320), (550, 320), (580, 320),
        ]
        
        for x, y in coins_positions:
            coin = Coin(x, y)
            self.coins.add(coin)
            self.all_sprites.add(coin)
        
        enemies_data = [
            (300, SCREEN_HEIGHT - 100, 'goomba'),
            (500, SCREEN_HEIGHT - 100, 'koopa'),
            (650, SCREEN_HEIGHT - 100, 'goomba'),
        ]
        
        for x, y, etype in enemies_data:
            enemy = Enemy(x, y, etype)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
        
        powerup = PowerUp(320, 250, 'life')
        self.powerups.add(powerup)
        self.all_sprites.add(powerup)
        
        flag = Flag(720, SCREEN_HEIGHT - 250)
        self.flags.add(flag)
        self.all_sprites.add(flag)
    
    def create_level_2(self):
        ground = Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50, GROUND_COLOR, 'ground')
        self.platforms.add(ground)
        self.all_sprites.add(ground)
        
        platforms_data = [
            (100, 480, 80, 20, 'brick'),
            (200, 430, 80, 20, 'brick'),
            (300, 380, 80, 20, 'brick'),
            (400, 330, 80, 20, 'brick'),
            (500, 280, 80, 20, 'brick'),
            (600, 330, 80, 20, 'brick'),
            (250, 250, 40, 40, 'mystery'),
            (450, 200, 40, 40, 'mystery'),
            (150, 350, 60, 20, 'brick'),
        ]
        
        for x, y, w, h, ptype in platforms_data:
            platform = Platform(x, y, w, h, BRICK_COLOR, ptype)
            self.platforms.add(platform)
            self.all_sprites.add(platform)
        
        coins_positions = [
            (120, 450), (150, 450),
            (220, 400), (250, 400),
            (320, 350), (350, 350),
            (420, 300), (450, 300),
            (520, 250), (550, 250),
            (620, 300), (650, 300),
        ]
        
        for x, y in coins_positions:
            coin = Coin(x, y)
            self.coins.add(coin)
            self.all_sprites.add(coin)
        
        enemies_data = [
            (250, SCREEN_HEIGHT - 100, 'goomba'),
            (400, SCREEN_HEIGHT - 100, 'koopa'),
            (550, SCREEN_HEIGHT - 100, 'goomba'),
            (300, 350, 'koopa'),
        ]
        
        for x, y, etype in enemies_data:
            enemy = Enemy(x, y, etype)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
        
        powerup = PowerUp(270, 200, 'star')
        self.powerups.add(powerup)
        self.all_sprites.add(powerup)
        
        flag = Flag(720, SCREEN_HEIGHT - 250)
        self.flags.add(flag)
        self.all_sprites.add(flag)
    
    def create_level_3(self):
        platforms_data = [
            (0, SCREEN_HEIGHT - 50, 250, 50, 'ground'),
            (350, SCREEN_HEIGHT - 50, 450, 50, 'ground'),
            (100, 450, 100, 20, 'brick'),
            (250, 400, 100, 20, 'brick'),
            (450, 450, 100, 20, 'brick'),
            (600, 400, 100, 20, 'brick'),
            (150, 320, 80, 20, 'brick'),
            (350, 300, 80, 20, 'brick'),
            (550, 320, 80, 20, 'brick'),
            (300, 250, 40, 40, 'mystery'),
            (500, 250, 40, 40, 'mystery'),
        ]
        
        for x, y, w, h, ptype in platforms_data:
            platform = Platform(x, y, w, h, GROUND_COLOR if ptype == 'ground' else BRICK_COLOR, ptype)
            self.platforms.add(platform)
            self.all_sprites.add(platform)
        
        coins_positions = [
            (120, 420), (150, 420), (180, 420),
            (270, 370), (300, 370), (330, 370),
            (470, 420), (500, 420), (530, 420),
            (620, 370), (650, 370), (680, 370),
            (170, 290), (370, 270), (570, 290),
        ]
        
        for x, y in coins_positions:
            coin = Coin(x, y)
            self.coins.add(coin)
            self.all_sprites.add(coin)
        
        enemies_data = [
            (200, SCREEN_HEIGHT - 100, 'goomba'),
            (500, SCREEN_HEIGHT - 100, 'koopa'),
            (650, SCREEN_HEIGHT - 100, 'goomba'),
            (280, 370, 'koopa'),
            (480, 420, 'goomba'),
        ]
        
        for x, y, etype in enemies_data:
            enemy = Enemy(x, y, etype)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
        
        powerup1 = PowerUp(320, 200, 'life')
        powerup2 = PowerUp(520, 200, 'star')
        self.powerups.add(powerup1, powerup2)
        self.all_sprites.add(powerup1, powerup2)
        
        flag = Flag(720, SCREEN_HEIGHT - 250)
        self.flags.add(flag)
        self.all_sprites.add(flag)
    
    def create_level_4(self):
        platforms_data = [
            (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50, 'ground'),
            (80, 480, 60, 20, 'brick'),
            (160, 430, 60, 20, 'brick'),
            (240, 380, 60, 20, 'brick'),
            (320, 330, 60, 20, 'brick'),
            (400, 280, 60, 20, 'brick'),
            (480, 330, 60, 20, 'brick'),
            (560, 380, 60, 20, 'brick'),
            (640, 430, 60, 20, 'brick'),
            (200, 250, 40, 40, 'mystery'),
            (400, 200, 40, 40, 'mystery'),
            (600, 250, 40, 40, 'mystery'),
            (100, 350, 80, 20, 'brick'),
            (300, 200, 80, 20, 'brick'),
            (500, 200, 80, 20, 'brick'),
        ]
        
        for x, y, w, h, ptype in platforms_data:
            platform = Platform(x, y, w, h, GROUND_COLOR if ptype == 'ground' else BRICK_COLOR, ptype)
            self.platforms.add(platform)
            self.all_sprites.add(platform)
        
        coins_positions = [
            (100, 450), (180, 400), (260, 350), 
            (340, 300), (420, 250), (500, 300),
            (580, 350), (660, 400),
            (320, 170), (350, 170), (520, 170), (550, 170),
        ]
        
        for x, y in coins_positions:
            coin = Coin(x, y)
            self.coins.add(coin)
            self.all_sprites.add(coin)
        
        enemies_data = [
            (150, SCREEN_HEIGHT - 100, 'koopa'),
            (300, SCREEN_HEIGHT - 100, 'goomba'),
            (450, SCREEN_HEIGHT - 100, 'koopa'),
            (600, SCREEN_HEIGHT - 100, 'goomba'),
            (700, SCREEN_HEIGHT - 100, 'koopa'),
            (250, 350, 'goomba'),
        ]
        
        for x, y, etype in enemies_data:
            enemy = Enemy(x, y, etype)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
        
        powerup1 = PowerUp(220, 200, 'star')
        powerup2 = PowerUp(420, 150, 'life')
        powerup3 = PowerUp(620, 200, 'star')
        self.powerups.add(powerup1, powerup2, powerup3)
        self.all_sprites.add(powerup1, powerup2, powerup3)
        
        flag = Flag(720, SCREEN_HEIGHT - 250)
        self.flags.add(flag)
        self.all_sprites.add(flag)
    
    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        
        pygame.quit()
        sys.exit()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.player.lives <= 0:
                    self.current_level = 1
                    self.score = 0
                    self.load_level(self.current_level)
    
    def update(self):
        if self.player.lives <= 0:
            return
        
        coins_collected = self.player.update(
            self.platforms, 
            self.enemies, 
            self.coins, 
            self.powerups
        )
        self.score += coins_collected * 10
        
        self.enemies.update(self.platforms)
        self.coins.update()
        
        flag_hit = pygame.sprite.spritecollide(self.player, self.flags, False)
        if flag_hit:
            self.current_level += 1
            if self.current_level > 4:
                self.current_level = 1
            self.load_level(self.current_level)
    
    def draw(self):
        self.screen.fill(SKY_BLUE)
        
        clouds = [
            (100, 80, 60, 30),
            (300, 100, 80, 40),
            (550, 70, 70, 35),
        ]
        for x, y, w, h in clouds:
            pygame.draw.ellipse(self.screen, WHITE, (x, y, w, h))
            pygame.draw.ellipse(self.screen, WHITE, (x + 20, y - 10, w - 20, h))
            pygame.draw.ellipse(self.screen, WHITE, (x + 10, y + 5, w - 20, h - 10))
        
        self.all_sprites.draw(self.screen)
        
        if self.player.invincible and self.player.invincible_timer % 10 < 5:
            temp_pos = self.player.rect.topleft
            self.player.rect.x += random.randint(-2, 2)
            self.player.rect.y += random.randint(-2, 2)
            self.screen.blit(self.player.image, self.player.rect)
            self.player.rect.topleft = temp_pos
        
        score_text = self.font.render(f'Score: {self.score}', True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        lives_text = self.font.render(f'Lives: {self.player.lives}', True, RED)
        self.screen.blit(lives_text, (10, 50))
        
        level_text = self.font.render(f'Level: {self.current_level}', True, BLACK)
        self.screen.blit(level_text, (SCREEN_WIDTH - 150, 10))
        
        if self.player.invincible:
            invincible_text = self.small_font.render('INVINCIBLE!', True, (255, 215, 0))
            self.screen.blit(invincible_text, (SCREEN_WIDTH // 2 - 60, 10))
        
        if self.player.lives <= 0:
            game_over_text = self.font.render('GAME OVER', True, RED)
            restart_text = self.small_font.render('Press R to Restart', True, BLACK)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run()
