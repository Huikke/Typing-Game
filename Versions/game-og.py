# Typing game

import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
pygame.display.set_caption("Typing Game")

# Generate and display a letter into the game
# Is ran every time player presses the correct button
# Returns index which corresponds with pygame keyboard button for checking the answer
def char_spawn(next, randchar=None):
    chars = "????ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if next:
        randchar = random.randint(4,29)
    char = chars[randchar]

    char_surf = pygame.font.SysFont(None, 500).render(char, False, "Black")
    char_rect = char_surf.get_rect(center = (400, 400))
    screen.blit(char_surf, char_rect)

    return randchar

# Update score by 1 and display it
# Takes parameter score and return score with +1
def score_handler(score, next):
    if next:
        score += 1

    score_surf = pygame.font.SysFont(None, 100).render(str(score), False, "Black")
    score_rect = score_surf.get_rect(center = (400, 100))
    screen.blit(score_surf, score_rect)

    return score

# Time limit in the game, game ends when remaining_time hits zero
# Returns remaining_time for the game to know when timer ends
def timer():
    current_time = int(pygame.time.get_ticks() / 10)
    remaining_time = time * 100 - current_time

    timer_surf = pygame.font.SysFont(None, 50).render(str(remaining_time), False, "Black")
    timer_rect = timer_surf.get_rect(topright = (800, 0))
    screen.blit(timer_surf,timer_rect)

    return remaining_time

# Gameplay variables
score = -1
next = True
time = 30 # In seconds

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Screen background
    screen.fill((204, 190, 35))

    # If next is True, the game updates
    # Else blit the same view again
    if next == True:
        answer = char_spawn(True)
        score = score_handler(score, True)
        next = False
    else:
        answer = char_spawn(False, answer)
        score = score_handler(score, False)
    
    # When timer reaches zero, game ends
    remaining_time = timer()
    if remaining_time < 0:
        print("Final Score:", score)
        pygame.quit()
        sys.exit()

    # Handles keyboard presses
    keys = pygame.key.get_pressed()
    for index, key in enumerate(keys):
        if key != False:
            if index == answer:
                next = True
    
    pygame.display.update()
    clock.tick(30)