##############################################################
###               S P A C E     E S C A P E                ###
##############################################################
###                  versao Alpha 0.3  
############################################################
# CRÉDITOS DO ÁUDIO
#
# Música de fundo:
# Título: Classic Game Action - Positive
# Autor: Manu_Proso
# Fonte: https://pixabay.com/sound-effects/classic-game-action-positive-5-224402/
# Licença: Pixabay Content License 
#
# Som de power-up:
# Fonte: Pixabay (power-up-type-1-230548.mp3)
#
# Som de colisão:
# Fonte: Pixabay (stab-f-01-brvhrtz-224599.mp3)
#
##############################################################
### Objetivo: desviar dos meteoros que caem. Cada colisão   ###
### tira uma vida. Pegue power-ups para efeitos especiais.  ###
##############################################################

import pygame
import random
import os

pygame.init()

# ----------------------------------------------------------
# 🔧 CONFIGURAÇÕES GERAIS DO JOGO
# ----------------------------------------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60
pygame.display.set_caption("🚀 Space Escape – versão do grupo 3")

# ----------------------------------------------------------
# 🧩 SEÇÃO DE ASSETS
# ----------------------------------------------------------

ASSETS = {
    "background": "fundo_espacial.png",
    "player": "nave001.png",
    "meteor": "meteoro001.png",
    "sound_powerup": "power-up-type-1-230548.mp3",
    "sound_hit": "stab-f-01-brvhrtz-224599.mp3",
    "music": "classic-game-action-positive-5-224402.mp3"
}

# ----------------------------------------------------------
# 🖼️ CARREGAMENTO DE IMAGENS E SONS
# ----------------------------------------------------------

WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (60, 100, 255)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

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

background = load_image(ASSETS["background"], WHITE, (WIDTH, HEIGHT))
player_img = load_image(ASSETS["player"], BLUE, (80, 60))
meteor_img = load_image(ASSETS["meteor"], RED, (40, 40))

def load_sound(filename):
    if os.path.exists(filename):
        return pygame.mixer.Sound(filename)
    return None

sound_hit = load_sound(ASSETS["sound_hit"])
sound_powerup = load_sound(ASSETS["sound_powerup"])

# Música de fundo
if os.path.exists(ASSETS["music"]):
    pygame.mixer.music.load(ASSETS["music"])
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

# ----------------------------------------------------------
# 🧠 VARIÁVEIS DO JOGO
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
# 🟦 VARIÁVEIS DO POWER-UP (FUNCIONALIDADE 3)
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
# 🕹️ LOOP PRINCIPAL
# ----------------------------------------------------------
while running:
    clock.tick(FPS)
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimento do jogador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += player_speed

    # Movimento dos meteoros
    for meteor in meteor_list:
        meteor.y += meteor_speed

        if meteor.y > HEIGHT:
            meteor.y = random.randint(-100, -40)
            meteor.x = random.randint(0, WIDTH - meteor.width)
            score += 1

        if meteor.colliderect(player_rect):

            #SOM DE EXPLOSÃO
            if sound_hit:
                sound_hit.play()

            #EFEITO VISUAL: piscar o jogador rapidamente
            for _ in range(3):
                screen.blit(background, (0, 0))
                for m in meteor_list:
                    screen.blit(meteor_img, m)
                # pisca vermelho
                flash = pygame.Surface(player_rect.size)
                flash.fill((255, 50, 50))
                screen.blit(flash, player_rect)
                pygame.display.flip()
                pygame.time.delay(80)

                screen.blit(background, (0, 0))
                for m in meteor_list:
                    screen.blit(meteor_img, m)
                # pisca normal
                screen.blit(player_img, player_rect)
                pygame.display.flip()
                pygame.time.delay(80)

            #reduzir vidas
            lives -= 1

            # reposiciona meteoro
            meteor.y = random.randint(-100, -40)
            meteor.x = random.randint(0, WIDTH - meteor.width)

            if lives <= 0:
                running = False

    # Movimento do power-up
    powerup_rect.y += powerup_speed

    if powerup_rect.y > HEIGHT:
        powerup_rect.x = random.randint(0, WIDTH - POWERUP_SIZE)
        powerup_rect.y = random.randint(-500, -40)

    # Colisão com power-up
    if player_rect.colliderect(powerup_rect):
        if sound_powerup:
            sound_powerup.play()

        powerup_rect.x = random.randint(0, WIDTH - POWERUP_SIZE)
        powerup_rect.y = random.randint(-500, -40)

    # Desenho dos elementos
    screen.blit(player_img, player_rect)

    for meteor in meteor_list:
        screen.blit(meteor_img, meteor)

    pygame.draw.rect(screen, YELLOW, powerup_rect)

    text = font.render(f"Pontos: {score}   Vidas: {lives}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()

# ------------------------------------------------
