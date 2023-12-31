# Japanese Typing Game

import pygame
import sys
import random
from save_score import save_score

pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
pygame.display.set_caption("Kana Strike")

# Database
letters_dict = {
                'a': ('あ', 'ア'), 'i': ('い', 'イ'), 'u': ('う', 'ウ'), 'e': ('え', 'エ'), 'o': ('お', 'オ'),
                'ka': ('か', 'カ'), 'ki': ('き', 'キ'), 'ku': ('く', 'ク'), 'ke': ('け', 'ケ'), 'ko': ('こ', 'コ'),
                'sa': ('さ', 'サ'), 'shi': ('し', 'シ'), 'su': ('す', 'ス'), 'se': ('せ', 'セ'), 'so': ('そ', 'ソ'),
                'ta': ('た', 'タ'), 'chi': ('ち', 'チ'), 'tsu': ('つ', 'ツ'), 'te': ('て', 'テ'), 'to': ('と', 'ト'),
                'na': ('な', 'ナ'), 'ni': ('に', '二'), 'nu': ('ぬ', 'ヌ'), 'ne': ('ね', 'ネ'), 'no': ('の', 'ノ'),
                'ha': ('は', 'ハ'), 'hi': ('ひ', 'ヒ'), 'fu': ('ふ', 'フ'), 'he': ('へ', 'ヘ'), 'ho': ('ほ', 'ホ'),
                'ma': ('ま', 'マ'), 'mi': ('み', 'ミ'), 'mu': ('む', 'ム'), 'me': ('め', 'メ'), 'mo': ('も', 'モ'),
                'ya': ('や', 'ヤ'),                     'yu': ('ゆ', 'ユ'),                    'yo': ('よ', 'ヨ'),
                'ra': ('ら', 'ラ'), 'ri': ('り', 'リ'), 'ru': ('る', 'ル'), 're': ('れ', 'レ'), 'ro': ('ろ', 'ロ'),
                'wa': ('わ', 'ワ'),                                                            'wo': ('を', 'ヲ'),
                'n': ('ん', 'ン')
                }

# Generate and display a letter into the game
# Is ran every loop, and gives next letter when letter == None
# Takes in what writing system should be used and optionally the letter when refreshing screen
# Returns the letter and writing system
def char_spawn(writing_system=int, letter=None) -> tuple:
    if letter == None:
        # If mode is elimination, choose from temporary dict, and delete the entry from dict
        if mode == "elimination":
            if len(letters_dict_current) > 0: # Skip when dict is empty
                letter = random.choice(list(letters_dict_current.keys()))
                del letters_dict_current[letter]
        # Else just choose a random entry from dict
        else:
            letter = random.choice(list(letters_dict_current.keys()))
        
        # Changes writing system to hiragana or katakana randomly when writing_system is 3
        if writing_system == 3:
            writing_system = random.randint(0, 1)

    if letter != None: # For the case when dict is empty, skip drawing
        if writing_system == 2:
            letter_surf = pygame.font.SysFont(None, 500).render(letter.upper(), False, "Black")
        else:
            letter_surf = pygame.font.SysFont("msgothic", 500).render(letters_dict[letter][writing_system], False, "Black")
        letter_rect = letter_surf.get_rect(center = (400, 400))
        screen.blit(letter_surf, letter_rect)

    return letter, writing_system

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

def counter(count):
    counter_surf = pygame.font.SysFont(None, 50).render("Left: " + str(count), False, "Black")
    counter_rect = counter_surf.get_rect(topright = (800, 0))
    screen.blit(counter_surf, counter_rect)

# After getting correct/incorrect answer, visually show it with +1 or -1 besides the score
def score_ghost(correct):
    if correct:
        ghost_surf = pygame.font.SysFont(None, 50).render("+1", False, "Dark Green")
    else:
        ghost_surf = pygame.font.SysFont(None, 50).render("-1", False, "Red")
    ghost_rect = ghost_surf.get_rect(center = (460, 100))
    screen.blit(ghost_surf, ghost_rect)

