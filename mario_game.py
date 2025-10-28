import pygame
import sys
import random
import math

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
PURPLE = (147, 112, 219)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color, vel_x=None, vel_y=None):
        super().__init__()
        self.size = random.randint(3, 8)
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (self.size//2, self.size//2), self.size//2)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_x = vel_x if vel_x is not None else random.uniform(-3, 3)
        self.vel_y = vel_y if vel_y is not None else random.uniform(-5, -2)
        self.life = random.randint(30, 60)
        self.gravity = 0.3
        
    def update(self):
        self.vel_y += self.gravity
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.life -= 1
        
        alpha = int(255 * (self.life / 60))
        self.image.set_alpha(max(0, alpha))
        
        if self.life <= 0:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 45
        self.height = 50
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.facing_right = True
        self.animation_frame = 0
        self.draw_kitten()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.jump_power = -15
        self.gravity = 0.8
        self.speed = 5
        self.lives = 3
        self.invincible = False
        self.invincible_timer = 0
        
    def draw_kitten(self):
        self.image.fill((0, 0, 0, 0))
        
        body_color = (255, 230, 200)
        dark_color = (200, 150, 100)
        
        body_x = 22 if self.facing_right else 22
        
        pygame.draw.ellipse(self.image, body_color, (body_x - 12, 25, 24, 20))
        
        head_x = body_x
        pygame.draw.circle(self.image, body_color, (head_x, 15), 13)
        
        ear_offset = 1 if self.facing_right else -1
        ear1_points = [(head_x - 8, 5), (head_x - 10, 2), (head_x - 5, 8)]
        ear2_points = [(head_x + 8, 5), (head_x + 10, 2), (head_x + 5, 8)]
        pygame.draw.polygon(self.image, (255, 200, 180), ear1_points)
        pygame.draw.polygon(self.image, (255, 200, 180), ear2_points)
        
        eye_offset = 2 if self.facing_right else -2
        pygame.draw.circle(self.image, BLACK, (head_x - 4 + eye_offset, 13), 2)
        pygame.draw.circle(self.image, BLACK, (head_x + 4 + eye_offset, 13), 2)
        pygame.draw.circle(self.image, WHITE, (head_x - 3 + eye_offset, 12), 1)
        pygame.draw.circle(self.image, WHITE, (head_x + 5 + eye_offset, 12), 1)
        
        pygame.draw.circle(self.image, (255, 150, 150), (head_x, 18), 2)
        
        pygame.draw.line(self.image, BLACK, (head_x, 18), (head_x - 3, 20), 1)
        pygame.draw.line(self.image, BLACK, (head_x, 18), (head_x + 3, 20), 1)
        
        whisker_start = head_x - 5 if self.facing_right else head_x + 5
        for i in range(3):
            y_offset = 15 + i * 2
            if self.facing_right:
                pygame.draw.line(self.image, (100, 100, 100), (whisker_start, y_offset), (whisker_start - 8, y_offset - 1 + i), 1)
                pygame.draw.line(self.image, (100, 100, 100), (whisker_start + 10, y_offset), (whisker_start + 18, y_offset - 1 + i), 1)
            else:
                pygame.draw.line(self.image, (100, 100, 100), (whisker_start, y_offset), (whisker_start + 8, y_offset - 1 + i), 1)
                pygame.draw.line(self.image, (100, 100, 100), (whisker_start - 10, y_offset), (whisker_start - 18, y_offset - 1 + i), 1)
        
        leg_x1 = body_x - 6
        leg_x2 = body_x + 6
        pygame.draw.rect(self.image, body_color, (leg_x1, 42, 5, 8))
        pygame.draw.rect(self.image, body_color, (leg_x2, 42, 5, 8))
        
        tail_points = []
        for i in range(8):
            angle = 90 + i * 20
            radius = 10 - i * 0.5
            x = body_x + 12 + radius * math.cos(math.radians(angle))
            y = 30 + radius * math.sin(math.radians(angle))
            tail_points.append((x, y))
        if len(tail_points) > 1:
            pygame.draw.lines(self.image, dark_color, False, tail_points, 3)
        
    def update(self, platforms, enemies, coins, powerups, particles):
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
        
        self.animation_frame += 1
        
        self.vel_x = 0
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.vel_x = -self.speed
            if self.facing_right:
                self.facing_right = False
                self.draw_kitten()
        if keys[pygame.K_RIGHT]:
            self.vel_x = self.speed
            if not self.facing_right:
                self.facing_right = True
                self.draw_kitten()
        if keys[pygame.K_UP] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
            for _ in range(8):
                particles.add(Particle(
                    self.rect.centerx + random.randint(-10, 10),
                    self.rect.bottom,
                    random.choice([WHITE, (200, 200, 255), (150, 150, 255)]),
                    vel_x=random.uniform(-2, 2),
                    vel_y=random.uniform(-1, 1)
                ))
        
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
            for _ in range(20):
                particles.add(Particle(
                    self.rect.centerx + random.randint(-15, 15),
                    self.rect.centery + random.randint(-15, 15),
                    RED
                ))
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        
        coin_hits = pygame.sprite.spritecollide(self, coins, True)
        for coin in coin_hits:
            for _ in range(15):
                particles.add(Particle(
                    coin.rect.centerx + random.randint(-5, 5),
                    coin.rect.centery + random.randint(-5, 5),
                    random.choice([COIN_COLOR, (255, 255, 100), ORANGE])
                ))
        
        if not self.invincible:
            enemy_hits = pygame.sprite.spritecollide(self, enemies, False)
            for enemy in enemy_hits:
                if self.vel_y > 0 and self.rect.bottom - 10 < enemy.rect.top:
                    enemy.kill()
                    self.vel_y = -8
                    for _ in range(20):
                        particles.add(Particle(
                            enemy.rect.centerx + random.randint(-10, 10),
                            enemy.rect.centery + random.randint(-10, 10),
                            random.choice([GREEN, (100, 200, 100), (150, 255, 150)])
                        ))
                else:
                    self.lives -= 1
                    self.invincible = True
                    self.invincible_timer = 60
                    self.rect.x -= 50 if self.facing_right else -50
                    for _ in range(15):
                        particles.add(Particle(
                            self.rect.centerx + random.randint(-10, 10),
                            self.rect.centery + random.randint(-10, 10),
                            RED
                        ))
        
        powerup_hits = pygame.sprite.spritecollide(self, powerups, True)
        for powerup in powerup_hits:
            if powerup.type == 'life':
                self.lives += 1
            elif powerup.type == 'star':
                self.invincible = True
                self.invincible_timer = 300
            for _ in range(20):
                particles.add(Particle(
                    powerup.rect.centerx + random.randint(-8, 8),
                    powerup.rect.centery + random.randint(-8, 8),
                    random.choice([PURPLE, PINK, (255, 100, 255)])
                ))
        
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
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
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
                    base_color = BRICK_COLOR
                    highlight = (min(255, base_color[0] + 30), min(255, base_color[1] + 30), min(255, base_color[2] + 30))
                    shadow = (max(0, base_color[0] - 30), max(0, base_color[1] - 30), max(0, base_color[2] - 30))
                    
                    pygame.draw.rect(self.image, base_color, (i, j, brick_width-2, brick_height-2))
                    pygame.draw.rect(self.image, highlight, (i, j, brick_width-2, brick_height-2), 2)
                    pygame.draw.line(self.image, shadow, (i, j + brick_height-2), (i + brick_width-2, j + brick_height-2), 2)
                    pygame.draw.line(self.image, shadow, (i + brick_width-2, j), (i + brick_width-2, j + brick_height-2), 2)
                    
        elif platform_type == 'mystery':
            gradient_colors = [(255, 215, 0), (255, 235, 100), (255, 215, 0)]
            for i in range(self.height):
                ratio = i / self.height
                if ratio < 0.5:
                    color = self.interpolate_color(gradient_colors[0], gradient_colors[1], ratio * 2)
                else:
                    color = self.interpolate_color(gradient_colors[1], gradient_colors[2], (ratio - 0.5) * 2)
                pygame.draw.line(self.image, color, (0, i), (self.width, i))
            
            pygame.draw.rect(self.image, (200, 170, 0), (0, 0, self.width, self.height), 3)
            font = pygame.font.Font(None, 36)
            text = font.render('?', True, (255, 100, 0))
            text_rect = text.get_rect(center=(self.width//2, self.height//2))
            self.image.blit(text, text_rect)
            self.has_item = True
        else:
            for i in range(self.height):
                ratio = i / self.height
                r = int(color[0] * (1 - ratio * 0.3))
                g = int(color[1] * (1 - ratio * 0.3))
                b = int(color[2] * (1 - ratio * 0.3))
                pygame.draw.line(self.image, (r, g, b), (0, i), (self.width, i))
            
            for i in range(0, self.width, 30):
                pygame.draw.line(self.image, (100, 50, 20), (i, 0), (i, self.height), 2)
    
    def interpolate_color(self, color1, color2, ratio):
        return tuple(int(color1[i] + (color2[i] - color1[i]) * ratio) for i in range(3))
    
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
        
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw_enemy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = -2
        self.vel_y = 0
        self.gravity = 0.8
        
    def draw_enemy(self):
        self.image.fill((0, 0, 0, 0))
        
        if self.type == 'goomba':
            base_color = (139, 69, 19)
            for i in range(25):
                ratio = i / 25
                color = tuple(int(base_color[j] * (1 + ratio * 0.3)) for j in range(3))
                pygame.draw.ellipse(self.image, color, (5, 10 + i, 25, 1))
            
            pygame.draw.circle(self.image, WHITE, (12, 15), 4)
            pygame.draw.circle(self.image, WHITE, (22, 15), 4)
            pygame.draw.circle(self.image, BLACK, (12, 15), 2)
            pygame.draw.circle(self.image, BLACK, (22, 15), 2)
            
            pygame.draw.rect(self.image, (101, 67, 33), (8, 28, 8, 7))
            pygame.draw.rect(self.image, (101, 67, 33), (19, 28, 8, 7))
        else:
            shell_color = GREEN if random.random() > 0.5 else RED
            for i in range(30):
                ratio = i / 30
                color = tuple(int(shell_color[j] * (1 - ratio * 0.3)) for j in range(3))
                pygame.draw.ellipse(self.image, color, (0, 10 + i, 40, 1))
            
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
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw_coin()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animation_timer = 0
        self.glow_timer = 0
        
    def draw_coin(self, glow=False):
        self.image.fill((0, 0, 0, 0))
        
        if glow:
            pygame.draw.ellipse(self.image, (255, 255, 100, 128), (0, 0, 20, 25))
        
        pygame.draw.ellipse(self.image, COIN_COLOR, (2, 2, 16, 21))
        pygame.draw.ellipse(self.image, (255, 255, 0), (5, 5, 10, 15))
        highlight = (255, 255, 200)
        pygame.draw.ellipse(self.image, highlight, (6, 6, 5, 8))
        
    def update(self):
        self.animation_timer += 1
        self.glow_timer += 1
        
        glow = (self.glow_timer // 10) % 2 == 0
        
        if self.animation_timer % 20 < 10:
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self.draw_coin(glow)
        else:
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self.image.fill((0, 0, 0, 0))
            if glow:
                pygame.draw.ellipse(self.image, (255, 255, 100, 128), (5, 0, 10, 25))
            pygame.draw.ellipse(self.image, COIN_COLOR, (7, 2, 6, 21))
            pygame.draw.ellipse(self.image, (255, 255, 0), (8, 5, 4, 15))

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, powerup_type='life'):
        super().__init__()
        self.type = powerup_type
        self.width = 30
        self.height = 30
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw_powerup()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.base_y = y
        self.float_wave = random.uniform(0, math.pi * 2)
        
    def draw_powerup(self):
        self.image.fill((0, 0, 0, 0))
        
        if self.type == 'life':
            pygame.draw.polygon(self.image, (255, 0, 100), [
                (15, 8), (20, 3), (25, 8), (15, 20), (5, 8), (10, 3)
            ])
            pygame.draw.polygon(self.image, (255, 100, 150), [
                (15, 10), (18, 7), (21, 10), (15, 17), (9, 10), (12, 7)
            ])
        else:
            points = []
            for i in range(5):
                angle = i * 144 - 90
                x = 15 + 12 * math.cos(math.radians(angle))
                y = 15 + 12 * math.sin(math.radians(angle))
                points.append((x, y))
            pygame.draw.polygon(self.image, (255, 255, 100), points)
            pygame.draw.circle(self.image, (255, 255, 200), (15, 15), 6)
    
    def update(self):
        self.float_wave += 0.05
        self.rect.y = self.base_y + math.sin(self.float_wave) * 5

class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 50
        self.height = 200
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw_flag()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.wave_offset = 0
        
    def draw_flag(self):
        self.image.fill((0, 0, 0, 0))
        
        pygame.draw.rect(self.image, BLACK, (5, 0, 5, 200))
        
        flag_points = [(10, 10), (45, 25), (10, 40)]
        pygame.draw.polygon(self.image, GREEN, flag_points)
        pygame.draw.polygon(self.image, (0, 200, 0), [(10, 10), (45, 25), (40, 27), (10, 15)])

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Super Kitten Adventure - 超级小猫冒险")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = 'start'
        self.current_level = 1
        self.score = 0
        
        # 使用支持中文的字体
        try:
            # Windows 系统字体路径
            chinese_font = "C:/Windows/Fonts/msyh.ttc"  # 微软雅黑
            self.font = pygame.font.Font(chinese_font, 48)
            self.small_font = pygame.font.Font(chinese_font, 28)
            self.title_font = pygame.font.Font(chinese_font, 72)
        except:
            # 如果找不到微软雅黑，尝试其他中文字体
            try:
                chinese_font = "C:/Windows/Fonts/simhei.ttf"  # 黑体
                self.font = pygame.font.Font(chinese_font, 48)
                self.small_font = pygame.font.Font(chinese_font, 28)
                self.title_font = pygame.font.Font(chinese_font, 72)
            except:
                # 如果都找不到，使用系统默认字体
                self.font = pygame.font.SysFont('microsoftyahei', 48)
                self.small_font = pygame.font.SysFont('microsoftyahei', 28)
                self.title_font = pygame.font.SysFont('microsoftyahei', 72)
        
        self.particles = pygame.sprite.Group()
        self.stars = []
        for _ in range(50):
            self.stars.append([random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT//2), random.randint(1, 3)])
        
    def load_level(self, level):
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.flags = pygame.sprite.Group()
        self.particles.empty()
        
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
    
    def draw_start_screen(self):
        for i in range(SCREEN_HEIGHT):
            ratio = i / SCREEN_HEIGHT
            r = int(20 + (135 - 20) * ratio)
            g = int(20 + (206 - 20) * ratio)
            b = int(50 + (235 - 50) * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, i), (SCREEN_WIDTH, i))
        
        for star in self.stars:
            size = star[2]
            alpha = int(128 + 127 * math.sin(pygame.time.get_ticks() / 500 + star[0]))
            star_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(star_surf, (255, 255, 255, alpha), (size, size), size)
            self.screen.blit(star_surf, (star[0], star[1]))
        
        title_text = self.title_font.render('超级小猫', True, (255, 200, 100))
        title_shadow = self.title_font.render('超级小猫', True, (100, 50, 0))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
        self.screen.blit(title_text, title_rect)
        
        subtitle_text = self.font.render('冒险之旅', True, (255, 220, 150))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 210))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        kitten = Player(SCREEN_WIDTH // 2 - 25, 280)
        kitten_shadow = pygame.Surface((kitten.width + 10, kitten.height // 2), pygame.SRCALPHA)
        pygame.draw.ellipse(kitten_shadow, (0, 0, 0, 80), (0, 0, kitten.width + 10, kitten.height // 2))
        self.screen.blit(kitten_shadow, (SCREEN_WIDTH // 2 - 30, 330))
        self.screen.blit(kitten.image, (SCREEN_WIDTH // 2 - 22, 280))
        
        for _ in range(3):
            if random.random() < 0.05:
                self.particles.add(Particle(
                    SCREEN_WIDTH // 2 + random.randint(-30, 30),
                    300 + random.randint(-10, 20),
                    random.choice([(255, 200, 200), (200, 200, 255), (255, 255, 200)])
                ))
        
        self.particles.update()
        self.particles.draw(self.screen)
        
        controls_title = self.small_font.render('操作说明:', True, WHITE)
        self.screen.blit(controls_title, (SCREEN_WIDTH // 2 - 50, 380))
        
        controls = [
            '← → 方向键: 移动',
            '↑ 上方向键: 跳跃',
            'ESC: 退出'
        ]
        
        y_offset = 420
        for control in controls:
            control_text = self.small_font.render(control, True, (200, 255, 200))
            control_rect = control_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(control_text, control_rect)
            y_offset += 30
        
        start_text = self.font.render('按空格键开始', True, (255, 255, 100))
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        
        pulse = abs(math.sin(pygame.time.get_ticks() / 500))
        scaled_size = int(48 + pulse * 10)
        pulse_font = pygame.font.Font(None, scaled_size)
        start_text_pulse = pulse_font.render('按空格键开始', True, (255, 255, 100))
        start_rect_pulse = start_text_pulse.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        self.screen.blit(start_text_pulse, start_rect_pulse)
        
    def draw_background(self):
        for i in range(SCREEN_HEIGHT):
            ratio = i / SCREEN_HEIGHT
            r = int(135 + (200 - 135) * ratio)
            g = int(206 + (220 - 206) * ratio)
            b = int(235 + (255 - 235) * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, i), (SCREEN_WIDTH, i))
        
        clouds = [
            (100, 80, 60, 30),
            (300, 100, 80, 40),
            (550, 70, 70, 35),
            (650, 120, 65, 32),
        ]
        for x, y, w, h in clouds:
            pygame.draw.ellipse(self.screen, (255, 255, 255, 200), (x, y, w, h))
            pygame.draw.ellipse(self.screen, (255, 255, 255, 200), (x + 20, y - 10, w - 20, h))
            pygame.draw.ellipse(self.screen, (255, 255, 255, 200), (x + 10, y + 5, w - 20, h - 10))
    
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
                elif event.key == pygame.K_SPACE and self.game_state == 'start':
                    self.game_state = 'playing'
                    self.load_level(self.current_level)
                elif event.key == pygame.K_r and self.game_state == 'game_over':
                    self.current_level = 1
                    self.score = 0
                    self.game_state = 'playing'
                    self.load_level(self.current_level)
    
    def update(self):
        if self.game_state != 'playing':
            return
            
        if self.player.lives <= 0:
            self.game_state = 'game_over'
            return
        
        coins_collected = self.player.update(
            self.platforms, 
            self.enemies, 
            self.coins, 
            self.powerups,
            self.particles
        )
        self.score += coins_collected * 10
        
        self.enemies.update(self.platforms)
        self.coins.update()
        self.powerups.update()
        self.particles.update()
        
        flag_hit = pygame.sprite.spritecollide(self.player, self.flags, False)
        if flag_hit:
            for _ in range(50):
                self.particles.add(Particle(
                    flag_hit[0].rect.centerx + random.randint(-20, 20),
                    flag_hit[0].rect.centery + random.randint(-40, 40),
                    random.choice([GREEN, (100, 255, 100), (200, 255, 200), COIN_COLOR])
                ))
            self.current_level += 1
            if self.current_level > 4:
                self.current_level = 1
            self.load_level(self.current_level)
    
    def draw(self):
        if self.game_state == 'start':
            self.draw_start_screen()
        else:
            self.draw_background()
            
            self.all_sprites.draw(self.screen)
            self.particles.draw(self.screen)
            
            if self.player.invincible and self.player.invincible_timer % 10 < 5:
                glow_surf = pygame.Surface((self.player.width + 20, self.player.height + 20), pygame.SRCALPHA)
                pygame.draw.ellipse(glow_surf, (255, 255, 100, 100), (0, 0, self.player.width + 20, self.player.height + 20))
                self.screen.blit(glow_surf, (self.player.rect.x - 10, self.player.rect.y - 10))
            
            panel_surf = pygame.Surface((220, 100), pygame.SRCALPHA)
            pygame.draw.rect(panel_surf, (0, 0, 0, 120), (0, 0, 220, 100), border_radius=10)
            pygame.draw.rect(panel_surf, (255, 255, 255, 100), (0, 0, 220, 100), 2, border_radius=10)
            self.screen.blit(panel_surf, (5, 5))
            
            score_text = self.small_font.render(f'分数: {self.score}', True, (255, 255, 100))
            self.screen.blit(score_text, (15, 15))
            
            lives_text = self.small_font.render(f'生命: {self.player.lives}', True, (255, 100, 100))
            self.screen.blit(lives_text, (15, 45))
            
            level_text = self.small_font.render(f'关卡: {self.current_level}', True, (100, 255, 100))
            self.screen.blit(level_text, (15, 75))
            
            if self.player.invincible:
                invincible_text = self.font.render('无敌状态!', True, (255, 215, 0))
                invincible_shadow = self.font.render('无敌状态!', True, (100, 100, 0))
                self.screen.blit(invincible_shadow, (SCREEN_WIDTH // 2 - 98, 12))
                self.screen.blit(invincible_text, (SCREEN_WIDTH // 2 - 100, 10))
            
            if self.game_state == 'game_over':
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                pygame.draw.rect(overlay, (0, 0, 0, 150), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
                self.screen.blit(overlay, (0, 0))
                
                game_over_text = self.title_font.render('游戏结束', True, (255, 100, 100))
                game_over_shadow = self.title_font.render('游戏结束', True, (100, 0, 0))
                game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
                self.screen.blit(game_over_shadow, (game_over_rect.x + 3, game_over_rect.y + 3))
                self.screen.blit(game_over_text, game_over_rect)
                
                final_score_text = self.font.render(f'最终分数: {self.score}', True, WHITE)
                final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
                self.screen.blit(final_score_text, final_score_rect)
                
                restart_text = self.small_font.render('按 R 键重新开始', True, (200, 255, 200))
                restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
                self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run()
