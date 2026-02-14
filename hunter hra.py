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


repete = pygame.image.load("repete-obr.png").convert_alpha()
repete = pygame.transform.scale(repete, (50, 50))

home = pygame.image.load("home-obr.png").convert_alpha()
home = pygame.transform.scale(home, (50, 50))


prekazka1_rect = pygame.Rect(prekazka1_x, prekazka1_y, sirka_prekazky1, vyska_prekazky1)
prekazka2_rect = pygame.Rect(prekazka2_x, prekazka2_y, sirka_prekazky2, vyska_prekazky2)
prekazka3_rect = pygame.Rect(prekazka3_x, prekazka3_y, sirka_prekazky3, vyska_prekazky3)



# Stavy hry
hlavni_nabidka = True
hra_bezi = False

play_tlacitko = pygame.Rect(300, 320, 200, 60)

# Tyto zustanou stejne
repeat_tlacitko = pygame.Rect(220, 380, 50, 50)
home_tlacitko = pygame.Rect(530, 380, 50, 50)

def reset_game():
    global hrac1_x, hrac1_y, hrac2_x, hrac2_y
    global hra_bezi, game_over_obrazovka, manualni_posun

    hrac1_x = 20
    hrac1_y = 520
    hrac2_x = 720
    hrac2_y = 20
    manualni_posun = 10
    hra_bezi = True
    game_over_obrazovka = False
    
def zpet_do_menu():
    global hlavni_nabidka, hra_bezi, game_over_obrazovka
    hlavni_nabidka = True
    hra_bezi = False
    game_over_obrazovka = False

#nekonecna vykreslovaci smycka
while True:
    # kod umoznujici vypnout aplikaci
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    #ovladani mysi 
        if udalost.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = udalost.pos
        #kliknuti na playy v H.nabidce
            if hlavni_nabidka and play_tlacitko.collidepoint(mouse_pos):
                hlavni_nabidka = False
                reset_game()
        #kliknuti na repeat v nabidce
            if game_over_obrazovka and play_tlacitko.collidepoint(mouse_pos):
               reset_game()
        
            if game_over_obrazovka and home_tlacitko.collidepoint(mouse_pos):
              zpet_do_menu()
              
    #  Kontrola R klavesy 
        if udalost.type == pygame.KEYDOWN:
            if udalost.key == pygame.K_r and game_over_obrazovka:
               reset_game()
               
    # === HLAVNI NABIDKA ===
    if hlavni_nabidka:
        okno.fill((20, 20, 20))
    
    # Nazev hry
        nazev_font = pygame.font.Font(None, 100)
        nazev_text = nazev_font.render("HRA NA BABU", True, (255, 255, 255))
        okno.blit(nazev_text, nazev_text.get_rect(center=(400, 200)))
    
    # Zelene tlacitko PLAY
        pygame.draw.rect(okno, (0, 200, 0), play_tlacitko)
        pygame.draw.rect(okno, (255, 255, 255), play_tlacitko, 3)
    
        play_font = pygame.font.Font(None, 50)
        play_text = play_font.render("PLAY", True, (255, 255, 255))
        okno.blit(play_text, play_text.get_rect(center=play_tlacitko.center))

    # === Zbytek hry === 
    elif hra_bezi and not game_over_obrazovka:
    # vykresleni podlahy
        for y in range(0, 600, 100):
           for x in range(0, 800, 100):
               okno.blit(podlaha, (x, y))
   
    #  Pohyb hracu jen kdyz neni game over
    
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
    elif game_over_obrazovka:
        # tmavé pozadí 
         pygame.draw.rect(okno, (0, 0, 0), (0, 0, 800, 600))
        # okno uprostřed
         pygame.draw.rect(okno, (40, 40, 40), (200, 150, 400, 300))
         pygame.draw.rect(okno, (200, 200, 200), (200, 150, 400, 300), 4)
        #repete tlacitko
         okno.blit(repete, (220, 380))
        #home tlacitko
         okno.blit(home, (530,380))
        # GAME OVER text
         text = pygame.font.Font(None, 74).render("GAME OVER", True, (255, 0, 0))
         okno.blit(text, text.get_rect(center=(400, 300)))
        # Text pro restart
         restart_text = pygame.font.Font(None, 36).render("", True, (255, 255, 255))
         okno.blit(restart_text, restart_text.get_rect(center=(400, 400)))
    
    clock.tick(FPS)
    pygame.display.flip()
    
    