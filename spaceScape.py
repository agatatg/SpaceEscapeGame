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
#Som de power-up:
#  Fonte: https://pixabay.com/sound-effects/power-up-type-1-230548/
#Som de colisão:
#  Fonte: https://pixabay.com/sound-effects/stab-f-01-brvhrtz-224599/

import pygame
import random
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
pygame.display.set_caption("🚀 Space Escape")

ASSETS = {
    "background": "fundo_espacial.png",
    "player": "nave001.png",
    "meteor": "meteoro001.png",
    "sound_powerup": "power-up-type-1-230548.mp3",
    "sound_hit": "stab-f-01-brvhrtz-224599.mp3",
    "music": "cool-hip-hop-loop-275527.mp3"
}

WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (60, 100, 255)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

def load_image(filename, fallback_color, size=None):
    if os.path.exists(filename):
        img = pygame.image.load(filename).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
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

if os.path.exists(ASSETS["music"]):
    pygame.mixer.music.load(ASSETS["music"])
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))
player_speed = 7

meteor_list = []
for _ in range(5):
    x = random.randint(0, WIDTH - 40)
    y = random.randint(-500, -40)
    meteor_list.append(pygame.Rect(x, y, 40, 40))
meteor_speed = 5

POWERUP_SIZE = 40
powerup_rect = pygame.Rect(
    random.randint(0, WIDTH - POWERUP_SIZE),
    random.randint(-800, -400),
    POWERUP_SIZE,
    POWERUP_SIZE
)
powerup_speed = 4

score = 0
lives = 3
running = True

while running:
    clock.tick(FPS)
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += player_speed

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

    powerup_rect.y += powerup_speed

    if powerup_rect.y > HEIGHT:
        powerup_rect.x = random.randint(0, WIDTH - POWERUP_SIZE)
        powerup_rect.y = random.randint(-500, -40)

    if player_rect.colliderect(powerup_rect):
        if sound_powerup:
            sound_powerup.play()
        powerup_rect.x = random.randint(0, WIDTH - POWERUP_SIZE)
        powerup_rect.y = random.randint(-500, -40)

    screen.blit(player_img, player_rect)

    for meteor in meteor_list:
        screen.blit(meteor_img, meteor)

    pygame.draw.rect(screen, YELLOW, powerup_rect)

    text = font.render(f"Pontos: {score}   Vidas: {lives}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()

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
