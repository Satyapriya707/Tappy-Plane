# Intro Music -> https://soundcloud.com/alexandr-zhelanov
# 'Happy Tune' -> http://opengameart.org/users/syncopika
# Game Over Music -> https://opengameart.org/users/kistol
# Art from Kenney.nl

import pygame as pg
import random
from settings import *
from sprites import *
from os import path
import sys

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # load high score
        if getattr(sys, 'frozen', False):
            self.dir = path.dirname(sys.executable)
        else:
            self.dir = path.dirname(__file__)
        with open(HS_FILE, 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
            f.close()
        # load spritesheet image
        self.img_dir = path.join(self.dir, 'img')
        self.spritesheet = Spritesheet(path.join(self.img_dir, SPRITESHEET[0]))
        # background image
        self.bg_img = pg.image.load(path.join(self.img_dir, 'background.png')).convert()
        self.bg_img = pg.transform.scale(self.bg_img, (800,600))
        # intro image
        self.intro_img = pg.image.load(path.join(self.img_dir, 'textGetReady.png')).convert()
        self.intro_rect = self.intro_img.get_rect()
        self.intro_img = pg.transform.scale(self.intro_img, (int(self.intro_rect.width * .75), int(self.intro_rect.height * .75)))
        self.intro_img.set_colorkey(BLACK)
        # game over image 
        self.go_img = pg.image.load(path.join(self.img_dir, 'textGameOver.png')).convert()
        self.go_img.set_colorkey(BLACK)
        # numbers
        self.numbers = []
        for num in NUMBERS:
            img = self.spritesheet.get_image(*num)
            img.set_colorkey(BLACK)
            self.numbers.append(img)
        # cloud images
        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(pg.image.load(path.join(self.img_dir, 'cloud{}.png'.format(i))).convert())
        # load sounds
        self.snd_dir = path.join(self.dir, 'snd')
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Boost.wav'))
        self.exp_sound = pg.mixer.Sound(path.join(self.snd_dir, 'explosion.wav'))

    def new(self):
        # start a new game
        self.score = 0
        self.exp = 0
        self.count = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.counted_mobs = pg.sprite.Group()
        self.grounds = pg.sprite.Group()
        self.explosions = pg.sprite.Group()
        self.player = Player(self)
        for mob in MOB_UP_LIST:            
            Mob_up(self, *mob, random.randrange(90, 101)/100)
        for mob in MOB_DOWN_LIST:
            Mob_down(self, *mob, random.randrange(65, 95)/100)
        Ground(self, 0)
        self.mob_timer = 0
        for i in range(8):
            c = Cloud(self)
            c.rect.x -= 500
        pg.mixer.music.load(path.join(self.snd_dir, 'Happy Tune.ogg'))
        self.run()

    def run(self):
        # Game Loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

        # spawn a mob
        if len(self.mobs) < 8:
            scale1 = random.randrange(70,131)/100
            diff = random.randrange(120,150)
            scale2 = (HEIGHT - diff - 239*scale1)/239
            Mob_up(self, randrange(WIDTH + 185, WIDTH + 200), 0, scale1)
            Mob_down(self, randrange(WIDTH + 185, WIDTH + 200), HEIGHT, scale2)
            if randrange(100) < POW_SPAWN_PCT:
                Pow(self)

        # hit mobs or ground?
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        if mob_hits:
            if self.count == 0:
                self.exp = Explosion(self, self.player)
                self.exp_sound.play()
                self.exp_sound.fadeout(1000)
                self.player.pos.y = HEIGHT + 1000
                self.player.pos.x = WIDTH - 1000
            self.count += 1
            if not self.exp.alive():
                self.playing = False

        ground_hits = pg.sprite.spritecollide(self.player, self.grounds, False, pg.sprite.collide_mask)
        if ground_hits:
            if self.count == 0:
                self.exp = Explosion(self, self.player)
                self.exp_sound.play()
                self.exp_sound.fadeout(1000)
                self.player.pos.y = HEIGHT + 1000
                self.player.pos.x = WIDTH - 1000
            self.count += 1
            if not self.exp.alive():
                self.playing = False

        # score
        for mob in self.mobs:
            if mob.rect.left + 70 < self.player.rect.left:
                if not self.counted_mobs.has(mob):
                    self.counted_mobs.add(mob)
                    self.score += 1

        # if player reaches a certain part of screen
        if self.player.rect.right > int(WIDTH*.4) or self.explosions.has(self.exp):
            if random.randrange(100) < 5:
                Cloud(self)
            for cloud in self.clouds:
                cloud.rect.x -= int(PLAYER_DISP/2)
            self.player.pos.x -= PLAYER_DISP
            for mob in self.mobs:
                mob.rect.x -= PLAYER_DISP
                if mob.rect.x + mob.rect.width < 0:
                    mob.kill()
            for gr in self.grounds:
                gr.rect.x -= PLAYER_DISP
                if gr.rect.right < 0:
                    gr.kill()
            for pw in self.powerups:
                pw.rect.x -= PLAYER_DISP
                if pw.rect.right < 0:
                    pw.kill()
            for exp in self.explosions:
                exp.rect.centerx -= PLAYER_DISP

        # if player hits powerup
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for Pow1 in pow_hits:
            if Pow1.type == 'boost':
                self.boost_sound.play()
                self.score += BOOST_POWER

        # Die!
        if self.player.rect.bottom > HEIGHT or self.player.rect.top < 0:
            if self.count == 0:
                self.exp = Explosion(self, self.player)
                self.exp_sound.play()
                self.exp_sound.fadeout(1000)
                self.player.pos.y = HEIGHT + 1000
                self.player.pos.x = WIDTH - 1000
            self.count += 1
            if not self.exp.alive():
                self.playing = False

        # spawn new platforms to keep same average number
        if len(self.grounds)<2:
            for g in self.grounds:
                Ground(self, g.rect.right)

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.bg_img, (0,0))
        self.all_sprites.draw(self.screen)
        scr = str(self.score)
        wid = 0
        for i in range(len(scr)):
            self.screen.blit(self.numbers[int(scr[i])], (int(WIDTH / 2) + wid + 2*i - 10, 15))
            rect = self.numbers[int(scr[i])].get_rect()
            wid += rect.width
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pg.mixer.music.load(path.join(self.snd_dir, 'Intro.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.bg_img, (0,0))

        self.button = pg.image.load(path.join(self.img_dir, 'buttonLarge.png')).convert()
        self.button.set_colorkey(BLACK)
        self.int_rect = self.intro_img.get_rect()
        self.button = pg.transform.scale(self.button, (self.int_rect.width + 20, self.int_rect.height + 30))
        self.screen.blit(self.button, (WIDTH * .32 -10,HEIGHT * .3 -15))
        self.screen.blit(self.intro_img, (WIDTH * .32,HEIGHT * .3))

        self.plane = pg.image.load(path.join(self.img_dir, 'planeRed1.png')).convert()
        self.plane.set_colorkey(BLACK)
        self.screen.blit(self.plane, (WIDTH * .40,HEIGHT * .5))

        self.tap = pg.image.load(path.join(self.img_dir, 'tapTick.png')).convert()
        self.tap.set_colorkey(BLACK)
        self.screen.blit(self.tap, (WIDTH * .55,HEIGHT * .5))
        
        self.draw_text(TITLE, 80, GOLDEN, WIDTH / 2, HEIGHT * .05)
        self.draw_text("Click the right mouse button to jump", 22, BLACK, WIDTH / 2, HEIGHT * .7)
        self.draw_text("Click the right mouse button to play", 22, BLACK, WIDTH / 2, HEIGHT * .8)
        self.draw_text("High Score: " + str(self.highscore), 22, BLACK, WIDTH / 2, HEIGHT * .9)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        pg.mixer.music.load(path.join(self.snd_dir, 'Game Over.ogg'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.bg_img, (0,0))
        
        self.go_rect = self.go_img.get_rect()
        self.button = pg.transform.scale(self.button, (self.go_rect.width + 40, self.go_rect.height + 30))
        self.screen.blit(self.button, (WIDTH * .25 - 20, HEIGHT * .1 - 15))
        self.screen.blit(self.go_img, (WIDTH * .25, HEIGHT * .1))

        self.gold = pg.image.load(path.join(self.img_dir, 'medalGold.png')).convert()
        self.gold.set_colorkey(BLACK)
        self.silver = pg.image.load(path.join(self.img_dir, 'medalSilver.png')).convert()
        self.silver.set_colorkey(BLACK)
        self.bronze = pg.image.load(path.join(self.img_dir, 'medalBronze.png')).convert()
        self.bronze.set_colorkey(BLACK)
        if 25 > self.score:
            self.draw_text("NO MEDAL !", 50, SPL_RED, WIDTH * .50, HEIGHT * .4)
            self.draw_text("SCORE AT LEAST 25 TO EARN A MEDAL", 30, SPL_RED, WIDTH * .5, HEIGHT * .55)
        if 50 > self.score >= 25:
            self.screen.blit(self.bronze, (WIDTH * .43, HEIGHT * .37))
            self.draw_text("BRONZE", 30, BRONZE_CLR, WIDTH * .5, HEIGHT * .57)
        if 100 > self.score >= 50:
            self.screen.blit(self.silver, (WIDTH * .43, HEIGHT * .37))
            self.draw_text("SILVER", 30, SILVER_CLR, WIDTH * .5, HEIGHT * .57)
        if self.score >= 100:
            self.screen.blit(self.gold, (WIDTH * .43, HEIGHT * .37))
            self.draw_text("GOLD", 30, GOLDEN, WIDTH * .5, HEIGHT * .57)

        self.draw_text("Score: " + str(self.score), 30, BLACK, WIDTH / 2, HEIGHT * .7)
        self.draw_text("Click the right mouse button to play again", 30, BLACK, WIDTH / 2, HEIGHT * .85)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE !", 30, BLACK, WIDTH / 2, HEIGHT * .7 + 40)
            with open(HS_FILE, 'w') as f:
                f.write(str(self.score))
                f.close()
        else:
            self.draw_text("High Score: " + str(self.highscore), 30, BLACK, WIDTH / 2, HEIGHT * .7 + 40)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

        

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            click = pg.mouse.get_pressed()
            if click[0] == 1:
                waiting = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()

while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
