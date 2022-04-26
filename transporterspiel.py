import random
from math import radians

import pygame
from pygame.locals import *

#Standard für RGB und weitere
GRUEN = (0, 255, 0)
ROT   = (255, 0, 0)
BLAU  = (0, 0, 255)
SCHWARZ = (0, 0, 0)
WEISS = (255, 255, 255)

#Fenster Angaben
BREITE = 1600
HOEHE = 900
FPS = 60

#Geschwindigkeiten für die bewegenden Objekte
G_TRANSPORTER = 5
G_HELI = 6
G_TRANSPORTER_MINUS = -5
G_HELI_MINUS = -6

#Gebäudeparameter für Tankstelle, Lager und der Mine
class Gebaeude(pygame.sprite.Sprite):

    def __init__(self, ladestand, kapazitaet, posX, posY, bildPfad):
        super().__init__()
        self.ladestand_ = ladestand
        self.kapazitaet_ = kapazitaet
        self.posX = posX
        self.posY = posY
        self.image = pygame.image.load(bildPfad)
        self.scalled = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center=(self.posX, self.posY)

    def draw(self, flaeche):
        flaeche.blit(self.scalled, self.rect)

    def setLadestand(self, neuLadestand):
        self.ladestand_ = neuLadestand

    def getLadeStand(self):
        return self.ladestand_

    def setKapazität(self, Kapazitaet):
        self.kapazitaet_ = Kapazitaet

    def getKapazitaet(self):
        return self.kapazitaet_

#Transporterparameter
class Transporter(pygame.sprite.Sprite):

    def __init__(self, ladung, tank):
        super().__init__()
        self.transporter = pygame.image.load('grafik/transporter.png')
        self.image = pygame.transform.scale(self.transporter, (125,100))
        self.rect = self.image.get_rect()
        self.rect.center=(1000, 600)
        self.ladung_ = ladung
        self.tank_ = tank

    def draw(self, flaeche):
        flaeche.blit(self.image, self.rect)

    def setTank(self, tank):
        self.tank_ = tank

    def getTank(self):
        return self.tank_

    def setLadung(self, ladung):
        self.ladung_ = ladung

    def getLadung(self):
        return self.ladung_

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        #print("Top: " + str(self.rect.top) + " Bottom: " + str(self.rect.bottom) + " Left: " + str(self.rect.left) + " Right: " + str(self.rect.right))
        if self.rect.top > 0:
            if pressed_keys[K_w]:
                self.rect.move_ip(0, G_TRANSPORTER_MINUS)
        if self.rect.bottom < HOEHE:
            if pressed_keys[K_s]:
                self.rect.move_ip(0, G_TRANSPORTER)
        if self.rect.left > 0:
            if pressed_keys[K_a]:
                self.rect.move_ip(G_TRANSPORTER_MINUS, 0)
        if self.rect.left < BREITE-self.rect.width:
            if pressed_keys[K_d]:
                self.rect.move_ip(G_TRANSPORTER, 0)
                

#Heliparameter
class Helikopter(pygame.sprite.Sprite):

    def __init__(self): 
        super().__init__()
        self.heli = pygame.image.load('grafik/heli.png')
        self.image = pygame.transform.scale(self.heli, (75, 75))
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(10, BREITE-400), 0)
        self.ladestand = 0

    def draw(self, flaeche):
        flaeche.blit(self.image, self.rect)

    def setLadestand(self, ladestand):
        self.ladestand = ladestand

    def getLadestand(self):
        return self.ladestand

    def move(self):
        self.rect.move_ip(random.randint(-5, 10), random.randint(-5, 10))
        if(self.rect.bottom > HOEHE):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)


    def followPoint(self, x, y):
        xAway = x - self.rect.x
        yAway = y - self.rect.y
        if(xAway > 0 and yAway > 0):
            self.rect.move_ip(random.randint(0, G_HELI), random.randint(0, G_HELI))
        if(xAway < 0 and yAway < 0):
            self.rect.move_ip(random.randint(G_HELI_MINUS, 0), random.randint(G_HELI_MINUS, 0))
        if(xAway < 0 and yAway > 0):
            self.rect.move_ip(random.randint(G_HELI_MINUS, 0), random.randint(0, G_HELI))
        if(xAway > 0 and yAway < 0):
            self.rect.move_ip(random.randint(0, G_HELI), random.randint(G_HELI_MINUS, 0))
        if(xAway == 0 and yAway < 0):
            self.rect.move_ip(0, random.randint(G_HELI_MINUS, 0))
        if(xAway == 0 and yAway > 0):
            self.rect.move_ip(0, random.randint(0, G_HELI))
        if(xAway < 0 and yAway == 0):
            self.rect.move_ip(random.randint(G_HELI_MINUS, 0), 0)
        if(xAway > 0 and yAway == 0):
            self.rect.move_ip(random.randint(0, G_HELI), 0)
