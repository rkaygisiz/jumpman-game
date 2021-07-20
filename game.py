import pygame

from enemy import Enemy
from player import Player

idle = pygame.image.load("./animation/idle/idle-1.png")
running_left_animations = [pygame.image.load("./animation/run/left/run-left-1.png"), pygame.image.load("./animation/run/left/run-left-2.png"), pygame.image.load("./animation/run/left/run-left-3.png"), pygame.image.load("./animation/run/left/run-left-4.png")]
running_right_animations = [pygame.image.load("./animation/run/right/run-right-1.png"), pygame.image.load("./animation/run/right/run-right-2.png"), pygame.image.load("./animation/run/right/run-right-3.png"), pygame.image.load("./animation/run/right/run-right-4.png")]

class Game():
    def __init__(self, player, screen_width, screen_height):
        self.caption = "Jumpman"

        self.started_at = None

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(self.caption)

        self.clock = pygame.time.Clock()

        self.lato_big = pygame.font.Font("./font/Lato/Lato-Bold.ttf", 60)
        self.lato_normal = pygame.font.Font("./font/Lato/Lato-Bold.ttf", 45)

        self.modes = ["KOLAY", "ORTA", "ZOR"]
        self.default_mode = self.modes[0]
        self.mode = self.default_mode

        self.grounds = [pygame.Rect(0, 775, 1000, 25), pygame.Rect(0, 493, 150, 25), pygame.Rect(850, 493, 150, 25), pygame.Rect(200, 550, 600, 25), pygame.Rect(350, 375, 300, 25), pygame.Rect(0, 325, 200, 25), pygame.Rect(800, 325, 200, 25), pygame.Rect(200, 131, 600, 25)]
        self.stairs = [pygame.Rect(250, 505, 70, 270), pygame.Rect(680, 505, 70, 270), pygame.Rect(465, 338, 70, 212)]
        self.bombs = [pygame.Rect(400, 450, 50, 50), pygame.Rect(550, 450, 50, 50), pygame.Rect(10, 400, 50, 50), pygame.Rect(940, 400, 50, 50), pygame.Rect(10, 225, 50, 50), pygame.Rect(940, 225, 50, 50), pygame.Rect(300, 30, 50, 50), pygame.Rect(700, 30, 50, 50)]
        self.ropes = [pygame.Rect(485, 131, 30, 130), pygame.Rect(60, 493, 30, 130), pygame.Rect(910, 493, 30, 130)]

        self.bomb_image = pygame.image.load("./assets/bomb.png")
        self.heart_image = pygame.image.load("./assets/heart.png")

        self.button_color_1 = (255, 255, 255)
        self.button_color_2 = (255, 255, 255)
        self.button_color_3 = (255, 255, 255)

        self.play_again_button_color = (255, 255, 255)

        self.buttons = [pygame.Rect(317, 375, 367, 85), pygame.Rect(317, 475, 367, 85), pygame.Rect(317, 575, 367, 85)]

        self.play_again_button = pygame.Rect(290, 475, 418, 85)

        self.map = pygame.image.load("./assets/map.png")

        self.animation_controller = 0

        self.started = False
        self.over = False

        self.current_ground = None

        self.player = player

        self.enemy_1 = Enemy(self.player, self.screen, self.screen_width, self.screen_height)
        self.enemy_2 = Enemy(self.player, self.screen, self.screen_width, self.screen_height)
        self.enemy_3 = Enemy(self.player, self.screen, self.screen_width, self.screen_height)
        self.enemy_4 = Enemy(self.player, self.screen, self.screen_width, self.screen_height)

    def reset_game(self):
        self.bombs = [pygame.Rect(400, 450, 50, 50), pygame.Rect(550, 450, 50, 50), pygame.Rect(10, 400, 50, 50), pygame.Rect(940, 400, 50, 50), pygame.Rect(10, 225, 50, 50), pygame.Rect(940, 225, 50, 50), pygame.Rect(300, 30, 50, 50), pygame.Rect(700, 30, 50, 50)]
        self.default_mode = self.modes[0]
        self.player.hearts = 3

    def deactivate_bomb(self):
        if self.player.player_control_rect != None:    
            for bomb in self.bombs:
                if self.player.player_control_rect.colliderect(bomb):
                    self.bombs.remove(bomb)

    def display_menu(self, event):
        if self.started == False and self.over == False:
            self.menu = pygame.image.load("./assets/menu.png")

            self.text_width_1, self.text_height_1 = self.lato_big.size("KOLAY")
            self.text_width_2, self.text_height_2 = self.lato_big.size("ORTA")
            self.text_width_3, self.text_height_3 = self.lato_big.size("ZOR")

            self.text_1 = self.lato_big.render('KOLAY', False, (0, 0, 0))
            self.text_2 = self.lato_big.render('ORTA', False, (0, 0, 0))
            self.text_3 = self.lato_big.render('ZOR', False, (0, 0, 0))

            self.screen.fill((0, 0, 0))

            self.screen.blit(self.menu, (0, 0))

            pygame.draw.rect(self.screen, self.button_color_1, self.buttons[0])
            pygame.draw.rect(self.screen, self.button_color_2, self.buttons[1])
            pygame.draw.rect(self.screen, self.button_color_3, self.buttons[2])

            self.screen.blit(self.text_1, (self.buttons[0].x + self.buttons[0].width / 2 - self.text_width_1 / 2, self.buttons[0].y + self.buttons[0].height / 2 - self.text_height_1 / 2))
            self.screen.blit(self.text_2, (self.buttons[1].x + self.buttons[1].width / 2 - self.text_width_2 / 2, self.buttons[1].y + self.buttons[1].height / 2 - self.text_height_2 / 2))
            self.screen.blit(self.text_3, (self.buttons[2].x + self.buttons[2].width / 2 - self.text_width_3 / 2, self.buttons[2].y + self.buttons[2].height / 2 - self.text_height_3 / 2))

            pygame.display.update() 

            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
            
            if self.mouse_x < self.buttons[0].x + self.buttons[0].width and self.mouse_x > self.buttons[0].x:
                if self.mouse_y > self.buttons[0].y and self.mouse_y < self.buttons[0].y + self.buttons[0].height:
                    self.button_color_1 = (220, 22, 22)

                else: 
                    self.button_color_1 = (255, 255, 255)

            else: 
                self.button_color_1 = (255, 255, 255)

            if self.mouse_x < self.buttons[1].x + self.buttons[1].width and self.mouse_x > self.buttons[1].x:
                if self.mouse_y > self.buttons[1].y and self.mouse_y < self.buttons[1].y + self.buttons[1].height:
                    self.button_color_2 = (220, 22, 22)

                else: 
                    self.button_color_2 = (255, 255, 255)

            else: 
                self.button_color_2 = (255, 255, 255)

            if self.mouse_x < self.buttons[2].x + self.buttons[2].width and self.mouse_x > self.buttons[2].x:
                if self.mouse_y > self.buttons[2].y and self.mouse_y < self.buttons[2].y + self.buttons[2].height:
                    self.button_color_3 = (220, 22, 22)

                else: 
                    self.button_color_3 = (255, 255, 255)

            else: 
                self.button_color_3 = (255, 255, 255)

            if event.type == pygame.MOUSEBUTTONDOWN and not self.started: 
                if event.button == 1:
                    if self.mouse_x < self.buttons[0].x + self.buttons[0].width and self.mouse_x > self.buttons[0].x:
                        if self.mouse_y > self.buttons[0].y and self.mouse_y < self.buttons[0].y + self.buttons[0].height:
                            self.mode = self.modes[0]

                            self.started = True

                    if self.mouse_x < self.buttons[1].x + self.buttons[1].width and self.mouse_x > self.buttons[1].x:
                        if self.mouse_y > self.buttons[1].y and self.mouse_y < self.buttons[1].y + self.buttons[1].height:
                            self.mode = self.modes[1]

                            self.started = True

                    if self.mouse_x < self.buttons[2].x + self.buttons[2].width and self.mouse_x > self.buttons[2].x:
                        if self.mouse_y > self.buttons[2].y and self.mouse_y < self.buttons[2].y + self.buttons[2].height:
                            self.mode = self.modes[2]

                            self.started = True

    def game_over(self, event):
        if self.over:
            self.started = False
            self.play_again_screen = pygame.image.load("./assets/play-again.png")

            self.play_again_text_width, self.play_again_text_height = self.lato_normal.size("TEKRAR OYNA")
            self.play_again_text = self.lato_normal.render('TEKRAR OYNA', False, (0, 0, 0))

            self.screen.fill((0, 0, 0))

            self.screen.blit(self.play_again_screen, (0, 0))

            pygame.draw.rect(self.screen, self.play_again_button_color, self.play_again_button)

            self.screen.blit(self.play_again_text, (self.play_again_button.x + self.play_again_button.width / 2 - self.play_again_text_width / 2, self.play_again_button.y + self.play_again_button.height / 2 - self.play_again_text_height / 2))

            pygame.display.update() 

            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

            if self.mouse_x < self.play_again_button.x + self.play_again_button.width and self.mouse_x > self.play_again_button.x:
                if self.mouse_y > self.play_again_button.y and self.mouse_y < self.play_again_button.y + self.play_again_button.height:
                    self.play_again_button_color = (220, 22, 22)

                else: 
                    self.play_again_button_color = (255, 255, 255)

            else: 
                self.play_again_button_color = (255, 255, 255)

            if event.type == pygame.MOUSEBUTTONDOWN and not self.started: 
                if event.button == 1:
                    if self.mouse_x < self.play_again_button.x + self.play_again_button.width and self.mouse_x > self.play_again_button.x:
                        if self.mouse_y > self.play_again_button.y and self.mouse_y < self.play_again_button.y + self.play_again_button.height:
                            self.reset_game()

                            self.over = False
                            self.started = False

    def display(self):
        self.screen.fill((0, 0, 0))

        for ground in self.grounds:
            pygame.draw.rect(self.screen, (0, 0, 0), ground)

        for stair in self.stairs:
            pygame.draw.rect(self.screen, (0, 0, 0), stair)

        for rope in self.ropes:
            pygame.draw.rect(self.screen, (0, 0, 0), rope)

        self.screen.blit(self.map, (0, 0))

        for bomb in self.bombs:
            self.screen.blit(self.bomb_image, bomb)

        for i in range(1, self.player.hearts + 1):
            self.screen.blit(self.heart_image, (950 - i * 50, 10))

        self.player.animations()

        self.enemy_1.display()
        self.enemy_1.move()
        self.enemy_1.check_collision()

        self.enemy_2.display()
        self.enemy_2.move()
        self.enemy_2.check_collision() 

        if self.mode == "ORTA":
            self.enemy_3.display()
            self.enemy_3.move()
            self.enemy_3.check_collision()   

            self.enemy_1.velocity = 22.5  
            self.enemy_2.velocity = 22.5 
            self.enemy_3.velocity = 22.5                  

        elif self.mode == "ZOR":
            self.enemy_3.display()
            self.enemy_3.move()
            self.enemy_3.check_collision()   

            self.enemy_4.display()
            self.enemy_4.move()
            self.enemy_4.check_collision()   

            self.enemy_1.velocity = 30   
            self.enemy_2.velocity = 30   
            self.enemy_3.velocity = 30  
            self.enemy_4.velocity = 30  

        pygame.display.update()          

    def game_over_check(self):
        if self.started == True:
            if len(self.bombs) == 0 or self.player.hearts == 0:
                self.over = True
                self.started = False

                self.player = Player(Game(None, self.screen_width, self.screen_height).screen, self.screen_width / 2  - idle.get_width() / 2, self.screen_height - idle.get_height() - 25)

                self.enemy_1 = Enemy(self.player, self.screen, self.screen_width, self.screen_height)
                self.enemy_2 = Enemy(self.player, self.screen, self.screen_width, self.screen_height)
