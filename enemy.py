import pygame
import random 

class Enemy():
    def __init__(self, player, screen, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.screen = screen

        self.random_x_array = [100, 200, 300, 400, 500, 600, 700, 800, 900]
        self.random_y_array = [100, 200, 300, 400, 500, 600]

        self.directions = ["horizontal", "vertical"]
        self.direction = "horizontal"

        self.x = random.choice(self.random_x_array)
        self.y = 0

        self.velocity = 15

        self.enemy_rect = pygame.Rect(self.x, self.y, 15, 15)

        self.player = player

    # DÜŞMANIN BAŞLANGIÇ HALİNE GETİRİLMESİ
    def reset_enemy(self):
        self.enemy_rect = pygame.Rect(self.x, self.y, 15, 15)

    # DÜŞMANIN HAREKET ETTİRİLMESİ
    def move(self):
        if self.enemy_rect.x >= self.screen_width or self.enemy_rect.y >= self.screen_height:
            self.direction = random.choice(self.directions)

            if self.direction == "horizontal":
                self.enemy_rect.y = 0
                self.enemy_rect.x = random.choice(self.random_y_array)

            else:
                self.enemy_rect.x = 0
                self.enemy_rect.y = random.choice(self.random_x_array)

        else:
            if self.direction == "horizontal":
                self.enemy_rect.y += self.velocity

            else:
                self.enemy_rect.x += self.velocity

    # DÜŞMANLA ÇARPIŞMANIN KONTROL EDİLMESİ
    def check_collision(self):
        if self.player.player_control_rect.colliderect(self.enemy_rect):
            self.reset_enemy()
            self.player.hearts -= 1

    # DÜŞMANIN EKRANDA GÖSTERİLMESİ        
    def display(self):
        pygame.draw.circle(self.screen, (255, 255, 255), (self.enemy_rect.x, self.enemy_rect.y), 15, 15)
