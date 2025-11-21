##############################################################
###               S P A C E     E S C A P E                ###
##############################################################
###                  versao Alpha 0.3                      ###
##############################################################
### Objetivo: desviar dos meteoros que caem.               ###
### Cada colisão tira uma vida. Sobreviva o máximo que     ###
### conseguir!                                             ###
##############################################################
### Prof. Filipo Novo Mor - github.com/ProfessorFilipo     ###
##############################################################
# Música de fundo:
# Título: Cool Hip-Hop Loop
# Autor: Serge Quadrado
# Fonte: https://pixabay.com/sound-effects/cool-hip-hop-loop-275527/
# Licença: Pixabay Content License
# Som de power-up:
# Fonte: https://pixabay.com/sound-effects/power-up-type-1-230548/
# Som de colisão:
# Fonte: https://pixabay.com/sound-effects/stab-f-01-brvhrtz-224599/
# Imagens dos meteoros:
# blaze.png, firetex3.png, sun.png  — autor: FacadeGaikan, baixado de OpenGameArt.org

import pygame
import random
import os

pygame.init()

# ----------------------------------------------------------
# 🔧 CONFIGURAÇÕES GERAIS DO JOGO
# ----------------------------------------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60
pygame.display.set_caption("🚀 Space Escape")

# ----------------------------------------------------------
# 🧩 ASSETS
# ----------------------------------------------------------
ASSETS = {
    "background": "fundo_espacial.png",
    "player": "nave001.png",

    # FUNCIONALIDADE 8 — novos meteoros
    "meteor1": "blaze.png",
    "meteor2": "firetex3.png",
    "meteor3": "sun.png",
    "sound_point": "classic-game-action-positive-5-224402.mp3",
    "sound_hit": "stab-f-01-brvhrtz-224599.mp3",
    "sound_powerup": "power-up-type-1-230548.mp3",
    "music": "cool-hip-hop-loop-275527.mp3"
}
# ----------------------------------------------------------
# 🖼️ CARREGAMENTO DE IMAGENS E SONS
# ----------------------------------------------------------
# Cores para fallback (caso os arquivos não existam)
WHITE  = (255, 255, 255)
RED    = (255, 60, 60)
BLUE   = (60, 100, 255)
YELLOW = (255, 255, 0)
GREEN  = (0, 255, 0)
CYAN   = (0, 120, 255)

# Tela do jogo
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Função auxiliar para carregar imagens de forma segura
def load_image(filename, fallback_color, size=None):
    if os.path.exists(filename):
        img = pygame.image.load(filename).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    else:
        surf = pygame.Surface(size or (50, 50))
        surf.fill(fallback_color)
        return surf

# Carrega imagens
background = load_image(ASSETS["background"], WHITE, (WIDTH, HEIGHT))
player_img = load_image(ASSETS["player"], BLUE, (80, 60))

meteor_img1 = load_image(ASSETS["meteor1"], RED, (60, 60))
meteor_img2 = load_image(ASSETS["meteor2"], RED, (60, 60))
meteor_img3 = load_image(ASSETS["meteor3"], RED, (60, 60))

meteor_sprites = [meteor_img1, meteor_img2, meteor_img3]

# Sons
def load_sound(filename):
    if os.path.exists(filename):
        return pygame.mixer.Sound(filename)
    return None

sound_point   = load_sound(ASSETS["sound_point"])
sound_hit     = load_sound(ASSETS["sound_hit"])
sound_powerup = load_sound(ASSETS["sound_powerup"])
# Música de fundo (Funcionalidade 1)
if os.path.exists(ASSETS["music"]):
    pygame.mixer.music.load(ASSETS["music"])
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

