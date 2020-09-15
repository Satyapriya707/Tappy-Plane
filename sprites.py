# Sprite classes for platform game
import pygame as pg
from settings import *
from random import choice, randrange
vec = pg.math.Vector2
from os import path

Dir = path.dirname(__file__)
img_dir = path.join(Dir, 'img')

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.plane_frames = choice(self.plane_frames_all)
        self.image = self.plane_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (30, HEIGHT/2)
        self.pos = vec(30, HEIGHT/2)
        self.vel = 0
        self.acc = 0
        Puff(self.game, self)

    def load_images(self):
        self.plane_frames_all = []
        self.plane_frames = [self.game.spritesheet.get_image(216, 1878, 88, 73),
                             self.game.spritesheet.get_image(372, 1059, 88, 73),
                             self.game.spritesheet.get_image(372, 986, 88, 73)]
        for frame in self.plane_frames:
            frame.set_colorkey(BLACK)
        self.plane_frames_all.append(self.plane_frames)

        self.plane_frames = [self.game.spritesheet.get_image(114, 1639, 88, 73),
                             self.game.spritesheet.get_image(216, 1951, 88, 73),
                             self.game.spritesheet.get_image(222, 1489, 88, 73)]
        for frame in self.plane_frames:
            frame.set_colorkey(BLACK)
        self.plane_frames_all.append(self.plane_frames)

        self.plane_frames = [self.game.spritesheet.get_image(304, 1967, 88, 73),
                             self.game.spritesheet.get_image(330, 1298, 88, 73),
                             self.game.spritesheet.get_image(330, 1225, 88, 73)]
        for frame in self.plane_frames:
            frame.set_colorkey(BLACK)
        self.plane_frames_all.append(self.plane_frames)

##    def jump_cut(self):
##        if self.vel < -12:
##            self.vel = -12

    def jump(self):
        #self.game.jump_sound.play()
        self.vel = -PLAYER_JUMP

    def update(self):
        self.acc = PLAYER_GRAV
        self.animate()
        # equations of motion
        self.vel += self.acc
        self.pos.y += self.vel + 0.5 * self.acc
        self.pos.x += PLAYER_DISP

        self.rect.midbottom = self.pos
        self.mask = pg.mask.from_surface(self.image)

        click = pg.mouse.get_pressed()
        if click[0] == 1:
            self.jump()

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 25:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.plane_frames)
            bottom = self.rect.bottom
            self.image = self.plane_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

class Mob_up(pg.sprite.Sprite):
    def __init__(self, game, midtopx, midtopy, scale):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game        
        self.image = pg.image.load(path.join(img_dir, MOB_UP_IMG)).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        #scale = randrange(90, 101) / 100
        self.scale = scale
        self.image = pg.transform.scale(self.image, (int(self.rect.width * self.scale),
                                                     int(self.rect.height * self.scale)))
        self.rect = self.image.get_rect()
        self.rect.midtop = (midtopx, midtopy)
        self.mask = pg.mask.from_surface(self.image)

class Mob_down(pg.sprite.Sprite):
    def __init__(self, game, midbottomx, midbottomy, scale):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(path.join(img_dir, MOB_DOWN_IMG)).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        #scale = randrange(65, 95) / 100
        self.scale = scale
        self.image = pg.transform.scale(self.image, (int(self.rect.width * self.scale),
                                                     int(self.rect.height * self.scale)))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (midbottomx, midbottomy)
        self.mask = pg.mask.from_surface(self.image)

class Ground(pg.sprite.Sprite):
    def __init__(self, game, x):
        self._layer = GROUND_LAYER
        self.groups = game.all_sprites, game.grounds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(path.join(img_dir, GROUND_IMG)).convert()
        self.image = pg.transform.scale(self.image,(800,70))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = HEIGHT - self.rect.height
        self.mask = pg.mask.from_surface(self.image)


class Cloud(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = CLOUD_LAYER
        self.groups = game.all_sprites, game.clouds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = choice(self.game.cloud_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        scale = randrange(50, 101) / 100
        self.image = pg.transform.scale(self.image, (int(self.rect.width * scale),
                                                     int(self.rect.height * scale)))
        self.rect.x = randrange(WIDTH + 20, WIDTH + 100)
        self.rect.y = randrange(int(HEIGHT*.6))

    def update(self):
        if self.rect.right < 0:
            self.kill()

class Puff(pg.sprite.Sprite):
    def __init__(self, game, player):
        self._layer = PUFF_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.player = player
        self.puff_images = [self.game.spritesheet.get_image(114, 1712, 42, 35),
                       self.game.spritesheet.get_image(196, 1250, 25, 21)]
        for img in self.puff_images:
            img.set_colorkey(BLACK)
        self.image = self.puff_images[0]
        self.rect = self.image.get_rect()
        self.last_update = pg.time.get_ticks()
        self.current_frame = 0
        x = self.player.rect.midleft[0] - 5
        y = self.player.rect.midleft[1]
        self.rect.midright = (x, y)

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.puff_images)
            center = self.rect.center
            self.image = self.puff_images[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.center = center
        x = self.player.rect.midleft[0] - 5
        y = self.player.rect.midleft[1]
        self.rect.midright = (x, y)

class Explosion(pg.sprite.Sprite):
    def __init__(self, game, player):
        self._layer = PUFF_LAYER
        self.groups = game.all_sprites, game.explosions
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.player = player
        self.explosion_anim = []
        for i in range(9):
            filename = 'sonicExplosion0{}.png'.format(i)
            img = pg.image.load(path.join(img_dir, filename)).convert()
            img.set_colorkey(BLACK)
            self.explosion_anim.append(img)
        self.image = self.explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = self.player.rect.center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Pow(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = choice(['boost'])
        self.image = pg.image.load(path.join(img_dir, 'starGold.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (randrange(WIDTH + 20, WIDTH + 100), randrange(HEIGHT * .47, HEIGHT * .53))
        
