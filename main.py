import pygame
import sys

from player import Player
from game import Game


pygame.init()
pygame.font.init()

# RENKLER
white = (255, 255, 255)
red = (156, 19, 19)
blue = ((48, 95, 156))

enemy_1 = None
enemy_2 = None
enemy_3 = None

ended_at = None

idle = pygame.image.load("./animation/idle/idle-1.png")
running_left_animations = [pygame.image.load("./animation/run/left/run-left-1.png"), pygame.image.load("./animation/run/left/run-left-2.png"), pygame.image.load("./animation/run/left/run-left-3.png"), pygame.image.load("./animation/run/left/run-left-4.png")]
running_right_animations = [pygame.image.load("./animation/run/right/run-right-1.png"), pygame.image.load("./animation/run/right/run-right-2.png"), pygame.image.load("./animation/run/right/run-right-3.png"), pygame.image.load("./animation/run/right/run-right-4.png")]

screen_width = 1000
screen_height = 800

player = Player(Game(None, screen_width, screen_height).screen, screen_width / 2  - idle.get_width() / 2, screen_height - idle.get_height() - 25)
game = Game(player, screen_width, screen_height)

while True:
    game.player.gravity()

    game.animation_controller += 1

    if game.player.player_control_rect != None:
        game.player.x = game.player.player_control_rect.x
        game.player.y = game.player.player_control_rect.y

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()

        game.display_menu(event)

        game.game_over(event)

    if game.started: 
        keys = pygame.key.get_pressed()

        if game.player.player_control_rect != None and game.player.climb_up == False and game.player.climb_down == False:
            if keys[pygame.K_LEFT] and game.player.player_control_rect.x > 0 + game.player.velocity and game.player.check_horizontal_collision(game.player.player_control_rect, game.grounds) != "collide-right":
                game.player.player_control_rect.x -= game.player.velocity
                game.player.left = True
                game.player.right = False

                if game.animation_controller % 6 == 0:
                    game.player.animation_counter += 1

                    if game.player.animation_counter >= len(running_right_animations):
                        game.player.animation_counter = 0

                    game.animation_controller = 0
                    
            elif keys[pygame.K_RIGHT] and game.player.player_control_rect.x + game.player.width < game.screen_width and game.player.check_horizontal_collision(game.player.player_control_rect, game.grounds) != "collide-left":
                game.player.player_control_rect.x += game.player.velocity
                game.player.right = True
                game.player.left = False

                if game.animation_controller % 6 == 0:
                    game.player.animation_counter += 1

                    if game.player.animation_counter >= len(running_right_animations):
                        game.player.animation_counter = 0

                    game.animation_controller = 0

            else:
                game.player.right = False
                game.player.left = False

                game.player.animation_counter = 0

        if keys[pygame.K_UP]:
            if game.player.player_control_rect != None and game.player.player_control_rect.collidelist(game.stairs) != -1:
                for stair in game.stairs:
                    if game.player.player_control_rect.colliderect(stair):
                        game.player.current_stair = stair
                        game.player.climb_up = True 

                        break

                if game.player.climb_up:
                    game.player.player_control_rect.centerx = game.player.current_stair.centerx
                    game.player.player_control_rect.y -= game.player.velocity * 2 

            elif game.player.player_control_rect != None and game.player.player_control_rect.collidelist(game.ropes) != -1:
                for rope in game.ropes:
                    if game.player.player_control_rect.colliderect(rope):
                        game.player.current_rope = rope
                        game.player.rope_climb = True 

                        break

                if game.player.rope_climb:
                    game.player.player_control_rect.centerx = game.player.current_rope.centerx
                    game.player.player_control_rect.y -= game.player.velocity * 2                 

            else:
                game.player.rope_climb = False
                game.player.climb_up = False
                game.player.jump = True            

        elif keys[pygame.K_DOWN]:
            if game.player.player_control_rect != None and game.player.player_control_rect.collidelist(game.stairs) != -1:
                for stair in game.stairs:
                    if game.player.player_control_rect.colliderect(stair):
                        game.player.current_stair = stair
                        game.player.climb_down = True 

                        break

                if game.player.current_stair.y + game.player.current_stair.height > game.player.player_control_rect.y + game.player.height and game.player.climb_down and len(game.player.grounds_down) > 0:
                    game.player.player_control_rect.centerx = game.player.current_stair.centerx
                    game.player.player_control_rect.y += game.player.velocity

                else:
                    game.player.climb_down = False

            else:
                game.player.climb_down = False

        else:
            game.player.climb_up = False
            game.player.climb_down = False
            game.player.rope_climb = False

        game.deactivate_bomb()

        if game.animation_controller % 6 == 0:
            game.display()   

        game.game_over_check() 

    game.clock.tick(60)