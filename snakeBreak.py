import pygame

bricks = []

snakePositions = []

gameOver = False

class Snake(object):
    def __init__(self, w, h, color):
        global snakePositions
        self.w = w
        self.h = h
        self.color = color
        self.direction = [0, 0]
        for i in range(16):
            snakePositions.append([40, 50])

    def draw(self, window):
        for position in snakePositions: 
            pygame.draw.rect(window, self.color, [position[0]*10, position[1]*10, self.w, self.h])


    def handleSnakeMovement(self):
        temp = snakePositions[0]
        snakePositions[0] = [snakePositions[0][0] + (self.direction[0]), snakePositions[0][1] + (self.direction[1])]
        if snakePositions[0][0] < 1:
            snakePositions[0][0] = 100
        if snakePositions[0][0] > 100:
            snakePositions[0][0] = 1
        if snakePositions[0][1] < 36:
            snakePositions[0][1] = 76
        if snakePositions[0][1] > 76:
            snakePositions[0][1] = 36
        for i in range( 1,len(snakePositions) ):
            if (snakePositions[i][0] != temp[0] or snakePositions[i][1] != temp[1]):
                newTemp = snakePositions[i]
                snakePositions[i] = temp
                temp = newTemp


class Ball(object):
    def __init__(self,x,y,w,h,color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.xspeed = 3
        self.yspeed = 3

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
            bricks.append(Brick(10 + j * 82, 50 + i * 35, 72, 25, (255, 255, 0)))

def updateWindow():
    global bricks
    global gameOver
    window.blit(background,(0,0))
    if (gameOver):
        font = pygame.font.Font(None, 64)
        text = font.render(("Better luck next time!"), 100, (255,255,255))
        window.blit(text, (40, 400))   
        font = pygame.font.Font(None, 40)
        text = font.render(("Press r to restart or q to quit"), 100, (255,255,255))
        window.blit(text, (40, 600))   
        pygame.display.update()
        return
    ball.handleBallMovement()
    snake.handleSnakeMovement()
    ball.draw(window)
    snake.draw(window)
    for block in bricks:
        if block.hit == False:
            block.draw(window)
    font = pygame.font.Font(None, 32)
    #livesText = font.render(("Lives:"+str(Lives)), 100, (255,255,255))
    scoreText = font.render(("Score:"+str(Score)), 100, (255,255,255))
    #window.blit(livesText, (10, 20))
    window.blit(scoreText, (10, 20))
    pygame.display.update()

def handleEnd():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_r:
                main()
    updateWindow()


if __name__ == '__main__':

    Score = 0

    pygame.init()

    width = 1000
    height = 800

    window = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Snake-Break")
    background = pygame.image.load('images/background.jpg')

    clock = pygame.time.Clock()

    ball = Ball(10, 500, 10, 10, (255, 255, 255))
    snake = Snake(10, 10 , (0, 0, 200))
    wallSetup()
    updateWindow()

    running = True
    while(running):
        clock.tick(10)
        window.blit(background,(0,0))

        ### HANDLE COLLISIONS 
        for i in range(len(snakePositions)):
            if ((ball.x / 10 >= snakePositions[i][0] - 1 and ball.x / 10 <= snakePositions[i][0] + 1) and (ball.y / 10 >= snakePositions[i][1] - 1 and ball.y / 10 <= snakePositions[i][1] + 1)):
                if i > 0 and i < len(snakePositions) - 1:
                    cur = snakePositions[i]
                    prev = snakePositions[i-1]
                    nxt = snakePositions[i + 1]
                    if (prev[0] == cur[0] == nxt[0]):
                        ball.xspeed = (ball.xspeed * -1)
                        break
                    elif (prev[1] == cur[1] == nxt[1]):
                        ball.yspeed = (ball.yspeed * -1)
                        break
                    else:
                        if (not (([round(ball.x + ball.xspeed,-1) // 10 , round(ball.y - ball.yspeed,-1) // 10] ) in snakePositions)):
                            ball.yspeed = (ball.yspeed * -1)
                        if (not (([round(ball.x - ball.xspeed, -1) // 10, round(ball.y + ball.yspeed, -1) // 10] ) in snakePositions)):
                            ball.xspeed = (ball.xspeed * -1)

        if ball.x < 2:
            ball.xspeed = (ball.xspeed * -1)
        
        if ball.x > 995:
            ball.xspeed = (ball.xspeed * -1)

        if ball.y > 800:
            gameOver = True

        for block in bricks:
            if not block.hit:
                if ((ball.x >= block.x - 10 and ball.x  <= block.x + 73) and (ball.y >= block.y - 3 and ball.y  <= block.y + 26)):
                    block.color = (0,0,0)
                    block.hit = True
                    ball.yspeed = ball.yspeed * -1
                    ball.xspeed += .2
                    Score += 1

        updateWindow()
        for event in pygame.event.get():
            if event.type ==  pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != [0, 1]:
                    snake.direction = [0,-1]
                elif event.key == pygame.K_DOWN and snake.direction != [0, -1]:
                    snake.direction = [0,1]
                elif event.key == pygame.K_LEFT and snake.direction != [1, 0]:
                    snake.direction = [-1,0]
                elif event.key == pygame.K_RIGHT and snake.direction != [-1, 0]:
                    snake.direction = [1,0]
                if event.key == pygame.K_q:
                    pygame.quit()
                elif event.key == pygame.K_r:
                    gameOver = False
                    wallSetup()
                    Score = 0
                    snakePositions = []
                    ball = Ball(10, 500, 10, 10, (255, 255, 255))
                    snake = Snake(10, 10 , (0, 0, 200))
            updateWindow()
    pygame.quit()



