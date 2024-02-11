import pygame as pg
import random
import game_logic_module as game_logic
import sys

pg.init()

res = (960, 540)
screen = pg.display.set_mode(res)

clock = pg.time.Clock()
current_time = 0
button_press_time = 0

font1 = pg.font.SysFont('Consolas', 200)
font2 = pg.font.SysFont('Consolas', 100)
font3 = pg.font.SysFont('Consolas', 50)
font4 = pg.font.SysFont('Consolas', 30)

bg = pg.image.load('images/background.png')
loading_bg = pg.image.load('images/loading_bg.png')

pg.mixer.music.load('songs/intro.wav')
pg.mixer.music.play()

music_end = pg.USEREVENT + 1
pg.mixer.music.set_endevent(music_end)

pg.display.set_caption('Rock Paper Scissors')
icon = pg.image.load('images/icon.png')
pg.display.set_icon(icon)

color_light = (255, 51, 51)
color_dark = (255, 0, 0)

p_score = 0
c_score = 0

mode = ['rock', 'paper', 'scissors']
hand_mode = 'none'

timer_started = False
game_started = False
game_running = False
no_choice = False
running = True
add = False
fingers_up = False
tutorial = False

detector = game_logic.GameLogic()


def random_choice():
    choice = random.choice(mode)
    picture = pg.image.load(f'images/{choice}.png')
    return choice, picture


while running:
    screen.fill((0, 255, 0))
    screen.blit(bg, (0,0))

    w, h = 960, 540
    ix, iy = w // 4, h // 2

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == music_end:
            pg.mixer.music.load('songs/loop.wav')
            pg.mixer.music.play(-1)
        if event.type == pg.MOUSEBUTTONDOWN:
            if 410 <= mouse[0] <= 410 + 140 and 425 <= mouse[1] <= 425 + 40:
                if tutorial:
                    tutorial = False
                else:
                    pg.quit()
                    sys.exit()
            elif 400 <= mouse[0] <= 400 + 160 and 350 <= mouse[1] <= 350 + 40:
                if not game_running:
                    tutorial = True
                else:
                    if 410 <= mouse[0] <= 410 + 140 and 350 <= mouse[1] <= 350 + 40:
                            pg.quit()
                            sys.exit()
            else:
                if not game_started:
                    if not timer_started:
                        button_press_time = pg.time.get_ticks()
                        timer_started = True
                        no_choice = False
                        game_running = False
                        add = False

    detector.main()

    current_time = pg.time.get_ticks()

    mouse = pg.mouse.get_pos()

    if tutorial:
        screen.blit(loading_bg, (0, 0))

    if not game_started:
        if timer_started:
            screen.blit(font3.render('Computer', True, (0, 0, 0)), (100, 25))
            screen.blit(font3.render(str(c_score), True, (0, 0, 0)), (200, 65))

            screen.blit(font3.render('You', True, (0, 0, 0)), (700, 25))
            screen.blit(font3.render(str(p_score), True, (0, 0, 0)), (725, 65))

            if (current_time - button_press_time) // 1000 < 1:
                screen.blit(font1.render('Ready', True, (0, 0, 0)), (225, 170))
            elif (current_time - button_press_time) // 1000 == 1:
                screen.blit(font1.render('3', True, (0, 0, 0)), (425, 175))
            elif (current_time - button_press_time) // 1000 == 2:
                screen.blit(font1.render('2', True, (0, 0, 0)), (425, 175))
            elif (current_time - button_press_time) // 1000 == 3:
                screen.blit(font1.render('1', True, (0, 0, 0)), (425, 175))

            if current_time - button_press_time >= 4000:
                timer_started = False
                game_started = True

    if game_started:
        c_choice, c_picture = random_choice()
        p_choice = detector.choice_detector()
        if p_choice != 'none':
            p_picture = pg.image.load(f'images/{p_choice}.png')
            game_running = True
        else:
            game_running = False
            no_choice = True
        game_started = False

    if no_choice:
        screen.blit(font2.render('Play Again', True, (0, 0, 0)), (225, 170))

    if game_running:
        screen.blit(font2.render('Computer', True, (0, 0, 0)), (25, 25))
        screen.blit(c_picture, (ix - 125, iy - 125))

        screen.blit(font2.render('You', True, (0, 0, 0)), (650, 25))
        screen.blit(p_picture, (480 + 125, iy - 125))

        if p_choice == 'rock':
            if c_choice == 'scissors':
                screen.blit(font2.render('You Win', True, (0, 0, 0)), (300, 420))
                if not add:
                    p_score += 1
                    add = True
            elif c_choice == 'paper':
                screen.blit(font2.render('You Lose', True, (0, 0, 0)), (280, 420))
                if not add:
                    c_score += 1
                    add = True
            else:
                screen.blit(font2.render('Draw', True, (0, 0, 0)), (370, 420))

        if p_choice == 'paper':
            if c_choice == 'scissors':
                screen.blit(font2.render('You Lose', True, (0, 0, 0)), (280, 420))
                if not add:
                    c_score += 1
                    add = True
            elif c_choice == 'paper':
                screen.blit(font2.render('Draw', True, (0, 0, 0)), (370, 420))
            else:
                screen.blit(font2.render('You Win', True, (0, 0, 0)), (300, 420))
                if not add:
                    p_score += 1
                    add = True

        if p_choice == 'scissors':
            if c_choice == 'scissors':
                screen.blit(font2.render('Draw', True, (0, 0, 0)), (370, 420))
            elif c_choice == 'paper':
                screen.blit(font2.render('You Win', True, (0, 0, 0)), (300, 420))
                if not add:
                    p_score += 1
                    add = True
            else:
                screen.blit(font2.render('You Lose', True, (0, 0, 0)), (280, 420))
                if not add:
                    c_score += 1
                    add = True

    if not timer_started:
        if not game_running:
            if not tutorial:
                if 400 <= mouse[0] <= 400 + 160 and 350 <= mouse[1] <= 350 + 40:
                    pg.draw.rect(screen, (51, 204, 255), [400, 350, 160, 40])
                else:
                    pg.draw.rect(screen, (0, 134, 179), [400, 350, 160, 40])

                screen.blit(font4.render('Tutorial', True, (0, 0, 0)), (415, 355))
                screen.blit(font3.render('Press anywhere to play', True, (255, 255, 255)), (250, 50))

            if 410 <= mouse[0] <= 410 + 140 and 425 <= mouse[1] <= 425 + 40:
                pg.draw.rect(screen, color_light, [410, 425, 140, 40])
            else:
                pg.draw.rect(screen, color_dark, [410, 425, 140, 40])

            screen.blit(font4.render('Quit', True, (0, 0, 0)), (447, 430))

        else:
            if 410 <= mouse[0] <= 410 + 140 and 350 <= mouse[1] <= 350 + 40:
                pg.draw.rect(screen, color_light, [410, 350, 140, 40])
            else:
                pg.draw.rect(screen, color_dark, [410, 350, 140, 40])

            screen.blit(font4.render('Quit', True, (0, 0, 0)), (447, 355))

    pg.display.update()
    clock.tick(60)
