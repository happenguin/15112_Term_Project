import pygame
from miscObjects import Weapon,Potion
from miscObjects import Ability
from spriteFunctions import SpriteSheet

#weapons:
smallSnowball = Weapon(15,30, "SmallSnowball")
snowball = Weapon(20,500, "Snowball")
bigSnowball = Weapon(25,1000, "BigSnowball")
#potions:
healthPotion = Potion("Health", 25, 10, "Health Potion")
manaPotion = Potion("Mana", 25, 10, "Mana Potion")
#abilities:
fireball = Ability("Fireball", 30, 30)
iceball = Ability("Iceball", 40, 50)

allAbilities = [Ability("Double Throw",0,10),Ability("Fireball", 30, 10),
                Ability("Iceball",  40, 30),Ability("Triple Throw", 0, 30)]


# Colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)
YELLOW   = ( 255, 255,   0)


class Monster(pygame.sprite.Sprite):

    screenHeight = 600

    change_x = 0
    change_y = 0

    level = None

    #stats
    maxHealth = 100
    maxMana = 100
    currentHealth = 100
    currentMana = 100
    isStunned = False
    monsterLevel = 0
    experience = (monsterLevel+1)*20

    walking_frames_l = []
    walking_frames_r = []

    blockDimensions = None

    def __init__(self):

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        sealSprites = SpriteSheet("enemy.png")

        # Load all the right facing images into a list
        image = sealSprites.get_image(0, 0, 64, 50)
        self.walking_frames_r.append(image)
        image = sealSprites.get_image(67, 0, 65, 60)
        self.walking_frames_r.append(image)

        # Load all the right facing images, then flip them
        # to face left.
        image = sealSprites.get_image(0, 0, 64, 50)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sealSprites.get_image(67, 0, 65, 60)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        # Set the image the player starts with
        self.image = self.walking_frames_r[0]

        # Set a referance to the image rect.

        super(Monster,self).__init__()
        self.rect = self.image.get_rect()
        self.moveDirection = "Right"
        self.attackDamage = 6

    def update(self):
        # Gravity
        self.calc_grav()

        pos = self.rect.x + self.level.world_shift
        if self.moveDirection == "Right":
            frame = (pos // 20) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            pos = self.rect.x 
            frame = (pos // 20) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.blockDimensions = block.platform.dimensions
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

            if(self.rect.x <= block.rect.x):
                self.moveDirection = "Right"
            elif(self.rect.x + self.rect.width >= block.rect.x + block.rect.width):
                self.moveDirection = "Left"


    def moveMonster(self):
        if(self.moveDirection == "Right"):
            self.go_right()
        else:
            self.go_left()

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= self.screenHeight - self.rect.height and self.change_y >= 0:
            self.currentJumps = 0
            self.change_y = 0
            self.rect.y = self.screenHeight - self.rect.height



    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -4

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 4

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

class Projectile(pygame.sprite.Sprite):

    screenWidth = 800
    
    change_x = 0
    change_y = 0

    level=None

    def __init__(self):
        super(Projectile,self).__init__()


        pygame.sprite.Sprite.__init__(self)
        snowball = SpriteSheet("SmallSnowball.png")

        self.image = snowball.get_image(0,0,11,11)
        self.rect = self.image.get_rect()

    def update(self):
        # Move left/right
        self.rect.x += self.change_x

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
                self.change_x=0
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
                self.change_x=0

        if(self.rect.x>=self.screenWidth or self.rect.x<=0):
            self.change_x=0



    def go_left(self):
        self.change_x = -10

    def go_right(self):
        self.change_x = 10

    def stop(self):
        self.change_x = 0

class Player(pygame.sprite.Sprite):
    """
    This class represents the bar at the bottom that the player controls.
    """

    # -- Attributes
    # Set speed vector of player
    change_x = 0
    change_y = 0

    walking_frames_l = []
    walking_frames_r = []

    # List of sprites we can bump against
    level = None
    facing = "Right"
    totalJumps = 2
    currentJumps = 0

    screenHeight = 600

    #player health
    maxHealth = 100
    maxMana = 100
    currentHealth = 100
    currentMana = 100

    playerLevel = 0
    currentExperience = 0
    maxExperience = 100

    isDead = False

    weapon = smallSnowball

    weaponInventory = []
    potionInventory = [healthPotion,manaPotion,]
    abilityList = []

    projectiles = 10 
    gold = 200

    onShop = False

    sealsKilled = 0
    

    # -- Methods
    def __init__(self):

        """ Constructor function """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        penguinSprites = SpriteSheet("penguinSprites.png")

        # Load all the right facing images into a list
        image = penguinSprites.get_image(64, 0, 66, 63)
        self.walking_frames_r.append(image)
        image = penguinSprites.get_image(61, 64, 67, 63)
        self.walking_frames_r.append(image)
        image = penguinSprites.get_image(0, 0, 63, 63)
        self.walking_frames_r.append(image)
        image = penguinSprites.get_image(61, 64, 67, 63)
        self.walking_frames_r.append(image)

        # Load all the right facing images, then flip them
        # to face left.
        image = penguinSprites.get_image(64, 0, 66, 63)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = penguinSprites.get_image(61, 64, 67, 63)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = penguinSprites.get_image(0, 0, 63, 63)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = penguinSprites.get_image(61, 64, 67, 63)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        # Set the image the player starts with
        self.image = self.walking_frames_r[0]

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x
        pos = self.rect.x + self.level.world_shift
        if self.facing == "Right":
            frame = (pos // 20) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (pos // 20) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y
        self.onShop = False

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.currentJumps = 0
                if block.isShop:
                    self.onShop = True
                if block.isHealing:
                    self.currentHealth = self.maxHealth
                    self.currentMana = self.maxMana
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= self.screenHeight - self.rect.height and self.change_y >= 0:
            self.isDead = True

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= self.screenHeight or self.currentJumps < self.totalJumps:
            self.currentJumps += 1
            self.change_y = -9

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -5
        self.facing = "Left"

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 5
        self.facing = "Right"

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

    def inEnemy(self,enemy):
        if(self.rect.x >= enemy.rect.x and self.rect.x <= enemy.rect.x+enemy.rect.width and 
            self.rect.y >= enemy.rect.y and self.rect.y <= enemy.rect.y + enemy.rect.height or
            self.rect.x+self.rect.width>enemy.rect.x and self.rect.x+self.rect.width <= enemy.rect.x+enemy.rect.width and 
            self.rect.y >= enemy.rect.y and self.rect.y <= enemy.rect.y + enemy.rect.height or
            self.rect.x >= enemy.rect.x and self.rect.x <= enemy.rect.x+enemy.rect.width and 
            self.rect.y+self.rect.height >= enemy.rect.y and self.rect.y+self.rect.height <= enemy.rect.y + enemy.rect.height or
            self.rect.x+self.rect.width >= enemy.rect.x and self.rect.x+self.rect.width <= enemy.rect.x+enemy.rect.width and 
            self.rect.y+self.rect.height >= enemy.rect.y and self.rect.y + self.rect.height <= enemy.rect.y + enemy.rect.height):
            return True

    def levelUp(self):
        if self.currentExperience >= self.maxExperience:
            self.currentExperience -= self.maxExperience
            self.maxExperience += 50
            self.playerLevel += 1
            self.maxHealth += 10
            self.currentHealth = self.maxHealth
            self.maxMana +=5
            self.currentMana = self.maxMana
            if (self.playerLevel == 2 or self.playerLevel % 5 == 0) and len(allAbilities) > 0:
                self.abilityList.append(allAbilities.pop(0))

