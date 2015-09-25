import pygame
from miscObjects import Weapon,Potion


class ShopMenu(object):

    def __init__(self, player, screen):
        pygame.font.init()
        self.player = player
        self.makePlayerItemList()
        self.allItems = ([Weapon(15,30, "SmallSnowball"),
                          Weapon(20,500, "Snowball"),
                          Weapon(25,1000, "BigSnowball"),
                          Potion("Health",25,10,"Health Potion"),
                          Potion("Mana",25,10,"Mana Potion")])
        self.allItemNames = ["SmallSnowball","Snowball","BigSnowball",
            "Health Potion","Mana Potion","Projectiles","Back"]

        self.inBuyMenu = False
        self.inSellMenu = False
        self.mainMenu = ["Buy","Sell","Quit"]
        self.mainMenuIndex = self.buyMenuIndex = self.sellMenuIndex = 0
        self.smallFont = pygame.font.SysFont("Arial", 20)
        self.screen = screen
        self.done = False

    def makePlayerItemList(self):
        self.playerItems = self.player.weaponInventory+self.player.potionInventory
        self.playerItemNames = []
        for item in self.playerItems:
            self.playerItemNames.append(item.name)
        self.playerItemNames.append("Back")

    def draw(self):
        pygame.init()
        while not self.done:
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self.done = True # Flag that we are done so we exit this loop
                elif event.type == pygame.KEYDOWN:
                    self.checkUserInput(event)
            self.drawWindow()
            self.drawItemText()
            self.drawSelectionArrow()
            pygame.display.flip()

    def drawWindow(self):
        screen = self.screen
        margin = 30
        saddleBrown = (139,69,19)
        sandyBrown = (244,164, 96)
        black = (0,0,0)
        pygame.draw.rect(screen,saddleBrown,(margin-5, margin-5, 300+10,300+10))
        pygame.draw.rect(screen,sandyBrown,(margin, margin, 300,300))
        pygame.draw.line(screen,black,((margin+300/2),2*margin),((margin+300/2),300+margin))
        pygame.draw.line(screen,black,(margin,2*margin),(margin+300,2*margin))

    def buyItem(self):
        if(len(self.playerItems) < 9):
            item = self.allItems[self.buyMenuIndex]
            if self.player.gold > item.price:
                if type(item) == Weapon:
                    inInventory = False
                    for weapon in self.player.weaponInventory:
                        if weapon.name == item.name:
                            inInventory = True
                    if not inInventory:
                        self.player.weaponInventory.append(item)
                        self.player.gold -= item.price
                elif type(item) == Potion and len(self.player.potionInventory)<6:
                    self.player.potionInventory.append(item)
                    self.player.gold -= item.price
                self.makePlayerItemList()
            

    def sellItem(self):
        item = self.playerItems[self.sellMenuIndex]
        if type(item) == Weapon:
            self.player.weaponInventory.remove(item)
        elif type(item) == Potion:
            self.player.potionInventory.remove(item)
        self.makePlayerItemList()
        self.player.gold += item.price/3

    def checkUserInput(self,event):
        if event.key == pygame.K_UP:
            if self.inSellMenu and self.sellMenuIndex > 0:
                self.sellMenuIndex -=1
            elif self.inBuyMenu and self.buyMenuIndex > 0:
                self.buyMenuIndex -= 1
            elif (not self.inSellMenu and not self.inBuyMenu and 
                self.mainMenuIndex > 0):
                self.mainMenuIndex -= 1
        if event.key == pygame.K_DOWN:
            if self.inSellMenu and self.sellMenuIndex < len(self.playerItemNames)-1:
                self.sellMenuIndex += 1
            elif self.inBuyMenu and self.buyMenuIndex < len(self.allItemNames)-1:
                self.buyMenuIndex += 1
            elif (not self.inBuyMenu and not self.inSellMenu and 
                self.mainMenuIndex < len(self.mainMenu)-1):
                self.mainMenuIndex +=1
        if event.key == 32:
            if self.inSellMenu:
                if self.playerItemNames[self.sellMenuIndex] == "Back":
                    self.inSellMenu = False
                else:
                    self.sellItem()
            elif self.inBuyMenu:
                if self.allItemNames[self.buyMenuIndex] == "Back":
                    self.inBuyMenu = False
                elif self.allItemNames[self.buyMenuIndex] == "Projectiles":
                    self.player.projectiles += 1
                    self.player.gold -= 10
                else:
                    self.buyItem()
            elif self.mainMenu[self.mainMenuIndex] == "Buy":
                self.inBuyMenu = True
                self.buyMenuIndex = 0
            elif self.mainMenu[self.mainMenuIndex] == "Sell":
                self.inSellMenu = True
                self.sellMenuIndex = 0
            elif self.mainMenu[self.mainMenuIndex] == "Quit":
                self.done = True
        if event.key == 115:
            self.done = True

    def drawSelectionArrow(self):
        if self.inSellMenu:
            index = self.sellMenuIndex
        elif self.inBuyMenu:
            index = self.buyMenuIndex
        else:
            index = self.mainMenuIndex
        screen = self.screen
        margin = 30
        arrowBound = 7
        leftX = margin + arrowBound
        rightX = 2*margin - 2*arrowBound
        topY = (index+2)*margin + arrowBound
        botY = topY + 20 - 1.5*arrowBound
        midY = (topY+botY)/2
        pygame.draw.polygon(screen, (0,0,0), [[leftX,10+topY],[rightX,10+midY],[leftX,10+botY]])
    
    def drawPrice(self,startY,index, itemList):
        screen = self.screen
        margin = 35
        if index < len(itemList)+1:
            if self.inBuyMenu:
                if self.allItemNames[index] == "Projectiles":
                    price = "10"
                else:
                    price = str(itemList[index].price)
            elif self.inSellMenu:
                if index < len(itemList):
                    price = str(itemList[index].price/3)
                else: price = ""
            label = self.smallFont.render(price,1,(0,0,0))
            screen.blit(label, (margin+160, startY+margin))

    def printGold(self):
        margin = 35
        screen = self.screen
        gold = "Gold: " + str(self.player.gold)
        label = self.smallFont.render(gold, 1, (0,0,0))
        screen.blit(label, (margin+180, margin))

    def drawItemText(self):
        screen = self.screen
        margin  = startY = 35
        if not self.inSellMenu and not self.inBuyMenu:
            #draw the title
            label = self.smallFont.render("Shop", 1, (0,0,0))
            screen.blit(label, (margin+20, margin))
            itemNameList = self.mainMenu
        elif self.inSellMenu:
            label = self.smallFont.render("Sell", 1, (0,0,0))
            screen.blit(label, (margin+20, margin))
            itemNameList = self.playerItemNames
            itemList = self.playerItems
        elif self.inBuyMenu:
            label = self.smallFont.render("Buy", 1, (0,0,0))
            screen.blit(label, (margin+20, margin))
            itemNameList = self.allItemNames
            itemList = self.allItems
        for index in xrange(len(itemNameList)):
            label = self.smallFont.render(itemNameList[index], 1, (0,0,0))
            screen.blit(label, (margin+20, startY+margin))
            if self.inSellMenu or self.inBuyMenu:
                self.drawPrice(startY, index, itemList)
            startY += 30
        self.printGold()

