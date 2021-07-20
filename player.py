import pygame

idle = pygame.image.load("./animation/idle/idle-1.png")
running_left_animations = [pygame.image.load("./animation/run/left/run-left-1.png"), pygame.image.load("./animation/run/left/run-left-2.png"), pygame.image.load("./animation/run/left/run-left-3.png"), pygame.image.load("./animation/run/left/run-left-4.png")]
running_right_animations = [pygame.image.load("./animation/run/right/run-right-1.png"), pygame.image.load("./animation/run/right/run-right-2.png"), pygame.image.load("./animation/run/right/run-right-3.png"), pygame.image.load("./animation/run/right/run-right-4.png")]
climb = pygame.image.load("./animation/climb/climb-1.png")
rope = pygame.image.load("./animation/climb/climb-1.png")


class Player():
    def __init__(self, screen, x, y):
        self.screen = screen

        self.grounds = [pygame.Rect(0, 775, 1000, 25), pygame.Rect(0, 493, 150, 25), pygame.Rect(850, 493, 150, 25), pygame.Rect(200, 550, 600, 25), pygame.Rect(350, 375, 300, 25), pygame.Rect(0, 325, 200, 25), pygame.Rect(800, 325, 200, 25), pygame.Rect(200, 131, 600, 25)]
        self.stairs = [pygame.Rect(250, 505, 70, 270), pygame.Rect(680, 505, 70, 270), pygame.Rect(465, 338, 70, 212)]
        self.bombs = [pygame.Rect(400, 450, 50, 50), pygame.Rect(550, 450, 50, 50), pygame.Rect(10, 400, 50, 50), pygame.Rect(940, 400, 50, 50), pygame.Rect(10, 225, 50, 50), pygame.Rect(940, 225, 50, 50), pygame.Rect(300, 30, 50, 50), pygame.Rect(700, 30, 50, 50)]
        self.ropes = [pygame.Rect(485, 131, 30, 130), pygame.Rect(60, 493, 30, 130), pygame.Rect(910, 493, 30, 130)]

        self.x = x
        self.y = y

        self.width = idle.get_width()
        self.height = idle.get_height()

        self.velocity = 5
        self.mass = 1

        self.direction = "right"

        self.jump = False
        self.jump_count = 10

        self.climb_up = False
        self.climb_down = False
        
        self.rope_climb = False

        self.climb_count = 0

        self.current_stair = None
        self.current_rope = None

        self.left = False
        self.right = False

        self.jump_count = 4

        self.animation_counter = 0
        self.jump_counter = 0

        self.player_control_rect = None

        self.hearts = 3

        self.grounds_down = []

    def check_horizontal_collision(self, player, grounds):
        if player != None:
            player_x = player.x
            player_width = player.width

            for ground in grounds:
                if player.colliderect(ground):
                    if ground.x + ground.width + self.player_control_rect.width >= player_x >= ground.x + ground.width - self.player_control_rect.width:
                        return 'collide-right'

                    if ground.x - self.player_control_rect.width <= player_x + player_width <= ground.x + self.player_control_rect.width:
                        return 'collide-left'

    def gravity(self):
        if self.player_control_rect != None:
            self.grounds_down = []

            for ground in self.grounds:
                if self.player_control_rect.x + self.player_control_rect.width >= ground.x and self.player_control_rect.x <= ground.x + ground.width:
                    if self.player_control_rect.y + self.height <= ground.y:
                        self.grounds_down.append(ground)

            if len(self.grounds_down) > 0:
                if self.grounds_down[-1].y > self.player_control_rect.y + self.height + self.velocity:
                    self.player_control_rect.y += self.velocity

    def animations(self):
        if self.jump:
            self.y -= (self.jump_count * abs(self.jump_count)) * 4     
            self.jump_count -= 2    

            if self.jump_count < 0:
                self.jump = False
                self.jump_count = 4

        if self.climb_up or self.climb_down or self.rope_climb:
            if self.climb_up:
                if self.climb_count < 3 and self.player_control_rect.y > self.current_stair.y + 30:
                    self.climb_count += 1

                else:
                    self.climb_count = 0

                self.player_control_rect = climb.get_rect(x=self.x, y=self.y)
                self.screen.blit(climb, self.player_control_rect)

            elif self.climb_down:
                if self.climb_count < 3:
                    self.climb_count += 1

                else:
                    self.climb_count = 0

                self.player_control_rect = climb.get_rect(x=self.x, y=self.y)
                self.screen.blit(climb, self.player_control_rect)

            elif self.rope_climb:
                if self.climb_count < 3:
                    self.climb_count += 1

                else:
                    self.climb_count = 0

                self.player_control_rect = rope.get_rect(x=self.x, y=self.y)
                self.screen.blit(rope, self.player_control_rect)   

            else:
                self.climb_up = False
                self.climb_down = False
                self.rope_climb = False             

        elif self.left:
            self.direction = "left"
            self.player_control_rect = running_left_animations[self.animation_counter].get_rect(x=self.x, y=self.y)
            self.screen.blit(running_left_animations[self.animation_counter], self.player_control_rect)

        elif self.right:
            self.direction = "right"
            self.player_control_rect = running_right_animations[self.animation_counter].get_rect(x=self.x, y=self.y)
            self.screen.blit(running_right_animations[self.animation_counter], (self.x, self.y))

        else:
            self.player_control_rect = idle.get_rect(x=self.x, y=self.y)
            self.screen.blit(idle, self.player_control_rect)