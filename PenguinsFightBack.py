"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/

Taken and adapted from:
http://programarcadegames.com/python_examples/f.php?file=platform_moving.py
"""

import random
import pygame
from RPGBattleScreen import BattleScreenMenu
from Tkinter import *
from miscObjects import Weapon, Potion, Ability, PlatformType
from menus import ShopMenu, AbilityMenu, ItemMenu
from spriteFunctions import SpriteSheet
from characterClasses import Monster, Player, Projectile
from startScreen import MainMenu

# Global constants

#weapons:
smallSnowball = Weapon(10,30, "smallSnowball")
snowball = Weapon(15,500, "snowball")
bigSnowball = Weapon(20,1000, "bigSnowball")
#potions:
healthPotion = Potion("Health", 10, 10, "Health Potion")
manaPotion = Potion("Mana", 10, 10, "Mana Potion")
#abilities:
fireball = Ability("Fireball", 30, 30)
iceball = Ability("Iceball", 40, 50)

allAbilities = [Ability("Fireball", 30, 15),Ability("Iceball", 40, 25),
                Ability("Double Throw", 10, 10)]


# Colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)
YELLOW   = ( 255, 255,   0)

class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height, platform):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        pygame.sprite.Sprite.__init__(self)
        platformSprite = SpriteSheet("platform.png")

        super(Platform,self).__init__()

        self.platform = platform
        self.isShop = platform.isShop
        self.isHealing = platform.isHealing
        if platform.isShop:
            self.image = platformSprite.get_image(0, 70, 210, 70)
        elif platform.isHealing:
            self.image = platformSprite.get_image(0, 140, 210, 70)
        else:
            self.image = platformSprite.get_image(0, 0, 210, 70)

        self.rect = self.image.get_rect()


class MovingPlatform(Platform):
    """ This is a fancier platform that can actually move. """
    change_x = 0
    change_y = 0

    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0

    player = None

    level = None

    def update(self):
        """ Move the platform.
            If the player is in the way, it will shove the player
            out of the way. This does NOT handle what happens if a
            platform shoves a player into another object. Make sure
            moving platforms have clearance to push the player around
            or add code to handle what happens if they don't. """

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # If we are moving right, set our right side
            # to the left side of the item we hit
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.player.rect.left = self.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # Reset our position based on the top/bottom of the object.
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom

        # Check the boundaries and see if we need to reverse
        # direction.
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1

        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1

