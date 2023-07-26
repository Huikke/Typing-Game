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
def letter_spawn():
    chars = "????ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    randchar = random.randint(4,29)
    char = chars[randchar]

    text_surf = pygame.font.SysFont(None, 500).render(char, False, "Black")
    text_rect = text_surf.get_rect(center = (400, 400))

    screen.blit(text_surf, text_rect)
    return randchar

# Update score by 1 and display it
# Takes parameter score and return score with +1
def score_handler(score):
    score += 1

    score_surf = pygame.font.SysFont(None, 100).render(str(score), False, "Black")
    score_rect = score_surf.get_rect(center = (400, 100))

    screen.blit(score_surf, score_rect)
    return score

# Gameplay variables
score = -1
next = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Logic behind the game
    if next == True:
        screen.fill((204, 190, 35))
        answer = letter_spawn()
        score = score_handler(score)
        next = False

    # Handles keyboard presses
    keys = pygame.key.get_pressed()
    for index, key in enumerate(keys):
        if key != False:
            if index == answer:
                next = True

    pygame.display.update()
    clock.tick(60)