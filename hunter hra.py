import sys
import pygame
import random
import math

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()
FPS = 60

ROZLISENI_X, ROZLISENI_Y = 800, 600
velikost = 60
manualni_posun = 10

okno = pygame.display.set_mode((ROZLISENI_X, ROZLISENI_Y))
pygame.display.set_caption("Hra na Babu")

# ─── OBRAZKY ────────────────────────────────────────────────────────────────
podlaha       = pygame.transform.scale(pygame.image.load("pixel.jpg").convert_alpha(), (100, 100))
zdi           = pygame.transform.scale(pygame.image.load("brick.png").convert_alpha(), (50, 50))
repete        = pygame.transform.scale(pygame.image.load("repete-obr.png").convert_alpha(), (50, 50))
home          = pygame.transform.scale(pygame.image.load("home-obr.png").convert_alpha(), (50, 50))
mainscreen    = pygame.transform.scale(pygame.image.load("mainscreen_wallpaper.png").convert_alpha(), (800, 600))
repete_screen = pygame.transform.scale(pygame.image.load("repeat_screen.jpg"), (400, 300))
cart          = pygame.transform.scale(pygame.image.load("cart.png").convert_alpha(), (200, 60))
PORTAL_IMG_A  = pygame.transform.scale(pygame.image.load("portal_A.png"), (50, 60))
PORTAL_IMG_B  = pygame.transform.scale(pygame.image.load("portal_B.png"), (50, 60))
raven_img     = pygame.image.load("raven_chest.png")
king_img      = pygame.image.load("king.png")
pumkin_img    = pygame.image.load("pumkin.png")

# ─── ZVUKY ──────────────────────────────────────────────────────────────────
def _load_sound(f):
    try:
        return pygame.mixer.Sound(f)
    except Exception:
        return None

gameover_zvuk = _load_sound("game_over.wav")
chycen_zvuk   = _load_sound("caught.wav")

