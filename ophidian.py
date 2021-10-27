import pygame
import random
pygame.init()
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)
yellow_green = (0, 255, 155)
blue = (0, 0, 255)
purple = (255, 0, 255)
display_height = 600
display_width = 800
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Ophidian')
icon = pygame.image.load('D:/Important/BRC/comp/icon.png')
pygame.display.set_icon(icon)
small_font = pygame.font.SysFont('palatinolinotype', 25)
med_font = pygame.font.SysFont('palatinolinotype', 50)
large_font = pygame.font.SysFont('palatinolinotype', 80)
img = pygame.image.load('D:/Important/BRC/comp/Snake head.png')
direction = 'right'
head = img
apple = pygame.image.load('D:/Important/BRC/comp/apple.png')
clock = pygame.time.Clock()


def button(surface, position, text):
    font = small_font
    text_render = font.render(text, True, (0, 0, 0))
    x, y, w, h = text_render.get_rect()
    x, y = position
    pygame.draw.line(surface, (150, 150, 150), (x - 5, y - 10), (x + 200, y - 10), 5)
    pygame.draw.line(surface, (150, 150, 150), (x - 5, y - 10), (x - 5, y + 20), 5)
    pygame.draw.line(surface, (50, 50, 50), (x + 200, y - 10), (x + 200, y + 20), 5)
    pygame.draw.line(surface, (50, 50, 50), (x - 5, y + 20), [x + 200, y + 20], 5)
    pygame.draw.rect(surface, (255, 255, 255), (x - 5 , y - 10, 203, 30))
    return surface.blit(text_render, (x + 50, y - 5))


def pause():
    paused = True
    screen.fill(purple)
    continue_button = button(screen, (300, 300), 'CONTINUE (C)')
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(pygame.mouse.get_pos()):
                    paused = False
        message_to_screen('PAUSED', white, -100, size='large')
        pygame.display.update()
        clock.tick(5)


def score(points):
    text = small_font.render('Score : '+str(points), True, black)
    screen.blit(text, [0, 0])
    p = small_font.render('Press P to pause', True, black)
    screen.blit(p, [0, 30])


def rules():
    rule = True
    screen.fill(yellow_green)
    quit_button = button(screen, (300, 400), 'QUIT (Q)')
    home_button = button(screen, (300, 500), 'HOME')
    while rule:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if home_button.collidepoint(pygame.mouse.get_pos()):
                    rule = False
                    game_intro()
                elif quit_button.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    quit()
    message_to_screen('RULES', blue, -100, size='large')
    message_to_screen('1. Eat as many apples as possible and grow in length', black, -60)
    message_to_screen('2. Do not crash into the boundaries of the game area', black, -50)
    message_to_screen('3. Do not crash into yourself', black, -40)
    pygame.display.update()
    clock.tick(5)


def game_intro():
    intro = True
    screen.fill(yellow_green)
    quit_button = button(screen, (300, 400), "QUIT")
    start_button = button(screen, (300, 300), "START")
    rule_button = button(screen, (300, 500), 'RULES')
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    intro = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(pygame.mouse.get_pos()):
                    intro = False
                elif quit_button.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    quit()
                elif rule_button.collidepoint(pygame.mouse.get_pos()):
                    intro = False
                    rules()
        message_to_screen('OPHIDIAN', green, -100, size='large')
        screen.blit(icon, [400, 100])
        pygame.display.update()
        clock.tick(5)


def snake(block_size, snake_list):
    global head
    if direction == 'right':
        head = pygame.transform.rotate(img, 270)
    if direction == 'left':
        head = pygame.transform.rotate(img, 90)
    if direction == 'up':
        head = img
    if direction == 'down':
        head = pygame.transform.rotate(img, 180)
    screen.blit(head, (snake_list[-1][0], snake_list[-1][1]))
    for XnY in snake_list[:-1]:
        pygame.draw.rect(screen, green, [XnY[0], XnY[1], block_size, block_size])


def text_objects(text, color, size):
    text_surface = small_font
    if size == 'small':
        text_surface = small_font.render(text, True, color)
    if size == 'med':
        text_surface = med_font.render(text, True, color)
    if size == 'large':
        text_surface = large_font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_to_screen(msg, color, y_displace, size='small'):

    text_surface, text_rect = text_objects(msg, color, size)
    text_rect.center = display_width/2, (display_height/2) + y_displace
    screen.blit(text_surface, text_rect)


def game_loop():
    global direction
    game_exit = False
    game_over = False
    lead_x = display_width / 2
    lead_y = display_height / 2
    lead_x_change = 0
    lead_y_change = 0
    block_size = 20
    fps = 10
    snake_list = []
    snake_length = 1
    rand_apple_x = random.randrange(0, display_width-block_size, block_size)
    rand_apple_y = random.randrange(0, display_height-block_size, block_size)
    while not game_exit:

        while game_over:
            screen.fill(black)
            message_to_screen('Game over', red, -50, size='large')
            message_to_screen('Press C to restart or Q to quit', yellow_green, 50, size='med')
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_c:
                    game_loop()
                else:
                    pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                    direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                    direction = 'right'
                elif event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                    direction = 'up'
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0
                    direction = 'down'
                elif event.key == pygame.K_p:
                    pause()
                if event.key == pygame.K_UP or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    for segment in snake_list[:-1]:
                        if segment == snake_head:
                            game_over = True
        if lead_x > display_width or lead_x < 0 or lead_y > display_height or lead_y < 0:
            game_over = True

        lead_x += lead_x_change
        lead_y += lead_y_change
        screen.fill(white)
        screen.blit(apple, (rand_apple_x, rand_apple_y))
        snake_head = [lead_x, lead_y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        snake(block_size, snake_list)
        score(snake_length-1)
        pygame.display.update()
        if rand_apple_x <= lead_x <= rand_apple_x+block_size:
            if rand_apple_y <= lead_y <= rand_apple_y + block_size:
                rand_apple_x = random.randrange(0, display_width - block_size, block_size)
                rand_apple_y = random.randrange(0, display_height - block_size, block_size)
                snake_length += 1

        clock.tick(fps)


game_intro()
game_loop()