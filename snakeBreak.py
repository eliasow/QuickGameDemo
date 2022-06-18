import pygame

bricks = []

snakePositions = []

class Snake(object):
    def __init__(self, w, h, color):
        global snakePositions
        self.w = w
        self.h = h
        self.color = color
        self.direction = [0, 0]
        for i in range(8):
            snakePositions.append([40, 50])

    def draw(self, window):
        for position in snakePositions: 
            pygame.draw.rect(window, self.color, [position[0]*10, position[1]*10, self.w, self.h])


    def handleSnakeMovement(self):
        temp = snakePositions[0]
        snakePositions[0] = [snakePosition[0][0] + (self.direction[0] * 10), snakePosition[0][1] + (self.direction[1] * 10)]
        for i in range( 1,len(snakePositions) - 1):
            if (snakePositions[i][0] != snakePositions[i - 1][0] and snakePositions[i][1] != snakePositions[i - 1][1]):
                snakePositions[i] = snakePositions[i - 1]


class Ball(object):
    def __init__(self,x,y,w,h,color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.xspeed = 0
        self.yspeed = 0

    def draw(self, window):
        pygame.draw.rect(window, self.color, [self.x, self.y, self.w, self.h])

    def handleBallMovement(self):
        self.y += self.yspeed
        self.x += self.xspeed

class Brick(object):
    def __init__(self,x,y,w,h,color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.hit = False

    def draw(self, window):
        pygame.draw.rect(window, self.color, [self.x, self.y, self.w, self.h])

def wallSetup():
    global bricks
    bricks = []
    for i in range(8):
        for j in range(12):
            bricks.append(Brick(10 + j * 79, 50 + i * 35, 70, 25, (255, 255, 0)))

def updateWindow():
    global bricks
    window.blit(background,(0,0))
    ball.draw(window)
    snake.draw(window)
    for block in bricks:
        block.draw(window)
    pygame.display.update()


if __name__ == '__main__':
    pygame.init()

    width = 1000
    height = 800

    window = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Snake-Break")
    background = pygame.image.load('images/background.jpg')

    clock = pygame.time.Clock()

    ball = Ball(0, 500, 10, 10, (255, 255, 255))
    snake = Snake(10, 10 , (0, 0, 200))
    wallSetup()
    updateWindow

    running = True
    while(running):
        clock.tick(100)
        window.blit(background,(0,0))

        for event in pygame.event.get():
            if event.type ==  pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != [1, 0]:
                    self.direction = [-1,0]
        updateWindow()
    pygame.quit()