class AbilityMenu(object):

    def __init__(self, player, screen):
        pygame.font.init()
        self.player = player
        self.abilityNames = []
        for ability in self.player.abilityList:
            self.abilityNames.append(ability.name)
        self.abilityNames.append("Back")
        self.screen = screen
        self.smallFont = pygame.font.SysFont("Arial", 20)
        self.abilityMenuIndex = 0
        self.done = False

    def draw(self):
        pygame.init()
        while not self.done:
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self.done = True # Flag that we are done so we exit this loop
                elif event.type == pygame.KEYDOWN:
                    self.checkUserInput(event)
            self.drawWindow()
            self.drawText()
            self.drawSelectionArrow()
            self.drawDescription()
            pygame.display.flip()

    def drawWindow(self):
        screen = self.screen
        margin = 30
        saddleBrown = (139,69,19)
        sandyBrown = (244,164, 96)
        black = (0,0,0)
        pygame.draw.rect(screen,saddleBrown,(margin-5, margin-5, 500+10,300+10))
        pygame.draw.rect(screen,sandyBrown,(margin, margin, 500,300))
        pygame.draw.line(screen,black,((margin+300/2),2*margin),((margin+300/2),300+margin))
        pygame.draw.line(screen,black,(margin,2*margin),(margin+500,2*margin))

    def checkUserInput(self,event):
        if event.key == pygame.K_UP and self.abilityMenuIndex > 0:
            self.abilityMenuIndex -=1
        if event.key == pygame.K_DOWN and self.abilityMenuIndex < len(self.abilityNames)-1:
            self.abilityMenuIndex +=1
        if event.key == 107:
            self.done = True
        if event.key == 32 and self.abilityNames[self.abilityMenuIndex] == "Back":
            self.done = True

    def drawSelectionArrow(self):
        index = self.abilityMenuIndex
        screen = self.screen
        margin = 30
        arrowBound = 7
        leftX = margin + arrowBound
        rightX = 2*margin - 2*arrowBound
        topY = (index+2)*margin + arrowBound
        botY = topY + 20 - 1.5*arrowBound
        midY = (topY+botY)/2
        pygame.draw.polygon(screen, (0,0,0), [[leftX,10+topY],[rightX,10+midY],[leftX,10+botY]])

    def drawDescription(self):
        index = self.abilityMenuIndex
        screen = self.screen
        margin = 35
        if index < len(self.player.abilityList):
            description = self.player.abilityList[index].description
            label = self.smallFont.render(description,1,(0,0,0))
            screen.blit(label, (margin+160, 2*margin))
    
    def drawText(self):
        screen = self.screen
        margin  = startY = 35
        label = self.smallFont.render("Abilities", 1, (0,0,0))
        screen.blit(label, (margin+20, margin))
        for item in self.abilityNames:
            label = self.smallFont.render(item, 1, (0,0,0))
            screen.blit(label, (margin+20, startY+margin))
            startY += 30
        # self.printGold()

