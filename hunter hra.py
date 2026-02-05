import sys
import pygame
pygame.init()

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
sirka_prekazky1 = 300
vyska_prekazky1 = 250

#souradnice prekazka2
prekazka2_x = 140
prekazka2_y = 100
sirka_prekazky2 = 150
vyska_prekazky2 = 100

#souradnice prekazka3
prekazka3_x = 200
prekazka3_y = 500
sirka_prekazky3 = 300
vyska_prekazky3 = 100

#hrac2
hrac2_x = 720
hrac2_y = 20

#hrac1
hrac1_x = 20
hrac1_y = 520

#pozadi
podlaha = pygame.image.load("pixel.jpg").convert_alpha()
podlaha = pygame.transform.scale(podlaha, (100, 100))

zdi = pygame.image.load("brick.png").convert_alpha()
zdi = pygame.transform.scale(zdi, (50, 50))

prekazka1_rect = pygame.Rect(prekazka1_x, prekazka1_y, sirka_prekazky1, vyska_prekazky1)
prekazka2_rect = pygame.Rect(prekazka2_x, prekazka2_y, sirka_prekazky2, vyska_prekazky2)
prekazka3_rect = pygame.Rect(prekazka3_x, prekazka3_y, sirka_prekazky3, vyska_prekazky3)

game_over = False
game_over_obrazovka = False

def reset_game():
    global hrac1_x, hrac1_y, hrac2_x, hrac2_y
    global game_over, game_over_obrazovka, manualni_posun

    hrac1_x = 20
    hrac1_y = 520
    hrac2_x = 720
    hrac2_y = 20
    manualni_posun = 10
    game_over = False
    game_over_obrazovka = False

#nekonecna vykreslovaci smycka
while True:
    # kod umoznujici vypnout aplikaci
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # OPRAVA: Kontrola R klavesy presunuta sem do spravneho event handleru
        if udalost.type == pygame.KEYDOWN:
            if udalost.key == pygame.K_r and game_over_obrazovka:
                reset_game()

    # vykresleni podlahy
    for y in range(0, 600, 100):
        for x in range(0, 800, 100):
            okno.blit(podlaha, (x, y))
    
    # OPRAVA: Pohyb hracu jen kdyz neni game over
    if not game_over_obrazovka:
        stara_x = hrac1_x
        stara_y = hrac1_y  
        
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
            
        hrac1_rect = pygame.Rect(hrac1_x, hrac1_y, velikost, velikost)

        if (hrac1_rect.colliderect(prekazka1_rect) or
                hrac1_rect.colliderect(prekazka2_rect) or
                    hrac1_rect.colliderect(prekazka3_rect)):
            hrac1_x = stara_x
            hrac1_y = stara_y  
        
        stara_x2 = hrac2_x
        stara_y2 = hrac2_y
           
        #ovladani klavenice 2
        if stisknuto[pygame.K_RIGHT]:
            hrac2_x += manualni_posun
        if stisknuto[pygame.K_LEFT]:
            hrac2_x -= manualni_posun
        if stisknuto[pygame.K_DOWN]:
            hrac2_y += manualni_posun
        if stisknuto[pygame.K_UP]:
            hrac2_y -= manualni_posun
            
        hrac2_rect = pygame.Rect(hrac2_x, hrac2_y, velikost, velikost)

        if (hrac2_rect.colliderect(prekazka1_rect) or
                hrac2_rect.colliderect(prekazka2_rect) or
                    hrac2_rect.colliderect(prekazka3_rect)):
            hrac2_x = stara_x2
            hrac2_y = stara_y2 
            
        #kolize s okraji okna - hrac1
        if hrac1_x < 0:
            hrac1_x = 0
        if hrac1_y < 0:
            hrac1_y = 0
        if hrac1_x > ROZLISENI_X - velikost:
            hrac1_x = ROZLISENI_X - velikost
        if hrac1_y > ROZLISENI_Y - velikost:
            hrac1_y = ROZLISENI_Y - velikost
            
        #kolize s okraji okna - hrac2
        if hrac2_x < 0:
            hrac2_x = 0
        if hrac2_y < 0:
            hrac2_y = 0
        if hrac2_x > ROZLISENI_X - velikost:
            hrac2_x = ROZLISENI_X - velikost
        if hrac2_y > ROZLISENI_Y - velikost:
            hrac2_y = ROZLISENI_Y - velikost
            
        # Kontrola kolize mezi hraci
        if hrac1_rect.colliderect(hrac2_rect):
            game_over = True
            game_over_obrazovka = True
              
    # vykreslovani geometrie hrac1
    pygame.draw.rect(okno, (255, 24, 5), (hrac1_x, hrac1_y, velikost, velikost))
    #vykresleni geometrie hrac2
    pygame.draw.rect(okno, (170, 22, 111), (hrac2_x, hrac2_y, velikost, velikost))
     
    #vykresleni geometrie prekazka1
    for offset_x in range(0, sirka_prekazky1, 50):
        for offset_y in range(0, vyska_prekazky1, 50):
            okno.blit(zdi, (prekazka1_x + offset_x, prekazka1_y + offset_y))
    #vykresleni geometrie prekazka2
    for offset_x in range(0, sirka_prekazky2, 50):
        for offset_y in range(0, vyska_prekazky2, 50):
            okno.blit(zdi, (prekazka2_x + offset_x, prekazka2_y + offset_y))
    #vykreseleni geometrie prekazka3
    for offset_x in range(0, sirka_prekazky3, 50):
        for offset_y in range(0, vyska_prekazky3, 50):
            okno.blit(zdi, (prekazka3_x + offset_x, prekazka3_y + offset_y))

    # Game over obrazovka
    if game_over_obrazovka:
        # tmavé pozadí 
        pygame.draw.rect(okno, (0, 0, 0), (0, 0, 800, 600))
        # okno uprostřed
        pygame.draw.rect(okno, (40, 40, 40), (200, 150, 400, 300))
        pygame.draw.rect(okno, (200, 200, 200), (200, 150, 400, 300), 4)
        # try again tlacitko
        pygame.draw.rect(okno, (200, 200, 200), (220, 380, 50, 50))
        # GAME OVER text
        text = pygame.font.Font(None, 74).render("GAME OVER", True, (255, 0, 0))
        okno.blit(text, text.get_rect(center=(400, 300)))
        # Text pro restart
        restart_text = pygame.font.Font(None, 36).render("Stiskni R pro restart", True, (255, 255, 255))
        okno.blit(restart_text, restart_text.get_rect(center=(400, 400)))
    
    clock.tick(FPS)
    pygame.display.flip()