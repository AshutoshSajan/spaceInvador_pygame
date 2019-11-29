import math
import random

import pygame
from pygame import mixer

# print(pygame, "pygame...")
# initializing the pygame
pygame.init()

# creating a screen
screen = pygame.display.set_mode((1200, 800))

# background image
background = pygame.image.load("background.png")

# background sound
mixer.music.load("background.wav");
mixer.music.play(-1) #-1 will play the music in loop

# title and icon
pygame.display.set_caption("space invader")

game_icon = pygame.image.load("logo.png");
pygame.display.set_icon(game_icon)

# player
playerImg = pygame.image.load("logo.png")
playerX = 600
playerY = 700
playerX_change = 0
playerY_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 6

for i in range(number_of_enemies):
	enemyImg.append(pygame.image.load("monster.png"))
	enemyX.append(random.randint(0,1100))
	enemyY.append(random.randint(50,150))
	enemyX_change.append(1)
	enemyY_change.append(4)

# bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 700
bulletX_change = 0
bulletY_change = 4

# fire and ready are the two bullet states
bullet_state = "ready"

# score
points = 0
# add font to the score text, download free fonts at => https://www.dafont.com
font = pygame.font.Font('freesansbold.ttf', 30) #font and font size 2 parameters
textX = 10
textY = 10

# game over function
game_over_font = pygame.font.Font('freesansbold.ttf', 64) #font and font size 2 parameters
# game_over_text_posX = 400
# game_over_text_posY = 300

def game_over():
	game_over_text = font.render("GAME OVER", True, (255,0,0))
	screen.blit(game_over_text, (400, 300))

def show_score(x,y):
	score = font.render("SCORE : " + str(points), True, (255,255,255))
	screen.blit(score, (x, y))

def player(x,y):
	screen.blit(playerImg, (x,y))

def enemy(x,y,i):
	screen.blit(enemyImg[i], (x,y))

def fire_bullet(x,y):
	global bullet_state
	bullet_state = "fire"
	screen.blit(bulletImg, (x + 5,y + 6))

def isCollision(enemyX,enemyY, bulletX,bulletY):
	distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
	if distance < 25:
		return True
	else:
		return False


# game loop everything which is changing continuously will comes under game loop 
running = True

while running:
	
	# game window background color in rgb values
	screen.fill((0,0,0))

	# background image
	screen.blit(background, (0, 0))

	for event in pygame.event.get():
		# print(event)

		if event.type == pygame.QUIT:
			running = False

		# if keystroke is pressed check which key is that	
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change = -2
			if event.key == pygame.K_RIGHT:
				playerX_change = 2
			if event.key == pygame.K_UP:
				playerY_change = -2
			if event.key == pygame.K_DOWN:
				playerY_change = 2
			if event.key == pygame.K_SPACE:
				if bullet_state is "ready":
					bullet_sound = mixer.Sound("laser.wav")
					bullet_sound.play()
					# get the current x position of space-ship
					bulletX = playerX
					fire_bullet(bulletX, bulletY)

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerX_change = 0
			elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
				playerY_change = 0

	

	# drow the player on game window
	playerX += playerX_change
	playerY += playerY_change

	#checking for boundry for spaceship 
	if playerX <= 0:
		playerX = 0
	elif playerX >= 1200:
		playerX = 1150
	if playerY <= 0:
		playerY = 0
	elif playerY >= 800:
		playerY = 750

	# enemy movement
	for i in range(number_of_enemies):

		# game over
		if(enemyY[i] > 800):
			for j in range(number_of_enemies):
				enemyY[j] = 2000

			game_over()
			break

		enemyX[i] += enemyX_change[i]
		# enemyY += enemyY_change

		#checking for boundry for enemy
		if enemyX[i] <= 0:
			enemyX_change[i] = 1
			enemyY[i] += enemyY_change[i]
		elif enemyX[i] >= 1100:
			enemyX_change[i] = -1
			enemyY[i] += enemyY_change[i]

		# collision report
		collision = isCollision(enemyX[i],enemyY[i], bulletX,bulletY)

		if collision:
			expolsion_sound = mixer.Sound("expolsion.wav")
			expolsion_sound.play()
			bulletY = 700
			bullet_state = "ready"
			points += 1
			enemyX[i] = random.randint(0, 1100)
			enemyY[i] = random.randint(50, 150)

		enemy(enemyX[i], enemyY[i], i)

	# bullet movement
	if bulletY <= 0:
		bulletY = 700
		bullet_state = "ready"

	if bullet_state is "fire":
		fire_bullet(bulletX, bulletY)
		bulletY -= bulletY_change

	player(playerX,playerY)
	show_score(textX, textY)
	# update the game window after adding the bg color otherwise bg will not get applied
	pygame.display.update()

