import sys # pouziti systemoveho balicku
import pygame # pouziti balicku pygame
pygame.init() # spusteni pygame

clock = pygame.time.Clock()
FPS = 60

# rozliseni okna
ROZLISENI_OKNA = ROZLISENI_X, ROZLISENI_Y = 800, 600

# vlastnosti vykreslovaneho tvaru
velikost = 60

posun_x = 0.1
posun_y = 0.1
manualni_posun = 10
#vykresleni okna 
okno = pygame.display.set_mode(ROZLISENI_OKNA)
#souradnice prekazka1
prekazka1_x = 420
prekazka1_y = 100
#souradnice prekazka2
prekazka2_x = 140
prekazka2_y = 100
#souradnice prekazka3
prekazka3_x = 100
prekazka3_y = 500
#hrac2
hrac2_x = 720
hrac2_y = 20
#hrac1
hrac1_x = 20
hrac1_y = 520
 #pozadi
podlaha = pygame.image.load("pixel.jpg").convert_alpha()
podlaha = pygame.transform.scale(podlaha, (100, 100))



# nekonecna vykreslovaci smycka
while True:
    # kod umoznujici vypnout aplikaci
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        

    for y in range(0, 600, 100):
        for x in range(0, 800, 100):
            okno.blit(podlaha, (x, y))
        
    #ovladani klavesnice
    stisknuto = pygame.key.get_pressed()        
    if stisknuto[pygame.K_d]:
        hrac1_x += manualni_posun
    if stisknuto[pygame.K_a]:
        hrac1_x -= manualni_posun
    if stisknuto[pygame.K_s]:
        hrac1_y += manualni_posun
    if stisknuto[pygame.K_w]:
        hrac1_y -= manualni_posun
        
    #ovladani klavenice 2
    stisknuto = pygame.key.get_pressed()        
    if stisknuto[pygame.K_RIGHT]:
        hrac2_x += manualni_posun
    if stisknuto[pygame.K_LEFT]:
        hrac2_x -= manualni_posun
    if stisknuto[pygame.K_DOWN]:
        hrac2_y += manualni_posun
    if stisknuto[pygame.K_UP]:
        hrac2_y -= manualni_posun
        
        
    #kolize s okraji okna
    if hrac1_x < 0:  # presazeni horniho okraje okna
        hrac1_x = 0  # posunuti zpet do okna
        posun_x *= -1 # zmena smeru
    if hrac1_y < 0:  # presazeni horniho okraje okna
        hrac1_y = 0  # posunuti zpet do okna
        posun_y *= -1 # zmena smeru
    if hrac1_x > ROZLISENI_X - velikost: # presazeni dolniho okraje okna
        hrac1_x = ROZLISENI_X - velikost # posunuti zpet do okna
        posun_x *= -1                     # zmena smeru
    if hrac1_y > ROZLISENI_Y - velikost: # presazeni dolniho okraje okna
        hrac1_y = ROZLISENI_Y - velikost # posunuti zpet do okna
        posun_y *= -1                     # zmena smeru
        
            
    # vykreslovani geometrie hrac1
    pygame.draw.rect(okno, (255, 24, 5), (hrac1_x, hrac1_y, velikost, velikost))
    #vykresleni geometrie hrac2
    pygame.draw.rect(okno, (170, 22, 111), (hrac2_x, hrac2_y, 60, 60))
    #vykresleni geometrie prekazka1
    pygame.draw.rect(okno, (255, 255 ,255), (prekazka1_x, prekazka1_y, 250, 300))
    #vykresleni geometrie prekazka2
    pygame.draw.rect(okno, (255, 255, 255), (prekazka2_x, prekazka2_y, 120, 150))
    #vykreseleni geometrie prekazka3
    pygame.draw.rect(okno, (255, 255, 255), (prekazka3_x, prekazka3_y, 320, 100))
    
    #kolize s prekazkami
    
       
       
       
    okno.blit(podlaha, (800, 600))
    clock.tick(FPS)
       
    pygame.display.update()
        
           

    