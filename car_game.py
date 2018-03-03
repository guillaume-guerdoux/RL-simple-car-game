import pygame
import random
import numpy as np
# Let's import the Car Class
from car import Car

GREEN = (20, 255, 140)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
BLUE = (100, 100, 255)

colorList = (RED, GREEN, PURPLE, YELLOW, CYAN, BLUE)


class CarGame():

    def __init__(self, speed, min_speed, screenheight):
        # This will be a list that will contain all the sprites we intend to use in our game.
        self.all_sprites_list = pygame.sprite.Group()
        self.SPEED = speed
        self.MIN_SPEED = min_speed
        self.screenheight = screenheight

        self.playerCar = Car(RED, 60, 80, 70)
        self.playerCar.rect.x = 430
        self.playerCar.rect.y = screenheight - 100

        self.car1 = Car(PURPLE, 60, 80, random.randint(50, 100))
        self.car1.rect.x = 310
        self.car1.rect.y = -100

        self.car2 = Car(YELLOW, 60, 80, random.randint(50, 100))
        self.car2.rect.x = 430
        self.car2.rect.y = -600

        """self.car3 = Car(CYAN, 60, 80, random.randint(50, 100))
        self.car3.rect.x = 260
        self.car3.rect.y = -300

        self.car4 = Car(BLUE, 60, 80, random.randint(50, 100))
        self.car4.rect.x = 360
        self.car4.rect.y = -900"""

        # Add the car to the list of objects
        self.all_sprites_list.add(self.playerCar)
        self.all_sprites_list.add(self.car1)
        self.all_sprites_list.add(self.car2)
        """self.all_sprites_list.add(self.car3)
        self.all_sprites_list.add(self.car4)"""

        self.all_coming_cars = pygame.sprite.Group()
        self.all_coming_cars.add(self.car1)
        self.all_coming_cars.add(self.car2)
        """self.all_coming_cars.add(self.car3)
        self.all_coming_cars.add(self.car4)"""

        # Allowing the user to close the window...
        self.clock = pygame.time.Clock()

    def play_one_step(self, action):
        """ Action is 0 (nothing), 1 (left) or 2 (right)
        Update the game and return :
            state, reward, done"""
        done = False
        if action == 0:
            pass
        if action == 1:
            self.playerCar.moveLeft(5)
        if action == 2:
            self.playerCar.moveRight(5)
        """if K_UP:
            self.SPEED += 0.05
        if K_DOWN:
            if self.SPEED > self.MIN_SPEED + 0.05:
                self.SPEED -= 0.05"""

        # Game Logic
        for car in self.all_coming_cars:
            car.moveForward(self.SPEED)
            if car.rect.y > self.screenheight:
                car.changeSpeed(random.randint(50, 100))
                car.repaint(random.choice(colorList))
                car.rect.y = -200

        # Car collision
        car_collision_list = pygame.sprite.spritecollide(
            self.playerCar, self.all_coming_cars, False)
        for car in car_collision_list:
            print("Car crash!")
            # End Of Game
            done = True
        # Detect if out of pistes
        if self.playerCar.rect.x < 310:
            print("Car out")
            done = True
        if self.playerCar.rect.x > 440:
            print("Car out")
            done = True
        return ([self.playerCar.rect.x, self.playerCar.rect.y, self.playerCar.speed,
                self.car1.rect.x, self.car1.rect.y, self.car1.speed,
                self.car2.rect.x, self.car2.rect.y, self.car2.speed],
                1, done)
