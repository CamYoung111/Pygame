import pygame
from random import randint

pygame.init()

# define colours
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
darkBlue = (36, 90, 190)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
orange = (255, 69, 0)

# initialises variables
score = 0
chance = 0
lives = 3
Quit = False

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Breakout")
clock = pygame.time.Clock()

allSpritesList = pygame.sprite.Group()
allPower = pygame.sprite.Group()
allBricks = pygame.sprite.Group()
powerSpritesList = []

# creates a power up class
class Power(pygame.sprite.Sprite):
	def __init__(self, power):
		super().__init__()

		self.image = pygame.Surface([40, 15])
		self.image.fill(black)
		self.image.set_colorkey(black)

		# allows for other power ups to be identified
		self.power = power

		pygame.draw.rect(self.image, (200, 0, 200), (0, 0, 40, 15))

		self.rect = self.image.get_rect()

# creates a paddle class
class Paddle(pygame.sprite.Sprite):
	def __init__(self, colour, width, height):
		super().__init__()

		self.image = pygame.Surface([width, height])
		self.image.fill(black)
		self.image.set_colorkey(black)

		pygame.draw.rect(self.image, colour, (0, 0, width, height))

		self.rect = self.image.get_rect()

	# method to move left
	def moveLeft(self, pixels):
		self.rect.x -= pixels
		if self.rect.x < 0:
			self.rect.x = 0

	# method to move right
	def moveRight(self, pixels):
		self.rect.x += pixels
		if self.rect.x > 700:
			self.rect.x = 700

# creates a ball class
class Ball(pygame.sprite.Sprite):
	def __init__(self, color, width, height):
		super().__init__()

		self.image = pygame.Surface([width, height])
		self.image.fill(black)
		self.image.set_colorkey(black)

		pygame.draw.rect(self.image, color, (0, 0, width, height))

		self.speed = [randint(4, 8), randint(-6, 6)]

		# stops the ball getting stuck horizontally
		if self.speed[1] == 0:
			self.speed[1] = 1

		self.rect = self.image.get_rect()

	# changes the speed of the ball
	def update(self):
		self.rect.x += self.speed[0]
		self.rect.y += self.speed[1]

	# bounces the ball in the opposite direction and a random speed vertically, stopping the ball getting stuck horizontally
	def bounce(self):
		self.speed[0] = -self.speed[0]
		self.speed[1] = randint(-6, 6)
		if self.speed[1] == 0:
			self.speed[1] = 1

#creates a class for the bricks
class Brick(pygame.sprite.Sprite):
	def __init__(self, colour, width, height):
		super().__init__()

		self.image = pygame.Surface([width, height])
		self.image.fill(black)
		self.image.set_colorkey(black)

		self.colour = colour

		pygame.draw.rect(self.image, colour, [0, 0, width, height])

		self.rect = self.image.get_rect()


# creates a new instance of the paddle class
paddle = Paddle(white, 100, 10)
paddle.rect.x = 350
paddle.rect.y = 560

# creates a new instance of the ball class
ball = Ball(white, 10, 10)
ball.rect.x = 345
ball.rect.y = 300

# creates the first layer of red bricks
for i in range(7):
	brick = Brick(red, 80, 30)
	brick.rect.x = 60 + i * 100
	brick.rect.y = 60

	# adds the brick to the all brick sprite list
	allBricks.add(brick)

# creates the second layer of orange bricks
for i in range(7):
	brick = Brick(orange, 80, 30)
	brick.rect.x = 60 + i * 100
	brick.rect.y = 100
	allBricks.add(brick)

# creates a third layer of yellow bricks
for i in range(7):
	brick = Brick(yellow, 80, 30)
	brick.rect.x = 60 + i * 100
	brick.rect.y = 140
	allBricks.add(brick)

# creates a fourth layer of green bricks
for i in range(7):
	brick = Brick(green, 80, 30)
	brick.rect.x = 60 + i * 100
	brick.rect.y = 180
	allBricks.add(brick)

# adds the paddle and ball to both the sprite lists
allSpritesList.add(paddle)
allSpritesList.add(ball)

