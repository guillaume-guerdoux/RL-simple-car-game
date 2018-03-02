import pygame
import random
# Let's import the Car Class
from car import Car
pygame.init()

GREEN = (20, 255, 140)
GREY = (210, 210, 210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
BLUE = (100, 100, 255)

colorList = (RED, GREEN, PURPLE, YELLOW, CYAN, BLUE)


SCREENWIDTH = 800
SCREENHEIGHT = 600

size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Car Racing")


class CarGame():

    def __init__(self):

# This will be a list that will contain all the sprites we intend to use in our game.
        self.all_sprites_list = pygame.sprite.Group()
        self.SPEED = 1
        self.MIN_SPEED = 0.5

        self.playerCar = Car(RED, 60, 80, 70)
        self.playerCar.rect.x = 160
        self.playerCar.rect.y = SCREENHEIGHT - 100

        self.car1 = Car(PURPLE, 60, 80, random.randint(50, 100))
        self.car1.rect.x = 60
        self.car1.rect.y = -100

        self.car2 = Car(YELLOW, 60, 80, random.randint(50, 100))
        self.car2.rect.x = 160
        self.car2.rect.y = -600

        self.car3 = Car(CYAN, 60, 80, random.randint(50, 100))
        self.car3.rect.x = 260
        self.car3.rect.y = -300

        self.car4 = Car(BLUE, 60, 80, random.randint(50, 100))
        self.car4.rect.x = 360
        self.car4.rect.y = -900


        # Add the car to the list of objects
        self.all_sprites_list.add(self.playerCar)
        self.all_sprites_list.add(self.car1)
        self.all_sprites_list.add(self.car2)
        self.all_sprites_list.add(self.car3)
        self.all_sprites_list.add(self.car4)

        self.all_coming_cars = pygame.sprite.Group()
        self.all_coming_cars.add(self.car1)
        self.all_coming_cars.add(self.car2)
        self.all_coming_cars.add(self.car3)
        self.all_coming_cars.add(self.car4)


        # Allowing the user to close the window...
        self.carryOn = True
        self.clock = pygame.time.Clock()

    def play_one_step(self, K_LEFT, K_RIGHT, K_UP, K_DOWN):
        """ Update the game and return :
        state, reward, done"""
        if K_LEFT:
            self.playerCar.moveLeft(5)
        if K_RIGHT:
            self.playerCar.moveRight(5)
        if K_UP:
            self.SPEED += 0.05
        if K_DOWN:
            if self.SPEED > self.MIN_SPEED + 0.05:
                self.SPEED -= 0.05

        # Game Logic
        for car in self.all_coming_cars:
            car.moveForward(self.SPEED)
            if car.rect.y > SCREENHEIGHT:
                car.changeSpeed(random.randint(50, 100))
                car.repaint(random.choice(colorList))
                car.rect.y = -200

        # Car collision
        car_collision_list = pygame.sprite.spritecollide(
            self.playerCar, self.all_coming_cars, False)
        for car in car_collision_list:
            print("Car crash!")
            # End Of Game
            self.carryOn = False

        # Detect if out of pistes
        if self.playerCar.rect.x < 50:
            print("Car out")
            self.carryOn = False
        if self.playerCar.rect.x > 370:
            print("Car out")
            self.carryOn = False

    def play(self):

        while self.carryOn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.carryOn = False
            keys = pygame.key.get_pressed()
            self.play_one_step(keys[pygame.K_LEFT], keys[pygame.K_RIGHT],
                               keys[pygame.K_UP], keys[pygame.K_DOWN])
            self.all_sprites_list.update()

            # Drawing on Screen
            screen.fill(GREEN)
            # Draw The Road
            pygame.draw.rect(screen, GREY, [40, 0, 400, SCREENHEIGHT])
            # Draw Line painting on the road
            pygame.draw.line(screen, WHITE, [140, 0], [140, SCREENHEIGHT], 5)
            # Draw Line painting on the road
            pygame.draw.line(screen, WHITE, [240, 0], [240, SCREENHEIGHT], 5)
            # Draw Line painting on the road
            pygame.draw.line(screen, WHITE, [340, 0], [340, SCREENHEIGHT], 5)

            # Now let's draw all the sprites in one go. (For now we only have 1 sprite!)
            self.all_sprites_list.draw(screen)

            # Refresh Screen
            pygame.display.flip()

            # Number of frames per secong e.g. 60
            self.clock.tick(20)

        pygame.quit()

if __name__ == "__main__":
    car_game = CarGame()
    car_game.play()
