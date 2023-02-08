import pygame

pygame.init()

win = pygame.display.set_mode((765, 430))
#win = pygame.display.set_mode((500, 480))
pygame.display.set_caption("First Game")


walkRight = [pygame.image.load('../Game/R1.png'), pygame.image.load('../Game/R2.png'), pygame.image.load(
    '../Game/R3.png'),
             pygame.image.load('../Game/R4.png'), pygame.image.load('../Game/R5.png'), pygame.image.load(
        '../Game/R6.png'),
             pygame.image.load('../Game/R7.png'), pygame.image.load('../Game/R8.png'), pygame.image.load(
        '../Game/R9.png')]
walkLeft = [pygame.image.load('../Game/L1.png'), pygame.image.load('../Game/L2.png'), pygame.image.load(
    '../Game/L3.png'),
            pygame.image.load('../Game/L4.png'), pygame.image.load('../Game/L5.png'), pygame.image.load(
        '../Game/L6.png'),
            pygame.image.load('../Game/L7.png'), pygame.image.load('../Game/L8.png'), pygame.image.load(
        '../Game/L9.png')]

#bg = pygame.image.load('../Game/bg.jpg')
bg_images = []
for i in range(1, 6):
    bg_images.append(pygame.image.load(f'../Background_1/plx-{i}.png').convert_alpha())
bg_width = bg_images[0].get_width()

ground_image = pygame.image.load('../Background_1/ground.png').convert_alpha()
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

char = pygame.image.load('../Game/standing.png')

clock = pygame.time.Clock()
bulletSound = pygame.mixer.Sound('../Game/pistol.wav') # sound when shooting
hitSound = pygame.mixer.Sound('../Game/hit.mp3') # sound when hit
music = pygame.mixer.music.load('../Game/doom.mp3') # background music
pygame.mixer.music.play(-1) # -1 means play the music in a loop
score = 0

# Create a class for the player
class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) # rectangle around the player
    # Function to draw the player
    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not (self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        # rectangle around the player
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)  # rectangle around the player
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2) # draw the hitbox

    # Function to make the player jump
    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 60
        self.y = 320
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 35)
        text = font1.render('-5', 1, (250, 0, 0)) # red color
        win.blit(text, (50 - (text.get_width() / 2), 5)) # center the text
        pygame.display.update()
        # wait 1 second
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

# Create a class for the projectiles
class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class enemy(object):
    walkRight = [pygame.image.load('../Game/R1E.png'), pygame.image.load('../Game/R2E.png'), pygame.image.load('../Game/R3E.png'),
                 pygame.image.load('../Game/R4E.png'), pygame.image.load('../Game/R5E.png'), pygame.image.load('../Game/R6E.png'),
                 pygame.image.load('../Game/R7E.png'), pygame.image.load('../Game/R8E.png'), pygame.image.load('../Game/R9E.png'),
                 pygame.image.load('../Game/R10E.png'), pygame.image.load('../Game/R11E.png')]
    walkLeft = [pygame.image.load('../Game/L1E.png'), pygame.image.load('../Game/L2E.png'), pygame.image.load('../Game/L3E.png'),
                pygame.image.load('../Game/L4E.png'), pygame.image.load('../Game/L5E.png'), pygame.image.load('../Game/L6E.png'),
                pygame.image.load('../Game/L7E.png'), pygame.image.load('../Game/L8E.png'), pygame.image.load('../Game/L9E.png'),
                pygame.image.load('../Game/L10E.png'), pygame.image.load('../Game/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)  # rectangle around the player
        self.health = 10 # health of the enemy
        self.visible = True # if the enemy is visible

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10)) # health bar (red color)
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10)) # health bar (green color)
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)  # rectangle around the player
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # draw the hitbox

    def move(self):
        if self.vel > 0:
            # move right
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            # move left
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('hit')

# <-----------------FUNCTIONS------------------->
# Redraw the game window
def redrawGameWindow():
    # win.blit(bg, (0, 0)) # Draw the background
    # Draw the scenario
    for x in range(5):
        speed = 1
        for i in bg_images:
            win.blit(i, ((x * bg_width) - scroll * speed, 0))
            speed += 0.08
    # Draw the ground
    for x in range(15):
        win.blit(ground_image, ((x * ground_width) - scroll * 2.2, 430 - ground_height))

    text = font.render('Score: ' + str(score), 1, (0, 0, 0)) # Draw the score
    win.blit(text, (600, 5)) # Draw the score
    man.draw(win) # Draw the player
    goblin.draw(win) # Draw the goblin
    for bullet in bullets:  # Draw the bullets
        bullet.draw(win)
    # Update the display
    pygame.display.update()


# <-----------------MAIN LOOP------------------->
font = pygame.font.SysFont('comicsans', 27, True) # font for the text
man = player(200, 320, 64, 64)
goblin = enemy(100, 325, 64, 64, 700)
shootLoop = 0 # to limit the number of bullets
bullets = []
run = True
scroll = 0
while run:
    # Set the FPS
    clock.tick(30)

    if goblin.visible == True:
        # Check if the goblin is hit
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                # Hit the goblin
                man.hit()
                # Add to the score
                score -= 5

    # shootLoop restriction
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # Loop through the bullets
    for bullet in bullets:
        # Check if the bullet hits the goblin (bottom of a rectangle, top of a rectangle)
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                #  Play the hit sound
                hitSound.play()
                # Hit the goblin
                goblin.hit()
                # Add to the score
                score += 1
                # Remove the bullet
                bullets.pop(bullets.index(bullet))
        # Check if the bullet is still on the screen
        if bullet.x < 725 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    # Check for key presses
    keys = pygame.key.get_pressed()
    # Check for space bar
    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), facing)) # 6 is the radius of the bullet
        shootLoop = 1

    # Check for left and right keys
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_LEFT] and scroll > 0:
        scroll -= 5
    elif keys[pygame.K_RIGHT] and man.x < 725 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and scroll < 3000:
        scroll += 5
    else:
        man.standing = True
        man.walkCount = 0
    # Check for up key
    if not (man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()

pygame.quit()