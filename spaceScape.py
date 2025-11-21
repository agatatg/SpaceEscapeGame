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
#
# Som de power-up:
# Fonte: https://pixabay.com/sound-effects/power-up-type-1-230548/
#
# Som de colisão:
# Fonte: https://pixabay.com/sound-effects/stab-f-01-brvhrtz-224599/

import pygame
import random
import os

# Inicializa o PyGame
pygame.init()

# ----------------------------------------------------------
# 🔧 CONFIGURAÇÕES GERAIS DO JOGO
# ----------------------------------------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60
pygame.display.set_caption("🚀 Space Escape")

# ----------------------------------------------------------
# 🧩 SEÇÃO DE ASSETS (troque os arquivos de assets aqui)
# ----------------------------------------------------------
# Dica: coloque as imagens e sons na mesma pasta do arquivo .py
# e troque apenas os nomes abaixo.

ASSETS = {
    "background": "fundo_espacial.png",                         
    "player": "nave001.png",                                    
    "meteor": "meteoro001.png",                                 
    "sound_point": "classic-game-action-positive-5-224402.mp3",
    "sound_hit": "stab-f-01-brvhrtz-224599.mp3",
    "sound_powerup": "power-up-type-1-230548.mp3",
    "music": "cool-hip-hop-loop-275527.mp3"
}

# ----------------------------------------------------------
# 🖼️ CARREGAMENTO DE IMAGENS E SONS
# ----------------------------------------------------------
# Cores para fallback (caso os arquivos não existam)
WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (60, 100, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

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
meteor_img = load_image(ASSETS["meteor"], RED, (40, 40))

# Sons
def load_sound(filename):
    if os.path.exists(filename):
        return pygame.mixer.Sound(filename)
    return None

sound_point = load_sound(ASSETS["sound_point"])
sound_hit = load_sound(ASSETS["sound_hit"])
sound_powerup = load_sound(ASSETS["sound_powerup"])

# Música de fundo (opcional)
if os.path.exists(ASSETS["music"]):
    pygame.mixer.music.load(ASSETS["music"])
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)  # loop infinito

# ----------------------------------------------------------
# 🧠 VARIÁVEIS DE JOGO
# ----------------------------------------------------------
player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))
player_speed = 7

meteor_list = []
for _ in range(5):
    x = random.randint(0, WIDTH - 40)
    y = random.randint(-500, -40)
    meteor_list.append(pygame.Rect(x, y, 40, 40))

meteor_speed = 5
score = 0
lives = 3
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
running = True

# ----------------------------------------------------------
# 🟨 POWER-UP (Funcionalidade 3)
# ----------------------------------------------------------
POWERUP_SIZE = 40
powerup_rect = pygame.Rect(
    random.randint(0, WIDTH - POWERUP_SIZE),
    random.randint(-800, -400),
    POWERUP_SIZE,
    POWERUP_SIZE
)
powerup_speed = 4

# ----------------------------------------------------------
# 🟩 POWER-UP DE VIDA EXTRA (Funcionalidade 5)
# ----------------------------------------------------------
LIFE_POWERUP_SIZE = 40
life_powerup_rect = pygame.Rect(
    random.randint(0, WIDTH - LIFE_POWERUP_SIZE),
    random.randint(-1200, -600),
    LIFE_POWERUP_SIZE,
    LIFE_POWERUP_SIZE
)
life_powerup_speed = 3

