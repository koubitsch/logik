import pygame
from sys import exit
from random import randint
from objekty import Pocitac, porovnat, Tlacitko, nacislo, nacti_radu, pohni_dolu, pohni_nahoru

# úvodní inicializace okna a hry
pygame.init()
screen = pygame.display.set_mode((800, 400))
screen.fill((51,93,66))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Calibri", 24)
pygame.display.set_caption("Logik")


def zmen_tip(pozice):  #f unkce upravující aktuální tip hráče
    global aktualni_tip
    aktualni_tip[pozice] = (aktualni_tip[pozice] + 1) % 8

def potvrd(skupina,left, top , static): # funkce tlačítka potvrď
    global gamestate
    if skupina.sprites() != []:  # posouvá správně provedené tipy, aby byly všechny vidět a aby se dal načíst nový
        nejniz = max(list(map(lambda x: x.rect.y, (skupina.sprites()))))
        rozdil = 250 - nejniz

        if rozdil > 0:
            for i in range(rozdil // 50 - 1):
                pohni_dolu(skupina)

        elif rozdil <= 0:
            for i in range(abs(rozdil) // 50 +1):
                pohni_nahoru(skupina)

    barvy = aktualni_tip
    nacti_radu(skupina, left, top, barvy, hadam, static)  #přidá hráčův tip na obrazovku

    if gamestate == 1:  #přidá tip počítače, pokud se proti němu hraje
        tip = poc()
        poc.akce(tip,porovnat(tip, pocitac_hada))
        nacti_radu(skupina, left + 450, top, tip, pocitac_hada, static)

    pohni_nahoru(skupina)



    if porovnat(nacislo(barvy), hadam) == 50:  #kontroluje zda někdo nevyhrál a kdyžtak přepne okno
        if gamestate == 1 and tip == pocitac_hada:
            gamestate = 5
        else:
            gamestate = 4
    elif gamestate == 1 and tip == pocitac_hada:
        gamestate = 6



def change_gamestate(x): #přepíná okna a připravuje novou hru
    global gamestate, hadam, aktualni_tip, poc, pocitac_hada
    gamestate = x
    posuvne.empty()
    hadam = randint(0, 8**5)
    aktualni_tip = [0]*5
    poc = Pocitac()
    pocitac_hada = randint(0, 8 ** 5)

posuvne = pygame.sprite.Group() #skupina pro tipy hráče a počítače

objekty_vyber_hry = pygame.sprite.Group() #skupina pro úvodní obrazovku a tlačítka pro úvodní obrazovku
objekty_vyber_hry.add(Tlacitko(250,175, "sprites/proti.png",change_gamestate, [1], None))
objekty_vyber_hry.add(Tlacitko(430,175, "sprites/sam.png",change_gamestate, [2], None))

sipecky = pygame.sprite.Group() #skupina, která v sobě má šipky na změnu tipu hráče,šipky na posun provedených tipů a tlačítko na stvrzení

for i in range(5):
    sipecky.add(Tlacitko(40 + i*50,310, "sprites/arrowup_white.png",zmen_tip, [i], "sprites/arrowup_red.png"))
sipecky.add(Tlacitko(290, 330, "sprites/potvrd.png", potvrd, (posuvne, 30, 250, False), None))
sipecky.add(Tlacitko(400,290,"sprites/sipka_nahoru.png", pohni_nahoru, [posuvne], None))
sipecky.add(Tlacitko(400,330,"sprites/sipka_dolu.png", pohni_dolu, [posuvne], None))
sipecky.add(Tlacitko(770,0, "sprites/menu.png", change_gamestate, [0], None))



spodni =  pygame.sprite.Group() #skupina na aktuální tip hráče a toho, co hádá počítač

pressed = False #proměnná na zmáčknutí myši, jelikož se mi kliknutí počítalo vždy víckrát

hadam = randint(0,8**5)#co hádá hráč
pocitac_hada = randint(0,8**5)#co hádá počítač
poc = Pocitac() #instance třídy řídící počítač
gamestate = 0 #jaké okno se má ukazovat
aktualni_tip = [0,0,0,0,0]


while True: #samotný cyklus, kde probíhá hra

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pressed = False


    if gamestate == 0: #úvodní obrazovka
        screen.fill((51, 93, 66))
        objekty_vyber_hry.draw(screen)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in objekty_vyber_hry:
                i.klik()


    if gamestate == 1: #hra dvou hráčů
        screen.fill((51, 93, 66))
        posuvne.draw(screen)
        pygame.draw.rect(screen, 'pink',(0, 290, 800, 110))
        sipecky.draw(screen)
        sipecky.update()
        spodni.empty()
        nacti_radu(spodni, 30, 330, aktualni_tip, 0, True)
        nacti_radu(spodni, 480, 330, pocitac_hada, 0, True)
        spodni.draw(screen)
        if event.type == pygame.MOUSEBUTTONDOWN and pressed == False:
            pressed = True
            for i in sipecky:
                i.klik()
        screen.blit(font.render("počítač hádá:", 1, (0, 0, 0)), (550, 300))

    if gamestate == 2: #hra jednoho hráče
        screen.fill((51, 93, 66))
        posuvne.draw(screen)
        pygame.draw.rect(screen, 'white', (0, 290, 800, 110))
        sipecky.draw(screen)
        sipecky.update()
        spodni.empty()
        nacti_radu(spodni, 30, 330, aktualni_tip, 0, True)
        spodni.draw(screen)
        if event.type == pygame.MOUSEBUTTONDOWN and pressed == False:
            pressed = True
            for i in sipecky:
                i.klik()

    #obrazovky pro konec hry v závislosti na vítězi
    if gamestate == 4:
        screen.fill((51,93,66))
        screen.blit(font.render("Vyhrál jsi", 1, (255,255,255)), (400,200))
        if event.type == pygame.MOUSEBUTTONDOWN and pressed == False:
            gamestate = 0

    if gamestate == 5:
        screen.fill((51,93,66))
        screen.blit(font.render("remíza", 1, (255,255,255)), (400,200))
        if event.type == pygame.MOUSEBUTTONDOWN and pressed == False:
            gamestate = 0

    if gamestate == 6:
        screen.fill((51, 93, 66))
        screen.blit(font.render("prohra", 1, (255, 255, 255)), (400, 200))
        if event.type == pygame.MOUSEBUTTONDOWN and pressed == False:
            gamestate = 0



    pygame.display.update()
    clock.tick(60)