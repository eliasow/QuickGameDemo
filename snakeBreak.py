import pygame
import random

###GLOBAL VARIABLES
bricks = []
snakePositions = []
gameOver = False

###OBJECT/CLASS DEFENITIONS
class Snake(object):
    def __init__(self):
        global snakePositions
        self.direction = [0, 0]
        for i in range(17):
            snakePositions.append([40, 50])

    def draw(self, window):
        color = 10
        index = 0
        for position in snakePositions: 
            if index != len(snakePositions) - 1:
                pygame.draw.rect(window, (color / 2,255,color), [position[0]*10, position[1]*10, 10, 10])
                color += 15
                index += 1

    def handleSnakeMovement(self):
        temp = snakePositions[0]
        snakePositions[0] = [snakePositions[0][0] + (self.direction[0]), snakePositions[0][1] + (self.direction[1])]
        if snakePositions[0][0] < 1:
            snakePositions[0][0] = 99
        if snakePositions[0][0] >= 100:
            snakePositions[0][0] = 1
        if snakePositions[0][1] < 36:
            snakePositions[0][1] = 78
        if snakePositions[0][1] > 78:
            snakePositions[0][1] = 36
        for i in range( 1,len(snakePositions) ):
            if (snakePositions[i][0] != temp[0] or snakePositions[i][1] != temp[1]):
                newTemp = snakePositions[i]
                snakePositions[i] = temp
                temp = newTemp

class Ball(object):
    def __init__(self,x,y,w,h,color):
        self.x = random.randint(1,100) * 10
        self.y = 350
        self.w = w
        self.h = h
        self.color = color
        self.xspeed = random.randint(2,4)
        self.yspeed = random.randint(2,4)

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

###HELPER FUNCTIONS

###DRAW GAME OVER SCREEN
def gameOverScreen():
    font = pygame.font.Font(None, 64)
    text = font.render(("Better luck next time!"), 100, (255,255,255))
    window.blit(text, (40, 400))   
    font = pygame.font.Font(None, 40)
    text = font.render(("Press R to restart or Q to quit"), 100, (255,255,255))
    window.blit(text, (40, 600))  
    scoreText = font.render(("You got a final score of "+str(Score)+"."), 100, (255,255,255))
    window.blit(scoreText, (40, 520)) 
    pygame.display.update()
    return
    
###SETUP BRICKS FOR START OF GAME
def wallSetup():
    global bricks
    bricks = []
    for i in range(8):
        for j in range(12):
            bricks.append(Brick(10 + j * 82, 50 + i * 35, 72, 25, (255,100 + i * 5, i * 15)))

###DRAW CURRENT GAME STATE
def updateWindow():
    global bricks
    global gameOver
    window.blit(background,(0,0))
    if (gameOver):
        return gameOverScreen()
    ball.handleBallMovement()
    snake.handleSnakeMovement()
    ball.draw(window)
    snake.draw(window)
    for block in bricks:
        if block.hit == False:
            block.draw(window)
    font = pygame.font.Font(None, 32)
    scoreText = font.render(("Score:"+str(Score)), 100, (255,255,255))
    window.blit(scoreText, (10, 20))
    pygame.display.update()

###MAIN GAME LOGIC
if __name__ == '__main__':

    Score = 0
    
    width = 1000
    height = 800

    pygame.init()
    ###SOUND SETUP
    pygame.mixer.init()
    bounce = pygame.mixer.Sound('sounds/bounce.wav')
    snakeSound = pygame.mixer.Sound('sounds/snake.wav')
    bounce.set_volume(.1)
    snakeSound.set_volume(.1)
    ###IMAGE SETUP
    window = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Snake-Break")
    background = pygame.image.load('images/background.jpg')

    clock = pygame.time.Clock()

    ball = Ball(10, 500, 10, 10, (255, 255, 255))
    snake = Snake()
    wallSetup()
    updateWindow()

    running = True

    ###CORE LOOP
    while(running):

        clock.tick(10)
        window.blit(background,(0,0))

        ### HANDLE COLLISIONS 
        for i in range(len(snakePositions)):
            tolerance = .8
            if ((ball.x / 10 >= snakePositions[i][0] - tolerance and ball.x / 10 <= snakePositions[i][0] + tolerance) and (ball.y / 10 >= snakePositions[i][1] - tolerance and ball.y / 10 <= snakePositions[i][1] + tolerance)):
                ###HEAD OF SNAKE
                if (i == 0):
                    ball.x += (snake.direction[0] * 10)
                    ball.y += (snake.direction[1] * 10)
                    if ((snake.direction[0] < 0 and ball.xspeed > 0) or (snake.direction[0] > 0 and ball.xspeed < 0)):
                        ball.xspeed *= -1
                    if ((snake.direction[1] < 0 and ball.yspeed > 0) or (snake.direction[1] > 0 and ball.yspeed < 0)):
                        ball.yspeed *= -1
                    ball.handleBallMovement()
                    pygame.mixer.Sound.play(snakeSound)
                    break
                ###BODY OF SNAKE
                if i > 0 and i < len(snakePositions) - 1:
                    cur = snakePositions[i]
                    prev = snakePositions[i-1]
                    nxt = snakePositions[i + 1]
                    ###HORIZONTAL SNAKE
                    if (prev[0] == cur[0] == nxt[0]):
                        ball.xspeed = (ball.xspeed * -1)
                        ball.handleBallMovement()
                        pygame.mixer.Sound.play(snakeSound)
                        break
                    ###VERTICAL SNAKE
                    elif (prev[1] == cur[1] == nxt[1]):
                        ball.yspeed = (ball.yspeed * -1)
                        ball.handleBallMovement()
                        pygame.mixer.Sound.play(snakeSound)
                        break
                    ###CORNER SNAKE
                    else:
                        if (not (([round(ball.x + ball.xspeed,-1) // 10 , round(ball.y - ball.yspeed,-1) // 10] ) in snakePositions)):
                            ball.yspeed = (ball.yspeed * -1)
                        if (not (([round(ball.x - ball.xspeed, -1) // 10, round(ball.y + ball.yspeed, -1) // 10] ) in snakePositions)):
                            ball.xspeed = (ball.xspeed * -1)
                        ball.handleBallMovement()
                        pygame.mixer.Sound.play(snakeSound)
                        break

        ###COLLISIONS WITH SIDES 
        if (ball.x < 1):
            ball.x = 1
            ball.xspeed = (ball.xspeed * -1)
            if ball.yspeed > 0:
                ball.yspeed += .1
            else:
                ball.yspeed -= .1

        if (ball.x > 988):
            ball.x = 988
            ball.xspeed = (ball.xspeed * -1)
            if ball.yspeed > 0:
                ball.yspeed += .1
            else:
                ball.yspeed -= .1

        ###COLLISION WITH CEILING
        if (ball.y <= 0):
            ball.yspeed = (ball.yspeed * -1)

        ###BALL LOST
        if ball.y > 800:
            gameOver = True

        ###BRICK COLLISIONS
        for block in bricks:
            if not block.hit:
                if ((ball.x >= block.x - 10 and ball.x  <= block.x + 73) and (ball.y >= block.y - 10 and ball.y  <= block.y + 26)):
                    pygame.mixer.Sound.play(bounce)
                    block.color = (0,0,0)
                    block.hit = True
                    ball.yspeed = ball.yspeed * -1
                    if ball.xspeed > 0:
                        ball.xspeed += .1
                    else:
                        ball.xspeed -= .1
                    Score += 1

        updateWindow()

        ###HANDLE INPUT
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
                    snake = Snake()
            updateWindow()
    pygame.quit()



