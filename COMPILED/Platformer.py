import pygame
from pygame_functions import *
#import mysql.connector as db

screenSize(852,384)

class game() :

    def __init__(self) :
        pygame.init()
        self.running = True
        self.playing = False
        self.score_screen = False
        self.level_end = False
        self.game_ovr = False
        self.START = False
        self.BACK = False
        self.DOWN = False
        self.UP = False
        self.RIGHT = False
        self.LEFT = False
        self.width = 852
        self.height = 384
        self.display = pygame.Surface((self.width, self.height))
        self.window = pygame.display.set_mode(((self.width, self.height)))
        self.font_name = "8-BIT WONDER.TTF"
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.current_menu = MainMenu(self)
        self.score = 0
        
    def game_loop(self) :
        while self.playing :
            self.check_events()
            if self.START :
                self.playing = False
            win = self.window
            dis = self.display
            def platformer():
                walkright = [pygame.image.load('Animations/R%s.png' % frame) for frame in range(1, 10)]
                walkleft = [pygame.image.load('Animations/L%s.png' % frame) for frame in range(1, 10)]
                bg = pygame.image.load('background_1.png')
                char = pygame.image.load('Animations/standing.png')
                pause_screenimg = pygame.image.load("pause1.png")
                ps1 = pygame.transform.scale(pause_screenimg, (782, 332))
                spikes_1 = pygame.image.load('Tiles/spikes1.png')
                spikes_2 = pygame.image.load('Tiles/spikes2.png')
                spikes_3 = pygame.image.load('Tiles/spikes3.png')
                signboard = pygame.image.load('Tiles/sign.png')
                floorl = [pygame.image.load('Tiles/floor%s.png' % i) for i in range(1,9)]
                flag = pygame.image.load('Tiles/Flag.png')
                end = pygame.image.load('Tiles/end.png')
                clock = pygame.time.Clock()

                sc_wdth = 852
                shotcount = 4
                scene = 1

                class player() :
                   
                    def __init__(self, x, y, width, height) :
                        self.x = x
                        self.y = y
                        self.width = width
                        self.height = height
                        self.vel = 5
                        self.isjump = False
                        self.jumpcount = 6
                        self.left = False
                        self.right = True
                        self.walkcount = 0
                        self.standing = True
                        self.hitbox = (self.x + 18, self.y + 10, 27, 50)
                        self.damage = 3
                        self.shootspeed = 12
                        self.health = 3
                        self.onground = True
                        self.falling = False
                        
                    def draw(self, win) :     
                        if self.walkcount + 1 >= 27 :
                            self.walkcount = 0
                        
                        if not (self.standing) :
                            if self.left :
                                win.blit(walkleft[self.walkcount//3], (self.x, self.y))
                                self.walkcount += 1
                            elif self.right :
                                win.blit(walkright[self.walkcount//3], (self.x, self.y))
                                self.walkcount += 1
                        else:
                            if self.right :
                                win.blit(walkright[0], (self.x, self.y))
                            else :
                                win.blit(walkleft[0], (self.x, self.y))

                        self.hitbox = (self.x + 18, self.y + 10, 27, 50)
                ##        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

                    def hit(self) :
                        self.walkcount = 0
                        self.health -= 1
                        hitloop = 1
                        

                class enemy(object) :

                    walkright = [pygame.image.load('Animations/R%sE.png' % frame) for frame in range(1, 12)]
                    walkleft = [pygame.image.load('Animations/L%sE.png' % frame) for frame in range(1, 12)]
                    
                    def __init__(self, x, y, width, height, end) :
                        self.x = x
                        self.y = y
                        self.width = width
                        self.height = height
                        self.end = end
                        self.path = [self.x, self.end]
                        self.vel = 4
                        self.walkcount = 0
                        self.hitbox = (self.x + 17, self.y, 28, 60)
                        self.health = 12
                        self.visible = True

                    def draw(self, win) :
                        self.move()
                        if self.visible :
                            if self.walkcount + 1 >= 24 :
                                self.walkcount = 0

                            if self.vel > 0 :
                                win.blit(self.walkright[self.walkcount//3],[self.x, self.y])
                                self.walkcount += 1
                            else :
                                win.blit(self.walkleft[self.walkcount//3],[self.x, self.y])
                                self.walkcount += 1
                            self.hitbox = (self.x + 17, self.y, 28, 60)
                            if self.health != 12 :
                                pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0] - 6, self.hitbox[1] - 10, 40, 10))
                                pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0] - 6, self.hitbox[1] - 10, 40 - (40//(12//p1.damage))*((12 - self.health)//p1.damage)+1, 10))  
                ##            pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

                    def move(self) :
                        if self.vel > 0 :
                            if self.x + self.vel < self.path[1]:
                                self.x += self.vel
                            else :
                                self.vel *= -1
                                self.walkcount = 0
                        else :
                            if self.x - self.vel > self.path[0]:
                                self.x += self.vel
                            else :
                                self.vel *= -1
                                self.walkcount = 0
                    def hit(self) :
                        if self.health > 3:
                            self.health -= p1.damage
                        else :
                            self.health -= p1.damage
                            self.visible = False
                        
                class projectile() :

                    fbanimlist = [pygame.image.load('Animations/FB%s.png' % frame) for frame in range(1, 10)]
                    fbanimlistr = []
                    fbanimlistl = []
                    for i in range (9) :
                        x = pygame.transform.scale(fbanimlist[i], (56,28))
                        y = pygame.transform.rotate(x, 180)
                        fbanimlistr.append(x)
                        fbanimlistl.append(y)
                    
                    def __init__(self, x, y, facing) :
                        self.x = x
                        self.y = y - 15
                        self.hitbox = (self.x + 2, self.y, 20, 24)
                        self.facing = facing
                        self.vel = 16 * facing
                        self.animcount = 0

                    def draw(self, win) :

                        self.hitbox = (self.x + 32, self.y, 20, 24)
                        if self.animcount == 27 :
                            self.animcount = 0
                        if self.facing < 0 :
                            win.blit(self.fbanimlistl[self.animcount//3],[self.x, self.y])
                        elif self.facing > 0 :
                            win.blit(self.fbanimlistr[self.animcount//3],[self.x, self.y])
                        self.animcount += 1
                
                class coin(object) :

                    animlist = [pygame.image.load('Animations/coin %s.png' % frame) for frame in range(1, 10)]
                    animlist2 = []
                    for i in range (9) :
                        x = pygame.transform.scale(animlist[i], (24,24))
                        animlist2.append(x)
                                                   
                    def __init__(self, x, y, width, height) :
                        self.x = x
                        self.y = y
                        self.width = width
                        self.height = height
                        self.hitbox = (self.x + 2, self.y, 20, 24)
                        self.animcount = 0
                        self.points = 1
                        self.visible = True
                    def draw(self, win) :
                        if self.visible :
                            if self.animcount == 27 :
                                self.animcount = 0
                ##            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1], self.hitbox[2], self.hitbox[3]))
                            win.blit(self.animlist2[self.animcount//3],[self.x, self.y])
                            self.animcount += 1
                    def hit(self) :
                        self.visible = False

                class rcoin(object) :

                    ranimlist = [pygame.image.load('Animations/rcoin %s.png' % frame) for frame in range(1, 10)]
                    ranimlist2 = []
                    for i in range (9) :
                        x = pygame.transform.scale(ranimlist[i], (24,24))
                        ranimlist2.append(x)
                                                   
                    def __init__(self, x, y, width, height) :
                        self.x = x
                        self.y = y
                        self.width = width
                        self.height = height
                        self.hitbox = (self.x + 2, self.y, 20, 24)
                        self.animcount = 0
                        self.points = 5
                        self.visible = True
                    def draw(self, win) :
                        if self.visible :
                            if self.animcount == 27 :
                                self.animcount = 0
                ##            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1], self.hitbox[2], self.hitbox[3]))
                            win.blit(self.ranimlist2[self.animcount//3],[self.x, self.y])
                            self.animcount += 1
                    def hit(self) :
                        self.visible = False
                                    
                class floor1(object) :

                    def __init__(self, x, y) :
                        self.x = x
                        self.y = y
                        self.width = 352
                        self.height = 96
                        self.hitbox = (self.x, self.y, self.width, self.height)
                    def draw(self,win) :
                        floor1 = pygame.transform.scale(floorl[0], (356, 96))
                ##        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1], self.hitbox[2], self.hitbox[3]))
                        win.blit(floor1, (self.x, self.y))

                class floor2(object) :

                    def __init__(self, x, y) :
                        self.x = x
                        self.y = y
                        self.width = 288
                        self.height = 32
                        self.hitbox = (self.x, self.y, self.width, self.height)
                    def draw(self,win) :
                        floor2 = pygame.transform.scale(floorl[1], (288, 32))
                ##        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1], self.hitbox[2], self.hitbox[3]))
                        win.blit(floor2, (self.x, self.y))

                class floor3(object) :

                    def __init__(self, x, y) :
                        self.x = x
                        self.y = y
                        self.width = 32
                        self.height = 32
                        self.hitbox = (self.x, self.y, self.width, self.height)
                    def draw(self,win) :
                        floor3 = pygame.transform.scale(floorl[2], (32, 32))
                ##        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1], self.hitbox[2], self.hitbox[3]))
                        win.blit(floor3, (self.x, self.y))
                        
                class floor4(object) :

                    def __init__(self, x, y) :
                        self.x = x
                        self.y = y
                        self.width = 288
                        self.height = 128
                        self.hitbox = (self.x, self.y, self.width, self.height)
                    def draw(self,win) :
                        floor4 = pygame.transform.scale(floorl[3], (288, 128))
                ##        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1], self.hitbox[2], self.hitbox[3]))
                        win.blit(floor4, (self.x, self.y))

                class floor5(object) :

                    def __init__(self, x, y) :
                        self.x = x
                        self.y = y
                        self.width = 224
                        self.height = 128
                        self.hitbox = (self.x, self.y, self.width, self.height)
                    def draw(self,win) :
                        floor5 = pygame.transform.scale(floorl[4], (224, 128))
                ##        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1], self.hitbox[2], self.hitbox[3]))
                        win.blit(floor5, (self.x, self.y))

                class floor6(object) :

                    def __init__(self, x, y) :
                        self.x = x
                        self.y = y
                        self.width = 320
                        self.height = 96
                        self.hitbox = (self.x, self.y, self.width, self.height)
                    def draw(self,win) :
                        floor6 = pygame.transform.scale(floorl[5], (320, 96))
                ##        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1], self.hitbox[2], self.hitbox[3]))
                        win.blit(floor6, (self.x, self.y))

                class floor7(object) :

                    def __init__(self, x, y) :
                        self.x = x
                        self.y = y
                        self.width = 160
                        self.height = 32
                        self.hitbox = (self.x, self.y, self.width, self.height)
                    def draw(self,win) :
                        floor7 = pygame.transform.scale(floorl[6], (160, 32))
                ##        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1], self.hitbox[2], self.hitbox[3]))
                        win.blit(floor7, (self.x, self.y))

                class floor8(object) :

                    def __init__(self, x, y) :
                        self.x = x
                        self.y = y
                        self.width = 852
                        self.height = 96
                        self.hitbox = (self.x, self.y, self.width, self.height)
                    def draw(self,win) :
                        floor8 = pygame.transform.scale(floorl[7], (852, 96))
                ##        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1], self.hitbox[2], self.hitbox[3]))
                        win.blit(floor8, (self.x, self.y))
                        
                class spikes1(object) :
                    def __init__(self, x, y) :
                        self.x = x
                        self.y = y
                        self.width = 160
                        self.height = 32
                        self.hitbox = (self.x, self.y, self.width, self.height)
                    def draw(self,win) :
                        spikes1 = pygame.transform.scale(spikes_1, (160,32))
                ##        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1], self.hitbox[2], self.hitbox[3]))
                        win.blit(spikes1, (self.x, self.y))

                class spikes2(object) :
                    def __init__(self, x, y) :
                        self.x = x
                        self.y = y
                        self.width = 224
                        self.height = 32
                        self.hitbox = (self.x, self.y, self.width, self.height)
                    def draw(self,win) :
                        spikes2 = pygame.transform.scale(spikes_2, (224, 32))
                ##        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1], self.hitbox[2], self.hitbox[3]))
                        win.blit(spikes2, (self.x, self.y))

                class spikes3(object) :
                    def __init__(self, x, y) :
                        self.x = x
                        self.y = y
                        self.width = 64
                        self.height = 32
                        self.hitbox = (self.x, self.y, self.width, self.height)
                    def draw(self,win) :
                        spikes3 = pygame.transform.scale(spikes_3, (64, 32))
                ##        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1], self.hitbox[2], self.hitbox[3]))
                        win.blit(spikes3, (self.x, self.y))

                class sign(object) :
                    def __init__(self, x, y) :
                        self.x = x
                        self.y = y
                        self.width = 32
                        self.height = 32
                        self.hitbox = (self.x, self.y, self.width, self.height)
                    def draw(self,win) :
                        signb = pygame.transform.scale(signboard, (32, 32))
                ##        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1], self.hitbox[2], self.hitbox[3]))
                        win.blit(signb, (self.x, self.y))

                def redraw():
                    bg1 = pygame.transform.scale(bg, (852,384))
                    dis.blit(bg1, (0,0))
                    self.draw_text_black("Score " + str(self.score), 20, 770, 20)
                    self.draw_text_black("Health " + str(p1.health), 20, 90, 20)
                    win.blit(dis, (0, 0))    
                    if scene == 3 :
                        f1 = pygame.transform.scale(flag, (110, 220))
                        endsign = pygame.transform.scale(end, (32, 32))
                        win.blit(endsign, (790, 258))
                        win.blit(f1, (660, 70))
                    if scene == 1 :
                        sg1 = sign(240, 260)
                        sg1.draw(win)
                        if collisionchk(p1.hitbox[0], p1.hitbox[1], p1.hitbox[2], p1.hitbox[3], 240, 260, 32, 32) :
                            controlimg = pygame.image.load("tiles/controls.png")
                            controlimg1 = pygame.transform.scale(controlimg, (357, 123))
                            win.blit(controlimg1, (40, 40))
                            self.drawcontrols("Move", 10, 100, 80)
                            self.drawcontrols("Jump", 10, 155, 80)
                            self.drawcontrols("Shoot", 10, 240, 80)
                            self.drawcontrols("Sprint", 10, 335, 80)
                    
                    p1.draw(win)
                    for i in Enemies :
                        i.draw(win)
                    for i in Platforms :
                        i.draw(win)
                    for i in Spikes :
                        i.draw(win)
                    for i in Coins :
                        i.draw(win)
                    for bullet in bullets :
                        bullet.draw(win) 
                    pygame.display.update()

                def collisionchk(x1, y1, x2, y2, x3, y3, x4, y4) :
                    if y1 < y3 + y4 and y1 + y2 > y3:
                                if x1 + x2 > x3 and x1 < x3 + x4:
                                    return True
                    return False
                                    

                sfont = pygame.font.SysFont("comicsans",30, True)
                bullets=[]
                shootloop = 0
                hitloop = 0
                safetime = 0

                #Level Design

                p1 = player(20, 200, 64, 64)
                Enemies = []
                Platforms = []
                Spikes = []
                Coins = []

                def scene1(Enemies, Platforms, Spikes, Coins, tcheck) :
                    if tcheck != 0 :
                        return
                    en = enemy(532, 231, 64, 64, 720)
                    s1 = spikes1(352,320)
                    plat1 = floor1(0, 288)
                    plat2 = floor2(288, 352)
                    plat3 = floor3(416, 256)
                    plat4 = floor1(512, 288)
                    plat5 = floor4(768, 256)
                    coin1 = coin(420, 146 , 16, 16)
                    coin2 = coin(558, 166 , 16, 16)
                    coin3 = coin(578, 166 , 16, 16)
                    coin4 = coin(598, 166 , 16, 16)
                    coin5 = coin(618, 166 , 16, 16)
                    coin6 = coin(638, 166 , 16, 16)
                    coin7 = coin(658, 166 , 16, 16)
                    nEnemies = [en]
                    nPlatforms = [plat3, plat2, plat1, plat4, plat5]
                    nSpikes = [s1]
                    nCoins = [coin1, coin2, coin3, coin4, coin5, coin6, coin7]
                    return [nEnemies, nPlatforms, nSpikes, nCoins]

                def scene2(Enemies, Plaforms, Spikes, Coins, tcheck) :
                    if tcheck != 0 :
                        return
                    en = enemy(448, 199, 64, 64, 576)
                    s1 = spikes2(204, 320)
                    s2 = spikes3(652, 320)
                    plat1 = floor4(-86, 256)
                    plat2 = floor2(172, 352)
                    plat3 = floor3(268, 256)
                    plat4 = floor3(332, 256)
                    plat5 = floor5(428, 256)
                    plat6 = floor2(588, 351)
                    plat7 = floor6(716, 288)
                    plat8 = floor7(748, 192)
                    coin1 = coin(20, 146 , 16, 16)
                    coin2 = coin(45, 146 , 16, 16)
                    coin3 = coin(70, 146 , 16, 16)
                    coin4 = coin(95, 146 , 16, 16)
                    coin5 = coin(120, 146 , 16, 16)
                    coin6 = coin(145, 146 , 16, 16)
                    coin7 = coin(170, 146 , 16, 16)
                    coin8 = coin(272, 146 , 16, 16)
                    coin9 = coin(336, 146 , 16, 16)
                    coin10 = coin(443, 146 , 16, 16)
                    coin11 = coin(468, 146 , 16, 16)
                    coin12 = coin(493, 146 , 16, 16)
                    coin13 = coin(518, 146 , 16, 16)
                    coin14 = coin(543, 146 , 16, 16)
                    coin15 = coin(568, 146 , 16, 16)
                    coin16 = coin(593, 146 , 16, 16)
                    coin17 = coin(618, 146 , 16, 16)
                    coin18 = coin(760, 86 , 16, 16)
                    coin19 = coin(785, 86 , 16, 16)
                    coin20 = coin(810, 86 , 16, 16)
                    nEnemies = [en]
                    nPlatforms = [plat2, plat6, plat1, plat3 , plat4, plat5, plat7, plat8]
                    nSpikes = [s1, s2]
                    nCoins = [coin1, coin2, coin3, coin4, coin5, coin6, coin7, coin8, coin9, coin10, coin11, coin12, coin13, coin14, coin15, coin16, coin17, coin18, coin19, coin20]
                    return [nEnemies, nPlatforms, nSpikes, nCoins]

                def scene3(Enemies, Plaforms, Spikes, Coins, tcheck) :
                    if tcheck != 0 :
                        return
                    en = enemy(448, 234, 64, 64, 576)
                    plat1 = floor8(0, 288)
                    plat2 = floor7(-104, 192)
                    plat3 = floor7(140, 130)
                    plat4 = floor3(360, 130)
                    coin1 = rcoin(430, 50 , 16, 16)
                    coin2 = coin(140, 192 , 16, 16)
                    coin3 = coin(165, 192 , 16, 16)
                    coin4 = coin(190, 192 , 16, 16)
                    coin5 = coin(215, 192 , 16, 16)
                    coin6 = coin(240, 192 , 16, 16)
                    coin7 = coin(265, 192 , 16, 16)
                    coin8 = coin(290, 192 , 16, 16)
                    coin9 = coin(150, 60 , 16, 16)
                    coin10 = coin(175, 60 , 16, 16)
                    coin11 = coin(200, 60 , 16, 16)
                    coin12 = coin(225, 60 , 16, 16)
                    coin13 = coin(250, 60 , 16, 16)
                    nEnemies = [en]
                    nPlatforms = [plat1, plat2, plat3, plat4]
                    nSpikes = []
                    nCoins = [coin1, coin2, coin3, coin4, coin5, coin6, coin7, coin8, coin9, coin10, coin11, coin12, coin13]
                    return [nEnemies, nPlatforms, nSpikes, nCoins]

                class pause_menu() :

                    def __init__(self) :
                        self.pause = False
                        self.START = False
                        self.LEFT = False
                        self.RIGHT = False
                        self.switch = True
                        self.state = "Resume"
                        self.width = 852
                        self.height = 384
                        self.midw = self.width / 2
                        self.midh = self.height / 2
                        self.display = pygame.Surface((self.width, self.height))
                        self.window = pygame.display.set_mode(((self.width, self.height)))
                        self.pausex = self.midw
                        self.pausey = 130
                        self.resumex = self.midw - 100
                        self.resumey = self.midh + 110
                        self.exitx = self.midw + 130
                        self.exity = self.midh + 110
                        self.offset = -100
                        self.cursor_pos = (self.resumex + self.offset + 15, self.resumey)
                        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
                        self.cursor_rect.midtop = (int(self.resumex) + int(self.offset) - 55, int(self.resumey))


                    def pause_screen(self) :

                        while self.pause :
                            ps = pygame.image.load('pause1.png')
                            ps1 = pygame.transform.scale(pause_screenimg, (782, 332))
                            self.window.blit(ps1, (35, 40))
                            self.check_keypress()
                            self.check_input()
                            self.draw_text_black(" Game Paused", 30, self.pausex, self.pausey)
                            self.draw_text_black("Resume", 20, self.resumex, self.resumey)
                            self.draw_text_black("Exit", 20, self.exitx, self.exity)
                            self.draw_cursor_black()
                            pygame.display.update()
                            self.reset_keys()

                    def check_keypress(self):
                        for event in pygame.event.get() :
                            if event.type == pygame.KEYDOWN :
                                if event.key == pygame.K_RETURN :
                                    self.START = True
                                if event.key == pygame.K_LEFT :
                                    self.LEFT = True
                                if event.key == pygame.K_RIGHT :
                                    self.RIGHT = True

                    def draw_cursor_black(self) :
                        self.draw_text_black("*", 25, self.cursor_pos[0], self.cursor_pos[1])

                    def draw_text_black(self, text, size, x, y) :
                        font = pygame.font.Font("8-BIT WONDER.TTF", size)
                        text_surface = font.render(text, True, (0, 0, 0))
                        text_rect = text_surface.get_rect()
                        text_rect.center = (int(x), int(y))
                        self.window.blit(text_surface, text_rect)
                    
                    def move_cursor_pause(self) :

                        if self.RIGHT :
                            if self.state == "Resume" :
                                self.cursor_pos = (self.exitx + self.offset + 45, self.exity)
                                self.state = "Exit"
                            elif self.state == "Exit" :
                                self.cursor_pos = (self.resumex + self.offset + 15, self.resumey)
                                self.state = "Resume"

                        elif self.LEFT :
                            if self.state == "Resume" :
                                self.cursor_pos = (self.exitx + self.offset + 45, self.exity)
                                self.state = "Exit"
                            elif self.state == "Exit" :
                                self.cursor_pos = (self.resumex + self.offset + 15, self.resumey)
                                self.state = "Resume"

                    def check_input(self) :
                        
                        self.move_cursor_pause()
                        if self.START :
                            self.pause = False
                            if self.state == "Exit" :
                                self.switch = False

                    def reset_keys(self) :
                        
                        self.START = False
                        self.LEFT = False
                        self.RIGHT = False
                                

                t = 0
                tcheck = 0
                func = [scene1(Enemies, Platforms, Spikes, Coins, tcheck), scene2(Enemies, Platforms, Spikes, Coins, tcheck), scene3(Enemies, Platforms, Spikes, Coins, tcheck)]

                #Game Loop
                pscr = pause_menu()
                run = True
                while run:

                    clock.tick(27)

                    Enemies = func[scene - 1][0]
                    Platforms = func[scene - 1][1]
                    Spikes = func[scene - 1][2]
                    Coins = func[scene - 1][3]

                    if t < 27:
                        t += 1
                    else:
                        t = 0
                ##    if t % 3 == 0:
                ##        print([p1.x,p1.y])

                    for i in Enemies :
                        if i.visible == True :
                            if hitloop == 0 and safetime == 0 :
                                if collisionchk(p1.hitbox[0], p1.hitbox[1], p1.hitbox[2], p1.hitbox[3], i.hitbox[0], i.hitbox[1], i.hitbox[2], i.hitbox[3]) :
                                    p1.hit()
                                    hitloop = 1
                                    safetime = 1
                    if hitloop == 0 and safetime == 0 :
                        for s in Spikes :
                            if collisionchk(p1.hitbox[0], p1.hitbox[1], p1.hitbox[2], p1.hitbox[3], s.hitbox[0], s.hitbox[1], s.hitbox[2], s.hitbox[3]) :
                                p1.hit()
                                hitloop = 1
                                safetime = 1

                    if p1.health == 0 :
                        self.game_ovr = True
                        self.current_menu.cursor_rect.midtop = (self.current_menu.restartx + self.current_menu.offset + 15, self.current_menu.restarty)
                        self.current_menu.state = "Restart"
                        run = False
                        self.playing = False
                        break


                    if shootloop > 0 :
                        shootloop += 1
                    if shootloop > p1.shootspeed :
                        shootloop = 0

                    if safetime > 0:
                        safetime += 1
                        if safetime > 40:
                            safetime = 0


                    if hitloop == 1:
                        p1.jumpcount = 6
                        p1.isjump = True
                    if hitloop > 0:
                        p1.walkcount = 0
                        if p1.right and hitloop < 10 :
                            p1.x -= p1.vel
                        elif p1.left and hitloop < 10 :
                            p1.x += p1.vel
                        hitloop += 1
                    if hitloop > 10 :
                        hitloop = 0
                    
                    for event in pygame.event.get() :
                        if event.type == pygame.QUIT :
                            run = False
                            self.playing = False
                            break

                    for c in Coins:
                        if collisionchk(p1.hitbox[0], p1.hitbox[1], p1.hitbox[2], p1.hitbox[3], c.hitbox[0], c.hitbox[1], c.hitbox[2], c.hitbox[3]) :
                                if c.visible :
                                    self.score += c.points
                                c.hit()

                    for b in bullets :
                        for en in Enemies :
                            if en.visible :
##                                if collisionchk(b.x - b.radius, b.y - b.radius, 2*b.radius, 2*b.radius, en.hitbox[0], en.hitbox[1], en.hitbox[2], en.hitbox[3]) :
                                  if collisionchk(b.hitbox[0], b.hitbox[1], b.hitbox[2], b.hitbox[3], en.hitbox[0], en.hitbox[1], en.hitbox[2], en.hitbox[3]) :
                                    self.score += 1
                                    en.hit()
                                    bullets.pop(bullets.index(b))
                        
                        if b.x < sc_wdth and b.x>0 :
                            b.x += b.vel
                        else:
                            bullets.pop(bullets.index(b))
        
                    glist = []
                    for p in Platforms:
                        if p1.hitbox[1] + p1.hitbox[3] >= p.hitbox[1] and p1.hitbox[1] <= p.hitbox[1] and p1.hitbox[0] < p.hitbox[0] + p.hitbox[2] and p1.hitbox[0] + p1.hitbox[2] > p.hitbox[0]:
                            glist.append("True")
                            p1.y = p.hitbox[1] - 60
                        else:
                            glist.append("False")
                        if p1.hitbox[1] < p.hitbox[1] + p.hitbox[3] and p1.hitbox[0] < p.hitbox[0] + p.hitbox[2] and p1. hitbox[0] + p1.hitbox[2] > p.hitbox[0] and p1.hitbox[1] + p1.hitbox[3] > p.hitbox[1] + p.hitbox[3]:
                            if p1.isjump:
                                if p1.jumpcount > 0:
                                    p1.jumpcount *= -1               
                    if "True" in glist:
                            p1.onground = True
                    else:
                        p1.onground = False

                        
                    if p1.onground:
                        if p1.jumpcount <= -6:
                            p1.isjump = False
                            p1.jumpcount = 6
                        p1.falling = False

                    elif not p1.onground:
                        if p1.jumpcount == -7:
                            p1.falling = True
                            p1.isjump = False
                            p1.jumpcount = 6
                        elif not p1.isjump:
                            p1.falling = True
                #Walls/Transitions

                    if scene == 1:
                        for en in Enemies :
                            if en.health != 0 :
                                en.visible = True
                        if p1.y == 292 :
                            if p1.hitbox[0] - 5 < 348 :
                                p1.x = 338
                            elif p1.hitbox[0] + p1.hitbox[2] + 5 > 522 :
                                p1.x = 470
                        if p1.y == 228 :
                            if p1.x < -15 :
                                p1.x = -15
                        if p1.y == 196 :
                            if p1.hitbox[0] + p1.hitbox[2] + 5 > 852 :
                                p1.x = -15
                                tcheck = -1
                                for en in Enemies :
                                    en.visible = False
                                scene = 2
                    if scene == 2 :
                        for en in Enemies :
                            if en.health != 0 :
                                en.visible = True
                        if p1.y == 196 :
                            if p1.x < -15 :
                                p1.x = 806
                                tcheck = -1
                                scene = 1
                        if p1.y == 292 :
                            if p1.hitbox[0] - 5 < 193 :
                                p1.x = 183
                            elif p1.hitbox[0] + p1.hitbox[2] + 5 > 436 :
                                p1.x = 384
                        if p1.y == 291 :
                            if p1.hitbox[0] - 5 < 641 :
                                p1.x = 631
                            elif p1.hitbox[0] + p1.hitbox[2] + 5 > 724 :
                                p1.x = 672
                        if p1.y == 132 or p1.y == 228 :
                            if p1.hitbox[0] + p1.hitbox[2] + 5 > 852 :
                                p1.x = -15
                                tcheck = -1
                                for en in Enemies :
                                    en.visible = False
                                scene = 3
                    if scene == 3 :
                        if p1.y == 132 or p1.y == 228 :
                            if p1.x < -15 :
                                p1.x = 806
                                tcheck = -1
                                scene = 2
                        if p1.x > 650  and scene == 3 :
                            self.current_menu.cursor_rect.midtop = (self.current_menu.enter_namex + self.current_menu.offset - 20, self.current_menu.enter_namey)
                            self.current_menu.state = "Enter Name"
                            self.score += p1.health
                            self.level_end = True
                            run = False
                            self.playing = False
                            break
                        
                    keys = pygame.key.get_pressed()

                    if keys[pygame.K_ESCAPE] :
                        pscr.pause = True
                        while pscr.pause :
                            pscr.pause_screen()

                    if not pscr.switch :
                        run = False
                        self.playing = False
                        self.current_menu.cursor_rect.midtop = (self.current_menu.startx + self.current_menu.offset - 55, self.current_menu.starty)
                        self.current_menu.state = "Start"                                
                        break
                        

                    if not pscr.pause :
                        if hitloop == 0 :
                            if keys[pygame.K_SPACE] and shootloop == 0:
                                if p1.left:
                                    facing = -1
                                else:
                                    facing = 1
                                if len(bullets) < 3:
                                    bullets.append(projectile(round(p1.x + p1.width//2), round(p1.y + p1. height//2), facing))
                                shootloop = 1
                            
                            if keys[pygame.K_LEFT] :
                                if keys [pygame.K_LSHIFT] :
                                    p1.x -= p1.vel + 2
                                else :
                                    p1.x -= p1.vel
                                p1.left = True
                                p1.right = False
                                p1.standing = False
                                    
                            elif keys[pygame.K_RIGHT] :
                                if keys [pygame.K_LSHIFT]:
                                       p1.x += p1.vel + 2
                                else :
                                    p1.x += p1.vel
                                p1.left = False
                                p1.right = True
                                p1.standing = False
                                    
                            else :
                                p1.standing = True
                                p1.walkcount = 0
                                
                        if not (p1.isjump) and not p1.falling :
                            if hitloop == 0 :            
                                if keys[pygame.K_UP] :
                                    p1.isjump = True
                                    p1.walkcount = 0
                        elif not p1.falling and p1.isjump :
                            if p1.jumpcount >= -6:
                                neg = 1
                                if p1.jumpcount == 1 :
                                    p1.y -= 1
                                    p1.jumpcount = -1
                                if p1.jumpcount <= 0 :
                                    neg = -1
                                p1.y -= (p1.jumpcount**2) * neg
                                p1.jumpcount -= 1
                        elif p1.falling :
                            p1.y += 36
                    tcheck += 1
                    if not pscr.pause :
                        redraw()
            if self.playing :
                self.score = 0
                platformer()
            pygame.display.update()
            self.resetkeys()

    def scores(self) :
        while self.score_screen :
            self.check_events()
            if self.START :
                self.score_screen = False
            self.current_menu.score_menu()

    def playerded(self) :
        while self.game_ovr :
            self.check_events()
            if self.START :
                self.game_ovr = False
            self.current_menu.game_over()

    def lvlcomp(self) :
        while self.level_end :
            self.check_events()
            if self.START :
                self.level_end = False
            self.current_menu.level_complete()
            

    def check_events(self) :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                self.current_menu.run_display1 = False
                self.running = False
                self.playing = False
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_RETURN :
                    self.START = True
                if event.key == pygame.K_BACKSPACE :
                    self.BACK = True
                if event.key == pygame.K_DOWN :
                    self.DOWN = True
                if event.key == pygame.K_UP :
                    self.UP = True
                if event.key == pygame.K_LEFT :
                    self.LEFT = True
                if event.key == pygame.K_RIGHT :
                    self.RIGHT = True
                    
    def resetkeys(self) :
        self.START = False
        self.BACK = False
        self.DOWN = False
        self.UP = False
        self.LEFT = False
        self.RIGHT = False

    def drawcontrols(self, text, size, x, y) :
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.black)
        text_rect = text_surface.get_rect()
        text_rect.center = (int(x), int(y))
        self.window.blit(text_surface, text_rect)

    def draw_text_black(self, text, size, x, y) :
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.black)
        text_rect = text_surface.get_rect()
        text_rect.center = (int(x), int(y))
        self.display.blit(text_surface, text_rect)

    def draw_text_white(self, text, size, x, y) :
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.white)
        text_rect = text_surface.get_rect()
        text_rect.center = (int(x), int(y))
        self.display.blit(text_surface, text_rect)


class Menu() :
    
    def __init__(self, game) :
        self.game = game
        self.mid_w = self.game.width / 2
        self.mid_h = self.game.height / 2
        self.run_display1 = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -100

    def draw_cursor_black(self) :
        self.game.draw_text_black("*", 25, self.cursor_rect.x, self.cursor_rect.y)

    def draw_cursor_white(self) :
        self.game.draw_text_white("*", 25, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self) :
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.resetkeys()

class MainMenu(Menu) :
    
    def __init__(self, game) :
        Menu.__init__(self, game)
        self.state = "Start"
        self.score_num = 0
        self.score_num_get = 0
        self.datalen = 0
        self.startx = self.mid_w
        self.starty = self.mid_h + 20
        self.scoresx = self.mid_w
        self.scoresy = self.mid_h + 60
        self.quitx = self.mid_w
        self.quity = self.mid_h + 100
        self.exitx = 120
        self.exity = 360
        self.upx = self.mid_w - 50
        self.upy = 360
        self.downx = self.mid_w + 50
        self.downy = 360
        self.clearscorex = self.game.width - 125
        self.clearscorey = 360
        self.completex = self.mid_w
        self.completey = 90
        self.scorex = self.mid_w
        self.scorey = 120
        self.enter_namex = self.mid_w - 150
        self.enter_namey = self.mid_h + 105
        self.main_menux = self.mid_w + 150
        self.main_menuy = self.mid_h + 105
        self.restartx = self.mid_w - 125
        self.restarty = self.mid_h + 105
        self.name = ""
        self.namelist = []
        self.data = []
        self.cursor_rect.midtop = (int(self.startx) + int(self.offset) - 55, int(self.starty))

    def display_menu(self) :
        self.run_display1 = True
        while self.run_display1 :
            self.game.check_events()
            self.check_input_Main()
            bg = pygame.image.load('background_1.png')
            bg1 = pygame.transform.scale(bg, (852,384))
            self.game.display.blit(bg1, (0, 0))
            self.game.draw_text_black("Main Menu", 30, self.game.width/2, 30)
            self.game.draw_text_black("Start Game", 30, self.startx, self.starty)
            self.game.draw_text_black("Scores", 30, self.scoresx, self.scoresy)
            self.game.draw_text_black("Exit", 30, self.quitx, self.quity)
            self.draw_cursor_black()
            self.blit_screen()

    def score_menu(self) :
        self.run_display2 = True
        while self.run_display2 :
            self.game.check_events()
            self.check_input_Scores()
            bg = pygame.image.load('background_1.png')
            bg1 = pygame.transform.scale(bg, (852,384))
            self.game.display.blit(bg1, (0, 0))
            ps = pygame.image.load('pause1.png')
            ps1 = pygame.transform.scale(ps, (782, 332))
            sp = pygame.image.load('Score pointer.png')
            sp1 = pygame.transform.scale(sp, (640, 200))
            self.game.display.blit(ps1, (40, 10))
            if len(self.namelist) != 0 :
                self.game.display.blit(sp, (80, 80 + (self.score_num)*50))
            for i in range(len(self.namelist)):            
                self.game.draw_text_black(self.namelist[i], 20, 420, 130 + i*50,)
            self.game.draw_text_black("High Scores", 25, self.game.width/2, 80)
            self.game.draw_text_white("Main Menu", 20, self.exitx, self.exity)
            self.game.draw_text_white("Up", 20, self.upx, self.upy)
            self.game.draw_text_white("Down", 20, self.downx, self.downy)
            self.game.draw_text_white("Clear Score", 20, self.clearscorex, self.clearscorey)
            self.draw_cursor_white()
            self.blit_screen()
        
    def level_complete(self) :
        self.run_display3 = True
        while self.run_display3 :
            self.game.check_events()
            self.check_input_Complete()
            bg = pygame.image.load('background_1.png')
            ps = pygame.image.load('pause1.png')
            bg1 = pygame.transform.scale(bg, (852,384))
            ps1 = pygame.transform.scale(ps, (782, 332))
            self.game.display.blit(bg1, (0, 0))
            self.game.display.blit(ps1, (40, 25))
            self.game.draw_text_black("!Level Complete!", 30, self.completex, self.completey)
            self.game.draw_text_black("Score " + str(self.game.score), 23, self.scorex, self.scorey)
            self.game.draw_text_black("Enter Name", 23, self.enter_namex, self.enter_namey)
            self.game.draw_text_black("Main Menu", 23, self.main_menux, self.main_menuy)
            self.draw_cursor_black()
            self.blit_screen()

    def game_over(self) :
        self.run_display4 = True
        while self.run_display4 :
            self.game.check_events()
            self.check_input_Over()
            bg = pygame.image.load('background_1.png')
            bg1 = pygame.transform.scale(bg, (852,384))
            ps = pygame.image.load('pause1.png')
            ps1 = pygame.transform.scale(ps, (782, 332))
            self.game.display.blit(bg1, (0, 0))
            self.game.display.blit(ps1, (40, 25))
            self.game.draw_text_black("!Game Over!", 30, self.completex, self.completey)
            self.game.draw_text_black("Restart", 23, self.restartx, self.restarty)
            self.game.draw_text_black("Main Menu", 23, self.main_menux, self.main_menuy)
            self.draw_cursor_black()
            self.blit_screen()

            
    def nameinput(self, name, score) :
        mydb = db.connect(host = "localhost", user = "root", passwd = "root123", database = "platformer")
        cur = mydb.cursor()
        t = (name, score)
        cur.execute("insert into highscores values(%s, %s)", t)
        mydb.commit()
        mydb.close()            

    def getname(self,lenreq) :
        mydb = db.connect(host = "localhost", user = "root", passwd = "root123", database = "platformer")
        cur = mydb.cursor()
        cur.execute("select * from highscores order by score desc;")
        s = []
        records = cur.fetchall()
        if len(records) > 4 :
            score_display = records[lenreq:lenreq+4]
        else :
            score_display = records[lenreq:lenreq+len(records)]    
        self.data = score_display
        for i in score_display :
            namevar = i[0]
            scorevar = i[1]
            s1 = namevar + " " * (50 - len(namevar)) + str(i[1])
            s.append(s1)
        mydb.commit()
        mydb.close()            
        return s, len(records)

    def clearrec(self, record) :
        mydb = db.connect(host = "localhost", user = "root", passwd = "root123", database = "platformer")
        cur = mydb.cursor()
        t = (record[0], record[1])
        print(t)
        cur.execute("delete from highscores where name = %s and score = %s;", t)
        mydb.commit()
        mydb.close()            

    def move_cursor_Main(self) :
        
        if self.game.DOWN : 
            if self.state == "Start" :
                self.cursor_rect.midtop = (self.scoresx + self.offset, self.scoresy)
                self.state = "Scores"
            elif self.state == "Scores":
                self.cursor_rect.midtop = (self.quitx + self.offset + 40, self.quity)
                self.state = "Quit"
            elif self.state == "Quit":
                self.cursor_rect.midtop = (self.startx + self.offset - 55, self.starty)
                self.state = "Start"
        if self.game.UP :
            if self.state == "Start" :
                self.cursor_rect.midtop = (self.quitx + self.offset + 40, self.quity)
                self.state = "Quit"
            elif self.state == "Scores":
                self.cursor_rect.midtop = (self.startx + self.offset - 55, self.starty)
                self.state = "Start"
            elif self.state == "Quit":
                self.cursor_rect.midtop = (self.scoresx + self.offset, self.scoresy)
                self.state = "Scores"

    def move_cursor_Scores(self) :
        
        if self.game.RIGHT :
            if self.state == "Exit" :
                self.cursor_rect.midtop = (self.upx + self.offset + 75, self.upy)
                self.state = "Up"
            elif self.state == "Up" :
                self.cursor_rect.midtop = (self.downx + self.offset + 50, self.downy)
                self.state = "Down"
            elif self.state == "Down" :
                self.cursor_rect.midtop = (self.clearscorex + self.offset - 10, self.clearscorey)
                self.state = "Clear Score"
            elif self.state == "Clear Score" :
                self.cursor_rect.midtop = (self.exitx + self.offset + 5, self.exity)
                self.state = "Exit"

        if self.game.LEFT :
            if self.state == "Exit" :
                self.cursor_rect.midtop = (self.clearscorex + self.offset - 10, self.clearscorey)
                self.state = "Clear Score"
            elif self.state == "Up" :
                self.cursor_rect.midtop = (self.exitx + self.offset + 5, self.exity)
                self.state = "Exit"
            elif self.state == "Down" :
                self.cursor_rect.midtop = (self.upx + self.offset + 75, self.upy)
                self.state = "Up"
            elif self.state == "Clear Score" :
                self.cursor_rect.midtop = (self.downx + self.offset + 50, self.downy)
                self.state = "Down"
            
    def move_cursor_Complete(self) :
        
        if self.game.RIGHT :
            if self.state == "Enter Name" :
                self.cursor_rect.midtop = (self.main_menux + self.offset - 10, self.main_menuy)
                self.state = "Main Menu"
            elif self.state == "Main Menu" :
                self.cursor_rect.midtop = (self.enter_namex + self.offset - 20, self.enter_namey)
                self.state = "Enter Name"
        elif self.game.LEFT :
            if self.state == "Enter Name" :
                self.cursor_rect.midtop = (self.main_menux + self.offset - 10, self.main_menuy)
                self.state = "Main Menu"
            elif self.state == "Main Menu" :
                self.cursor_rect.midtop = (self.enter_namex + self.offset - 20, self.enter_namey)
                self.state = "Enter Name"

    def move_cursor_Over(self) :
        
        if self.game.RIGHT :
            if self.state == "Restart" :
                self.cursor_rect.midtop = (self.main_menux + self.offset - 10, self.main_menuy)
                self.state = "Main Menu"
            elif self.state == "Main Menu" :
                self.cursor_rect.midtop = (self.restartx + self.offset + 15, self.restarty)
                self.state = "Restart"
        elif self.game.LEFT :
            if self.state == "Restart" :
                self.cursor_rect.midtop = (self.main_menux + self.offset - 10, self.main_menuy)
                self.state = "Main Menu"
            elif self.state == "Main Menu" :
                self.cursor_rect.midtop = (self.restartx + self.offset + 15, self.restarty)
                self.state = "Restart"
            

    def check_input_Main(self) :
        
        self.move_cursor_Main()
        if self.game.START :
            if self.state == "Start" :
                self.game.playing = True
            elif self.state == "Scores" :
                self.namelist, self.datalen = self.getname(self.score_num_get)
                self.cursor_rect.midtop = (self.exitx + self.offset + 5, self.exity)
                self.state = "Exit"
                self.game.score_screen = True
            elif self.state == "Quit" :
                self.game.runnning = False
                pygame.quit()
                sys.exit()
            self.run_display1 = False
            
    def check_input_Scores(self) :
        
        self.move_cursor_Scores()
        if self.game.START :
            if self.state == "Exit" :
                self.cursor_rect.midtop = (self.startx + self.offset - 55, self.starty)
                self.state = "Start"
                self.score_num = 0
                self.game.score_screen = False
                self.run_display2 = False
                self.run_display1 = True
            elif self.state == "Up"  and self.score_num != 0 :
                self.score_num -= 1
            elif self.state == "Up"  and self.score_num == 0  and self.score_num_get != 0:
                self.score_num_get -= 1
                self.namelist, self.datalen = self.getname(self.score_num_get)
            elif self.state == "Down"  and self.score_num < self.datalen -1 and self.score_num != 3 :
                self.score_num += 1
            elif self.state == "Down"  and self.score_num == 3 and self.datalen > self.score_num_get + 4:
                self.score_num_get += 1
                self.namelist, self.datalen = self.getname(self.score_num_get)
            elif self.state == "Clear Score" and len(self.namelist) != 0  :
                print(self.data[self.score_num])
                print(self.score_num)
                print(self.datalen)
                self.clearrec(self.data[self.score_num])
                self.namelist, self.datalen = self.getname(self.score_num_get)
                if self.score_num > len(self.data) - 1 and self.score_num != 0:
                    self.score_num = len(self.data) - 1
                        
    def check_input_Complete(self) :
        
        self.move_cursor_Complete()
        if self.game.START :
            if self.state == "Main Menu" :
                self.cursor_rect.midtop = (self.startx + self.offset - 55, self.starty)
                self.state = "Start"
                self.game.level_end = False
                self.run_display3 = False
                self.run_display1 = True
            elif self.state == "Enter Name" :
                name_box = makeTextBox(self.mid_w - 150, 170, 300, 0, "Enter Name Here", 10, 20)
                showTextBox(name_box)
                self.Name = textBoxInput(name_box)
                self.nameinput(self.Name, self.game.score)
                self.game.score = 0
                self.cursor_rect.midtop = (self.startx + self.offset - 55, self.starty)
                self.state = "Start"
                self.game.level_end = False
                self.run_display3 = False
                self.run_display1 = True

    def check_input_Over(self) :
        
        self.move_cursor_Over()
        if self.game.START :
            if self.state == "Main Menu" :
                self.cursor_rect.midtop = (self.startx + self.offset - 55, self.starty)
                self.state = "Start"
                self.game.game_ovr = False
                self.run_display4 = False
                self.run_display1 = True
            elif self.state == "Restart" :
                self.game.score = 0
                self.game.game_ovr = False
                self.game.playing = True
                self.run_display4 = False
           

Gameinit = game()

while Gameinit.running :
    if not Gameinit.playing :    
        Gameinit.current_menu.display_menu()
    Gameinit.game_loop()
    Gameinit.playerded()
    Gameinit.scores()
    Gameinit.lvlcomp()
    Gameinit.resetkeys()

pygame.quit()
