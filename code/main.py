import pygame
from os.path import join
from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.mask = pygame.mask.from_surface(self.image)

        self.direction = pygame.math.Vector2()
        self.speed = 400

        # Colldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time > self.laser_shoot_time + self.cooldown_duration:
                self.can_shoot = True
    def update(self , dt):
        keys = pygame.key.get_pressed()

        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction 
 
        self.rect.center += self.speed * self.direction * dt

        # Player input
        recent_key = pygame.key.get_just_pressed()
        if recent_key[pygame.K_SPACE] and self.can_shoot:
            Laser((all_sprites, laser_sptire), laser_surf, self.rect.midtop)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()
        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.speed = 300

    def update(self, dt):
        self.rect.top -= self.speed * dt 
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = randint(350, 450)
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.rotate = randint(0, 365)
        self.rotation_angle = randint(-50, 50)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if self.rect.top > WINDOW_HEIGHT:
            self.kill() 
        
        # Rotation
        self.rotate += self.rotation_angle* dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotate, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, group, frames, pos):
        super().__init__(group)
        self.frames = frames
        self.frame_index = 0
        self.image = frames[0]
        self.rect = self.image.get_frect(center = pos)
    
    def update(self, dt):
        self.frame_index += 15 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

def collision():
    global running
    
    collision_sprite = pygame.sprite.spritecollide(player, meteor_sprite, True, pygame.sprite.collide_mask)
    if collision_sprite:
        print("Game ended")
        running = False
    
    for laser in laser_sptire:
        collided_sprite = pygame.sprite.spritecollide(laser, meteor_sprite, True)
        if collided_sprite:
            AnimatedExplosion(all_sprites, explosion_frames, laser.rect.midtop)
            laser.kill()
            explosion_sound.play()

def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_serf = font.render(str(current_time), True, (180,180,180))
    text_rect = text_serf.get_frect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 20))

    display_surface.blit(text_serf, text_rect)
    pygame.draw.rect(display_surface, (150,150,150), text_rect.inflate(6, 6).move(0, -3), 3, 5)

# General set up
pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
pygame.display.set_caption("My first game")
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
running = True

# Imports
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
explosion_frames = [pygame.image.load(join('images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]
font = pygame.font.Font(join("images", "Oxanium-Bold.ttf"), 20)

laser_sound = pygame.mixer.Sound(join('audio', 'laser.wav'))
laser_sound.set_volume(0.1)
explosion_sound = pygame.mixer.Sound(join('audio', 'explosion.wav'))
explosion_sound.set_volume(0.1)
game_sound = pygame.mixer.Sound(join('audio', 'game_music.wav'))
game_sound.set_volume(0.08)
game_sound.play(-1)

# Sprites
all_sprites = pygame.sprite.Group()
meteor_sprite = pygame.sprite.Group()
laser_sptire = pygame.sprite.Group()

for i in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)

# Custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick(100) / 1000
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor((all_sprites, meteor_sprite), meteor_surf, (x, y))

    # Update
    all_sprites.update(dt)
    collision()

    # Draw the game
    display_surface.fill('#3a2e3f')
    all_sprites.draw(display_surface)
    display_score()

    pygame.display.update()

pygame.quit()