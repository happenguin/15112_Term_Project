import pygame
from Tkinter import *
from spriteFunctions import SpriteSheet
import time

class EnemyProjectile(pygame.sprite.Sprite):
    def __init__(self, enemy):
        pygame.sprite.Sprite.__init__(self)
        battleProjectile = SpriteSheet("icicleSprite.png")
        self.image = battleProjectile.get_image(0,0,76,40)

        super(EnemyProjectile,self).__init__()
        self.rect = self.image.get_rect()
        self.rect.x = enemy.rect.x
        self.rect.y = enemy.rect.y+enemy.rect.height/2-self.rect.height/2
        self.change_x = -15

class BattleProjectile(pygame.sprite.Sprite):
    def __init__(self, attack, player):
        pygame.sprite.Sprite.__init__(self)
        if attack == "Attack":
            path = player.weapon.name + ".png"
            battleProjectile = SpriteSheet(path)
            if player.weapon.name == "SmallSnowball":
                self.image = battleProjectile.get_image(0,0,11,11)
            elif player.weapon.name == "Snowball":
                self.image = battleProjectile.get_image(0,0,15,15)
            elif player.weapon.name == "BigSnowball":
                self.image = battleProjectile.get_image(0,0,20,20)

        elif attack == "Fireball":
            battleProjectile = SpriteSheet("FireballSprite.png")
            self.image = battleProjectile.get_image(0,0,52,32)

        elif attack == "Iceball":
            battleProjectile = SpriteSheet("IceballSprite.png")
            self.image = battleProjectile.get_image(0,0,52,32)

        elif attack == "Double Throw":
            if player.weapon.name == "SmallSnowball":
                battleProjectile = SpriteSheet("DoubleSmallSnowball.png")
                self.image = battleProjectile.get_image(0,0,25,11)
            elif player.weapon.name == "Snowball":
                battleProjectile = SpriteSheet("DoubleSnowball.png")
                self.image = battleProjectile.get_image(0,0,37,15)
            elif player.weapon.name == "BigSnowball":
                battleProjectile = SpriteSheet("DoubleBigSnowball.png")
                self.image = battleProjectile.get_image(0,0,50,20)
        elif attack == "Triple Throw":
            if player.weapon.name == "SmallSnowball":
                battleProjectile = SpriteSheet("SmallTripleThrow.png")
                self.image = battleProjectile.get_image(0,0,23,21)
            elif player.weapon.name == "Snowball":
                battleProjectile = SpriteSheet("TripleThrow.png")
                self.image = battleProjectile.get_image(0,0,31,29)
            if player.weapon.name == "BigSnowball":
                battleProjectile = SpriteSheet("BigTripleThrow.png")
                self.image = battleProjectile.get_image(0,0,42,39)

        super(BattleProjectile,self).__init__()
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x+player.rect.width
        self.rect.y = player.rect.y+player.rect.height/2-self.rect.height/2
        self.change_x = 15


class BattlePlayer(pygame.sprite.Sprite):
    def __init__(self, player):

        pygame.sprite.Sprite.__init__(self)
        battlePenguinSprites = SpriteSheet("battlePenguin.png")

        self.image = battlePenguinSprites.get_image(0, 0, 124, 135)

        super(BattlePlayer,self).__init__()
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 120
        self.weapon = player.weapon

class BattleEnemy(pygame.sprite.Sprite):
    def __init__(self, enemy):

        pygame.sprite.Sprite.__init__(self)
        battleSealSprite = SpriteSheet("battleSeal.png")

        image = battleSealSprite.get_image(0, 0, 232, 123)
        self.image = pygame.transform.flip(image, True, False)

        super(BattleEnemy,self).__init__()

        self.rect = self.image.get_rect()
        self.rect.x = 800-100-self.rect.width
        self.rect.y = 130

