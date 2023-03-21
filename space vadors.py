#pyright: strict

import pygame
import random
pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
running = True
pos = pygame.math.Vector2(400,750)
player = pygame.image.load('player.png')
bg = pygame.image.load("su back grondu.png")
bg = pygame.transform.scale(bg,(800,800))
timmer = 0
left = False
right = False
sheild = 3
score = 0

class Missile:
    def __init__(self):
        self.pos = pygame.math.Vector2(-10,-10)
        self.alive = True
    def draw(self):
        pygame.draw.rect(screen,(200,20,1),(self.pos, (3,20)))
    def move(self):
        if self.alive:
            self.pos.y+=10
        else:
            self.pos = pygame.math.Vector2(-10,-10)
        if self.pos.y > 800:
            self.alive = False

missiles: list[Missile] = []
for i in range (10):
    missiles.append(Missile())

class Bullet:
    def __init__(self,x,y):
        self.ppoos = pygame.math.Vector2(x,y)
        self.alive = False
    
    def move(self):
        if self.alive == True:
            self.ppoos.y -= 10
        else:
            self.ppoos.y = pos.y
            self.ppoos.x = pos.x 
        if self.ppoos.y < 0:
            self.alive = False
        
    def draw(self):
        pygame.draw.rect(screen,(200,200,1),(self.ppoos, (3,20)))

class Wall:
    def __init__(self,pos:pygame.math.Vector2):
        self.pos:pygame.math.Vector2 = pygame.math.Vector2(pos)
        self.hp = 0
        self.alive = True
        
    def draw(self):
        if self.hp == 1:
            pygame.draw.rect(screen, (20,250,250), (self.pos.x, self.pos.y, 30,30))
        elif self.hp == 2:
            pygame.draw.rect(screen, (20,150,150), (self.pos.x, self.pos.y, 30,30))
        else:
            pygame.draw.rect(screen, (20,50,50), (self.pos.x, self.pos.y, 30,30))

    def collide(self):
        if self.alive:
            if bullet.ppoos.x > self.pos.x:
                if bullet.ppoos.x < self.pos.x + 30:
                    if bullet.ppoos.y < self.pos.y + 30:
                        if bullet.ppoos.y > self.pos.y:
                            bullet.alive = False
                            self.hp += 1

class Allem:
    def __init__(self,pos:pygame.math.Vector2):
        self.pos = pos
        self.alive = True
        self.alin = pygame.image.load('alin.png')
        self.direcon = 1
    def draw(self):
        screen.blit(self.alin,(self.pos))
    def move(self,timmer: int):
        if timmer %  800 == 0:
            self.pos.y += 100
            self.direcon *= (1-2)
            return 0
        if timmer% 75== 0:
            self.pos.x += 25 * self.direcon
    
    def collide(self,pos):
        if self.alive:
            if bullet.ppoos.x > self.pos.x:
                if bullet.ppoos.x < self.pos.x + 40:
                    if bullet.ppoos.y < self.pos.y + 40:
                        if bullet.ppoos.y > self.pos.y:
                            bullet.alive = False
                            self.alive = False
                            global score
                            score += 1

bullet = Bullet(pos.x,pos.y)

vx = 0
anemyList: list[Allem] = []
for i in range (4):
    for j in range (12):
        anemyList.append(Allem(pygame.math.Vector2(j*60+60,i*50+50)))
wolllist: list[Wall] = []
for k in range (4):
    for i in range (2):
        for j in range (3):
            wolllist.append(Wall((j*30+200*k+50, i*30+650)))

while running:
    clock.tick(60)
    timmer += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bullet.alive == False:
                bullet.alive = True
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_d:
                right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False
    
    if left:
        vx = -3
    elif right:
        vx = 3
    else:
        vx= 0

    pos.x += vx

    rando = random.randrange(0,50)
    rando *= len(anemyList)
    if rando < 2:
        rando = random.randrange(0,len(anemyList))
        if anemyList[rando].alive == True:
            for rocket in missiles:
                if rocket.alive == False:
                    rocket.alive = True
                    rocket.pos = anemyList[rando].pos
                    break
    bullet.move()
    if bullet.alive == True:
        for alliin in anemyList:
            alliin.collide(bullet.ppoos)

            
    screen.blit(bg,(0,0))
    
    for allien in anemyList:
        allien.move(timmer)
        if allien.alive == True:
            allien.draw()
        if allien.pos.y >700:
            allien.alive = False

    temp = 0
    for enemy in anemyList:
        if enemy.alive == False:
            temp += 1
        if temp == len(anemyList):
            running = False
            print("you won!")
            print("you killed",score,"aliens") 

    for missile in missiles:
        if missile.alive:
            for wall in wolllist:
                if missile.pos.x > wall.pos.x:
                    if missile.pos.x < wall.pos.x + 30:
                        if missile.pos.y < wall.pos.y + 30:
                            if missile.pos.y > wall.pos.y:  
                                wall.hp +=1
                                missile.alive = False  
        if missile.pos.x > pos.x:
            if missile.pos.x < pos.x + 30:
                if missile.pos.y < pos.y + 30:
                    if missile.pos.y > pos.y:      
                        sheild -= 1
                        print('you were hit! ', sheild, " sheilds left")
                        missile.alive = False 
    if sheild < 1:
        print("you lose!")
        running = False
        print("you killed",score,"aliens")

    if bullet.alive == True:
        bullet.draw()
    for wall in wolllist:
        if wall.hp > 2:
            wall.alive = False
        if wall.alive:
            wall.draw()
    for wall in wolllist:
        if wall.alive:
            wall.collide()
    for rocket in missiles:
        rocket.move()
        if rocket.alive == True:
            rocket.draw()

    screen.blit(player,(pos))

    
    pygame.display.flip()

pygame.quit()