class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    # Lists of sprites used in all levels. Add or remove
    # lists as needed for your game.
    platform_list = None
    enemy_list = None

    # Background image
    background = None

    # How far this world has been scrolled left/right
    world_shift = 0
    level_limit = -1000
    respawnQueue = []

    def __init__(self, player, monster, projectile, screen):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.screen = screen
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.projectile_list = pygame.sprite.Group()
        self.monster = monster
        for enemy in monster:
            self.enemy_list.add(enemy)
        for eachProjectile in projectile:
            self.projectile_list.add(eachProjectile)
        self.player = player
        self.previousY = 280

        self.background = pygame.image.load("background.png").convert()
        self.background.set_colorkey((0,0,0))
        # self.monster = monster

    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        screen.fill(BLUE)
        screen.blit(self.background,(0,0))

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll everything:
        """

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

        for eachProjectile in self.projectile_list:
            eachProjectile.rect.x += shift_x

    def removeEnemy(self,enemy):
        self.enemy_list.remove(enemy)

    def checkHitEnemy(self,projectile):
        for enemy in self.monster:
            if(projectile.rect.x>enemy.rect.x and 
                projectile.rect.x<enemy.rect .x+enemy.rect.width and
                projectile.rect.y>enemy.rect.y and
                projectile.rect.y<enemy.rect.y+enemy.rect.height):
                return True

    def generateNextBlock(self, start, blockNumber):
        shopBlock = False
        healBlock = False
        if blockNumber % 2 == 0:
            shopBlock = True
        if blockNumber % 2 == 0:
            healBlock = True

        numCoordinates = 4
        previousY = self.previousY
        for i in xrange(numCoordinates):
            x = random.randint(start+250*i,start+250*i+40)
            y = random.randint(max(200,self.previousY-200),min(self.previousY+200,530))
            self.previousY = y
            newPlatform = PlatformType(210,70,x,y)
            if shopBlock:
                newPlatform.isShop = True
                shopBlock = False
            if i == 3 and healBlock:
                newPlatform.isHealing = True
                healBlock = False

            self.level.append(newPlatform)
        for platform in self.level:
            block = Platform(platform.dimensions[0], platform.dimensions[1], platform)
            block.rect.x = platform.dimensions[2] + self.world_shift
            block.rect.y = platform.dimensions[3]
            block.player = self.player
            self.platform_list.add(block)

    def generateMonsters(self, start, blockNumber, monster):
        enemy1 = Monster()
        enemy2 = Monster()

        enemy1.level = self
        enemy1.rect.x = self.level[len(self.level)-3].dimensions[2] + 100 + self.world_shift
        enemy1.rect.y = self.level[len(self.level)-3].dimensions[3]-enemy1.rect.height

        enemy1.maxHealth += 10*blockNumber
        enemy1.currentHealth = enemy1.maxHealth 
        enemy1.attackDamage += blockNumber
        enemy1.monsterLevel = blockNumber
        enemy1.experience = (blockNumber+1)*20

        self.enemy_list.add(enemy1)
        monster.append(enemy1)

        enemy2.level = self
        enemy2.rect.x = self.level[len(self.level)-2].dimensions[2] + 100 + self.world_shift
        enemy2.rect.y = self.level[len(self.level)-2].dimensions[3]-enemy1.rect.height

        enemy2.maxHealth += 10*blockNumber
        enemy2.currentHealth = enemy1.maxHealth 
        enemy2.attackDamage += blockNumber
        enemy2.moveDirection = "Left"
        enemy2.monsterLevel = blockNumber
        enemy2.experience = (blockNumber+1)*20

        monster.append(enemy2)
        self.enemy_list.add(enemy2)

    def respawnMonsters(self, monster):
        if len(self.respawnQueue) > 0:
            blockDimensions = self.respawnQueue[0][0]
            monsterLevel = self.respawnQueue[0][1]
            enemy = Monster()
            enemy.rect.x = blockDimensions[2] + 100 + self.world_shift
            enemy.rect.y = blockDimensions[3] - enemy.rect.height
            enemy.attackDamage += monsterLevel
            enemy.monsterLevel = monsterLevel
            enemy.experience = (monsterLevel + 1) * 10

            enemy.maxHealth += 10*monsterLevel
            enemy.currentHealth = enemy.maxHealth 
            enemy.level = self
            monster.append(enemy)
            self.enemy_list.add(enemy)
            self.respawnQueue = self.respawnQueue[1:]

# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player, monster, projectile, screen):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player, monster, projectile, screen)

        self.level_limit = -1500

        # Array with width, height, x, and y of platform

        platform1 = PlatformType(210, 70, 200, 400)
        platform2 = PlatformType(210, 70, 500, 500)
        platform3 = PlatformType(210, 70, 800, 400)
        platform4 = PlatformType(210, 70, 1000, 500)
        platform5 = PlatformType(210, 70, 1120, 280)

        level = [platform1,
                 platform2,
                 platform3,
                 platform4,
                 platform5,
                 ]
        self.level = level


        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform.dimensions[0], platform.dimensions[1], platform)
            block.rect.x = platform.dimensions[2]
            block.rect.y = platform.dimensions[3]
            block.player = self.player
            self.platform_list.add(block)

def drawHealthBar(player, screen):
    black       = (0  ,  0,  0)
    red         = (255,  0,  0)
    blue        = (  0,  0,255)
    saddleBrown = (244,164, 96)
    white       = (255,255,255)
    width = 800
    smallFont = pygame.font.SysFont("Arial", 12)
    #player health bar
    pygame.draw.rect(screen,saddleBrown,(10,10,width*.4-10,45))
    label = smallFont.render("Player",1,black)
    screen.blit(label, (11,10))
                 #perhaps replace with playerName to let player input own name
    health = "Health:%d/%d" % (player.currentHealth,player.maxHealth)
    label = smallFont.render(health,1,black)
    screen.blit(label,((width*.4)/2-40,10))

    mana = "Mana:%d/%d" % (player.currentMana,player.maxMana)
    label = smallFont.render(mana,1,black)
    screen.blit(label,(width*.4-85,10))

    pygame.draw.rect(screen,white,(15,25,width*.4-20,10))
    pygame.draw.rect(screen,red,(15,25,15+(width*.4-20)*player.currentHealth/player.maxHealth-15,10))
    pygame.draw.rect(screen,white,(15,40,width*.4-20,10))
    pygame.draw.rect(screen,blue,(15,40,15+(width*.4-20)*player.currentMana/player.maxMana-15,10))

def drawExperienceBar(player, screen):
    white = (255,255,255)
    gold = (255,215,0)
    width = 800
    height = 600
    pygame.draw.rect(screen,white,(0,height-10,width,10))
    pygame.draw.rect(screen,gold,(0,height-10,width*player.currentExperience/player.maxExperience,10))

def drawProjectilesLeft(player, screen):
    black = (0,0,0)
    font = pygame.font.SysFont("Arial", 17)

    text = "Projectiles Left: " + str(player.projectiles)
    label = font.render(text, 1, black)
    screen.blit(label, (10,55))

    text = "Level: " + str(player.playerLevel)
    label = font.render(text,1,black)
    screen.blit(label, (10,70))

    text = "Seals Defeated:" + str(player.sealsKilled)
    label = font.render(text,1,black)
    screen.blit(label, (10,85))

def main():
    """ Main Program """

    pygame.init()
    pygame.font.init()

    largeFont = pygame.font.SysFont("Arial", 50)
    # smallFont = pygame.font.SysFont("Arial", 25)

    inBattle = False

    inventoryOpen = False
    shopOpen = False
    inGame = False

    screenWidth = 800
    screenHeight = 600

    # Set the height and width of the screen
    size = [screenWidth, screenHeight]
    screen = pygame.display.set_mode(size)

    projectile=[Projectile()]

    pygame.display.set_caption("Penguins Fight Back") #put game title here

    # Create the player
    player = Player()

    monster = [Monster(),Monster()]

    # Create all the levels
    level_list = []
    level_list.append(Level_01(player, monster, projectile, screen))

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
    for eachProjectile in projectile:
        eachProjectile.level = current_level

    #creating enemies

    monster[0].level = current_level
    monster[0].rect.x = (600)
    monster[0].rect.y = 500-monster[0].rect.height

    monster[1].level = current_level
    monster[1].rect.x = 900
    monster[1].rect.y = 400-monster[1].rect.height
    monster[1].moveDirection = "Left"


    player.rect.x = 340
    player.rect.y = 400 - player.rect.height
    active_sprite_list.add(player)

    mainMenu = MainMenu(screen)

    #Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()


    blockSize = 1000
    numBlock = 1


    # -------- Main Program Loop -----------
    while not done:
        if not inGame:
            screen.fill((255,255,255))
            inGame = mainMenu.draw()
        elif player.isDead:
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done = True # Flag that we are done so we exit this loop

            current_level.draw(screen)
            active_sprite_list.draw(screen)

            label = largeFont.render("Game Over", 1, (0,0,0))
            screen.blit(label, (265, 230))

            # label = smallFont.render("Press r to reset level.", 1, (0,0,0))
            # screen.blit(label, (280, 280))

            pygame.display.flip()
        elif not inBattle and inGame:
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done = True # Flag that we are done so we exit this loop

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.go_left()
                    elif event.key == pygame.K_RIGHT:
                        player.go_right()
                    elif event.key == pygame.K_UP:
                        player.jump()
                    elif event.key == 32:
                        for eachProjectile in projectile:
                            if eachProjectile not in active_sprite_list and player.projectiles>0:
                                eachProjectile.rect.x = player.rect.x+player.rect.width/2
                                eachProjectile.rect.y = player.rect.y + player.rect.height/2
                                if(player.facing == "Right"):
                                    eachProjectile.go_right()
                                elif(player.facing == "Left"):
                                    eachProjectile.go_left()
                                active_sprite_list.add(eachProjectile)
                                player.projectiles -= 1
                                break
                    elif event.key == 105: #pressed "i", open inventory
                        inventory = ItemMenu(player.weaponInventory,player.potionInventory,screen, player)
                        inventoryOpen = True
                        player.stop()
                    elif event.key == 115 and player.onShop == True:
                        shop = ShopMenu(player,screen)
                        shopOpen = True
                        player.stop()
                    elif event.key == 107:
                        AbilityMenu(player,screen).draw()
                        player.stop()
                    elif event.key == 108:
                        player.currentExperience = player.maxExperience

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and player.change_x < 0:
                        player.stop()
                    if event.key == pygame.K_RIGHT and player.change_x > 0:
                        player.stop()

            for eachProjectile in projectile:
                if(eachProjectile.change_x==0):
                    active_sprite_list.remove(eachProjectile)
                    eachProjectile.rect.x = eachProjectile.rect.y = 0
                for enemy in monster:
                    # if current_level.checkHitEnemy(eachProjectile):
                    if(eachProjectile.rect.x>enemy.rect.x and 
                        eachProjectile.rect.x<enemy.rect.x+enemy.rect.width and
                        eachProjectile.rect.y>enemy.rect.y and
                        eachProjectile.rect.y<enemy.rect.y+enemy.rect.height):
                        eachProjectile.rect.x = eachProjectile.rect.y = 0
                        active_sprite_list.remove(eachProjectile)
                        current_level.respawnMonsters(monster)
                        current_level.respawnQueue.append((enemy.blockDimensions,enemy.monsterLevel))
                        monster.remove(enemy)
                        current_level.removeEnemy(enemy)
                        enemy.isStunned = True
                        battleScreen = BattleScreenMenu(player, enemy, screen)
                        inBattle = True
            for enemy in monster:
                if player.inEnemy(enemy) and type(enemy.blockDimensions) == list:
                    current_level.respawnMonsters(monster)
                    current_level.respawnQueue.append((enemy.blockDimensions,enemy.monsterLevel))
                    monster.remove(enemy)
                    current_level.removeEnemy(enemy)
                    battleScreen = BattleScreenMenu(player,enemy, screen)
                    inBattle = True

            if inventoryOpen:
                inventory.draw()
                inventoryOpen = False

            if shopOpen:
                shop.draw()
                shopOpen = False

            #move the monster aroundz
            for enemy in monster:
                enemy.moveMonster()

            player.levelUp()

            # Update the player.
            active_sprite_list.update()

            # Update items in the level
            current_level.update()

            # If the player gets near the right side, shift the world left (-x)
            if player.rect.right >= 500:
                diff = player.rect.right - 500
                player.rect.right = 500
                current_level.shift_world(-diff)
     
            # If the player gets near the left side, shift the world right (+x)
            if player.rect.left <= 120:
                diff = 120 - player.rect.left
                player.rect.left = 120
                current_level.shift_world(diff)
                
            # If the player gets to the end of the level, go to the next level
            current_position = player.rect.x - current_level.world_shift
            if current_position > blockSize*numBlock:
                current_level.generateNextBlock(350+blockSize*numBlock, numBlock+1)
                current_level.generateMonsters(350+blockSize*numBlock, numBlock+1, monster)
                numBlock+=1



            # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
            current_level.draw(screen)
            active_sprite_list.draw(screen)
            drawHealthBar(player,screen)
            drawExperienceBar(player,screen)
            drawProjectilesLeft(player,screen)

            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

            # Limit to 60 frames per second
            clock.tick(60)

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

        else:
            inBattle = battleScreen.run()


    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

if __name__ == "__main__":
    main()




"""
Sprites From:
http://www.spriters-resource.com/game_boy/animbreed4/sheet/2127/]
http://opengameart.org/content/platformer-art-deluxe
http://opengameart.org/content/artic-landscape-background
http://thepikuseru.deviantart.com/art/Penguin-Sprites-39302798
http://www.mariowiki.com/images/0/0e/Giant_Ice_Block.PNG
http://cdn.staticneo.com/w/minecraft/0/04/Snowball.png
Artwork modified by: Deniz Sokullu
Buttons made by: Steven Fu

Pre-beta testers:
Nikhil Jog
George Situ
"""
