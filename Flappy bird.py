import pygame
import sys
import random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 560))  # floor_level = 80
    screen.blit(floor_surface, (floor_x_pos + 480, 560))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    # both pipes is apart 120 pixels
    top_pipe = pipe_surface.get_rect(midbottom=(500, random_pipe_pos - 140))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2   # pipes speed
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 640:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe_surface = pygame.transform.flip(
                pipe_surface, False, True)
            screen.blit(flip_pipe_surface, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 560:
        return False
    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(
            f'{score:.0f}', True, (255, 255, 255))  # white color
        score_rect = score_surface.get_rect(center=(240, 50))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(
            f'Score: {score:.0f}', True, (255, 255, 255))  # white color
        score_rect = score_surface.get_rect(center=(240, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(
            f'High score: {high_score:.0f}', True, (255, 255, 255))  # white color
        high_score_rect = high_score_surface.get_rect(center=(240, 530))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


# pygame.mixer.pre_init(frequency=44100, size=16, channels=2, buffer=512)
pygame.init()
pygame.display.set_caption('Flappy Bird')
icon = pygame.image.load('assets/bluebird-upflap.png')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((480, 640))
clock = pygame.time.Clock()  # To limit framerate
game_font = pygame.font.Font('04B_19.ttf', 40)

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
mainloop = True


# Score Variables
score = 0
high_score = 0


bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (480, 640))


floor_level = 80
floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (480, floor_level))
floor_x_pos = 0

bird_downflap = pygame.transform.scale(pygame.image.load(
    'assets/bluebird-downflap.png'), (40, 30)).convert_alpha()
bird_midflap = pygame.transform.scale(pygame.image.load(
    'assets/bluebird-midflap.png'), (40, 30)).convert_alpha()
bird_upflap = pygame.transform.scale(pygame.image.load(
    'assets/bluebird-upflap.png'), (40, 30)).convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 320))

BIRDFLAP = pygame.USEREVENT + 1  # Don't create the same kink of USEREVENT
pygame.time.set_timer(BIRDFLAP, 200)

# bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
# bird_surface = pygame.transform.scale(bird_surface, (40, 30)) # bird size 40x30
# bird_rect = bird_surface.get_rect(center=(100, 320))


pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale(pipe_surface, (60, 500))
# pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 350, 400, 480]


game_over_surface = pygame.transform.scale(pygame.image.load(
    'assets/message.png'), (200, 350)).convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(240, 280))


flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

while mainloop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6   # bird go up speed
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 320)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Bird movement
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Score
        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown == 0:
            score_sound.play()
            score_sound_countdown = 100

    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -480:  # to make surface continuously
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)  # 120 fps
