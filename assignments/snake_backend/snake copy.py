import pygame, random, time
from color_palette import *

pygame.init()

HEIGHT = 720
WIDTH = 720

clock = pygame.time.Clock()
FPS = 5

count_food = 0
count_level = 1

color_index = 1 
color_random = COLOR_BLUE

screen = pygame.display.set_mode((WIDTH, HEIGHT))

font = pygame.font.Font('game_bubble.ttf', 30)
font_endgame = pygame.font.Font('game_bubble.ttf', 80)
sound_food = pygame.mixer.Sound('food_eating.wav')

CELL = 30

# def draw_grid(): 
#     for i in range(WIDTH // CELL):
#         for j in range(HEIGHT // CELL):
#             pygame.draw.rect(screen, COLOR_GRAY, (i * CELL, j * CELL, CELL, CELL))

def draw_chess_board(): # drawing a chess board
    colors = [COLOR_GRAY, COLOR_WHITE]
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))

class Point:
    def __init__(self, x, y): # we create a separate class for point, in order to easily get the x and y coords
        self.x = x            # while coding. Otherwise, we would create a tuple for each segment's x and y, 
        self.y = y            # and then working with a loop to get x and y, which is inconvenient

class Snake:
    def __init__(self):
        self.body = [Point(3, 10), Point(4, 10), Point(5, 10)] # the initial coords of the body 
        self.dx = 1 
        self.dy = 0 
        
    def move(self):
        for i in range(len(self.body) - 1, 0, -1): # we iterate from the last segment to the segment before the head of the snake
            self.body[i].x = self.body[i - 1].x # we get the coords of the previous segment and assign it 
            self.body[i].y = self.body[i - 1].y # to the last segment, and so on, until we reach the segment before the head of the snake

        self.body[0].x += self.dx # the head of the snake moves in the given direction of x and y
        self.body[0].y += self.dy


        # # checks the right border                 # going through borders, appearing in the wrong border
        # if self.body[0].x > WIDTH // CELL - 1:
        #     self.body[0].x = 0
        # # checks the left border
        # if self.body[0].x < 0:
        #     self.body[0].x = WIDTH // CELL - 1
        # # checks the top border
        # if self.body[0].y < 0:
        #     self.body[0].y = HEIGHT // CELL - 1
        # # checks the bottom border
        # if self.body[0].y > HEIGHT // CELL - 1:
        #     self.body[0].y = 0

    def draw_snake(self): # drawing the snake
        head = self.body[0]
        pygame.draw.rect(screen, COLOR_RED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, COLOR_GREEN, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food): # checking collision with food
        global FPS, count_food, count_level
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y: # if the coords of the head of the snake are the same
            self.body.append(Point(head.x, head.y))       # as the food's coords, add a segment to the snake's body 
            # in between the collision and next move(), graphically the tail and middle segments stay the same, and
            # a new segment is added at the head's position and the head is moved in its direction forward
            food.generate_random_pos()
            if color_index == 0:
                count_food += 3
            elif color_index == 1:
                count_food += 2
            elif color_index == 2:
                count_food += 1
            sound_food.play()
            if count_food % 5 == 0:
                count_level += 1
                FPS += 2

    def check_collision_wall(self): # checking collision with a wall
        global running
        head = self.body[0]
        if head.x > WIDTH // CELL - 1 or head.x < 0: # if the snake collides with the wall
            return True 
        if head.y < 0 or head.y > HEIGHT // CELL - 1: # if the snake collides with the wall
            return True
        return False
    
    # def check_collision_self(self):
    #     head = self.body[0]
    #     for segment in self.body[1:]:
    #         if segment.x == head.x and segment.y == head.y:
    #             return True
    #     return False
    
        
class Food:
    def __init__(self):
        self.pos = Point(10, 10)
        self.food_colors = [COLOR_PURPLE, COLOR_BLUE, COLOR_LIGHTBLUE]
        self.creation_time = time.time() # Storing time when food is created
        self.food_lifetime = 5 # Food's 'Life Time' in seconds 

    def generate_random_pos(self): # generating random position for food
        temp_x = random.randint(0, WIDTH // CELL - 1)
        temp_y = random.randint(0, HEIGHT // CELL - 1)
        
        if all((segment.x != temp_x or segment.y != temp_y) for segment in snake.body): 
            # if the generated x and y positions are the same in one of the segments of the body, 
            # generate the coordinates again
            self.pos.x = temp_x
            self.pos.y = temp_y
            self.creation_time = time.time() # the creation time of food
        else:
            self.generate_random_pos() 
    
    def draw_food(self): # drawing food
        pygame.draw.rect(screen, color_random, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_color(self): # generating random position for food
        global color_index, color_random
        # getting random color_index and color_random
        color_index = random.randint(0, 2)
        color_random = food.food_colors[color_index]

    def check_food_lifetime(self):
        if time.time() - self.creation_time > self.food_lifetime: # return True if the food appears on screen longer
            return True                                           # than it's lifetime
        return False

food = Food()
snake = Snake()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.dx != -1: # If the player pressed the RIGHT arrow key, and
                snake.dx = 1                                # the snake is not currently moving left, then 
                snake.dy = 0                                # allow the snake to turn right."
            if event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dx = -1
                snake.dy = 0
            if event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dx = 0
                snake.dy = 1
            if event.key == pygame.K_UP and snake.dy != 1:
                snake.dx = 0
                snake.dy = -1

    if snake.check_collision_wall(): # if the snake collides with the wall, 'running' would be False
        running = False
        screen.fill(COLOR_GREEN)

        # Rendering the final score and level messages
        image_endgame_score = font_endgame.render("Total Score: " + str(count_food), True, COLOR_BLACK)
        image_endgame_score_rect = image_endgame_score.get_rect(center = (WIDTH // 2, HEIGHT // 2 - 50))
        image_endgame_level = font_endgame.render("Level: " + str(count_level), True, COLOR_BLACK)
        image_endgame_level_rect = image_endgame_level.get_rect(center = (WIDTH // 2, HEIGHT // 2 + 50))

        # Displaying messages on the screen 
        screen.blit(image_endgame_score, image_endgame_score_rect)
        screen.blit(image_endgame_level, image_endgame_level_rect)    

        pygame.display.flip()

        time.sleep(5) # waiting for 5 seconds before quitting the game

    screen.fill(COLOR_BLACK) # we have to fill our screen with black, otherwise on the new iteration of our
                             # 'while' loop, everything that is to be drawn will be be drawn on top of 
                             # things that were drawn on the previous iteration 

    draw_chess_board()

    snake.move()
    snake.check_collision(food)

    if food.check_food_lifetime(): # if the food is 'expired', regenerate the position and color of the food
        food.generate_random_color()
        food.generate_random_pos()

    food.draw_food()
    snake.draw_snake()
    # if snake.check_collision_self():
    #     running = False

    score_text = font.render(f"Score: {count_food}", True, COLOR_BLUE) # the text of the score 
    level_text = font.render(f'Level: {count_level}', True, COLOR_RED)
    screen.blit(score_text, (10, 10)) # showing the score on the screen
    screen.blit(level_text, (600, 10))

    pygame.display.flip() # updating the screen, so that the user sees the changes
    clock.tick(FPS)

pygame.quit()

# 2. to understand why the game stops immediately