# Shows Hiragana and Katakana after answering in romaji system
def letter_ghost(letter):
    ghost_h_surf = pygame.font.SysFont("msgothic", 200).render(letters_dict[letter][0], False, "Black")
    ghost_h_rect = ghost_h_surf.get_rect(center = (200, 600))
    screen.blit(ghost_h_surf, ghost_h_rect)

    ghost_k_surf = pygame.font.SysFont("msgothic", 200).render(letters_dict[letter][1], False, "Black")
    ghost_k_rect = ghost_k_surf.get_rect(center = (600, 600))
    screen.blit(ghost_k_surf, ghost_k_rect)

# Adds +1 to correct index in stats_list
def stats_handler(correct):
    # Get letter's index corresponding to letters_dict
    letter_index = list(letters_dict.keys()).index(answer)
    # Katakana comes after hiragana
    if writing_system_current == 1:
        letter_index += len(letters_dict)
    # Wrong answers comes after katakana
    if correct == False:
        letter_index += len(letters_dict) * 2
    # Adds +1
    stats_list[letter_index] += 1


# Gameplay variables
# Currently available modes: time, count, elimination
mode = "elimination"
writing_system = 2 # 0 = hiragana, 1 = katakana, 2 = Romaji, 3 = Randomize
time_limit = 10 # In seconds, only used in time mode
count = 20 # how many characters to type, only used in count mode
letters_limit = False # how many letters are included. False with every letter, Int with that amount of letters.

# Stats
stats_list = [0] * len(letters_dict) * 4
score = 0

# Game loop
first = True
game_end = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Generate the first character
        if first == True:
            input_text = ""
            if letters_limit != False:
                letters_dict_current = {k: letters_dict[k] for k in list(letters_dict)[:letters_limit]}
            else:
                letters_dict_current = dict(letters_dict) # used in elimination mode
            answer, writing_system_current = char_spawn(writing_system)
            score_ghost_time = False
            letter_ghost_time = False # romaji specific
            first = False

        # Handles keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                # Don't do anything when user hasn't inputed yet to avoid missclicks
                if input_text != "":
                    # Answer is right
                    if input_text.lower() == answer:
                        stats_handler(True)
                        score += 1
                        correct = True
                    # Answer is wrong
                    else:
                        stats_handler(False)
                        score -= 1
                        correct = False

                    # Romajii system
                    if writing_system == 2:
                        letter_ghost_time = pygame.time.get_ticks() + 3000
                        ghost_letter = answer
                    # Generate a new letter
                    answer, writing_system_current = char_spawn(writing_system)
                    # Count mode specific
                    if mode == "count":
                        count -= 1

                    # Display score ghost for 1.25 sec
                    score_ghost_time = pygame.time.get_ticks() + 1250
                    

                # Reset input_text
                input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode


    # Screen elements
    screen.fill((204, 190, 35)) # Screen background
    char_spawn(writing_system_current, answer)
    score_handler(score)
    input_box()
    # Time based screen elements
    current_time = pygame.time.get_ticks()
    if score_ghost_time > current_time:
        score_ghost(correct)
    if letter_ghost_time > current_time:
        letter_ghost(ghost_letter)


    # Settings depending on the mode
    if mode == "time":
        # Blit timer
        remaining_time = timer()
        # When timer reaches zero, game ends
        if remaining_time <= 0:
            game_end = True
    elif mode == "count":
        # Blit remaining letters left to solve
        counter(count-1)
        # When count reaches zero, game ends
        if count == 0:
            game_end = True
    elif mode == "elimination":
        # Blit remaining letters left to solve
        counter(len(letters_dict_current))
        # answer == None means there is no more letters to solve, thus game ends
        if answer == None:
            game_end = True

    # Activates when game ends
    if game_end:
        print("Final Score:", score)
        print("Right answers:", sum(stats_list[:len(letters_dict)*2]))
        print("Wrong answers:", sum(stats_list[len(letters_dict)*2:]))
        save_score(stats_list)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    clock.tick(30)