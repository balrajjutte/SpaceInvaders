#!/usr/bin/env python

import pygame
import random
import math
from pygame import mixer  # for music
from datetime import date
import csv

loop = True
while loop:
    date_recorded = []
    name_recorded = []
    score_recorded = []
    f = open("score_log.txt")
    csv_f = csv.reader(f)
    for row in csv_f:
        date_record, name_record, score_record = row
        date_recorded.append(date_record)
        name_recorded.append(name_record)
        score_recorded.append(int(score_record))
    f.close()
    top_score_index = (score_recorded.index(max(score_recorded)))
    top_date = date_recorded[top_score_index]
    top_name = name_recorded[top_score_index]
    top_score = score_recorded[top_score_index]

    today = date.today()

    # Intialize the pygame
    pygame.init()

    # create the screen
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()  # main menu

    # load background
    background = pygame.image.load("background.PNG")
    background_menu = pygame.image.load("background_mainmenu.png")

    # Background Sound
    mixer.music.load("background.wav")  # use .music.load for a long sound, .sound for a short sound
    mixer.music.play(-1)  # the -1 allows it to play on loop

    # Title and Icon
    pygame.display.set_caption("Space Invaders")
    icon = pygame.image.load("001-ufo.png")
    pygame.display.set_icon(icon)

    # input name stuff

    name = ""
    input_rect = pygame.Rect(50, 400, 280, 64)
    colour_active = pygame.Color("lightskyblue3")
    colour_passive = pygame.Color("gray15")
    colour = colour_passive
    active = False

    # Player

    playerImg = pygame.image.load("space-invaders.png")
    # coordinates of the intial position, must be a little bit left of screen due to image size
    # and we want below the centre
    playerX = 370
    playerY = 480
    playerX_change = 0  # signify a change in x or y

    # Enemy want to appear randomly, adding multiple enemies requires a list
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    speed = 3

    # Bullet
    # at ready state you cant see the bullet on screen,
    # at fire, bullet is moving
    bulletImg = pygame.image.load("bullet.png")
    bulletX = 0  # not really need to be considered
    bulletY = 480  # intial height of bullet, always shot from the player height
    bulletX_change = 0  # will be required for allowing bullet to shoot in one direction
    bulletY_change = 13  # how fast you want it travel
    bullet_state = "ready"

    # for the score, choose font for display
    score_value = 0
    font = pygame.font.Font("freesansbold.ttf", 32)  # textname, size
    small_font = pygame.font.Font("freesansbold.ttf", 16)
    textX = 10
    textY = 10

    # Game over text
    over_font = pygame.font.Font("freesansbold.ttf", 64)


    def show_score(x, y):
        # render method (text wrote, TRUE to display onscreen, colour(Rgb)) used for text first render then blit
        score = font.render("Score: {}".format(score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))
        if score_value < top_score:
            highestscore_text = font.render("High Score: {}".format(top_score), True, (255, 0, 0))
        else:
            highestscore_text = font.render("High Score: {}".format(score_value), True, (255, 0, 0))
        screen.blit(highestscore_text, (565, textY))


    def game_over_text():
        over_text = over_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(over_text, (200, 250))


    def high_score():
        highestscore_text = font.render("TOP SCORE: {}".format(top_score), True, (255, 0, 0))
        screen.blit(highestscore_text, (550, 250))
        recordtext = small_font.render("By {} on {}".format(top_name, top_date), True, (255, 0, 0))
        screen.blit(recordtext, (550, 300))


    def new_record():
        new_record_text = over_font.render("NEW RECORD {}!!!".format(score_value), True, (255, 255, 255))
        screen.blit(new_record_text, (125, 150))


    def name_input():
        if active:
            colour = colour_active
        else:
            colour = colour_passive
        pygame.draw.rect(screen, colour, input_rect, 2)
        user_name = over_font.render(name, True, (0, 255, 0))
        screen.blit(user_name, input_rect)
        input_rect.w = max(200, user_name.get_width() + 20)


    def input_instruction():
        input_instruct_text = small_font.render(
            "Enter name below, each time you type a character or backspace click the box", True, (255, 255, 255))
        screen.blit(input_instruct_text, (50, 375))


    def closing_instruction():
        closing_instruct_text = small_font.render("To close game, press ESC or close window", True, (255, 255, 255))
        screen.blit(closing_instruct_text, (50, 480))


    def play_again_instruction():
        play_again_instruct = small_font.render("To play again, press ENTER", True, (255, 255, 255))
        screen.blit(play_again_instruct, (50, 530))


    def player(x, y):
        screen.blit(playerImg, (x, y))


    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))


    def fire_bullet(x, y):  # want to change from ready to fire when space is pressed
        global bullet_state  # using global allows you to access the variable inside the function
        bullet_state = "fire"
        # using same coordinates as player, but plus 16 (for centre in x direction)
        # and +10 to make it appear little bit above the player
        screen.blit(bulletImg, (x + 16, y + 10))


    def isCollision(enemyX, enemyY, bulletX, bulletY):  # use distance between formula equation
        distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
        if distance < 27:  # for collision
            return True
        return False


    menu = True
    # Game Loop(an infinite loop, that runs till we close the window, all events take place in here)
    running = True,
    while running:
        while menu:  # all for main menu

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        menu = False

            screen.fill((0, 0, 0))
            clock.tick(30)
            screen.blit(background_menu, (0, 0))
            high_score()
            pygame.display.update()
        # RGB - Red, Green, Blue 0-255
        screen.fill((0, 0, 0))

        # add background image
        screen.blit(background, (0, 0))
        # ANY INPUT CONTROL IE USING A KEYSTOKE IS AN EVENT
        # KEYDOWN IS HOLDING KEYDOWN, KEYUP VICEVERSA
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                loop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    loop = False
                elif event.key == pygame.K_RETURN:
                    running = False
            # if keystoke is pressed check whether its right or left or space
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -7
                if event.key == pygame.K_RIGHT:
                    playerX_change = 7
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":  # to ensure bullet only fired when in ready condition
                        bullet_sound = mixer.Sound("laser.wav")
                        bullet_sound.play()
                        bulletX = playerX  # gets the current player x coordinate stores it in new variable
                        fire_bullet(bulletX, bulletY)
                if event.key == pygame.K_p:
                    menu = True

            if event.type == pygame.KEYUP:
                # too make sure spaceship stops
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # increasing enemies
        num_of_enemies = 6
        if score_value > 5:
            num_of_enemies += 1
            speed = 3.5
        if score_value > 10:
            num_of_enemies += 1
            speed = 4
        if score_value > 15:
            num_of_enemies += 1
        if score_value > 20:
            num_of_enemies += 1
        if score_value > 25:
            num_of_enemies += 1
            speed = 4.5
        if score_value > 30:
            num_of_enemies += 1
            speed = 5
        if score_value > 40:
            num_of_enemies += 1
            speed = 6
        if score_value > 50:
            num_of_enemies += 1
            speed = 6.5
        for i in range(num_of_enemies):
            enemyImg.append(pygame.image.load("enemy.png"))
            enemyX.append(random.randint(0, 735))  # u want to appear randomly across the width
            enemyY.append(random.randint(50, 150))  # you want it to appear only near the top
            enemyX_change.append(speed)  # change speed here
            enemyY_change.append(40)
        # adding the change in coordinates
        playerX += playerX_change

        # adding the boundaries,
        if playerX <= 0:
            playerX = 0
        # the picture width is 64 by 64 thus must consider this when setting the boundary
        elif playerX >= 736:
            playerX = 736

        # use for loop to specify each enemy
        for i in range(num_of_enemies):
            # Game Over
            if enemyY[i] > 440:

                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                closing_instruction()
                play_again_instruction()
                menu = False
                if score_value > top_score:
                    input_instruction()
                    new_record()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if input_rect.collidepoint(event.pos):
                            active = True
                    if event.type == pygame.KEYDOWN:
                        if active:

                            if event.key == pygame.K_BACKSPACE:
                                name = name[:-1]
                                active = False
                            else:
                                name += event.unicode
                                active = False
                    name_input()
                break
            # Enemy movement
            enemyX[i] += enemyX_change[i]

            # adding the boundaries, for the enemy, so it moves left and right and down when boundary is hit
            if enemyX[i] <= 0:
                enemyX_change[i] = speed
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -1 * speed
                enemyY[i] += enemyY_change[i]

            # collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)  # will store value true or false
            if collision:  # you want to first reset the bullet, increase the score, reset enemy spawn
                explosion_sound = mixer.Sound("explosion.wav")
                explosion_sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)
            # ensure while loop to display enemy is also within the for loop
            enemy(enemyX[i], enemyY[i], i)

        # bullet movement, first if statement allows multiple bullets to fire, resets it to ready
        # second if statement ensure bullet remains on screen
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"
        if bullet_state is "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        # ensure player function is called after screen.fill as overwise it will be drawn over
        player(playerX, playerY)
        show_score(textX, textY)

        # constantly updating the display always need this
        pygame.display.update()

    # generating the csv
    if score_value > top_score:
        if name == "":
            name = "Anonymous"
        with open("score_log.txt", "a") as file:
            file.write("{},{},{}\n".format(today, name, score_value))