# Lobby hudba – hraje po cely cas v menu, shopu, game over
try:
    pygame.mixer.music.load("lobby_music.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
except Exception:
    pass

# ─── SKINY ──────────────────────────────────────────────────────────────────
# img = obrazek zobrazeny v karticce shopu a na hracich behem hry
SKINY = [
    {"nazev": "Default", "cena": 0,   "barva1": (220, 50,  50),  "barva2": (50,  80,  220), "img": None},
    {"nazev": "Raven",   "cena": 50,  "barva1": (30,  30,  100), "barva2": (100, 100, 255), "img": raven_img},
    {"nazev": "King",    "cena": 100, "barva1": (200, 160, 20),  "barva2": (255, 200, 50),  "img": king_img},
    {"nazev": "Pumkin",  "cena": 150, "barva1": (255, 80,  0),   "barva2": (200, 40,  0),   "img": pumkin_img},
    {"nazev": "Emerald", "cena": 200, "barva1": (0,   180, 80),  "barva2": (0,   120, 50),  "img": None},
    {"nazev": "Shadow",  "cena": 250, "barva1": (120, 0,   180), "barva2": (70,  0,   110), "img": None},
]
aktivni_skin = 0
hrac1_barva  = SKINY[0]["barva1"]
hrac2_barva  = SKINY[0]["barva2"]
mince   = 100
koupeno = {0}

# ─── POZICE HRACU ───────────────────────────────────────────────────────────
hrac1_x, hrac1_y = 20, 520
hrac2_x, hrac2_y = 720, 20

# ─── SAFE ZONY ──────────────────────────────────────────────────────────────
SAFE_ZONA_1 = pygame.Rect(0,   450, 150, 150)
SAFE_ZONA_2 = pygame.Rect(650, 0,   150, 150)
MIN_MEZERA  = 60

# ─── PORTALY ────────────────────────────────────────────────────────────────
PORTAL_SIRKA = 20
PORTAL_DELKA = 80
portal_cooldown = {}

# ─── ZBRAN (sitova puska s aimbotem) ────────────────────────────────────────
zbran_na_mape  = None    # {"x", "y", "rect"}
zbran_hrac     = None    # 1 nebo 2 – kdo drzi zbran
sit_projektily = []      # [{"x","y","vx","vy","rect","owner"}]
SIT_VEL        = 30      # velikost site (ctverecek)
SIT_RYCHLOST   = 9

# ─── STAV HRY ───────────────────────────────────────────────────────────────
hlavni_nabidka     = True
hra_bezi           = False
game_over_obrazovka = False
obchod_obrazovka   = False
losovani_obrazovka = False  # kasino vyber huntera

# Losovani (kasino animace)
hunter       = 1
los_cas      = 0
los_speed    = 80    # ms mezi prepinanim
los_done     = False
los_kdo      = 1     # aktualne zobrazeny "hunter" v animaci
los_fin_cas  = 0     # kdy bylo losovani dokonceno

prekazky_recty = []
portaly        = []

# ─── UI RECTANGLES ──────────────────────────────────────────────────────────
play_tlacitko   = pygame.Rect(300, 320, 200, 60)
shop_tlacitko   = pygame.Rect(300, 400, 200, 60)
repeat_tlacitko = pygame.Rect(220, 380, 50,  50)
home_tlacitko   = pygame.Rect(530, 380, 50,  50)
zpet_tlacitko   = pygame.Rect(20,  540, 150, 45)


# ═══════════════════════════════════════════════════════════════════════════════
# GENERATORY
# ═══════════════════════════════════════════════════════════════════════════════
def generuj_prekazky():
    prekazky = []
    pokusy   = 0
    while len(prekazky) < 3 and pokusy < 500:
        pokusy += 1
        w = random.randrange(100, 300, 50)
        h = random.randrange(100, 250, 50)
        x = random.randrange(MIN_MEZERA, ROZLISENI_X - w - MIN_MEZERA, 50)
        y = random.randrange(MIN_MEZERA, ROZLISENI_Y - h - MIN_MEZERA, 50)
        rect = pygame.Rect(x, y, w, h)
        if rect.inflate(MIN_MEZERA, MIN_MEZERA).colliderect(SAFE_ZONA_1): continue
        if rect.inflate(MIN_MEZERA, MIN_MEZERA).colliderect(SAFE_ZONA_2): continue
        if any(rect.inflate(MIN_MEZERA, MIN_MEZERA).colliderect(p.inflate(MIN_MEZERA, MIN_MEZERA)) for p in prekazky):
            continue
        prekazky.append(rect)
    return prekazky


def generuj_portaly():
    res     = []
    pouzite = []
    pokusy  = 0
    while len(res) < 2 and pokusy < 300:
        pokusy += 1
        volne = [z for z in range(4) if z not in pouzite]
        if not volne:
            break
        zed = random.choice(volne)
        if   zed == 0: r = pygame.Rect(0, random.randrange(50, ROZLISENI_Y - PORTAL_DELKA - 50, 10), PORTAL_SIRKA, PORTAL_DELKA)
        elif zed == 1: r = pygame.Rect(ROZLISENI_X - PORTAL_SIRKA, random.randrange(50, ROZLISENI_Y - PORTAL_DELKA - 50, 10), PORTAL_SIRKA, PORTAL_DELKA)
        elif zed == 2: r = pygame.Rect(random.randrange(50, ROZLISENI_X - PORTAL_DELKA - 50, 10), 0, PORTAL_DELKA, PORTAL_SIRKA)
        else:          r = pygame.Rect(random.randrange(50, ROZLISENI_X - PORTAL_DELKA - 50, 10), ROZLISENI_Y - PORTAL_SIRKA, PORTAL_DELKA, PORTAL_SIRKA)
        if r.inflate(20, 20).colliderect(SAFE_ZONA_1): continue
        if r.inflate(20, 20).colliderect(SAFE_ZONA_2): continue
        res.append({"rect": r, "zed": zed})
        pouzite.append(zed)
    return res


def generuj_zbran():
    """Vygeneruje zbran na nahodnem miste na mape, mimo prekazky a safe zony."""
    for _ in range(300):
        x = random.randrange(80, ROZLISENI_X - 80)
        y = random.randrange(80, ROZLISENI_Y - 80)
        r = pygame.Rect(x, y, 40, 40)
        if r.colliderect(SAFE_ZONA_1) or r.colliderect(SAFE_ZONA_2):
            continue
        if any(r.inflate(20, 20).colliderect(p) for p in prekazky_recty):
            continue
        return {"x": x, "y": y, "rect": r}
    return None


# ═══════════════════════════════════════════════════════════════════════════════
# LOGIKA
# ═══════════════════════════════════════════════════════════════════════════════
def aplikuj_skin():
    global hrac1_barva, hrac2_barva
    hrac1_barva = SKINY[aktivni_skin]["barva1"]
    hrac2_barva = SKINY[aktivni_skin]["barva2"]


def kup_skin(index):
    global mince, aktivni_skin
    if index in koupeno:
        aktivni_skin = index
        aplikuj_skin()
    elif mince >= SKINY[index]["cena"]:
        mince -= SKINY[index]["cena"]
        koupeno.add(index)
        aktivni_skin = index
        aplikuj_skin()


def reset_game():
    global hrac1_x, hrac1_y, hrac2_x, hrac2_y, manualni_posun
    global prekazky_recty, portaly, portal_cooldown
    global zbran_na_mape, zbran_hrac, sit_projektily
    global hra_bezi, game_over_obrazovka
    global losovani_obrazovka, los_cas, los_speed, los_done, los_kdo, los_fin_cas, hunter

    hrac1_x, hrac1_y = 20, 520
    hrac2_x, hrac2_y = 720, 20
    manualni_posun   = 10
    prekazky_recty   = generuj_prekazky()
    portaly          = generuj_portaly()
    portal_cooldown  = {}
    zbran_hrac       = None
    sit_projektily   = []
    zbran_na_mape    = generuj_zbran()
    aplikuj_skin()

    # Kasino – predurci vysledek, ale zobrazuj animaci
    hunter      = random.choice([1, 2])
    los_cas     = pygame.time.get_ticks()
    los_speed   = 80
    los_done    = False
    los_kdo     = random.choice([1, 2])
    los_fin_cas = 0

    hra_bezi            = False
    game_over_obrazovka = False
    losovani_obrazovka  = True


def zpet_do_menu():
    global hlavni_nabidka, hra_bezi, game_over_obrazovka, obchod_obrazovka, losovani_obrazovka
    hlavni_nabidka      = True
    hra_bezi            = False
    game_over_obrazovka = False
    obchod_obrazovka    = False
    losovani_obrazovka  = False
    # Vrat lobby hudbu
    try:
        pygame.mixer.music.load("lobby_music.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    except Exception:
        pass


def aktualizuj_losovani():
    """Animace kasinoveho losovani – postupne zpomaluje a odhali huntera."""
    global los_cas, los_speed, los_done, los_kdo, los_fin_cas, losovani_obrazovka, hra_bezi

    if los_done:
        if pygame.time.get_ticks() - los_fin_cas > 2600:
            losovani_obrazovka = False
            hra_bezi = True
        return

    now = pygame.time.get_ticks()
    if now - los_cas >= los_speed:
        los_cas   = now
        los_kdo   = 3 - los_kdo           # prepina mezi 1 a 2
        los_speed = min(int(los_speed * 1.22), 720)
        if los_speed >= 720:
            los_kdo     = hunter
            los_done    = True
            los_fin_cas = now


def teleportuj_hrace(hrac_id, hx, hy):
    now = pygame.time.get_ticks()
    if portal_cooldown.get(hrac_id, 0) > now:
        return None
    hrac_rect = pygame.Rect(hx, hy, velikost, velikost)
    for i, p in enumerate(portaly):
        if hrac_rect.colliderect(p["rect"]):
            cil = portaly[1 - i]
            cx  = max(0, min(ROZLISENI_X - velikost, cil["rect"].centerx - velikost // 2))
            cy  = max(0, min(ROZLISENI_Y - velikost, cil["rect"].centery - velikost // 2))
            portal_cooldown[hrac_id] = now + 800
            return (cx, cy)
    return None


def vystrel_sit(hrac_id):
    """Vystrel sit s aimbotem – automaticky namiri na soupere."""
    if zbran_hrac != hrac_id:
        return
    if hrac_id == 1:
        sx, sy = hrac1_x + velikost // 2, hrac1_y + velikost // 2
        tx, ty = hrac2_x + velikost // 2, hrac2_y + velikost // 2
    else:
        sx, sy = hrac2_x + velikost // 2, hrac2_y + velikost // 2
        tx, ty = hrac1_x + velikost // 2, hrac1_y + velikost // 2

    dist = math.hypot(tx - sx, ty - sy)
    if dist == 0:
        return
    vx = (tx - sx) / dist * SIT_RYCHLOST
    vy = (ty - sy) / dist * SIT_RYCHLOST
    sit_projektily.append({
        "x": float(sx - SIT_VEL // 2),
        "y": float(sy - SIT_VEL // 2),
        "vx": vx,
        "vy": vy,
        "rect": pygame.Rect(int(sx - SIT_VEL // 2), int(sy - SIT_VEL // 2), SIT_VEL, SIT_VEL),
        "owner": hrac_id,
    })


def pohyb_hracu():
    global hrac1_x, hrac1_y, hrac2_x, hrac2_y
    global game_over_obrazovka, hra_bezi, mince
    global zbran_hrac, zbran_na_mape

    k = pygame.key.get_pressed()

    # Hrac 1 (WASD)
    sx1, sy1 = hrac1_x, hrac1_y
    if k[pygame.K_d]: hrac1_x += manualni_posun
    if k[pygame.K_a]: hrac1_x -= manualni_posun
    if k[pygame.K_s]: hrac1_y += manualni_posun
    if k[pygame.K_w]: hrac1_y -= manualni_posun
    if any(pygame.Rect(hrac1_x, hrac1_y, velikost, velikost).colliderect(p) for p in prekazky_recty):
        hrac1_x, hrac1_y = sx1, sy1
    hrac1_x = max(0, min(ROZLISENI_X - velikost, hrac1_x))
    hrac1_y = max(0, min(ROZLISENI_Y - velikost, hrac1_y))

    # Hrac 2 (sipky)
    sx2, sy2 = hrac2_x, hrac2_y
    if k[pygame.K_RIGHT]: hrac2_x += manualni_posun
    if k[pygame.K_LEFT]:  hrac2_x -= manualni_posun
    if k[pygame.K_DOWN]:  hrac2_y += manualni_posun
    if k[pygame.K_UP]:    hrac2_y -= manualni_posun
    if any(pygame.Rect(hrac2_x, hrac2_y, velikost, velikost).colliderect(p) for p in prekazky_recty):
        hrac2_x, hrac2_y = sx2, sy2
    hrac2_x = max(0, min(ROZLISENI_X - velikost, hrac2_x))
    hrac2_y = max(0, min(ROZLISENI_Y - velikost, hrac2_y))

    # Portaly
    v1 = teleportuj_hrace(1, hrac1_x, hrac1_y)
    if v1: hrac1_x, hrac1_y = v1
    v2 = teleportuj_hrace(2, hrac2_x, hrac2_y)
    if v2: hrac2_x, hrac2_y = v2

    # Sebrat zbran
    if zbran_na_mape and zbran_hrac is None:
        r1 = pygame.Rect(hrac1_x, hrac1_y, velikost, velikost)
        r2 = pygame.Rect(hrac2_x, hrac2_y, velikost, velikost)
        if r1.colliderect(zbran_na_mape["rect"]):
            zbran_hrac = 1
            zbran_na_mape = None
        elif r2.colliderect(zbran_na_mape["rect"]):
            zbran_hrac = 2
            zbran_na_mape = None

    # Pohyb site (projektily)
    for proj in sit_projektily[:]:
        proj["x"] += proj["vx"]
        proj["y"] += proj["vy"]
        proj["rect"].topleft = (int(proj["x"]), int(proj["y"]))
        # Out of bounds
        if (proj["rect"].right < 0 or proj["rect"].left > ROZLISENI_X or
                proj["rect"].bottom < 0 or proj["rect"].top > ROZLISENI_Y):
            sit_projektily.remove(proj)
            continue
        # Kolize s prekazkami
        if any(proj["rect"].colliderect(p) for p in prekazky_recty):
            sit_projektily.remove(proj)
            continue
        # Zasah soupere
        cil = (pygame.Rect(hrac2_x, hrac2_y, velikost, velikost)
               if proj["owner"] == 1
               else pygame.Rect(hrac1_x, hrac1_y, velikost, velikost))
        if proj["rect"].colliderect(cil):
            sit_projektily.remove(proj)
            if chycen_zvuk:   chycen_zvuk.play()
            if gameover_zvuk: gameover_zvuk.play()
            mince += 10
            game_over_obrazovka = True
            hra_bezi = False
            return

    # Prima kolize hracu
    r1 = pygame.Rect(hrac1_x, hrac1_y, velikost, velikost)
    r2 = pygame.Rect(hrac2_x, hrac2_y, velikost, velikost)
    if r1.colliderect(r2):
        if chycen_zvuk:   chycen_zvuk.play()
        if gameover_zvuk: gameover_zvuk.play()
        mince += 10
        game_over_obrazovka = True
        hra_bezi = False


# ═══════════════════════════════════════════════════════════════════════════════
# VYKRESLOVANI – pomocna funkce pro hrace
# ═══════════════════════════════════════════════════════════════════════════════
def kresli_hrace(x, y, barva):
    """Vykresli hrace – pokud skin ma obrazek, zobrazi ho s barevnym ramenem."""
    img = SKINY[aktivni_skin]["img"]
    if img:
        scaled = pygame.transform.scale(img, (velikost, velikost))
        okno.blit(scaled, (x, y))
        pygame.draw.rect(okno, barva, (x, y, velikost, velikost), 4)
    else:
        pygame.draw.rect(okno, barva, (x, y, velikost, velikost))


# ═══════════════════════════════════════════════════════════════════════════════
# OBRAZOVKY
# ═══════════════════════════════════════════════════════════════════════════════
def vykresli_menu():
    okno.blit(mainscreen, (0, 0))
    f100 = pygame.font.Font(None, 100)
    f50  = pygame.font.Font(None, 50)
    f34  = pygame.font.Font(None, 34)

    t = f100.render("HRA NA BABU", True, (255, 255, 255))
    okno.blit(t, t.get_rect(center=(400, 200)))

    pygame.draw.rect(okno, (0, 200, 0), play_tlacitko, border_radius=10)
    pygame.draw.rect(okno, (255, 255, 255), play_tlacitko, 3, border_radius=10)
    pt = f50.render("PLAY", True, (255, 255, 255))
    okno.blit(pt, pt.get_rect(center=play_tlacitko.center))

    pygame.draw.rect(okno, (239, 255, 39), shop_tlacitko, border_radius=10)
    pygame.draw.rect(okno, (255, 255, 255), shop_tlacitko, 3, border_radius=10)
    okno.blit(cart, cart.get_rect(center=shop_tlacitko.center))

    okno.blit(f34.render(f"Mince: {mince}", True, (255, 220, 80)), (10, 10))


def vykresli_hru():
    # Podlaha
    for y in range(0, 600, 100):
        for x in range(0, 800, 100):
            okno.blit(podlaha, (x, y))

    # Portaly
    for i, portal in enumerate(portaly):
        img = PORTAL_IMG_A if i == 0 else PORTAL_IMG_B
        rot = {0: -90, 1: 90, 2: 0, 3: 0}.get(portal["zed"], 0)
        rotated = pygame.transform.rotate(img, rot) if rot else img
        scaled  = pygame.transform.scale(rotated, (portal["rect"].width, portal["rect"].height))
        okno.blit(scaled, portal["rect"].topleft)

    # Prekazky
    for rect in prekazky_recty:
        for ox in range(0, rect.w, 50):
            for oy in range(0, rect.h, 50):
                okno.blit(zdi, (rect.x + ox, rect.y + oy))

    # Zbran na mape
    if zbran_na_mape:
        zx, zy = zbran_na_mape["x"], zbran_na_mape["y"]
        # Zluta karta s blikajicim efektem
        pulse   = int(abs(math.sin(pygame.time.get_ticks() / 300)) * 40)
        zbr_clr = (215 + pulse, 200 + pulse, 0)
        pygame.draw.rect(okno, zbr_clr, (zx, zy, 40, 40), border_radius=6)
        pygame.draw.rect(okno, (180, 130, 0), (zx, zy, 40, 40), 3, border_radius=6)
        f = pygame.font.Font(None, 20)
        t = f.render("NET", True, (0, 0, 0))
        okno.blit(t, t.get_rect(center=(zx + 20, zy + 20)))

    # Sitove projektily (ctverecek s mrizkou)
    for proj in sit_projektily:
        r = proj["rect"]
        pygame.draw.rect(okno, (80, 200, 255), r)
        pygame.draw.rect(okno, (0, 100, 200), r, 3)
        step = SIT_VEL // 3
        for gx in range(r.x, r.x + SIT_VEL + 1, step):
            pygame.draw.line(okno, (0, 100, 200), (gx, r.y), (gx, r.y + SIT_VEL))
        for gy in range(r.y, r.y + SIT_VEL + 1, step):
            pygame.draw.line(okno, (0, 100, 200), (r.x, gy), (r.x + SIT_VEL, gy))

    # Hraci
    kresli_hrace(hrac1_x, hrac1_y, hrac1_barva)
    kresli_hrace(hrac2_x, hrac2_y, hrac2_barva)

    # HUD
    f28 = pygame.font.Font(None, 28)
    h1r = "[HUNTER]" if hunter == 1 else "[PREY]"
    h2r = "[HUNTER]" if hunter == 2 else "[PREY]"
    c1  = (255, 60, 60) if hunter == 1 else (60, 255, 100)
    c2  = (255, 60, 60) if hunter == 2 else (60, 255, 100)
    okno.blit(f28.render(f"P1 {h1r}", True, c1), (10, 10))
    okno.blit(f28.render(f"P2 {h2r}", True, c2), (10, 40))
    if zbran_hrac:
        klav = "MEZERNIK" if zbran_hrac == 1 else "ENTER"
        okno.blit(f28.render(f"P{zbran_hrac} drzi SIT! [{klav}] = Vystrel", True, (255, 220, 0)), (10, 70))
    okno.blit(f28.render(f"Mince: {mince}", True, (255, 220, 80)), (ROZLISENI_X - 155, 10))


def vykresli_gameover():
    okno.blit(mainscreen, (0, 0))
    pygame.draw.rect(okno, (40, 40, 40), (200, 150, 400, 300))
    okno.blit(repete_screen, (200, 150))
    okno.blit(repete, (220, 380))
    okno.blit(home, (530, 380))
    t = pygame.font.Font(None, 74).render("GAME OVER", True, (255, 0, 0))
    okno.blit(t, t.get_rect(center=(400, 300)))


def vykresli_obchod():
    okno.blit(mainscreen, (0, 0))
    f34 = pygame.font.Font(None, 34)
    f28 = pygame.font.Font(None, 28)
    f26 = pygame.font.Font(None, 26)

    okno.blit(f34.render(f"Mince: {mince}", True, (255, 220, 80)), (10, 10))

    nadpis = f34.render("OBCHOD SE SKINY", True, (255, 255, 255))
    okno.blit(nadpis, nadpis.get_rect(center=(400, 45)))

    karta_w, karta_h = 220, 195
    mg = (ROZLISENI_X - 3 * karta_w) // 4  # margin

    for i in range(6):
        x = mg + (i % 3) * (karta_w + mg)
        y = 75 + (i // 3) * (karta_h + 18)
        aktivna = (i == aktivni_skin)
        bg = (30, 80, 30) if aktivna else (40, 40, 60)

        pygame.draw.rect(okno, bg, (x, y, karta_w, karta_h), border_radius=12)
        lem_clr = (255, 220, 80) if aktivna else (255, 255, 255)
        lem_w   = 3 if aktivna else 2
        pygame.draw.rect(okno, lem_clr, (x, y, karta_w, karta_h), lem_w, border_radius=12)

        # Preview – obrazek nebo barevne ctverecky
        prev = pygame.Rect(x + 8, y + 8, karta_w - 16, karta_h - 70)
        img  = SKINY[i]["img"]
        if img:
            scaled = pygame.transform.scale(img, (prev.width, prev.height))
            okno.blit(scaled, prev)
        else:
            hw = (prev.width - 4) // 2
            pygame.draw.rect(okno, SKINY[i]["barva1"], (prev.x,          prev.y, hw, prev.height), border_radius=6)
            pygame.draw.rect(okno, SKINY[i]["barva2"], (prev.x + hw + 4, prev.y, hw, prev.height), border_radius=6)

        # Nazev
        nt = f28.render(SKINY[i]["nazev"], True, (255, 255, 255))
        okno.blit(nt, nt.get_rect(center=(x + karta_w // 2, y + karta_h - 52)))

        # Status / cena
        if aktivna:
            st = f26.render("* AKTIVNI *", True, (255, 220, 80))
        elif i in koupeno:
            st = f26.render("KOUPENO", True, (100, 255, 100))
        elif SKINY[i]["cena"] == 0:
            st = f26.render("ZDARMA", True, (100, 255, 100))
        else:
            st = f26.render(f"{SKINY[i]['cena']} minci", True, (255, 200, 50))
        okno.blit(st, st.get_rect(center=(x + karta_w // 2, y + karta_h - 22)))

    pygame.draw.rect(okno, (100, 40, 40), zpet_tlacitko, border_radius=8)
    pygame.draw.rect(okno, (255, 255, 255), zpet_tlacitko, 2, border_radius=8)
    zt = f34.render("<- ZPET", True, (255, 255, 255))
    okno.blit(zt, zt.get_rect(center=zpet_tlacitko.center))


def vykresli_losovani():
    """Kasino animace vyberu huntera."""
    okno.blit(mainscreen, (0, 0))
    overlay = pygame.Surface((ROZLISENI_X, ROZLISENI_Y))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    okno.blit(overlay, (0, 0))

    f80 = pygame.font.Font(None, 80)
    f50 = pygame.font.Font(None, 50)
    f36 = pygame.font.Font(None, 36)

    title = f80.render("KDO JE HUNTER?", True, (255, 220, 80))
    okno.blit(title, title.get_rect(center=(400, 100)))

    # Dve karticky – Hrac 1 a Hrac 2
    for idx, (bx, label, hrac_id) in enumerate([(80, "HRAC 1", 1), (480, "HRAC 2", 2)]):
        aktivni = (los_kdo == hrac_id)
        if aktivni and not los_done:
            pulse  = int(abs(math.sin(pygame.time.get_ticks() / 120)) * 50)
            bg_col = (min(255, 190 + pulse), 30, 30)
            lem    = (255, 220, 80)
        elif aktivni and los_done:
            bg_col = (180, 30, 30)
            lem    = (255, 220, 80)
        else:
            bg_col = (45, 45, 75)
            lem    = (120, 120, 160)

        pygame.draw.rect(okno, bg_col, (bx, 160, 240, 230), border_radius=18)
        pygame.draw.rect(okno, lem,    (bx, 160, 240, 230), 4, border_radius=18)

        lt = f50.render(label, True, (255, 255, 255))
        okno.blit(lt, lt.get_rect(center=(bx + 120, 250)))

        # Mini preview skinu
        skin_img = SKINY[aktivni_skin]["img"]
        if skin_img:
            si = pygame.transform.scale(skin_img, (64, 64))
            okno.blit(si, (bx + 88, 165))
        else:
            barva = hrac1_barva if hrac_id == 1 else hrac2_barva
            pygame.draw.rect(okno, barva, (bx + 88, 165, 64, 64), border_radius=8)

        if aktivni:
            ht = f36.render(">> HUNTER <<", True, (255, 220, 80))
            okno.blit(ht, ht.get_rect(center=(bx + 120, 350)))

    if los_done:
        rt = f50.render(f"HRAC {hunter} JDE CHYTAT!", True, (255, 220, 80))
        okno.blit(rt, rt.get_rect(center=(400, 450)))
        st = f36.render("Hra zacina za chvili...", True, (200, 200, 200))
        okno.blit(st, st.get_rect(center=(400, 510)))
    else:
        spin = f36.render("Losovani...", True, (180, 180, 180))
        okno.blit(spin, spin.get_rect(center=(400, 440)))


# ═══════════════════════════════════════════════════════════════════════════════
# INICIALIZACE (pred hlavni smyckou)
# ═══════════════════════════════════════════════════════════════════════════════
prekazky_recty = generuj_prekazky()
portaly        = generuj_portaly()


# ═══════════════════════════════════════════════════════════════════════════════
# HLAVNI SMYCKA
# ═══════════════════════════════════════════════════════════════════════════════
while True:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if udalost.type == pygame.MOUSEBUTTONDOWN:
            pos = udalost.pos

            if hlavni_nabidka and not obchod_obrazovka:
                if play_tlacitko.collidepoint(pos):
                    hlavni_nabidka = False
                    reset_game()
                elif shop_tlacitko.collidepoint(pos):
                    hlavni_nabidka = False
                    obchod_obrazovka = True

            elif obchod_obrazovka:
                if zpet_tlacitko.collidepoint(pos):
                    zpet_do_menu()
                else:
                    kw, kh = 220, 195
                    mg = (ROZLISENI_X - 3 * kw) // 4
                    for i in range(6):
                        x = mg + (i % 3) * (kw + mg)
                        y = 75 + (i // 3) * (kh + 18)
                        if pygame.Rect(x, y, kw, kh).collidepoint(pos):
                            kup_skin(i)

            elif game_over_obrazovka:
                if repeat_tlacitko.collidepoint(pos):
                    reset_game()
                elif home_tlacitko.collidepoint(pos):
                    zpet_do_menu()

        if udalost.type == pygame.KEYDOWN:
            if udalost.key == pygame.K_r and game_over_obrazovka:
                reset_game()
            # Vystrel site:  P1 = MEZERNIK,  P2 = ENTER
            if hra_bezi and not game_over_obrazovka:
                if udalost.key == pygame.K_SPACE and zbran_hrac == 1:
                    vystrel_sit(1)
                if udalost.key == pygame.K_RETURN and zbran_hrac == 2:
                    vystrel_sit(2)

    # Update
    if losovani_obrazovka:
        aktualizuj_losovani()

    if hra_bezi and not game_over_obrazovka:
        pohyb_hracu()

    # Vykresli spravnou obrazovku
    if hlavni_nabidka:
        vykresli_menu()
    elif obchod_obrazovka:
        vykresli_obchod()
    elif losovani_obrazovka:
        vykresli_losovani()
    elif hra_bezi and not game_over_obrazovka:
        vykresli_hru()
    elif game_over_obrazovka:
        vykresli_gameover()

    clock.tick(FPS)
    pygame.display.flip()
