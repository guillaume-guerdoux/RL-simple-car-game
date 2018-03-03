import numpy as np
from model import Agent
from car_game import CarGame
import pygame
import torch
import torch.optim as optim
from torch.autograd import Variable
from torch.distributions import Categorical
import matplotlib.pyplot as plt

GREEN = (20, 255, 140)
GREY = (210, 210, 210)
WHITE = (255, 255, 255)

SCREENWIDTH = 800
SCREENHEIGHT = 600

size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Car Racing")


def select_action(state):
    """ Action returned by agent"""
    state = torch.from_numpy(state).float().unsqueeze(0)
    probs = policy(Variable(state))
    # print(probs)
    m = Categorical(probs)
    action = m.sample()
    policy.saved_log_probs.append(m.log_prob(action))
    return action.data[0]


def finish_episode(show=False):
    """ bakprop and update agent"""
    R = 0
    policy_loss = []
    rewards = []
    for r in policy.rewards[::-1]:
        R = r + gamma * R
        rewards.insert(0, R)

    rewards = torch.Tensor(rewards)
    rewards = (rewards - rewards.mean()) / (rewards.std() + np.finfo(np.float32).eps)
    for log_prob, reward in zip(policy.saved_log_probs, rewards):
        policy_loss.append(-log_prob * reward)
    optimizer.zero_grad()
    policy_loss = torch.cat(policy_loss).sum()
    policy_loss.backward()
    optimizer.step()
    if show:
        print("Reward : ", R, ' Policy Loss', policy_loss.data[0])
    del policy.rewards[:]
    del policy.saved_log_probs[:]


def main():
        global nb_episodes_before_dying
        nb_episodes_before_dying = []
        for i_episode in range(0, 1000):
            car_game = CarGame(speed=1, min_speed=0.5, screenheight=SCREENHEIGHT)
            state = [car_game.playerCar.rect.x]
            pygame.init()
            # print(i_episode)
            carryOn = True
            nb_episodes = 0
            while carryOn:
                nb_episodes += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        carryOn = False
                action = select_action(np.array(state))
                # print(action)

                state, reward, done = car_game.play_one_step(action)
                policy.rewards.append(reward)
                if done or nb_episodes > 1000:
                    nb_episodes_before_dying.append(nb_episodes)
                    carryOn = False
                car_game.all_sprites_list.update()

                # Drawing on Screen
                screen.fill(GREEN)
                # Draw The Road
                pygame.draw.rect(screen, GREY, [300, 0, 200, SCREENHEIGHT])
                # Draw Line painting on the road
                pygame.draw.line(screen, WHITE, [400, 0], [400, SCREENHEIGHT], 5)
                # Draw Line painting on the road
                """pygame.draw.line(screen, WHITE, [240, 0], [240, SCREENHEIGHT], 5)
                # Draw Line painting on the road
                pygame.draw.line(screen, WHITE, [340, 0], [340, SCREENHEIGHT], 5)"""

                # Now let's draw all the sprites in one go. (For now we only have 1 sprite!)
                car_game.all_sprites_list.draw(screen)

                # Refresh Screen
                pygame.display.flip()

                # Number of frames per secong e.g. 60
                car_game.clock.tick(100)

            finish_episode(True)

if __name__ == "__main__":
    policy = Agent()
    optimizer = optim.Adam(policy.parameters(), lr=1e-2)
    gamma = 0.99
    main()
    plt.plot(nb_episodes_before_dying)
    plt.savefig('myfig.png')
