import sys
import pygame
pygame.init()

clock = pygame.time.Clock()
FPS = 60

# ============================================================================
# PROMENNE
# ============================================================================
ROZLISENI_X, ROZLISENI_Y = 800, 600
velikost = 60
manualni_posun = 10

# pozice
hrac1_x, hrac1_y = 20, 520
hrac2_x, hrac2_y = 720, 20

# prekazky
prekazka1_x, prekazka1_y = 420, 100
sirka_prekazky1, vyska_prekazky1 = 300, 250

prekazka2_x, prekazka2_y = 140, 100
sirka_prekazky2, vyska_prekazky2 = 150, 100

prekazka3_x, prekazka3_y = 200, 500
sirka_prekazky3, vyska_prekazky3 = 300, 100

# stavy
hlavni_nabidka = True
hra_bezi = False
game_over_obrazovka = False

# okno a obrazky
okno = pygame.display.set_mode((ROZLISENI_X, ROZLISENI_Y))
podlaha = pygame.transform.scale(pygame.image.load("pixel.jpg").convert_alpha(), (100, 100))
zdi = pygame.transform.scale(pygame.image.load("brick.png").convert_alpha(), (50, 50))
repete = pygame.transform.scale(pygame.image.load("repete-obr.png").convert_alpha(), (50, 50))
home = pygame.transform.scale(pygame.image.load("home-obr.png").convert_alpha(), (50, 50))
mainscreen = pygame.transform.scale(pygame.image.load("mainscreen_wallpaper.png").convert_alpha(), (800, 600))
repete_screen = pygame.transform.scale(pygame.image.load("repeat_screen.jpg"), (400, 300))

prekazka1_rect = pygame.Rect(prekazka1_x, prekazka1_y, sirka_prekazky1, vyska_prekazky1)
prekazka2_rect = pygame.Rect(prekazka2_x, prekazka2_y, sirka_prekazky2, vyska_prekazky2)
prekazka3_rect = pygame.Rect(prekazka3_x, prekazka3_y, sirka_prekazky3, vyska_prekazky3)

play_tlacitko = pygame.Rect(300, 320, 200, 60)
repeat_tlacitko = pygame.Rect(220, 380, 50, 50)
home_tlacitko = pygame.Rect(530, 380, 50, 50)


# ============================================================================
# LOGIKA
# ============================================================================
def reset_game():
    global hrac1_x, hrac1_y, hrac2_x, hrac2_y, hra_bezi, game_over_obrazovka, manualni_posun
    hrac1_x, hrac1_y = 20, 520
    hrac2_x, hrac2_y = 720, 20
    manualni_posun = 10
    hra_bezi = True
    game_over_obrazovka = False

def zpet_do_menu():
    global hlavni_nabidka, hra_bezi, game_over_obrazovka
    hlavni_nabidka = True
    hra_bezi = False
    game_over_obrazovka = False

def pohyb_hracu():
    global hrac1_x, hrac1_y, hrac2_x, hrac2_y, game_over_obrazovka, hra_bezi
    
    stisknuto = pygame.key.get_pressed()
    
    # hrac1
    stara_x, stara_y = hrac1_x, hrac1_y
    if stisknuto[pygame.K_d]: hrac1_x += manualni_posun
    if stisknuto[pygame.K_a]: hrac1_x -= manualni_posun
    if stisknuto[pygame.K_s]: hrac1_y += manualni_posun
    if stisknuto[pygame.K_w]: hrac1_y -= manualni_posun
    
    hrac1_rect = pygame.Rect(hrac1_x, hrac1_y, velikost, velikost)
    if (hrac1_rect.colliderect(prekazka1_rect) or hrac1_rect.colliderect(prekazka2_rect) or hrac1_rect.colliderect(prekazka3_rect)):
        hrac1_x, hrac1_y = stara_x, stara_y
    
    if hrac1_x < 0: hrac1_x = 0
    if hrac1_y < 0: hrac1_y = 0
    if hrac1_x > ROZLISENI_X - velikost: hrac1_x = ROZLISENI_X - velikost
    if hrac1_y > ROZLISENI_Y - velikost: hrac1_y = ROZLISENI_Y - velikost
    
    # hrac2
    stara_x2, stara_y2 = hrac2_x, hrac2_y
    if stisknuto[pygame.K_RIGHT]: hrac2_x += manualni_posun
    if stisknuto[pygame.K_LEFT]: hrac2_x -= manualni_posun
    if stisknuto[pygame.K_DOWN]: hrac2_y += manualni_posun
    if stisknuto[pygame.K_UP]: hrac2_y -= manualni_posun
    
    hrac2_rect = pygame.Rect(hrac2_x, hrac2_y, velikost, velikost)
    if (hrac2_rect.colliderect(prekazka1_rect) or hrac2_rect.colliderect(prekazka2_rect) or hrac2_rect.colliderect(prekazka3_rect)):
        hrac2_x, hrac2_y = stara_x2, stara_y2
    
    if hrac2_x < 0: hrac2_x = 0
    if hrac2_y < 0: hrac2_y = 0
    if hrac2_x > ROZLISENI_X - velikost: hrac2_x = ROZLISENI_X - velikost
    if hrac2_y > ROZLISENI_Y - velikost: hrac2_y = ROZLISENI_Y - velikost
    
    # kolize mezi hraci
    if hrac1_rect.colliderect(hrac2_rect):
        game_over_obrazovka = True
        hra_bezi = False