# starts the main loop
while not Quit:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			Quit = True

		# quits the game if the escape key is pressed
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				Quit = True

	# gets key input form keyboard and move the paddle accordingly
	keys = pygame.key.get_pressed()
	if keys[pygame.K_a]:
		paddle.moveLeft(8)
	if keys[pygame.K_d]:
		paddle.moveRight(8)
	if keys[pygame.K_LEFT]:
		paddle.moveLeft(8)
	if keys[pygame.K_RIGHT]:
		paddle.moveRight(8)

	allSpritesList.update()

	# collision detection for the ball
	if ball.rect.x >= 790:
		ball.speed[0] = -ball.speed[0]
	if ball.rect.x <= 0:
		ball.speed[0] = -ball.speed[0]

	if ball.rect.y < 40:
		ball.speed[1] = -ball.speed[1]

	# if the ball hits the bottom of the screen
	if ball.rect.y >= 590:
		ball.speed[1] = -ball.speed[1]
		lives -= 1

		# resets the ball
		ball.rect.x = 390
		ball.rect.y = 290

		# resets the paddle
		paddle.rect.x = 350
		paddle.rect.y = 560

		pygame.display.flip()
		pygame.time.wait(500)

		# kills all power ups
		for x in range(len(powerSpritesList)):
			powerSpritesList[x].kill()

		#displays game over screen if the player loses
		if lives == 0:
			font = pygame.font.Font(None, 74)
			text = font.render("Game Over", 1, white)
			screen.blit(text, (250, 300))
			pygame.display.flip()
			pygame.time.wait(3000)
			Quit = True

	# collision detection for the ball and paddle
	if pygame.sprite.collide_mask(ball, paddle):
		ball.rect.x -= ball.speed[0]
		ball.rect.y -= ball.speed[1]
		ball.bounce()

	# collision collection for the brick and ball
	brickCollisionList = pygame.sprite.spritecollide(ball, allBricks, False)
	for brick in brickCollisionList:
		ball.bounce()
		brick.kill()

		# gives a score dependant of the colour of brick and determines the chance of a power op
		if brick.colour == green:
			score += 1
			chance = randint(1, 100)
		elif brick.colour == yellow:
			score += 2
			chance = randint(10, 100)
		elif brick.colour == orange:
			score += 3
			chance = randint(35, 100)
		elif brick.colour == red:
			score += 4
			chance = randint(50, 100)

		# creates a power up when the check is passed
		if chance >= 80:
			lenPlus = Power("scorePlus")
			lenPlus.rect.x = brick.rect.x
			lenPlus.rect.y = brick.rect.y
			powerSpritesList.append(lenPlus)
			allPower.add(lenPlus)

		# displays win message if there is no bricks left
		if len(allBricks) == 0:
			font = pygame.font.Font(None, 74)
			text = font.render("Level Complete", 1, white)
			screen.blit(text, (200, 300))
			pygame.display.flip()
			pygame.time.wait(3000)
			Quit = True

	# moves all the power ups down the screen
	for x in range(len(powerSpritesList)):
		powerSpritesList[x].rect.y += 2

		# kills the power ups that hit the bottom of the screen
		if powerSpritesList[x].rect.y >= 785:
			powerSpritesList[x].kill()

		# if the power up hit the paddle then adds "1" to the score
		if pygame.sprite.collide_mask(powerSpritesList[x], paddle):
			# due to a bug more than one is added to the score, so the value was decreased from 10 to 1 to compensate
			score += 1
			powerSpritesList[x].kill()
			pygame.display.flip()

	# fills the background as dark blue
	screen.fill(darkBlue)

	# draws the heads up display
	pygame.draw.line(screen, white, (0, 38), (800, 38), 2)
	font = pygame.font.Font(None, 34)
	text = font.render("Score: " + str(score), 1, white)
	screen.blit(text, (20, 10))
	text = font.render("Lives: " + str(lives), 1, white)
	screen.blit(text, (650, 10))

	# resets the power up chance
	chance = 0

	# draws all the sprites to the screen
	allSpritesList.draw(screen)
	allBricks.draw(screen)
	allPower.draw(screen)

	# updates the screen
	pygame.display.flip()

	clock.tick(60)

# quits pygame when the loop ends
pygame.quit()
