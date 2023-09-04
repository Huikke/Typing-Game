# Hiragana game

import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
pygame.display.set_caption("Typing Game")

# Database
letters_dict = {"a": "あ", "i": "い", "u": "う", "e": "え", "o": "お"}

# Generate and display a letter into the game
# Is ran every time player presses the correct button
# Returns index which corresponds with pygame keyboard button for checking the answer
def char_spawn(letter=None):
    if letter == None:
        letter = random.choice(list(letters_dict.keys()))

    letter_surf = pygame.font.SysFont("msgothic", 500).render(letters_dict[letter], False, "Black")
    letter_rect = letter_surf.get_rect(center = (400, 400))
    screen.blit(letter_surf, letter_rect)

    return letter

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
score = 0
next = False
first = True
time = 30 # In seconds

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Generate the first character
        if first == True:
            answer = char_spawn()
            first = False

        # Handles keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                if answer == "a":
                    next = True
            elif event.key == pygame.K_i:
                if answer == "i":
                    next = True
            elif event.key == pygame.K_u:
                if answer == "u":
                    next = True
            elif event.key == pygame.K_e:
                if answer == "e":
                    next = True
            elif event.key == pygame.K_o:
                if answer == "o":
                    next = True

    # Screen background
    screen.fill((204, 190, 35))

    # If next is True, the game updates
    # Else blit the same view again
    if next == True:
        answer = char_spawn()
        score = score_handler(score, True)
        next = False
    else:
        answer = char_spawn(answer)
        score = score_handler(score, False)

    # When timer reaches zero, game ends
    remaining_time = timer()
    if remaining_time < 0:
        print("Final Score:", score)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    clock.tick(30)