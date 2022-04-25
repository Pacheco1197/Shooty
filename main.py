"""
This program creates a game where the player has to shoot and dodge bullets. The user uses the wasd keys to move and
the space-bar to shoot
"""

import pygame as pyg

from pygame.locals import *

pyg.font.init()

# sets screen to full screen
screen = pyg.display.set_mode((0, 0), FULLSCREEN)
font = pyg.font.SysFont('Times New Roman', 32)

clock = pyg.time.Clock()
FPS = 120
Dy = 0

# Lists that will hold the different bullets -> player's and enemy's
bullets = []
E_bullets = []


# creates a new background
def background():
    bg = pyg.image.load('img/background/background1.jpg')
    screen.blit(bg, (0, 0))


# creates the player class which is the character that the user plays.
class Player(pyg.sprite.Sprite):
    # Constructor Method for the Player Class
    def __init__(self, x, y, scale):
        pyg.sprite.Sprite.__init__(self)
        img = pyg.image.load('img/player/idle/0.png')
        self.image = pyg.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()  # Create coordinates for the character
        self.rect.center = (x, y)
        self.hitbox = (self.rect.x + 28, self.rect.y, self.rect.width, self.rect.height)  # Creates a hitbox to know when an object has collided with it
        self.hp = 50  # Player Health points

    # Moves the Player object and changes the sprite depending on the direction it is facing
    def move(self, moving_left, moving_right, falling_up, dy, direction):
        # Moves Player object Left as long as it's still in screen
        if moving_left and self.rect.x > 0:
            self.rect.x -= 4
            if direction == 0:
                self.image = pyg.transform.flip(self.image, True, False)
                direction = 1

        # Moves player object to the right as long as it's still in screen
        if moving_right and self.rect.x < screen.get_width() - 28:
            self.rect.x += 4
            if direction == 1:
                self.image = pyg.transform.flip(self.image, True, False)
                direction = 0

        # Falling
        if not falling_up and self.rect.y < screen.get_height() - 160:
            self.rect.y += 8

        # Jump
        elif falling_up:
            if dy < 160:
                self.rect.y -= 8
                dy += 8
            else:
                falling_up = False
        return dy, falling_up, direction

    # Method which draws the Player Object to the Screen
    def draw(self):
        background()
        screen.blit(self.image, self.rect)
        self.hitbox = (self.rect.x, self.rect.y, self.rect.width, self.rect.height)


