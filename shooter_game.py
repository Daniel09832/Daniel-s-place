from pygame import *
from random import *


window_width = 1500
window_height = 1100
window = display.set_mode((window_width,window_height))
display.set_caption('Шутер')
clock = time.Clock()
background = transform.scale(image.load('galaxy.jpg'), (window_width,window_height))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
clock = time.Clock()
clock_bullet = time.Clock()
FPS = 60
lives = 3
enemies = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
font.init()
Font1 = font.SysFont('Arial', 60)
lost = 0
win = 0
finish = False


class Game_sprite(sprite.Sprite):
    def __init__(self,pic,size_x,size_y,x,y,speed):
        super().__init__()
        self.image = transform.scale(image.load(pic),(size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed 
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(Game_sprite):
    clocker = 0
    shot = 0
    super_puper = 0
    fire = mixer.Sound('fire.ogg')
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < window_width - 145:            
            self.rect.x += self.speed
        if keys[K_SPACE]:
            if self.clocker >= 30 and self.shot < 5 and self.super_puper == 0:
                self.shoot()
                self.clocker = 0
                self.shot += 1
            if self.super_puper == 1 and self.clocker <= 120:
                self.shoot()
                self.clocker += 1        
        if self.shot == 5:
            self.reload()
        self.clocker += 1  
    def shoot(self):
            bullet = Bullet('bullet.png',40,100,self.rect.centerx,self.rect.top,7)
            bullets.add(bullet)
            self.fire.play()
    def reload(self):
        if self.clocker == 180:
            self.clocker = 0
            self.shot = 0
            self.super_puper += 1
        text_reload = Font1.render('Орудия перезаряжаются ждите', 1,(255,0,0)) 
        window.blit(text_reload,(100,1000))  

class Enemy(Game_sprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 1100:
            global lost
            lost += 1
            self.rect.y = -100
            self.rect.x = randint(0,window_width - (self.rect.right - self.rect.x)) 
            self.speed = randint(3,7) 
        
class Aster(Game_sprite):
    def update(self):        
        self.rect.y += self.speed
        if self.rect.y > 1100:
            self.kill()

class Bullet(Game_sprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y == -40:
            self.kill() 


rocket = Player('rocket.png',130,130,140,window_height-140,10)

for i in range(5):
    enemy = Enemy('ufo.png',150,100,randint(0,window_width - 140),-100,randint(2,3))
    enemies.add(enemy)

clocker_asteroid = 0
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if  not finish:
        text_win = Font1.render('Счет:'+ str(win), 1,(255,255,255))
        text_lose = Font1.render('Пропущено:'+ str(lost), 1,(255,255,255))
        window.blit(background,(0,0))
        enemies.draw(window)
        enemies.update()
        bullets.draw(window)
        bullets.update()
        window.blit(text_win,(10,40))
        window.blit(text_lose,(10,81))
        rocket.reset()
        rocket.update()
        clocker_asteroid += 1
        if clocker_asteroid >= 300:
            asteroid = Aster('asteroid.png',150,100,randint(0,window_width - 140),-100,randint(2,3))
            clocker_asteroid = 0
            asteroids.add(asteroid)
        asteroids.draw(window)
        asteroids.update()
        asteroid_list = sprite.spritecollide(rocket,asteroids,True)
        sprites_list = sprite.spritecollide(rocket,enemies,True)
        bullenemies = sprite.groupcollide(enemies, bullets, True,True)
        for bullenemy in bullenemies:
            enemy = Enemy('ufo.png',150,100,randint(0,window_width - 140),-100,randint(2,3))
            enemies.add(enemy)
            win += 1
        if sprites_list or asteroid_list:
            lives-=1
        if lives == 3:
                life_text = Font1.render('3', 1,(0,255,0))
                window.blit(life_text,(1400,50))                
        if lives == 2:
                life_text = Font1.render('2', 1,(255,255,0))
                window.blit(life_text,(1400,50))
        if lives == 1:
                life_text = Font1.render('1', 1,(255,0,0))
                window.blit(life_text,(1400,50))
        if lost >= 3 or lives == 0:
            text_lose = Font1.render('ПРОИГРАЛ!!!!!', 1,(255,0,0))
            finish = True
            window.blit(text_lose,(550,450))
        if win >= 10:
            finish = True
            text_win = Font1.render('Выиграл... ну блин!', 1,(255,255,0))
            window.blit(text_win,(550,450))
    else:
        finish = False
        win = 0
        lost = 0
        lives = 3
        for bullet in bullets:
            bullet.kill()
        for enemy in enemies:
            enemy.kill()  
        time.delay(5000)
        for i in range(5):
            enemy = Enemy('ufo.png',150,100,randint(0,window_width - 140),-100,randint(2,3))
            enemies.add(enemy)
          
    clock.tick(FPS)
    display.update() 
    