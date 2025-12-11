import pygame

pygame.init()
# Creating pygame window width:
width = 900
# Creating pygame window height:
height = 700
# Creating pygame window:
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("OURSO")
# fps for the game
clock = pygame.time.Clock()

# game variables
tile_size = 20
main_menu = True
confirm = False
end_game = False
# Creating loop variable:
running = True


class Button():
    """
    This class will draw a button based off a given image that can be declared, then will assign it functions such as if
    the button is clicked and if it is, it will return that the action is true.

    :param image: assigns an image to place onto the screen.
    :param x: x-coordinate on where to place the image along the screen.
    :param y: y-coordinate on where to place the image along the screen.
    """
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        """
        Description: Will take the givens, and draw a button that corresponds onto the screen along with
        the functionality of the buttons when clicked.
        Precondition: a given x, y, and image variables must be met (inputted/declared later on).
        Postcondition: Based off the given x and y coordinates as well as the given image/sprite, it will draw the image onto the screen
        as well as assigning it the given functions.
        :param self: able to access the variables declared in the class.
        """
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        screen.blit(self.image, self.rect)

        return action

class Player():
    """
     The player class will determine everything that the player is able to do and what are the set limits on what the
     player can not do.

     :param x: x-coordinate on where to place the player image along the screen.
     :param y: y-coordinate on where to place the player image along the screen.
     """
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 2):
            img_right = pygame.image.load(f'OURSO_{num}.png')
            img_right = pygame.transform.scale(img_right, (50, 50))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_right.append(img_left)
        self.images = self.images_right[self.index]
        self.rect = self.images.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.images.get_width()
        self.height = self.images.get_height()
        self.vel_y = 0
        self.vel_x = 3
        self.jump = False

    def update(self):
        """
        Description: Updates the player/character based of multiple and specific inputs.
        Precondition: The player must be called later, as well as calling this update function, as well has an assigned image and coordinates.
        Postcondition: Updates the player's position, look, and collisions based on inputs and math.
        :param self: able to access the variables declared in the class.
        """
        # changes in x and y-axis
        dx = 0
        dy = 0

        # movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.jump == False:
            self.vel_y = -17
            self.jump = True

        if not keys[pygame.K_SPACE]:
            self.jump = False

        if keys[pygame.K_a] and self.rect.x > -10:
            dx -= self.vel_x

        if keys[pygame.K_d] and self.rect.x < 870:
            dx += self.vel_x

        # gravity (yay)
        self.vel_y += 1
        if self.vel_y > 17:
            self.vel_y = 17
        dy += self.vel_y

        # collisions
        for tile in world.tile_list:
        # x collisions
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
        # y collisions
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):

                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0

                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0

        # changing the players coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > height:
            self.rect.bottom = height
            dy = 0

        # drawing the player onto screen
        screen.blit(self.images, self.rect)


class World():
    """
     This class will take images of multiple different "tiles" and will load them based of the assigned variable and
     it's position in the list. Then it will blit (draw) the tiles based of a given image, onto the screen.

     :param data: Takes the info that is in the tile_list list and will read it to tell the program on which tiles to draw.
     """
    def __init__(self, data):
        self.tile_list = []

        #load images
        ground = pygame.image.load('GROUND.png')
        crystals = pygame.image.load('CRYSTALS.png')
        stone = pygame.image.load('STONE.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(ground, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(crystals, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    img = pygame.transform.scale(stone, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        """
         Description: Will take the givens, and draw a tile.
         Precondition: a given x, y, and image variables must be met (inputted/declared later on).
         Postcondition: Based off the given x and y coordinates as well as the given image/sprite, it will draw the image onto the screen
         as well as assigning it the given functions.
         :param self: able to access the variables declared in the class.
         """
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])



world_data =[
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #1
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #2
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #3
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #4
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #5
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #6
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #7
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1], #8
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1], #9
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1], #10
[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0], #11
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #12
[1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #13
[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1], #14
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1], #15
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0], #16
[1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0], #17
[0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #18
[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #19
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0], #20
[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], #21
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1], #22
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 3, 1, 1], #23
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1], #24
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], #25
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], #26
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], #27
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], #28
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], #29
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], #30
[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3], #31
[1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3], #32
[1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3], #33
[1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3], #34
[1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], #35
]
# objects
player = Player(0, height - 150)
world = World(world_data)


# images
forest = pygame.image.load("01_lvl1bg.png")
menu = pygame.image.load("Load.png")
start_img = pygame.image.load('START_BUTTON.png')
exit_img = pygame.image.load('EXIT_BUTTON.png')
controls_img = pygame.image.load('CONTROLS.png')
control_menu_img = pygame.image.load('CONTROLS_MENU.png')
ok_img = pygame.image.load('OK_BUTTON.png')
cave = pygame.image.load("CAVE_ENTRANCE.png")
crystal_cave = pygame.image.load("02_lvl2bg.png")
win = pygame.image.load("WIN_TEXT.png")

# buttons
start_button = Button(350, 350, start_img)
exit_button = Button(350, 450, exit_img)
ok_button = Button(350, 550, ok_img)

while running:

    if main_menu:
        # game music
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("MAIN_MENU.wav")

            pygame.mixer.music.set_volume(1.2)

            pygame.mixer.music.play(-1)

        screen.blit(menu, (0, 0))
        if exit_button.draw():
            running = False
        if start_button.draw():
            main_menu = False

    else:

        screen.blit(control_menu_img, (0, 0))
        screen.blit(controls_img, (350, 100))

        if ok_button.draw():
            if pygame.mixer_music.get_busy():
                pygame.mixer_music.stop()
            confirm = True

        if main_menu == False and confirm == True:
            # background

            screen.blit(forest, (0, 0))

            # forest game music
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load("Forest_Theme.wav")

                pygame.mixer.music.set_volume(0.2)

                pygame.mixer.music.play(-1)

            world.draw()

            screen.blit(cave, (700, 600))
            cave_exit = pygame.draw.rect(screen, (21, 23, 46), pygame.Rect(725, 640, 20, 40))

            player.update()

            crystals1 = pygame.draw.rect(screen, (144, 116, 90), pygame.Rect(120, 670, 160, 10))
            crystals2 = pygame.draw.rect(screen, (47, 81, 103), pygame.Rect(325, 157, 30, 5))

            if crystals1.colliderect(player) or crystals2.colliderect(player):
                player = Player(0, height - 150)

            if cave_exit.colliderect(player):
                end_game = True
                screen.blit(crystal_cave, (0, 0))
                screen.blit(win, (350, 250))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                main_menu = True
    # Handling events:
    for event in pygame.event.get():
        # If statement for when the exit button for window like the red X in the corner for
        # windows or the red dot for macs is pressed:
        if event.type == pygame.QUIT:
            # Terminating loop:
            running = False

    # Refreshing screen for graphics:
    pygame.display.update()
    clock.tick(60)
# quiting pygame at the end of the program
pygame.quit()