# Creates the Enemy class
class Enemy(pyg.sprite.Sprite):
    # Constructor method for the Enemy Class
    def __init__(self, x, y, scale):
        pyg.sprite.Sprite.__init__(self)
        self.image = pyg.image.load('img/enemy/idle/0.png')
        self.image = pyg.transform.flip(self.image, True, False)
        self.image = pyg.transform.scale(self.image, ((self.image.get_width() * scale), (self.image.get_width() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hitbox = (self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        self.hp = 50  # Enemy Health Points

    # Method to turn the Enemy Object to track the Player
    def turn(self, direction):
        if self.rect.x < player.rect.x:
            if direction == 1:
                self.image = pyg.transform.flip(self.image, True, False)
                direction = 0
        elif self.rect.x > player.rect.x:
            if direction == 0:
                self.image = pyg.transform.flip(self.image, True, False)
                direction = 1

        return direction

    # Method to Draw Enemy Object to screen
    def draw(self):
        screen.blit(self.image, self.rect)
        self.hitbox = (self.rect.x, self.rect.y, self.rect.width, self.rect.height)


# Creates the Bullet Class
class Bullet(pyg.sprite.Sprite):
    # Bullet Class Constructor Method
    def __init__(self, x, y, scale, direction, type_num):
        pyg.sprite.Sprite.__init__(self)
        self.image = pyg.image.load("img/icons/bullet.png")
        self.image = pyg.transform.scale(self.image, ((self.image.get_width() * scale), (self.image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.type = type_num  # Variable to check if it's an Enemy or Player Bullet
        if direction == 0:
            self.rect.center = (x + 28, y)
        else:
            self.rect.center = (x - 28, y)
        self.direction = direction

    # moves Bullet object depending on the direction of either the player or enemy object
    def move(self):
        if self.direction == 0:
            self.rect.x += 6
        else:
            self.rect.x -= 6

    # Checks if the bullet object is out of the screen
    def out_bounds(self):
        if self.rect.x < 0 or self.rect.x > screen.get_width():
            return True
        return False

    # Checks if the bullet Object has hit either the player object if it's an enemy bullet or the enemy object if player bullet
    def collision(self):
        if (player.hitbox[0] + player.hitbox[2]) > self.rect.x > player.hitbox[0] and (
                player.hitbox[1] + player.hitbox[3]) > self.rect.y > player.hitbox[1] and self.type == 1:
            return True
        if self.type == 0:
            if (enemy.hitbox[0] + enemy.hitbox[2]) > self.rect.x > enemy.hitbox[0] and (
                    enemy.hitbox[1] + enemy.hitbox[3]) > self.rect.y > enemy.hitbox[1]:
                return True
        return False

    # Draws the bullet object to the screen
    def draw(self):
        screen.blit(self.image, self.rect)


# Adds a bullet to its respective list depending on what object shot it
def shoot(character, shot, b_direction, type_num):
    bullet = Bullet(character.rect.centerx, character.rect.centery, 2, b_direction, type_num)
    shot.append(bullet)


# Iterates through a list of elements to be removed and removes each element from a list then removes that element from the first list
def erased(alist, del_type):
    if not len(alist) == 0:
        del_type.remove(alist[0])
        alist.pop(0)


# checks if either the player or enemy objects have lost all their health points and returns who win
def check_hp():
    if enemy.hp == 0:
        return 2, False
    if player.hp == 0:
        return 1, False
    return 0, True


# Displays a message with a variable if wanted at a certain location or at a default location
def printf(message, variable = None, location_x = None, location_y = None, color = (0, 0, 0)):
    text = font.render(message + str(variable), True, color)
    if location_x is None and location_y is None:
        textRect = text.get_rect()
    elif location_x is None:
        textRect = (text.get_rect().x, location_y)
    elif location_y is None:
        textRect = (location_x, text.get_rect().x)
    else:
        textRect = (location_x, location_y)
    screen.blit(text, textRect)


# Keeps track of the bullets
def bullet_check(b_type, c_type):
    for amo in b_type:
        amo.move()
        amo.draw()
        if amo.collision() and removed.count(amo) == 0:
            removed.append(amo)
            erased(removed, b_type)
            c_type.hp -= 2
        if amo.out_bounds() and removed.count(amo) == 0:
            removed.append(amo)
            erased(removed, b_type)


movingLeft = False
movingRight = False
fallingUp = False
paused = True
won = 0
Direction = 0
E_Direction = 1
ticks, fired = 0, 0
removed = []
e_removed = []
player = Player(30, screen.get_height() - 160, 2)
enemy = Enemy((screen.get_width() - 300), (screen.get_height() - 120), 2.5)

background()

# Keeps game looping until someone wins or player wants to exit out
running = True
while running:

    if paused:
        for event in pyg.event.get():
            if event.type == QUIT:
                running = False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    paused = False

        sentence = "Press 'wasd' to move the character, and 'space-bar' to shoot. press 'ESC' to pause/unpause"
        printf(sentence, "", screen.get_width()/2 - len(sentence)*6.4, screen.get_height()/2)
        pyg.display.update()
    else:
        # Set Frame Rate for the game
        clock.tick(FPS)
        ticks += 1

        Dy, fallingUp, Direction = player.move(movingLeft, movingRight, fallingUp, Dy, Direction)
        player.draw()
        won, running = check_hp()

        E_Direction = enemy.turn(E_Direction)
        enemy.draw()

        # Makes Enemy object shoot bullets with a delay  depending on its health
        if ticks > 3 > fired:
            shoot(enemy, E_bullets, E_Direction, 1)
            ticks = 0
            fired += 1
        elif enemy.hp < 20 and ticks > 25:
            fired = 0
        elif enemy.hp < 30 and ticks > 40:
            fired = 0
        elif enemy.hp < 40 and ticks > 45:
            fired = 0
        elif enemy.hp > ticks > 50:
            fired = 0
        elif enemy.hp <= 100 and ticks > 60:
            fired = 0

        bullet_check(bullets, enemy)
        bullet_check(E_bullets, player)

        printf("Player HP: ", player.hp)
        printf("Enemy HP: ", enemy.hp, (screen.get_width() - 200))

        # Checks if a key was pressed
        for event in pyg.event.get():
            if event.type == QUIT:
                running = False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    paused = True
                if event.key == K_a:
                    movingLeft = True
                if event.key == K_d:
                    movingRight = True
                if event.key == K_w and Dy == 0:
                    fallingUp = True
                if event.key == K_SPACE:
                    shoot(player, bullets, Direction, 0)

            if event.type == KEYUP:
                if event.key == K_a:
                    movingLeft = False
                if event.key == K_d:
                    movingRight = False
                if event.key == K_w:
                    fallingUp = False

        # Updates the screen
        pyg.display.update()

        # Sets a boundary so the player object will stop falling
        if player.rect.y > screen.get_height() - 178:
            Dy = 0

screen.fill(0)

if not won == 0:
    if won == 2:
        printf("Congrats you won!!!", "", screen.get_width() / 2.4, screen.get_height() / 2, (255, 255, 255))
    elif won == 1:
        printf("Sorry you lost :(", "", screen.get_width() / 2.4, screen.get_height() / 2, (255, 255, 255))

    pyg.display.update()
    pyg.time.wait(5000)
    pyg.quit()
