import torch
import random
import numpy as np
from AI_snake_game import SnakeGameAI, Direction, Point
from collections import deque
from model import Linear_QNet, Qtrainer
from helper import plot



max_mem = 100_000
batch_size = 1000
lr = 0.001

class Agent:
    
    def __init__(self):
        self.num_games = 0
        self.epsilon = 0
        self.gamma = 0
        self.mem = deque(maxlen=max_mem)
        self.model = Linear_QNet(11,256,3)
        self.trainer = Qtrainer(self.model, lr=lr, gamma=self.gamma)

    def get_state(self, game):
        head = game.snake[0]

        pt_l = Point(head.x-20, head.y)
        pt_r = Point(head.x+20, head.y)
        pt_u = Point(head.x, head.y-20)
        pt_d = Point(head.x, head.y+20)

        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.is_collision(pt_r)) or 
            (dir_l and game.is_collision(pt_l)) or 
            (dir_u and game.is_collision(pt_u)) or 
            (dir_d and game.is_collision(pt_d)),

            # Danger right
            (dir_u and game.is_collision(pt_r)) or 
            (dir_d and game.is_collision(pt_l)) or 
            (dir_l and game.is_collision(pt_u)) or 
            (dir_r and game.is_collision(pt_d)),

            # Danger left
            (dir_d and game.is_collision(pt_r)) or 
            (dir_u and game.is_collision(pt_l)) or 
            (dir_r and game.is_collision(pt_u)) or 
            (dir_l and game.is_collision(pt_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y  # food down
            ]
        
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.mem.append((state, action, reward, next_state, done))

    def train_long_mem(self):
        if len(self.mem)>batch_size:
            mini_sample = random.sample(self.mem, batch_size)
        else:
            mini_sample = self.mem
        
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

        

    def train_short_mem(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 80 - self.num_games
        final_move = [0,0,0]
        if random.randint(0,200) < self.epsilon:
            move = random.randint(0,2)
            final_move[move] = 1
        else:
            state = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        
        return final_move
            


def train():
    plot_scores = []
    plot_mean_scores = []
    total = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()

    while True:
        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)

        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        agent.train_short_mem(state_old, final_move, reward, state_new, done)

        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            game.reset()
            agent.num_games += 1
            agent.train_long_mem()

            if score > record:
                record = score
            
            print('Game: ', agent.num_games, 'Score: ', score, 'Record: ', record)

            plot_scores.append(score)
            total += score
            mean_score = total/agent.num_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()