# ============================================================================
# VYKRESLOVANI
# ============================================================================
def vykresli_menu():
    okno.blit(mainscreen, (0, 0))
    nazev_text = pygame.font.Font(None, 100).render("HRA NA BABU", True, (255, 255, 255))
    okno.blit(nazev_text, nazev_text.get_rect(center=(400, 200)))
    pygame.draw.rect(okno, (0, 200, 0), play_tlacitko)
    pygame.draw.rect(okno, (255, 255, 255), play_tlacitko, 3)
    play_text = pygame.font.Font(None, 50).render("PLAY", True, (255, 255, 255))
    okno.blit(play_text, play_text.get_rect(center=play_tlacitko.center))

def vykresli_hru():
    # podlaha
    for y in range(0, 600, 100):
        for x in range(0, 800, 100):
            okno.blit(podlaha, (x, y))
    
    # prekazky
    for offset_x in range(0, sirka_prekazky1, 50):
        for offset_y in range(0, vyska_prekazky1, 50):
            okno.blit(zdi, (prekazka1_x + offset_x, prekazka1_y + offset_y))
    
    for offset_x in range(0, sirka_prekazky2, 50):
        for offset_y in range(0, vyska_prekazky2, 50):
            okno.blit(zdi, (prekazka2_x + offset_x, prekazka2_y + offset_y))
    
    for offset_x in range(0, sirka_prekazky3, 50):
        for offset_y in range(0, vyska_prekazky3, 50):
            okno.blit(zdi, (prekazka3_x + offset_x, prekazka3_y + offset_y))
    
    # hraci
    pygame.draw.rect(okno, (255, 24, 5), (hrac1_x, hrac1_y, velikost, velikost))
    pygame.draw.rect(okno, (170, 22, 111), (hrac2_x, hrac2_y, velikost, velikost))

def vykresli_gameover():
    okno.blit(mainscreen, (0, 0))
    pygame.draw.rect(okno, (40, 40, 40), (200, 150, 400, 300))
    okno.blit(repete_screen, (200, 150))
    okno.blit(repete, (220, 380))
    okno.blit(home, (530, 380))
    text = pygame.font.Font(None, 74).render("GAME OVER", True, (255, 0, 0))
    okno.blit(text, text.get_rect(center=(400, 300)))


# ============================================================================
# HLAVNI SMYCKA
# ============================================================================
while True:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if udalost.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = udalost.pos
            if hlavni_nabidka and play_tlacitko.collidepoint(mouse_pos):
                hlavni_nabidka = False
                reset_game()
            if game_over_obrazovka and repeat_tlacitko.collidepoint(mouse_pos):
                reset_game()
            if game_over_obrazovka and home_tlacitko.collidepoint(mouse_pos):
                zpet_do_menu()
        
        if udalost.type == pygame.KEYDOWN:
            if udalost.key == pygame.K_r and game_over_obrazovka:
                reset_game()
    
    # LOGIKA
    if hra_bezi and not game_over_obrazovka:
        pohyb_hracu()
    
    # VYKRESLOVANI
    if hlavni_nabidka:
        vykresli_menu()
    elif hra_bezi and not game_over_obrazovka:
        vykresli_hru()
    elif game_over_obrazovka:
        vykresli_gameover()
    
    clock.tick(FPS)
    pygame.display.flip()