class BattleScreenMenu(object):

    def __init__(self, player, enemy, screen):
        pygame.font.init()
        self.player = player
        self.player.stop()
        self.enemy = enemy
        (self.width,self.height) = (800, 600)
        self.inAbilityMenu = False
        self.inPotionMenu = False
        self.menu = ["Attack", "Abilties", "Potions"]
        self.menuIndex = 0

        self.abilityMenu = self.player.abilityList
        self.abilityMenuIndex = 0
        self.makeAbilityList()
        self.abilityMenuDescriptions = dict()
        for ability in self.abilityMenu:
            self.abilityMenuDescriptions[ability.name] = ability.description
        self.abilityMenuDescriptions["Back"] = ""

        self.potions = self.player.potionInventory
        self.makePotionList()

        self.screen = screen
        self.largeFont = pygame.font.SysFont("Arial", 20)
        self.smallFont = pygame.font.SysFont("Arial", 12)
        self.battlePlayer = BattlePlayer(player)
        self.battleEnemy = BattleEnemy(enemy)
        self.isPlayerTurn = True
        self.active_sprite_list = pygame.sprite.Group()

        self.background = pygame.image.load("battleground.png").convert()
        self.background.set_colorkey((0,0,0))

    def makeAbilityList(self):
        self.abilityNames = []
        for ability in self.abilityMenu:
            self.abilityNames.append(ability.name)
        self.abilityNames.append("Back")

    def makePotionList(self):
        self.potionNames = []
        for potion in self.potions:
            self.potionNames.append(potion.name)
        self.potionNames.append("Back")

    def checkUserInput(self,event):
        if event.key == pygame.K_UP:
            if self.inAbilityMenu and self.abilityMenuIndex > 0:
                self.abilityMenuIndex -= 1
            elif self.inPotionMenu and self.potionMenuIndex > 0:
                self.potionMenuIndex -= 1
            elif not self.inAbilityMenu and not self.inPotionMenu and self.menuIndex > 0:
                self.menuIndex -=1
        if event.key == pygame.K_DOWN:
            if self.inAbilityMenu and self.abilityMenuIndex < len(self.abilityNames)-1:
                self.abilityMenuIndex += 1
            elif self.inPotionMenu and self.potionMenuIndex < len(self.potionNames)-1:
                self.potionMenuIndex += 1
            elif not self.inAbilityMenu and not self.inPotionMenu and self.menuIndex < len(self.menu)-1:
                self.menuIndex += 1
        if event.key == 32:
            if self.inAbilityMenu:
                self.executeCommand()
            elif self.inPotionMenu:
                if self.potionNames[self.potionMenuIndex] == "Back": 
                    self.inPotionMenu = False
                else:
                    self.usePotion()
            elif self.menu[self.menuIndex] == "Abilties":
                self.inAbilityMenu = True
                self.abilityMenuIndex = 0
            elif self.menu[self.menuIndex] == "Potions":
                self.inPotionMenu = True
                self.potionMenuIndex = 0
            elif self.menu[self.menuIndex] == "Attack":
                attack = BattleProjectile("Attack", self.battlePlayer)
                self.active_sprite_list.add(attack)
                self.drawPlayerAttack(attack)
                self.enemy.currentHealth -= self.player.weapon.attackDamage
                self.isPlayerTurn = False

    def drawPlayerAttack(self,attack):
        while attack.rect.x + attack.rect.width < self.battleEnemy.rect.x:
            self.screen.fill([255,255,255])
            attack.rect.x += attack.change_x
            self.active_sprite_list.draw(self.screen)

            self.drawBox()
            self.drawWords()
            self.drawSelectionArrow()
            self.drawPlayerHealthBar()
            self.drawEnemyHealthBar()
            self.drawPlayerAndEnemy()

            pygame.display.flip()
        self.active_sprite_list.remove(attack)

    def executeCommand(self):
        if self.abilityNames[self.abilityMenuIndex] == "Back":
            self.inAbilityMenu = False
        elif self.player.currentMana >= self.abilityMenu[self.abilityMenuIndex].manaCost:
                attack = BattleProjectile(self.abilityMenu[self.abilityMenuIndex].name, self.battlePlayer)
                self.active_sprite_list.add(attack)
                self.drawPlayerAttack(attack)
                self.abilityMenu[self.abilityMenuIndex].useAbility(self.enemy, self.player)
                self.isPlayerTurn = False

    def usePotion(self):
        potion = self.potions[self.potionMenuIndex]
        if (potion.potionType == "Health" and 
            self.player.currentHealth < self.player.maxHealth or 
            potion.potionType == "Mana" and 
            self.player.currentMana < self.player.maxHealth):
            potion.usePotion(self.player)
            self.potions.remove(potion)
            self.makePotionList()
        self.player.currentMana = self.player.currentMana

    def drawSelectionArrow(self):
        if self.inAbilityMenu:
            index = self.abilityMenuIndex
        elif self.inPotionMenu:
            index = self.potionMenuIndex
        else:
            index = self.menuIndex
        screen = self.screen
        cy = self.height/2
        margin = 30
        arrowBound = 7
        leftX = margin + 2*arrowBound
        rightX = 2*margin - arrowBound
        topY = (index+2)*margin + arrowBound
        botY = topY + 20 - 1.5*arrowBound
        midY = (topY+botY)/2
        pygame.draw.polygon(screen, (0,0,0), [[leftX,cy+topY],[rightX,cy+midY],[leftX,cy+botY]])

    def drawBox(self):
        margin = 30
        screen = self.screen 
        cy = self.height/2
        cx = self.width/2
        screen.blit(self.background,(0,0))
        pygame.draw.rect(screen,(139,69,19),(0,cy,self.width,self.height/2))
        pygame.draw.rect(screen,(244,164,96),(margin,cy+margin,self.width-2*margin,self.height/2-2*margin))
        pygame.draw.line(screen,(0,0,0),[cx,cy+margin],[cx,self.height-margin])

    def drawWords(self):
        screen = self.screen
        margin = 30
        cy = startY = self.height/2
        cx = self.width/2
        if self.inAbilityMenu:
            menu = self.abilityNames
            desc = self.abilityMenuDescriptions[self.abilityNames[self.abilityMenuIndex]]
            label = self.largeFont.render(desc,1,(0,0,0))
            screen.blit(label, (cx+margin,cy+2*margin))

        elif self.inPotionMenu:
            menu = self.potionNames
        else:
            menu = self.menu
        for menuItem in menu:
            label = self.largeFont.render(menuItem, 1, (0,0,0))
            screen.blit(label, (2*margin, startY+2*margin))
            startY += margin
            
    def drawPlayerHealthBar(self):
        black       = (0  ,  0,  0)
        red         = (255,  0,  0)
        blue        = (  0,  0,255)
        saddleBrown = (244,164, 96)
        white       = (255,255,255)
        screen = self.screen
        #player health bar
        pygame.draw.rect(screen,saddleBrown,(10,10,self.width*.4-10,45))
        label = self.smallFont.render("Player",1,black)
        screen.blit(label, (11,10))
                     #perhaps replace with playerName to let player input own name
        health = "Health:%d/%d" % (self.player.currentHealth,self.player.maxHealth)
        label = self.smallFont.render(health,1,black)
        screen.blit(label,((self.width*.4)/2-40,10))

        mana = "Mana:%d/%d" % (self.player.currentMana,self.player.maxMana)
        label = self.smallFont.render(mana,1,black)
        screen.blit(label,(self.width*.4-85,10))

        pygame.draw.rect(screen,white,(15,25,self.width*.4-20,10))
        pygame.draw.rect(screen,red,(15,25,15+(self.width*.4-20)*self.player.currentHealth/self.player.maxHealth-15,10))
        pygame.draw.rect(screen,white,(15,40,self.width*.4-20,10))
        pygame.draw.rect(screen,blue,(15,40,15+(self.width*.4-20)*self.player.currentMana/self.player.maxMana-15,10))

    def drawEnemyHealthBar(self):
        screen = self.screen
        start = .6*self.width
        end = self.width-10
        pygame.draw.rect(screen,(244,164,96),(start,10,end-start,50))
        enemyName = "Seal: level " + str(self.enemy.monsterLevel)
        label = self.smallFont.render(enemyName,1,(0,0,0))
        screen.blit(label, (start+1,10))

        health = "Health:%d/%d" % (self.enemy.currentHealth,self.enemy.maxHealth)
        label = self.smallFont.render(health,1,(0,0,0))
        screen.blit(label,((start+end)/2-40,10))

        mana = "Mana:%d/%d" % (self.enemy.currentMana,self.enemy.maxMana)
        label = self.smallFont.render(mana,1,(0,0,0))
        screen.blit(label,(end-85,10))

        pygame.draw.rect(screen,(255,255,255),(start+5,25,end-start-10,10))
        pygame.draw.rect(screen,(255,0,0),(start+5,25,(end-start-10)*self.enemy.currentHealth/self.enemy.maxHealth,10))
        pygame.draw.rect(screen,(255,255,255),(start+5,40,end-start-10,10))
        pygame.draw.rect(screen,(0,0,255),(start+5,40,(end-start-10)*self.enemy.currentMana/self.enemy.maxMana,10))

    def drawPlayerAndEnemy(self):
        screen = self.screen
        active_sprite_list = self.active_sprite_list
        active_sprite_list.add(self.battlePlayer)
        active_sprite_list.add(self.battleEnemy)
        active_sprite_list.draw(screen)

    def drawEnemyAttack(self,attack):
        while attack.rect.x > self.battlePlayer.rect.x + self.battlePlayer.rect.width:
            self.screen.fill([255,255,255])
            attack.rect.x += attack.change_x
            self.active_sprite_list.draw(self.screen)

            self.drawBox()
            self.drawWords()
            self.drawSelectionArrow()
            self.drawPlayerHealthBar()
            self.drawEnemyHealthBar()
            self.drawPlayerAndEnemy()

            pygame.display.flip()
        self.active_sprite_list.remove(attack)

    def enemyAttack(self):
        if self.enemy.isStunned:
            self.enemy.isStunned = False
            self.isPlayerTurn = True
        else:
            attack = EnemyProjectile(self.battleEnemy)
            self.active_sprite_list.add(attack)
            self.drawEnemyAttack(attack)

            self.player.currentHealth -= max((self.enemy.attackDamage-self.player.playerLevel),0)
            self.isPlayerTurn = True


    def run(self):
        #returns False when done with the battle
        done = False
        pygame.init()
        while not done:
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done = True # Flag that we are done so we exit this loop
                if event.type == pygame.KEYDOWN and self.isPlayerTurn == True:
                    self.checkUserInput(event)
                if self.enemy.currentHealth <= 0:
                    self.player.gold += max(2*(self.enemy.monsterLevel)**.5,10)
                    self.player.currentExperience += self.enemy.experience
                    self.player.sealsKilled += 1
                    return False
            if not self.isPlayerTurn:
                self.enemyAttack()
                if self.player.currentHealth <= 0:
                    self.player.isDead = True
                    return False
            self.screen.fill([255,255,255])
            self.drawBox()
            self.drawWords()
            self.drawSelectionArrow()
            self.drawPlayerHealthBar()
            self.drawEnemyHealthBar()
            self.drawPlayerAndEnemy()
            pygame.display.flip()
        pygame.quit()



# screenWidth = 800
# screenHeight = 600

#     # Set the height and width of the screen
# size = [screenWidth, screenHeight]
# screen = pygame.display.set_mode(size)
# screen.fill([255,255,255])

# BattleScreenMenu(1,2,screen).drawMenu()