class ItemMenu(object):

    def __init__(self, weapons, potions, screen, player):
        pygame.font.init()
        self.player = player
        self.weapons = weapons
        self.weaponNames = []
        for weapon in weapons:
            self.weaponNames.append(weapon.name)
        self.weaponNames.append("Back")
        self.potions = potions
        self.makePotionList()
        self.starting = ["Weapons","Potions", "Back"]
        self.screen = screen
        self.smallFont = pygame.font.SysFont("Arial", 20)
        self.inWeaponMenu = False
        self.inPotionMenu = False
        self.weaponMenuIndex = self.potionMenuIndex = self.mainMenuIndex = 0
        self.done = False

    def makePotionList(self):
        self.potionNames = []
        for potion in self.potions:
            self.potionNames.append(potion.name)
        self.potionNames.append("Back")

    def equipWeapon(self):
        equippedWeapon = self.player.weapon
        self.player.weapon = self.weapons[self.weaponMenuIndex]
        self.weapons[self.weaponMenuIndex] = equippedWeapon
        self.weaponNames[self.weaponMenuIndex] = equippedWeapon.name

    def usePotion(self):
        potion = self.potions[self.potionMenuIndex]
        if (potion.potionType == "Health" and 
            self.player.currentHealth < self.player.maxHealth or 
            potion.potionType == "Mana" and 
            self.player.currentMana < self.player.maxHealth):
            potion.usePotion(self.player)
            self.potions.remove(potion)
            self.makePotionList()


    def draw(self):
        pygame.init()
        while not self.done:
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self.done = True # Flag that we are done so we exit this loop
                elif event.type == pygame.KEYDOWN:
                    self.checkUserInput(event)
            self.drawWindow()
            self.drawItemText()
            self.drawSelectionArrow()
            pygame.display.flip()

    def drawWindow(self):
        screen = self.screen
        margin = 30
        saddleBrown = (139,69,19)
        sandyBrown = (244,164, 96)
        black = (0,0,0)
        pygame.draw.rect(screen,saddleBrown,(margin-5, margin-5, 300+10,300+10))
        pygame.draw.rect(screen,sandyBrown,(margin, margin, 300,300))
        pygame.draw.line(screen,black,((margin+300/2),2*margin),((margin+300/2),300+margin))
        pygame.draw.line(screen,black,(margin,2*margin),(margin+300,2*margin))

    def checkUserInput(self,event):
        if event.key == pygame.K_UP:
            if self.inWeaponMenu and self.weaponMenuIndex > 0:
                self.weaponMenuIndex -=1
            elif self.inPotionMenu and self.potionMenuIndex > 0:
                self.potionMenuIndex -= 1
            elif (not self.inPotionMenu and not self.inWeaponMenu and 
                self.mainMenuIndex > 0):
                self.mainMenuIndex -=1
        if event.key == pygame.K_DOWN:
            if self.inWeaponMenu and self.weaponMenuIndex < len(self.weaponNames)-1:
                self.weaponMenuIndex +=1
            elif self.inPotionMenu and self.potionMenuIndex < len(self.potionNames)-1:
                self.potionMenuIndex += 1
            elif (not self.inPotionMenu and not self.inWeaponMenu and 
                self.mainMenuIndex < len(self.starting)-1):
                self.mainMenuIndex +=1
        if event.key == 32:
            if self.inWeaponMenu:
                if self.weaponNames[self.weaponMenuIndex] == "Back":
                    self.inWeaponMenu = False
                else:
                    self.equipWeapon()
            elif self.inPotionMenu:
                if self.potionNames[self.potionMenuIndex] == "Back":
                    self.inPotionMenu = False
                else:
                    self.usePotion()
            elif self.starting[self.mainMenuIndex] == "Weapons":
                self.inWeaponMenu = True
                self.weaponMenuIndex = 0
            elif self.starting[self.mainMenuIndex] == "Potions":
                self.inPotionMenu = True
                self.potionMenuIndex = 0
            elif self.starting[self.mainMenuIndex] == "Back":
                self.done = True
        if event.key == 105:
            self.done = True


    def drawSelectionArrow(self):
        if self.inWeaponMenu:
            index = self.weaponMenuIndex
        elif self.inPotionMenu:
            index = self.potionMenuIndex
        else:
            index = self.mainMenuIndex
        screen = self.screen
        margin = 30
        arrowBound = 7
        leftX = margin + arrowBound
        rightX = 2*margin - 2*arrowBound
        topY = (index+2)*margin + arrowBound
        botY = topY + 20 - 1.5*arrowBound
        midY = (topY+botY)/2
        pygame.draw.polygon(screen, (0,0,0), [[leftX,10+topY],[rightX,10+midY],[leftX,10+botY]])

    def printGold(self):
        margin = 35
        screen = self.screen
        gold = "Gold: " + str(self.player.gold)
        label = self.smallFont.render(gold, 1, (0,0,0))
        screen.blit(label, (margin+180, margin))
    
    def drawItemText(self):
        screen = self.screen
        margin  = startY = 35
        if not self.inWeaponMenu and not self.inPotionMenu:
            #draw the title
            label = self.smallFont.render("Items", 1, (0,0,0))
            screen.blit(label, (margin+20, margin))
            itemList = self.starting
        elif self.inWeaponMenu:
            label = self.smallFont.render("Weapons", 1, (0,0,0))
            screen.blit(label, (margin+20, margin))
            itemList = self.weaponNames
        elif self.inPotionMenu:
            label = self.smallFont.render("Potions", 1, (0,0,0))
            screen.blit(label, (margin+20, margin))
            itemList = self.potionNames
        for item in itemList:
            label = self.smallFont.render(item, 1, (0,0,0))
            screen.blit(label, (margin+20, startY+margin))
            startY += 30
        self.printGold()
