import pygame
import random
import time

pygame.init()
enemy_score = 0
screen_width = 1200
screen_height = 600
white = (255, 255, 255)
P_1 = (255, 0, 0)
black = (0, 0, 0)
purple = (150, 0, 255)
green = (17,175,0)

gamewindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("zain-Ul-game")
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


def scree_write(text, color, x, y):
    text = font.render(text, True, color)
    gamewindow.blit(text, [x, y])


def plot_snake(gamewindow, color, snk_list, s_size):
    for x, y in snk_list:
        pygame.draw.rect(gamewindow, color, [x, y, s_size, s_size])


def screen_text(text, color, x, y):
    text = font.render(text, True, color)
    gamewindow.blit(text, [x, y])


def enemy_greedy_search(enemy_x, enemy_y, food_x, food_y):
    dx = food_x - enemy_x
    dy = food_y - enemy_y

    # Prioritize movement along the x-axis if the difference is greater
    if abs(dx) > abs(dy):
        if dx > 0:
            return "RIGHT"
        else:
            return "LEFT"
    # Otherwise, prioritize movement along the y-axis
    else:
        if dy > 0:
            return "DOWN"
        else:
            return "UP"


def game_loop():
    start_time = time.time()  # Initialize the start time
    time_limit = 30  # Set the time limit in seconds
    snk_list = []
    snk_length = 1
    veloc_x = 0
    veloc_y = 0
    veloc = 3.5
    snake_x = 45
    snake_y = 55
    s_size = 25
    enemy_score = 0
    enemy_snk_list = []
    enemy_snk_length = 1
    enemy_veloc = 1.5
    enemy_snake_x = 65
    enemy_snake_y = 75

    exit_game = False
    game_over = False
    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    block_x = 300
    block_y = 300
    coll_x = 600
    coll_y = 300
    score = 0
    fps = 60
    elapsed_time = 0
    while not exit_game:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > time_limit:
            game_over = True
        if game_over:
            gamewindow.fill(white)
            screen_text("GAME OVER! PRESS ENTER TO CONTINUE", P_1, 200, 260)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_loop()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        veloc_y = veloc
                        veloc_x = 0
                    if event.key == pygame.K_LEFT:
                        veloc_x = -veloc
                        veloc_y = 0
                    if event.key == pygame.K_UP:
                        veloc_y = -veloc
                        veloc_x = 0
                    if event.key == pygame.K_RIGHT:
                        veloc_x = veloc
                        veloc_y = 0

            # Player snake
            snake_x += veloc_x
            snake_y += veloc_y

            # Computer-controlled snake
            enemy_move = enemy_greedy_search(enemy_snake_x, enemy_snake_y, food_x, food_y)
            if enemy_move == "UP":
                enemy_snake_y -= enemy_veloc

            elif enemy_move == "DOWN":
                enemy_snake_y += enemy_veloc

            elif enemy_move == "LEFT":
                enemy_snake_x -= enemy_veloc

            elif enemy_move == "RIGHT":
                enemy_snake_x += enemy_veloc

            # Player snake eats food
            if abs(snake_x - food_x) < 15 and abs(snake_y - food_y) < 15:
                score += 1
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length += 5

            # Computer-controlled snake eats food
            if abs(enemy_snake_x - food_x) < 15 and abs(enemy_snake_y - food_y) < 15:
                enemy_score += 1
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                enemy_snk_length += 5

            # Draw game elements
            gamewindow.fill("white")
            time_display = font.render("Time: {:.1f}".format(time_limit - elapsed_time), True, black)
            gamewindow.blit(time_display, (screen_width - 190, 500))
            pygame.draw.rect(gamewindow, green, [food_x, food_y, s_size, s_size])
            pygame.draw.rect(gamewindow, black, [block_x, block_y, 50, 50])
            pygame.draw.rect(gamewindow, black, [coll_x, coll_y, 50, 50])

            # Check collisions
            if (
                    snake_x < coll_x + 50 and snake_x + s_size > coll_x
                    and snake_y < coll_y + 50 and snake_y + s_size > coll_y
            ):
                game_over = True
            if (
                    snake_x < block_x + 50 and snake_x + s_size > block_x
                    and snake_y < block_y + 50 and snake_y + s_size > block_y
            ):
                game_over = True
            if (
                    enemy_snake_x < coll_x + 50 and enemy_snake_x + s_size > coll_x
                    and enemy_snake_y < coll_y + 50 and enemy_snake_y + s_size > coll_y
            ):
                game_over = True
            if (
                    enemy_snake_x < block_x + 50 and enemy_snake_x + s_size > block_x
                    and enemy_snake_y < block_y + 50 and enemy_snake_y + s_size > block_y
            ):
                game_over = True

            # Check boundaries
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True

            # Check self-collision
            if [snake_x, snake_y] in snk_list[:-1]:
                game_over = True

            # Update player snake
            head = [snake_x, snake_y]
            snk_list.append(head)
            if len(snk_list) > snk_length:
                del snk_list[0]
            plot_snake(gamewindow, P_1, snk_list, s_size)

            # Update computer-controlled snake
            enemy_head = [enemy_snake_x, enemy_snake_y]
            enemy_snk_list.append(enemy_head)
            if len(enemy_snk_list) > enemy_snk_length:
                del enemy_snk_list[0]
            plot_snake(gamewindow, black, enemy_snk_list, s_size)


            # Display score
            screen_text("P_1 S_Length: " + str(score), P_1, 0, 0)

            scree_write("Comp_S_length: " + str(enemy_score), black, 855, 0)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


game_loop()
