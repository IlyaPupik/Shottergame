#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer

window = display.set_mode((900, 700))
display.set_caption("Space Window")
background = transform.scale(image.load('galaxy.jpg'), (900, 700))
clock = time.Clock()
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.1)
lost = 0
score = 0
fire_sound = mixer.Sound('fire.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_width, player_hide):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_hide))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x >= 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x <= 800:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 15, 20)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 700:
            self.rect.y = 0
            self.rect.x = randint(100, 800)
            lost += 1

player = Player('rocket.png', 300, 580, 10, 100, 120)

monsters = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', randint(100, 800), 0, randint(1, 3), 100, 70)
    monsters.add(enemy)
    bullets = sprite.Group()
asteroids = sprite.Group()
for i in range (3):
    asteroid = Enemy('asteroid.png', randint(100, 800), 0, randint(1, 2), 80, 50)
    asteroids.add(asteroid)
life = 3
num_fire = 0
rel_time = False

font.init()
text1 = font.SysFont('Arial', 36)
text2 = font.SysFont('Arial', 70)
win = text2.render('Ты победил!', True, (0, 255, 0))
lose = text2.render('Ты проиграл!', True, (255, 0, 0))
finish = False
game = True
while game == True:
    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)
        score_text = text1.render('Счёт: ' + str(score), True, (0, 255, 0))
        lost_text = text1.render('Пропущено: ' + str(lost), True, (0, 255, 0))
        life_text = text1.render(str(life), True, (255, 0, 0))
        window.blit(life_text, (850, 10))
        window.blit(score_text, (10, 10))
        window.blit(lost_text, (10, 40))
        if rel_time == True:
            new_time = timer()
            if new_time - last_time < 3:
                reoload = text1.render('Идёт перезарядка...', True, (150, 0, 0))
                window.blit(reoload, (350, 650))
            else:
                num_fire = 0
                rel_time = False
        colides = sprite.groupcollide(monsters, bullets, True, True)
        for i in colides:
            score += 1
            enemy = Enemy('ufo.png', randint(100, 800), 0, randint(1, 3), 100, 70)
            monsters.add(enemy)
        if score >= 11:
            window.blit(win, (300, 200))
            finish = True
        if sprite.spritecollide(player, monsters, False) or lost >= 4 or life == 0:
            window.blit(lose, (300, 200))
            finish = True
        if sprite.spritecollide(player, asteroids, False):
            life -= 1
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    player.fire()
                    fire_sound.play()
    display.update()
    clock.tick(60)