# ----------------------------------------------------------
# 🔵 POWER-UP DE VELOCIDADE (Funcionalidade 6)
# ----------------------------------------------------------
SPEED_POWERUP_SIZE = 40
speed_powerup_rect = pygame.Rect(
    random.randint(0, WIDTH - SPEED_POWERUP_SIZE),
    random.randint(-1500, -800),
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
    screen.blit(background, (0, 0))

    # --- Eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Movimento do jogador ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += player_speed

    # --- Movimento dos meteoros ---
    for meteor in meteor_list:
        meteor.y += meteor_speed

        # Saiu da tela → reposiciona e soma pontos
        if meteor.y > HEIGHT:
            meteor.y = random.randint(-100, -40)
            meteor.x = random.randint(0, WIDTH - meteor.width)
            score += 1
            if sound_point:
                sound_point.play()

        # Colisão
        if meteor.colliderect(player_rect):
            lives -= 1
            meteor.y = random.randint(-100, -40)
            meteor.x = random.randint(0, WIDTH - meteor.width)
            if sound_hit:
                sound_hit.play()
            if lives <= 0:
                running = False

    # --- Movimento do power-up normal ---
    powerup_rect.y += powerup_speed
    if powerup_rect.y > HEIGHT:
        powerup_rect.x = random.randint(0, WIDTH - POWERUP_SIZE)
        powerup_rect.y = random.randint(-500, -40)

    # Colisão com o power-up normal
    if player_rect.colliderect(powerup_rect):
        if sound_powerup:
            sound_powerup.play()
        powerup_rect.x = random.randint(0, WIDTH - POWERUP_SIZE)
        powerup_rect.y = random.randint(-500, -40)

    # --- Movimento do power-up de vida extra ---
    life_powerup_rect.y += life_powerup_speed
    if life_powerup_rect.y > HEIGHT:
        life_powerup_rect.x = random.randint(0, WIDTH - LIFE_POWERUP_SIZE)
        life_powerup_rect.y = random.randint(-200, -40)

    # --- Movimento do power-up de velocidade ---
    speed_powerup_rect.y += speed_powerup_speed
    if speed_powerup_rect.y > HEIGHT:
        speed_powerup_rect.x = random.randint(0, WIDTH - SPEED_POWERUP_SIZE)
        speed_powerup_rect.y = random.randint(-1500, -800)

    # Colisão com power-up de vida extra
    if player_rect.colliderect(life_powerup_rect):
        lives = min(lives + 1, 5)  # limite de 5 vidas
        if sound_powerup:
            sound_powerup.play()
        life_powerup_rect.x = random.randint(0, WIDTH - LIFE_POWERUP_SIZE)
        life_powerup_rect.y = random.randint(-1200, -600)

    # Colisão com power-up de velocidade
    if player_rect.colliderect(speed_powerup_rect):
        speed_boost_active = True
        speed_boost_timer = pygame.time.get_ticks()
        player_speed = BOOST_SPEED
        if sound_powerup:
            sound_powerup.play()
        speed_powerup_rect.x = random.randint(0, WIDTH - SPEED_POWERUP_SIZE)
        speed_powerup_rect.y = random.randint(-1500, -800)

    # --- Controle do tempo do boost de velocidade ---
    if speed_boost_active:
        if pygame.time.get_ticks() - speed_boost_timer >= 5000:  # 5 segundos
            speed_boost_active = False
            player_speed = NORMAL_SPEED

    # --- Desenha tudo ---
    screen.blit(player_img, player_rect)
    for meteor in meteor_list:
        screen.blit(meteor_img, meteor)

    # Power-up normal (amarelo)
    pygame.draw.rect(screen, YELLOW, powerup_rect)

    # Power-up de vida extra (verde)
    pygame.draw.rect(screen, GREEN, life_powerup_rect)

    # Power-up de velocidade (azul)
    pygame.draw.rect(screen, (0, 120, 255), speed_powerup_rect)

    # --- Exibe pontuação e vidas ---
    text = font.render(f"Pontos: {score}   Vidas: {lives}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()

# ----------------------------------------------------------
# 🏁 TELA DE FIM DE JOGO
# ----------------------------------------------------------
pygame.mixer.music.stop()
screen.fill((20, 20, 20))
end_text = font.render("Fim de jogo! Pressione qualquer tecla para sair.", True, WHITE)
final_score = font.render(f"Pontuação final: {score}", True, WHITE)
screen.blit(end_text, (150, 260))
screen.blit(final_score, (300, 300))
pygame.display.flip()

waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            waiting = False

pygame.quit()