# ----------------------------------------------------------
# 🧠 VARIÁVEIS DE JOGO
# ----------------------------------------------------------
player_rect = player_img.get_rect(center=(WIDTH//2, HEIGHT-60))
player_speed = 7

# Lista de meteoros com sprites diferentes (Funcionalidade 8)
meteor_list = []
for _ in range(5):
    x = random.randint(0, WIDTH-40)
    y = random.randint(-500, -40)
    rect = pygame.Rect(x, y, 40, 40)
    img = random.choice(meteor_sprites)
    meteor_list.append({"rect": rect, "img": img})

# Velocidade base dos meteoros
meteor_speed = 5

# 🔥 Funcionalidade 7 — Aumento progressivo da velocidade
speed_increase_timer = 0       # tempo desde o último aumento
SPEED_INCREASE_INTERVAL = 5000 # aumenta a cada 5 segundos
SPEED_INCREASE_AMOUNT = 0.3    # quanto aumenta por vez
MAX_METEOR_SPEED = 12          # limite máximo

score = 0
lives = 3
font = pygame.font.Font(None,36)
clock = pygame.time.Clock()
running = True

# ----------------------------------------------------------
# 🟨 POWER-UP (Funcionalidade 3 - som ao pegar)
# ----------------------------------------------------------
POWERUP_SIZE = 40
powerup_rect = pygame.Rect(
    random.randint(0,WIDTH-POWERUP_SIZE),
    random.randint(-800,-400),
    POWERUP_SIZE,
    POWERUP_SIZE
)
powerup_speed = 4

# ----------------------------------------------------------
# 🟩 POWER-UP VIDA EXTRA
# ----------------------------------------------------------
LIFE_POWERUP_SIZE = 40
life_powerup_rect = pygame.Rect(
    random.randint(0,WIDTH-LIFE_POWERUP_SIZE),
    random.randint(-1200,-600),
    LIFE_POWERUP_SIZE,
    LIFE_POWERUP_SIZE
)
life_powerup_speed = 3

# ----------------------------------------------------------
# 🔵 POWER-UP VELOCIDADE
# ----------------------------------------------------------
SPEED_POWERUP_SIZE = 40
speed_powerup_rect = pygame.Rect(
    random.randint(0,WIDTH-SPEED_POWERUP_SIZE),
    random.randint(-1500,-800),
    SPEED_POWERUP_SIZE,
    SPEED_POWERUP_SIZE
)
speed_powerup_speed = 3

speed_boost_active = False
speed_boost_timer = 0
NORMAL_SPEED = 7
BOOST_SPEED = 12

# ----------------------------------------------------------
# 🕹️ LOOP PRINCIPAL
# ----------------------------------------------------------
while running:
    clock.tick(FPS)
    screen.blit(background, (0,0))

    # EVENTOS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # MOVIMENTO JOGADOR
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += player_speed

    # MOVIMENTO METEOROS
    for meteor in meteor_list:
        rect = meteor["rect"]
        rect.y += meteor_speed
        # Saiu da tela → reposiciona e soma pontos (Funcionalidade 2 + som_point)
        if rect.y > HEIGHT:
            rect.y = random.randint(-120, -40)
            rect.x = random.randint(0, WIDTH - rect.width)
            score += 1
            if sound_point:
                sound_point.play()

        # Colisão com a nave (som de explosão ao morrer - Funcionalidade 2)
        if rect.colliderect(player_rect):
            lives -= 1
            rect.y = random.randint(-120, -40)
            rect.x = random.randint(0, WIDTH - rect.width)
            if sound_hit:
                sound_hit.play()
            if lives <= 0:
                running = False
    # --- Aumento Progressivo da Velocidade dos Meteoros (Funcionalidade 7) ---
    speed_update_now = pygame.time.get_ticks()
    if speed_update_now - speed_increase_timer >= SPEED_INCREASE_INTERVAL:
        speed_increase_timer = speed_update_now
        if meteor_speed < MAX_METEOR_SPEED:
            meteor_speed += SPEED_INCREASE_AMOUNT
            print(f"Velocidade dos meteoros aumentada para: {meteor_speed}")

    # --- Movimento do power-up normal ---
    powerup_rect.y += powerup_speed
    if powerup_rect.y > HEIGHT:
        powerup_rect.x = random.randint(0, WIDTH - POWERUP_SIZE)
        powerup_rect.y = random.randint(-600, -300)

    # Colisão com o power-up normal (som de power-up - Funcionalidade 3)
    if player_rect.colliderect(powerup_rect):
        if sound_powerup:
            sound_powerup.play()
        powerup_rect.x = random.randint(0, WIDTH - POWERUP_SIZE)
        powerup_rect.y = random.randint(-600, -300)

    # POWER-UP VIDA EXTRA
    life_powerup_rect.y += life_powerup_speed
    if life_powerup_rect.y > HEIGHT:
        life_powerup_rect.x = random.randint(0, WIDTH - LIFE_POWERUP_SIZE)
        life_powerup_rect.y = random.randint(-900, -400)

    # Colisão com power-up de vida extra (Funcionalidade 5)
    if player_rect.colliderect(life_powerup_rect):
        lives = min(lives+1,5)
        if sound_powerup:
            sound_powerup.play()
        life_powerup_rect.x = random.randint(0, WIDTH - LIFE_POWERUP_SIZE)
        life_powerup_rect.y = random.randint(-900, -400)

    # --- Movimento do power-up de velocidade ---
    speed_powerup_rect.y += speed_powerup_speed
    if speed_powerup_rect.y > HEIGHT:
        speed_powerup_rect.x = random.randint(0, WIDTH - SPEED_POWERUP_SIZE)
        speed_powerup_rect.y = random.randint(-1500, -800)

    # Colisão com power-up de velocidade (Funcionalidade 6)
    if player_rect.colliderect(speed_powerup_rect):
        speed_boost_active = True
        speed_boost_timer = pygame.time.get_ticks()
        player_speed = BOOST_SPEED
        if sound_powerup:
            sound_powerup.play()
        speed_powerup_rect.x = random.randint(0,WIDTH-SPEED_POWERUP_SIZE)
        speed_powerup_rect.y = random.randint(-1500,-800)

    # DESATIVAR BOOST
    if speed_boost_active:
        if pygame.time.get_ticks() - speed_boost_timer >= 5000:
            speed_boost_active = False
            player_speed = NORMAL_SPEED

    # DESENHO
    screen.blit(player_img, player_rect)
    for meteor in meteor_list:
        screen.blit(meteor["img"], meteor["rect"])

    pygame.draw.rect(screen, YELLOW, powerup_rect)
    pygame.draw.rect(screen, GREEN, life_powerup_rect)
    pygame.draw.rect(screen, CYAN, speed_powerup_rect)
    # Power-up de velocidade (azul/ciano)
    pygame.draw.rect(screen, CYAN, speed_powerup_rect)

    # --- Exibe pontuação e vidas (Funcionalidade 4) ---
    text = font.render(f"Pontos: {score}   Vidas: {lives}", True, WHITE)
    screen.blit(text, (10,10))

    pygame.display.flip()

# ----------------------------------------------------------
# GAME OVER
# ----------------------------------------------------------
pygame.mixer.music.stop()
screen.fill((20,20,20))
end_text = font.render("Fim de jogo! Pressione qualquer tecla para sair.", True,WHITE)
final_score = font.render(f"Pontuação final: {score}", True,WHITE)
screen.blit(end_text, (150,260))
screen.blit(final_score, (300,300))
pygame.display.flip()

waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            waiting = False

pygame.quit()