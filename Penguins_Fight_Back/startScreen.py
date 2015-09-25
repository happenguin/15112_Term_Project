import pygame
from spriteFunctions import SpriteSheet





        # titleFont = pygame.font.SysFont("Arial", 40)
        # subTitleFont = pygame.font.SysFont("Arial", 20)


class MainMenu(object):

    def __init__(self, screen):
        pygame.init()
        self.screen = screen
        background = SpriteSheet("arctic background.png")
        title = SpriteSheet("Title.png")
        helpButton = SpriteSheet("HelpButton.png")
        startButton = SpriteSheet("StartButton.png")
        self.background = background.get_image(0,0,800,600)
        self.titleImage = title.get_image(0,0,443,51)
        self.helpButton = helpButton.get_image(0,0,100,50)
        self.startButton = startButton.get_image(0,0,100,50)
        self.inMainMenu = True

    def clickedStart(self,x,y):
        screenWidth,screenHeight = 800,600
        if (x > screenWidth/3-50 and x < screenWidth/3+50 and
            y > 2*screenHeight/3 - 25 and y < screenHeight + 25):
            return True

    def clickedHelp(self,x,y):
        screenWidth,screenHeight = 800,600
        if (x > 2*screenWidth/3-50 and x < 2*screenWidth/3+50 and
            y > 2*screenHeight/3 - 25 and y < screenHeight + 25):
            return True

    def checkClick(self,(x,y)):
        if self.clickedStart(x,y):
            self.inMainMenu = False
        elif self.clickedHelp(x,y):
            HelpScreen(self.screen).draw()

    def draw(self):
        screenWidth,screenHeight = 800,600
        done = False
        while not done:
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done = True # Flag that we are done so we exit this loop
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.checkClick(pygame.mouse.get_pos())
                    if not self.inMainMenu:
                        return True

            self.screen.fill((255,255,255))
            self.screen.blit(self.background, (0,0))
            self.screen.blit(self.titleImage, (screenWidth/2-221,screenHeight/2-25))
            self.screen.blit(self.startButton, (screenWidth/3-50, 2*screenHeight/3-25))
            self.screen.blit(self.helpButton, (2*screenWidth/3-50, 2*screenHeight/3-25))
            pygame.display.flip()
        pygame.quit()

class HelpScreen(object):
    def __init__(self,screen):
        pygame.font.init()
        helpScreen = SpriteSheet("HelpScreen.png")
        self.helpScreen = helpScreen.get_image(0,0,800,600)
        self.screen = screen
        self.inHelpScreen = True

    def checkClick(self,(x,y)):
        if x > 649 and x < 749 and y > 521 and y < 571: 
            #dimensions of the button on the help screen
            self.inHelpScreen = False

    def draw(self):
        done = False
        while not done:
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done = True # Flag that we are done so we exit this loop
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.checkClick(pygame.mouse.get_pos())
                    if not self.inHelpScreen:
                        return

            self.screen.fill((0,0,0))
            self.screen.blit(self.helpScreen, (0,0))
            pygame.display.flip()
        return


