#Создай собственный Шутер!

from pygame import *
from random import *
from time import time as timer

bullets = sprite.Group()
lastFire = timer()
firet = timer()
fireCooldown = 0.3     
cooldown = 0
recharge = 1

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Gamer(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_SPACE]:
            self.fireS()
            
    def fireS(self):
        global lastFire
        firet = timer()
        if firet - lastFire >= fireCooldown :
            lastFire = firet
            bullets.add(Bullet('bullet.png', self.rect.centerx - 7, self.rect.top, 15, 25, 4))
            fire.play()
class Asteroids(GameSprite):
    direction = 'down'
    def update(self):
        global lost
        global killed 
        global finish
        global finish_lose

        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

        if len(sprite.groupcollide(gg, asteroids, False, False)) > 0 or lost >= 3:
            finish = True
            finish_lose = True
            
class Enemy(GameSprite):
    direction = 'down'
    def update(self):
        global lost
        global killed 
        global finish
        global finish_lose
        global finish_win

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
        if self.direction == 'down':
            self.rect.y += self.speed
        else:
            self.rect.y += self.speed
        sprites_list = sprite.groupcollide(
            monsters, bullets, False, True
        )
        if len(sprites_list) != 0:
            killed += len(sprites_list)
            if killed >= 10:
                finish = True
                finish_win = True
            for i in sprites_list:
                i.rect.x = randint(80, win_width - 80)
                i.rect.y = 0 
        gg = sprite.Group()
        gg.add(gamer)
           
        if len(sprite.groupcollide(gg, monsters, False, False)) > 0 or lost >= 3:
            finish = True
            finish_lose = True

class Bullet(GameSprite):
    direction = 'up'
    #self.image = transform.scale(image.load("bullet.png"), (65, 65))
    def update(self): 
        self.rect.y -= self.speed

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire = mixer.Sound('fire.ogg')

x1 = 400
y1 = 300
x2 = 300
y2 = 300

monsters = sprite.Group()
monsters.add(Enemy("ufo.png", 100, 20, 65, 65, 3))
monsters.add(Enemy("ufo.png", 160, 20, 65, 65, 1))
monsters.add(Enemy("ufo.png", 310, 20, 65, 65, 2))
monsters.add(Enemy("ufo.png", 360, 20, 65, 65, 3))
monsters.add(Enemy("ufo.png", 470, 20, 65, 65, 2))

# asteroids = sprite.Group()
# asteroids.add(Asteroids('asteroid.png', 150, 0, 80, 50, 4))
# asteroids.add(Asteroids('asteroid.png', 370, 0, 80, 50, 3))

# gg = sprite.Group()
# gg.add(rocket)

lost = 0
killed = 0

font.init()
font1 = font.Font(None, 36)

#ufo = Enemy("ufo.png", win_width - 80, 280, 2)

gamer = Gamer("rocket.png", 5, win_height - 80, 65, 65, 5)

clock = time.Clock()

FPS = 60

font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))

game = True
finish = False
finish_lose = False
finish_win = False

while game:
    clock.tick(FPS)
    if finish != True:
        text_lose = font1.render('Пропущено: ' + str(lost), 10, (255, 255, 255))
        text_win = font1.render('Счёт: ' + str(killed), 10, (255, 255, 255))
        window.blit(background,(0, 0))
        window.blit(text_lose,(10, 10))
        window.blit(text_win, (10, 40))
        # rocket.update()
        # rocket.reset()
        gamer.update()
        monsters.update()
        # asteroids.draw(window)
        # asteroids.update()
        bullets.draw(window)
        bullets.update()

        gamer.reset()
        monsters.draw(window)
    
    elif finish_lose:
        window.blit(lose, (250, 250))
    elif finish_win:
        window.blit(win, (250, 250))

    for e in event.get():
        if e.type == QUIT:
            game = False
    
    display.update()
    
    

