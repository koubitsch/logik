import pygame
from collections.abc import Callable
from random import randint

class Tlacitko(pygame.sprite.Sprite): #třída pro zmáčknutelné objekty
    def __init__(self, left, top, image:str,akce:Callable[[any], None], promenne, hover):
        super().__init__()
        self.hover = hover
        if self.hover != None:
            self.orig_image = pygame.image.load(image).convert_alpha()
            self.alt_image = pygame.image.load(hover).convert_alpha()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft=(left,top))
        self.akce = akce
        self.promenne = promenne

    def update(self): #pro šipečky, protože mají alternativní obraz, když na ně ukážete myśí
        pos = pygame.mouse.get_pos()
        if self.hover != None:
            if self.rect.collidepoint(pos):
                self.image = self.alt_image
            else:
                self.image = self.orig_image

    def klik(self): #provede přidělenou funkci po kliknutí na obraz
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.akce(*self.promenne)

def porovnat(a: int, b: int) -> int: #funkce vyhodnocující shodu tipů
    pocet_a, pocet_b = [0] * 8, [0] * 8
    vystup = 0
    for i in range(5):
        aktualni_a = a % 8
        aktualni_b = b % 8
        a, b = a // 8, b // 8
        if aktualni_b == aktualni_a:
            vystup += 10
        else:
            pocet_a[aktualni_a] += 1
            pocet_b[aktualni_b] += 1
    for i in range(8):
        vystup += min(pocet_a[i], pocet_b[i])
    return vystup


class Pocitac(): #třídá spravující tipy počítače
    def __init__(self):
        self.moznosti = [True] * (8**5) #seznam možností

    def akce(self, tip_pocitac, shoda): #aktualizace možných správných možností
        for moznost in range(8**5):
            if porovnat(moznost, tip_pocitac) != shoda:
                self.moznosti[moznost] = False

    def __call__(self): #po zavolání vybere náhodnou možnost
        ukazatel = randint(0, 8**5)
        while self.moznosti[ukazatel] == False:
            ukazatel += 1
            ukazatel %= 8**5
        return ukazatel
#funkce na převod mezi vektorem a číslem, reprezentující pětici barev
#používám obojí, jelikož pro práci s počítačem se hodí číslo, ale na aktualizaci tipu hráće vektor
def navektor(x:int):
    vystup = []
    for i in range(5):
        vystup.append(x % 8)
        x = x // 8
    return vystup

def nacislo(v:list):
    vystup = 0
    for i in range(5):
        vystup += v[i] * (8**i)
    return vystup

class Kruh(pygame.sprite.Sprite):
    def __init__(self,left, top, barva:int, static:bool):
        super().__init__()
        self.barva = barva
        self.static = static
        if self.barva == 0: self.image = pygame.image.load("sprites/kruh_red.png").convert_alpha()
        elif self.barva == 1: self.image = pygame.image.load("sprites/kruh_black.png").convert_alpha()
        elif self.barva == 2: self.image = pygame.image.load("sprites/kruh_teal.png").convert_alpha()
        elif self.barva == 3: self.image = pygame.image.load("sprites/kruh_orange.png").convert_alpha()
        elif self.barva == 4: self.image = pygame.image.load("sprites/kruh_blue.png").convert_alpha()
        elif self.barva == 5: self.image = pygame.image.load("sprites/kruh_yellow.png").convert_alpha()
        elif self.barva == 6: self.image = pygame.image.load("sprites/kruh_brown.png").convert_alpha()
        elif self.barva == 7: self.image = pygame.image.load("sprites/kruh_purple.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(left,top))

    def nahoru(self):
        if self.static == False:
            self.rect.y -=50

    def dolu(self):
        if self.static == False:
            self.rect.y +=50

class Spunt(pygame.sprite.Sprite):
    def __init__(self, left, top, barva):
        super().__init__()
        if barva == 0:
            self.image = pygame.image.load("sprites/spunt_bila.png").convert_alpha()
        else:
            self.image = pygame.image.load("sprites/spunt_cerna.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(left, top))

    def nahoru(self):
        self.rect.y -= 50

    def dolu(self):
        self.rect.y += 50

def nacti_radu(skupina,left, top ,barvy, porovnani, static): #sestaví řadu kruhů a špuntů
    if type(barvy) is list:
        shoda = porovnat(nacislo(barvy), porovnani)
    else:
        shoda = porovnat(barvy, porovnani)
    if type(barvy) is int:
        barvy = navektor(barvy)
    for i in range(5):
        skupina.add(Kruh(left + 50*i, top, barvy[i],static))
    if not static:
        for j in range(shoda % 10 + shoda // 10):
            if shoda // 10 != 0:
                skupina.add(Spunt(left + 250 + j*15, top, 0))
                shoda += -10
            else:
                skupina.add(Spunt(left + 250 + j * 15, top, 1))
                shoda += -1

def pohni_nahoru(skupina):
    for x in skupina:
        if type(x) is Kruh or type(x) is Spunt:
            x.nahoru()

def pohni_dolu(skupina):
    for x in skupina:
        if type(x) is Kruh or type(x) is Spunt:
            x.dolu()