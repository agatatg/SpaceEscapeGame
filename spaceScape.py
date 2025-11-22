##############################################################
###               S P A C E     E S C A P E                ###
##############################################################
###                  versao Alpha 0.4                      ###
##############################################################
### Funcionalidade 10 implementada: Tela de Game Over      ###
##############################################################

import pygame
import random
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
pygame.display.set_caption("🚀 Space Escape")

# ----------------------------------------------------------
# ASSETS
# ----------------------------------------------------------
ASSETS = {
    "background": "fundo_espacial.png",
    "player": "nave001.png",
    "meteor1": "blaze.png",
    "meteor2": "firetex3.png",
    "meteor3": "sun.png",
    "sound_point": "classic-game-action-positive-5-224402.mp3",
    "sound_hit": "stab-f-01-brvhrtz-224599.mp3",
    "sound_powerup": "power-up-type-1-230548.mp3",
    "music": "cool-hip-hop-loop-275527.mp3"
}

WHITE  = (255,255,255)
RED    = (255,60,60)
BLUE   = (60,100,255)
YELLOW = (255,255,0)
GREEN  = (0,255,0)
CYAN   = (0,120,255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# ----------------------------------------------------------
# FUNÇÕES AUXILIARES
# ----------------------------------------------------------
def load_image(filename, fallback_color, size=None):
    if os.path.exists(filename):
        img = pygame.image.load(filename).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    surf = pygame.Surface(size or (50,50))
    surf.fill(fallback_color)
    return surf

def load_sound(filename):
    if os.path.exists(filename):
        return pygame.mixer.Sound(filename)
    return None

# ----------------------------------------------------------
# CARREGA IMAGENS E SONS
# ----------------------------------------------------------
background = load_image(ASSETS["background"], WHITE, (WIDTH, HEIGHT))
player_img = load_image(ASSETS["player"], BLUE, (80,60))

meteor_img1 = load_image(ASSETS["meteor1"], RED, (60,60))
meteor_img2 = load_image(ASSETS["meteor2"], RED, (60,60))
meteor_img3 = load_image(ASSETS["meteor3"], RED, (60,60))
meteor_sprites = [meteor_img1, meteor_img2, meteor_img3]

sound_point   = load_sound(ASSETS["sound_point"])
sound_hit     = load_sound(ASSETS["sound_hit"])
sound_powerup = load_sound(ASSETS["sound_powerup"])

# Música
if os.path.exists(ASSETS["music"]):
    pygame.mixer.music.load(ASSETS["music"])
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

# ----------------------------------------------------------
# VARIÁVEIS GLOBAIS DO JOGO
# ----------------------------------------------------------
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Estados do jogo
game_state = "playing"

# ----------------------------------------------------------
# FUNÇÃO PARA RESETAR O JOGO (para reiniciar no Game Over)
# ----------------------------------------------------------
def reset_game():
    global player_rect, meteor_list, meteor_speed, score, lives
    global powerup_rect, life_powerup_rect, speed_powerup_rect
    global speed_boost_active, player_speed, speed_boost_timer
    global speed_increase_timer, game_state

    player_rect = player_img.get_rect(center=(WIDTH//2, HEIGHT-60))
    player_speed = 7

    meteor_list = []
    for _ in range(5):
        x = random.randint(0, WIDTH-40)
        y = random.randint(-500, -40)
        rect = pygame.Rect(x, y, 40, 40)
        img = random.choice(meteor_sprites)
        meteor_list.append({"rect": rect, "img": img})

    meteor_speed = 5
    score = 0
    lives = 3

    # Power-ups
    POWERUP_SIZE = 40
    powerup_rect.x = random.randint(0, WIDTH-POWERUP_SIZE)
    powerup_rect.y = random.randint(-800, -400)

    life_powerup_rect.y = random.randint(-1200, -600)
    speed_powerup_rect.y = random.randint(-1500, -800)

    speed_boost_active = False
    player_speed = 7
    speed_boost_timer = 0

    # Velocidade progressiva
    speed_increase_timer = pygame.time.get_ticks()

    game_state = "playing"


# ----------------------------------------------------------
# VARIÁVEIS INICIAIS DO JOGO
# ----------------------------------------------------------
player_rect = player_img.get_rect(center=(WIDTH//2, HEIGHT-60))
player_speed = 7

meteor_list = []
for _ in range(5):
    rect = pygame.Rect(random.randint(0, WIDTH-40),
                       random.randint(-500,-40),
                       40,40)
    img = random.choice(meteor_sprites)
    meteor_list.append({"rect": rect, "img": img})

meteor_speed = 5
speed_increase_timer = pygame.time.get_ticks()
SPEED_INCREASE_INTERVAL = 5000
SPEED_INCREASE_AMOUNT = 0.3
MAX_METEOR_SPEED = 12

score = 0
lives = 3

# Power-ups
POWERUP_SIZE = 40
powerup_rect = pygame.Rect(random.randint(0,WIDTH-POWERUP_SIZE),
                           random.randint(-800,-400),
                           POWERUP_SIZE,POWERUP_SIZE)
powerup_speed = 4

LIFE_POWERUP_SIZE = 40
life_powerup_rect = pygame.Rect(random.randint(0,WIDTH-LIFE_POWERUP_SIZE),
                                random.randint(-1200,-600),
                                LIFE_POWERUP_SIZE,LIFE_POWERUP_SIZE)
life_powerup_speed = 3

SPEED_POWERUP_SIZE = 40
speed_powerup_rect = pygame.Rect(random.randint(0,WIDTH-SPEED_POWERUP_SIZE),
                                 random.randint(-1500,-800),
                                 SPEED_POWERUP_SIZE,SPEED_POWERUP_SIZE)
speed_powerup_speed = 3

speed_boost_active = False
speed_boost_timer = 0
NORMAL_SPEED = 7
BOOST_SPEED = 12

paused = False
running = True

# ----------------------------------------------------------
# LOOP PRINCIPAL
# ----------------------------------------------------------
while running:
    clock.tick(FPS)
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Pausa
        if event.type == pygame.KEYDOWN:
            if game_state == "playing":
                if event.key == pygame.K_p:
                    paused = not paused

        # Controles do Game Over
        if game_state == "game_over":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    running = False

    # -----------------------------
    # ESTADO: PAUSADO
    # -----------------------------
    if paused and game_state == "playing":
        pause_text = font.render("Jogo Pausado - Pressione P para continuar", True, WHITE)
        screen.blit(pause_text, (120,250))
        pygame.display.flip()
        continue

    # -----------------------------
    # ESTADO: GAME OVER
    # -----------------------------
    if game_state == "game_over":
        screen.fill((0,0,0))
        over = font.render("GAME OVER", True, RED)
        score_text = font.render(f"Pontuação Final: {score}", True, WHITE)
        restart = font.render("Pressione R para reiniciar", True, WHITE)
        leave = font.render("Pressione ESC para sair", True, WHITE)

        screen.blit(over, (320,200))
        screen.blit(score_text, (290,260))
        screen.blit(restart, (250,320))
        screen.blit(leave, (270,360))

        pygame.display.flip()
        continue

    # -----------------------------
    # ESTADO: JOGO NORMAL
    # -----------------------------
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += player_speed

    # METEOROS
    for meteor in meteor_list:
        meteor["rect"].y += meteor_speed

        if meteor["rect"].y > HEIGHT:
            meteor["rect"].y = random.randint(-120,-40)
            meteor["rect"].x = random.randint(0,WIDTH-40)
            score += 1
            if sound_point: sound_point.play()

        # colisão
        if meteor["rect"].colliderect(player_rect):
            lives -= 1
            meteor["rect"].y = random.randint(-120,-40)
            meteor["rect"].x = random.randint(0,WIDTH-40)
            if sound_hit: sound_hit.play()

            if lives <= 0:
                game_state = "game_over"

    # aumento gradual
    now = pygame.time.get_ticks()
    if now - speed_increase_timer >= SPEED_INCREASE_INTERVAL:
        speed_increase_timer = now
        if meteor_speed < MAX_METEOR_SPEED:
            meteor_speed += SPEED_INCREASE_AMOUNT

    # POWER-UP NORMAL
    powerup_rect.y += powerup_speed
    if powerup_rect.y > HEIGHT:
        powerup_rect.y = random.randint(-600,-300)

    if player_rect.colliderect(powerup_rect):
        if sound_powerup: sound_powerup.play()
        powerup_rect.y = random.randint(-600,-300)

    # VIDA EXTRA
    life_powerup_rect.y += life_powerup_speed
    if life_powerup_rect.y > HEIGHT:
        life_powerup_rect.y = random.randint(-900,-400)

    if player_rect.colliderect(life_powerup_rect):
        lives = min(lives+1,5)
        if sound_powerup: sound_powerup.play()
        life_powerup_rect.y = random.randint(-900,-400)

    # POWER-UP VELOCIDADE
    speed_powerup_rect.y += speed_powerup_speed
    if speed_powerup_rect.y > HEIGHT:
        speed_powerup_rect.y = random.randint(-1500,-800)

    if player_rect.colliderect(speed_powerup_rect):
        speed_boost_active = True
        speed_boost_timer = pygame.time.get_ticks()
        player_speed = BOOST_SPEED
        if sound_powerup: sound_powerup.play()
        speed_powerup_rect.y = random.randint(-1500,-800)

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

    hud = font.render(f"Pontos: {score}   Vidas: {lives}", True, WHITE)
    screen.blit(hud, (10,10))

    pygame.display.flip()

pygame.quit()
