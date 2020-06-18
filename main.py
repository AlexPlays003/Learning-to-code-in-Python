import pygame, sys
from classXYCordinates import Vector2
from images.imageDict import Images
from levelLoader import Level
from player import Player

class mainGame:

     def __init__(self, screenSize = (640,320)):
          """The main part of the game

          takes in the values of the screen, as a touple in (X,Y) format. 
          default is (640,320)

          ! this just starts pygame, it does not run anything else, to run pygame use mainGame.runGame()
          """
          self.sprites = Images()
          self.screenSize = screenSize

          pygame.init() # start pygame
          pygame.display.set_caption("Learn python") # add text to window

          self.screenSurface = pygame.display.set_mode(screenSize)
          self.FPS = pygame.time.Clock()

     def _center_msg(self, msg):
          """ creates a centalized msg on screen"""
          for i, line in enumerate(msg.splitlines()):
               msg_image =  pygame.font.Font(
                    pygame.font.get_default_font(), 12).render(
                         line, False, (255,255,255), (0,0,0))
          
               msgim_center_x, msgim_center_y = msg_image.get_size()
               msgim_center_x //= 2
               msgim_center_y //= 2
          
               self.screenSurface.blit(msg_image, ( self.screenSize[0] // 2-msgim_center_x, self.screenSize[1] // 2-msgim_center_y+i*22))
     
     def drawMsg(self, msg = '', pos = Vector2(), colour = (255,255,255), size = 12):
          """Creates a msg on screen at Vector2 coordinates from top left corner.
          
          colour in RGB touple (0,0,0 is black, 255,255,255 white)
          size is font zize"""
          for i, line in enumerate(msg.splitlines()):
               msg_image =  pygame.font.Font(
                    pygame.font.get_default_font(), size).render(
                         line, False, colour)
          
               self.screenSurface.blit(msg_image, ( pos.X, pos.Y + i * (size+5)))

     def runGame(self):
          """Main function of pygame. All events are handeled here"""
          while True:
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                         self.Quitify()

                    if event.type == pygame.KEYDOWN:
                         if event.key == pygame.K_w:
                              self.player.move()
                         if event.key == pygame.K_a:
                              self.player.rotateLeft()
                         if event.key == pygame.K_d:
                              self.player.rotateRight()

                         
               
               pygame.display.update()
               self.FPS.tick(15)
	
     def Quitify(self):
          """Quits, what did you expect?
          """
          self._center_msg("Exiting...")
          pygame.display.update()
          pygame.quit()
          sys.exit("user exit")

     def drawObject(self, pos = Vector2(), img = "grass tile.png", image = True, size = Vector2()):
          """Draws an image from dictionary of images. 
          Takes in agument pos as Vector2 type.(position is with tileset, not pixelwise) 
          img argument is the image name. If left blank, default is grass tile.
          if image is False, img will be drawn as text, in the posisiton of vector2 on pixel coordinates, not tile coordinates."""
          if image:
               self.screenSurface.blit(self.sprites.images[img], (pos.X * 32,pos.Y * 32))
          else:
               pygame.draw.rect(self.screenSurface, (0,0,0) , (pos.X,pos.Y, size.X, size.Y))
               game.drawMsg(img, pos) #Vector2(10, self.currentLevel.height * 32 + 10))


     def drawLevel(self,level = Level()):
          """ draws a level of type level.
          Usage:
               drawLevel(Level('nameOfLevel.txt'))
               -> if 'level' argument is left blank, default level will be loaded
               -> level takes in a Level() class
               """

          self.currentLevel = level
          self.player = Player(self.currentLevel ,self.drawObject)

          # rezizes the screen zize to fit the level and extra stuff
          self.screenSize = (self.currentLevel.width * 32 + 64, self.currentLevel.height * 32 + 64)
          self.screenSurface = pygame.display.set_mode(self.screenSize)

          for x in range(0,level.width): 
               for y in range(0,level.height):
                    try:
                         if level.level[y][x] == 'G':
                              self.screenSurface.blit(self.sprites.images["grass tile.png"], (x * 32,y * 32))
                         elif level.level[y][x] == 'W':
                              self.screenSurface.blit(self.sprites.images["water tile.png"], (x * 32,y * 32))
                         elif level.level[y][x] == 'M':
                              self.screenSurface.blit(self.sprites.images["grass tile.png"], (x * 32,y * 32))
                              self.screenSurface.blit(self.sprites.images["flag-2.png"], (x * 32,y * 32))
                              self.player.flagPos = Vector2(x,y)
                         elif level.level[y][x] == 'P':
                              self.screenSurface.blit(self.sprites.images["grass tile.png"], (x * 32,y * 32))
                              self.screenSurface.blit(self.sprites.images["Player-1.png"], (x * 32,y * 32))
                              self.player.pos = Vector2(x,y)
                         elif level.level[y][x] == 'S':
                              self.screenSurface.blit(self.sprites.images["grass tile.png"], (x * 32,y * 32))
                              self.screenSurface.blit(self.sprites.images["Crystal.png"], (x * 32,y * 32))
                              self.player.totalCrystalCount += 1
                    except Exception as e:
                         print ('error in', x , y , e)
          
          self.screenSurface.blit(self.sprites.images["Crystal.png"], (self.currentLevel.width * 32 + 16, 16))
          game.drawMsg("Crystals\nobtained:\n\n" + str(self.player.crystalsCollected) + ' / ' + str(self.player.totalCrystalCount), Vector2(self.currentLevel.width * 32 + 7, 50))
          game.drawMsg("Currently running:", Vector2(10, self.currentLevel.height * 32 + 10))
          pygame.display.update()
                    
game = mainGame((700,400))

game.drawLevel()

# game.player.move()
# game.player.rotateLeft()
# game.player.move()
# game.player.rotateRight()
# game.player.move()
# game.player.rotateLeft()
# game.player.move()
# game.player.move()


game.runGame()