# Hiragana game

import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
pygame.display.set_caption("Typing Game")

# Database
letters_dict = {"a": "あ", "i": "い", "u": "う", "e": "え", "o": "お",
                "ka": "か", "ki": "き", "ku": "く", "ke": "け", "ko": "こ",
                "sa": "さ", "shi": "し", "su": "す", "se": "せ", "so": "そ",
                "ta": "た", "chi": "ち", "tsu": "つ", "te": "て", "to": "と",
                "na": "な", "ni": "に", "nu": "ぬ", "ne": "ね", "no": "の",
                "ha": "は", "hi": "ひ", "fu": "ふ", "he": "へ", "ho": "ほ",
                # ま,み,む,め,も,
                # や,ゆ,よ
                # ら,り,る,れ,ろ
                # わ,を,
                # ん
                }

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

# Creates input box below the letter
def input_box():
    text_box = pygame.Rect(350, 650, 80, 50)
    pygame.draw.rect(screen, "White", text_box)

    text_surf = pygame.font.SysFont(None, 50).render(input_text, False, "Black")
    screen.blit(text_surf, (text_box.x+10, text_box.y+10))

# Blit score
def score_handler(score):
    score_surf = pygame.font.SysFont(None, 100).render(str(score), False, "Black")
    score_rect = score_surf.get_rect(center = (400, 100))
    screen.blit(score_surf, score_rect)

# Time limit in the game, game ends when remaining_time hits zero
# Returns remaining_time for the game to know when timer ends
def timer():
    current_time = int(pygame.time.get_ticks() / 10)
    remaining_time = time_limit * 100 - current_time

    timer_surf = pygame.font.SysFont(None, 50).render(str(remaining_time), False, "Black")
    timer_rect = timer_surf.get_rect(topright = (800, 0))
    screen.blit(timer_surf, timer_rect)

    return remaining_time

def counter():
    counter_surf = pygame.font.SysFont(None, 50).render(str(count), False, "Black")
    counter_rect = counter_surf.get_rect(topright = (800, 0))
    screen.blit(counter_surf, counter_rect)

# Gameplay variables
mode = "count"
time_limit = 30 # In seconds, only used in time mode
count = 20 # how many characters to type, only used in count mode

# Stats
score = 0
right = 0
wrong = 0

# Game loop
first = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Generate the first character
        if first == True:
            input_text = ""
            answer = char_spawn()
            first = False

        # Handles keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                # Don't do anything when user hasn't inputed yet to avoid missclicks
                if input_text == "":
                    pass
                # Answer is right
                elif input_text.lower() == answer:
                    # Generate a new letter and update stats
                    answer = char_spawn()
                    score += 1
                    score_handler(score)
                    right += 1
                    if mode == "count":
                        count -= 1
                # Answer is wrong
                else:
                    # Generate a new letter and update stats
                    answer = char_spawn()
                    score -= 1
                    score_handler(score)
                    wrong += 1
                    if mode == "count":
                        count -= 1
                
                # Reset input_text
                input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    # Screen background
    screen.fill((204, 190, 35))
    # Blit after screen update
    char_spawn(answer)
    score_handler(score)
    input_box()

    # When timer reaches zero, game ends
    if mode == "time":
        remaining_time = timer()
        if remaining_time <= 0:
            print("Right answers:", right)
            print("Wrong answers:", wrong)
            print("Final Score:", score)
            pygame.quit()
            sys.exit()
    if mode == "count":
        counter()
        if count <= 0:
            print("Right answers:", right)
            print("Wrong answers:", wrong)
            print("Final Score:", score)
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(30)