class Game:

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.breite, self.hoehe = BREITE, HOEHE
        self.gameOver = False
 
    def initials(self):
        pygame.init()
        pygame.display.set_caption('Transporterspiel')
        pygame.font.init()
        pygame.mixer.init()

        self.FramePerSec = pygame.time.Clock()
        self._running = True

        self.map_ = pygame.image.load('grafik/map.png')
        self.map = pygame.transform.scale(self.map_, (1600, 900))
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._display_surf.blit(self.map, (0, 0))

        self.win = pygame.image.load('grafik/win.png')
        self.winScreen = pygame.transform.scale(self.win, (1600, 900))
        self.win_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.win_surf.blit(self.winScreen, (0, 0))

        self.lose = pygame.image.load('grafik/gameover.png')
        self.loseScreen = pygame.transform.scale(self.lose, (1600, 900))
        self.lose_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.lose_surf.blit(self.loseScreen, (0, 0))

        self.font = pygame.font.Font(None, 20)
        self.helikopter = Helikopter()
        self.transporter = Transporter(0, 100)

        self.lager = Gebaeude(0, 100, 1400, 900, 'grafik/lager.png')
        self.mine = Gebaeude(100, 100, 410, 110, 'grafik/mine.png')
        self.tankstelle = Gebaeude(100, 100, 1375, 250, 'grafik/tankstelle.png')

    def start(self):
        if self.initials() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.event(event)
            self.game_loop()
            self.render()
        self.quit()

    def textAnzeige(self):
        self.erzcounter = self.font.render('Transporter: [Erz: ' + str(self.transporter.getLadung()) + ' | Tank: ' + str(round(self.transporter.getTank())) + ']', False, (0, 0, 0));
        self._display_surf.blit(self.erzcounter, (10, 10))
        self.lagercounter = self.font.render('Lager: [Erz: ' + str(self.lager.getLadeStand()) + ']', False, (0, 0, 0))
        self._display_surf.blit(self.lagercounter, (10, 30))
        self.helicounter = self.font.render('Helikopter: [Geklaut: ' + str(self.helikopter.getLadestand()) + ']', False, (0, 0, 0))
        self._display_surf.blit(self.helicounter, (10, 50))
 
    def event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def game_loop(self):
        self._display_surf.blit(self.map, (0, 0))
        if self.helikopter.rect.colliderect(self.transporter.rect):
            self.heli_collision()
        if self.transporter.rect.colliderect(self.tankstelle.rect):
            self.tanken()
        if self.transporter.rect.colliderect(self.mine.rect):
            self.aufladen()
        if self.transporter.rect.colliderect(self.lager.rect):
            self.abladen()
        if  self.helikopter.rect.colliderect(self.mine.rect):
            self.helikopter.move()
        

        if self.gameOver:
            self.lose_screen()
            return

        self.transporter.update()
        self.helikopter.draw(self._display_surf)
        self.transporter.draw(self._display_surf)
        self.helikopter.followPoint(self.transporter.rect.x, self.transporter.rect.y)
        self.tankstelle.draw(self._display_surf)
        self.mine.draw(self._display_surf)
        self.lager.draw(self._display_surf)

        self.burn_petrol()
        self.textAnzeige()
        
        pygame.display.update()
        pass

    def render(self):
        self.FramePerSec.tick(FPS)
        pygame.display.update()
        pass

    def quit(self):
        pygame.quit()
 
    def heli_collision(self):
        if self.transporter.getLadung() > 0:
            self.transporter.setLadung(self.transporter.getLadung() - 5)
            self.helikopter.setLadestand(self.helikopter.getLadestand() + 5)
        if self.helikopter.getLadestand() >= 20:
            self.lose_screen()

    def tanken(self):
        self.tankstelle.setLadestand(self.tankstelle.ladestand_-100)
        self.transporter.setTank(100)
        return

    def aufladen(self):
        #print("LKW an Mine")
        self.mine.setLadestand(self.mine.ladestand_-5)
        self.transporter.setLadung(5)
        return

    def abladen(self):
        self.lager.setLadestand(self.lager.getLadeStand() + self.transporter.getLadung())
        self.transporter.setLadung(self.transporter.getLadung() - self.transporter.getLadung())
        if self.lager.getLadeStand() >= 80:
            self.win_screen()
        return

    def lose_screen(self):
        if not self.gameOver:
            self.lose_surf.blit(self.loseScreen, (0, 0))
            self.gameOver = True
            self.gameOverScreenShown = False
        return

    def win_screen(self):
        self.win_surf.blit(self.winScreen, (0, 0))
        return


    def burn_petrol(self):
        neue_tankfüllung = self.transporter.getTank() - 0.05
        if(neue_tankfüllung < 0):
            self.lose_screen("TANK LEER!")
        else:
            self.transporter.setTank(neue_tankfüllung)
        return

def main():
    game = Game()
    game.start()

if __name__ == "__main__" :
    main()
