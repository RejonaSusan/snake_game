import pygame, sys, random
from pygame.math import Vector2


class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x*cell_size), int(self.pos.y*cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, (197, 55, 76), fruit_rect)

    def randomize(self):
        self.x = random.randint(0,cell_num-1)
        self.y = random.randint(0,cell_num-1)
        self.pos = Vector2(self.x, self.y)


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (143, 101, 75), block_rect)

    def move(self):
        if self.new_block == True:
            body_cpy = self.body[:]
            body_cpy.insert(0,body_cpy[0]+self.direction)
            self.body = body_cpy[:]
            self.new_block = False
        else:
            body_cpy = self.body[:-1]
            body_cpy.insert(0,body_cpy[0]+self.direction)
            self.body = body_cpy[:]

    def add_block(self):
        self.new_block = True

    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)


class MAIN_AI:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.frame_iteration = 0


    def update(self):
        self.snake.move()
        self.check_collision()
        self.check_fail()
        
    
    def draw_ele(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.score()


    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()


    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_num or not 0 <= self.snake.body[0].y < cell_num:
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()


    def game_over(self):
        score = len(self.snake.body) - 3
        print(f"Game Over! Your Score: {score}")
        pygame.quit()
        sys.exit()
        

    def score(self):
        score_text = "Score: " + str(len(self.snake.body)-3)
        score_surface = game_font.render(score_text,True,(56,74,12))
        score_x = int(cell_size*cell_num - 60)
        score_y = int(cell_size*cell_num - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        screen.blit(score_surface,score_rect)


    def play_step(self, action):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.update()
            if event.type == SCREEN_UPDATE:
                self.update()


pygame.init()
cell_size = 40
cell_num = 20
screen = pygame.display.set_mode((cell_size*cell_num,cell_size*cell_num))
clock = pygame.time.Clock()
game_font = pygame.font.Font('arial_1.ttf', 25)


SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)



main_game = MAIN_AI()


while True:
    main_game.play_step()

    screen.fill((175, 215, 70))
    main_game.draw_ele()
    pygame.display.update()
    clock.tick(60)