'''
Robert Brzostek
Date: 1/22/2020
Aqua Adventure 3
'''
# Import needed modules, functions, and settings
import pygame as pg, time, random, math
from settings import *
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Initialize Pygame
pg.init()
pg.mixer.init()

# Init screen settings
size = (1500, 800) # screen width and height
screen = pg.display.set_mode(size)
pg.display.set_caption("Aqua Adventure 3") # caption text

# Loop until the user clicks the close button
done = False

# Manage how fast the screen updates
clock = pg.time.Clock()

# # FUNCTIONS # #

# Text that fades in, holds for a duration, and fades out again
def fadingText(screen, x, y, txt, size, color, holdTime, maxOpacity, fadeSpeed, bold=False, itallic=False):
    if uiText.fadeActive:
        # Counts the number of frames since fade initialized
        uiText.frameCounter += 1
        # Fade up when text is below maxOpacity
        if uiText.frameCounter * fadeSpeed <= maxOpacity:
            # Stop fadeFrame from exceeding 255 (pygame max opacity)
            if uiText.fadeFrame + fadeSpeed > maxOpacity:
                uiText.fadeFrame = maxOpacity
            else:  
                uiText.fadeFrame += fadeSpeed

        # Hold opacity for duration of holdTime
        elif maxOpacity < uiText.frameCounter * fadeSpeed <= maxOpacity + holdTime:
            uiText.fadeFrame = uiText.fadeFrame

        # Decrease opacity
        elif uiText.frameCounter * fadeSpeed >= maxOpacity + holdTime:
            if uiText.fadeFrame > 0:
                uiText.fadeFrame -= fadeSpeed
            elif uiText.fadeFrame == 0:
                uiText.fadeActive = False
                
        # Draw the text
        uiText.draw(screen, x, y, txt, size, color, uiText.fadeFrame, bold, itallic) 

    # Reset appropriate variables
    else:
        uiText.frameCounter = 1
        uiText.fadeFrame = 0

# Core code for each segment
def segmentCore(ev):
    # Display new location text if entering new segment
    if player.current_location not in player.visited_list:
        fadingText(screen, 550, 200, player.location_list[player.current_location][0], 50, black, 240, 255, 10, False, True)
    else:
        uiText.fadeActive = False

    # Update player needs
    player.updateNeeds(ev)

    # when player ui closed
    if not player.uiActive and not player.tuiActive:
        # update local position and health
        player.updatePos(screen, ev)
        player.healthCheck(ev)

    # Draw main on-screen and minilog UI
    player.drawUI(ev)
    player.updateMiniLog(ev)

    # Handle projectile behaviour
    for projectile in projectiles:
        # Ensure projectiles are on screen
        if projectile.x < 1500 and projectile.x > 0 and projectile.y < 800 and projectile.y > 0:
            # Set projectile velocity according to angle
            if projectile.angle == 0:
                projectile.x += projectileSpeed
            elif projectile.angle == 315:
                projectile.x += projectileSpeed
                projectile.y += projectileSpeed
            elif projectile.angle == 270:
                projectile.y += projectileSpeed
            elif projectile.angle == 225:
                projectile.x -= projectileSpeed
                projectile.y += projectileSpeed
            elif projectile.angle == 180:
                projectile.x -= projectileSpeed
            elif projectile.angle == 135:
                projectile.x -= projectileSpeed
                projectile.y -= projectileSpeed
            elif projectile.angle == 90:
                projectile.y -= projectileSpeed
            elif projectile.angle == 45:
                projectile.x += projectileSpeed
                projectile.y -= projectileSpeed

            # Check for collisions with npcs
            for npc in player.npcList:
                # Check x coords
                if projectile.y - projectile.radius < npc.rect.y + npc.rect.h and projectile.y + projectile.radius > npc.rect.y:
                    # Check y coords
                    if projectile.x + projectile.radius > npc.rect.x and projectile.x - projectile.radius < npc.rect.x + npc.rect.w:
                        npc.hit(projectile.damage, projectile.origin)
                        projectiles.remove(projectile)

            # Check for collisions with walls
            for wall in player.sprites:
                # Check x coords
                if projectile.y - projectile.radius < wall.rect.y + wall.rect.h and projectile.y + projectile.radius > wall.rect.y:
                    # Check y coords
                    if projectile.x + projectile.radius > wall.rect.x and projectile.x - projectile.radius < wall.rect.x + wall.rect.w:
                        if projectile in projectiles:
                            projectiles.remove(projectile)

            # Check for collisions with gameObjects
            for gameObject in gameObjectList:
                # Check x coords
                if projectile.y - projectile.radius < gameObject.rect.y + gameObject.rect.h and projectile.y + projectile.radius > gameObject.rect.y:
                    # Check y coords
                    if projectile.x + projectile.radius > gameObject.rect.x and projectile.x - projectile.radius < gameObject.rect.x + gameObject.rect.w:
                        if projectile in projectiles:
                            projectiles.remove(projectile)

        # Remove projectiles when off screen
        else:
            projectiles.remove(projectile)

        # Draw the projectiles
        projectile.draw(screen)

    # Handle hostileProjectile behaviour
    for projectile in hostileprojectiles:
        # Ensure projectiles are on screen
        if projectile.x < 1500 and projectile.x > 0 and projectile.y < 800 and projectile.y > 0:
            # Set projectile velocity according to angle
            if projectile.angle == 0:
                projectile.x += projectileSpeed
            elif projectile.angle == 315:
                projectile.x += projectileSpeed
                projectile.y += projectileSpeed
            elif projectile.angle == 270:
                projectile.y += projectileSpeed
            elif projectile.angle == 225:
                projectile.x -= projectileSpeed
                projectile.y += projectileSpeed 
            elif projectile.angle == 180:
                projectile.x -= projectileSpeed
            elif projectile.angle == 135:
                projectile.x -= projectileSpeed
                projectile.y -= projectileSpeed
            elif projectile.angle == 90:
                projectile.y -= projectileSpeed
            elif projectile.angle == 45:
                projectile.x += projectileSpeed
                projectile.y -= projectileSpeed

            # Check for collisions with player
            if projectile.y - projectile.radius < player.rect.y + player.rect.h and projectile.y + projectile.radius > player.rect.y:
                # Check y coords
                if projectile.x + projectile.radius > player.rect.x and projectile.x - projectile.radius < player.rect.x + player.rect.w:
                    player.combatHit(projectile.damage, projectile.origin)
                    hostileprojectiles.remove(projectile)
        
            # Check for collisions with walls
            for wall in player.sprites:
                # Check x coords
                if projectile.y - projectile.radius < wall.rect.y + wall.rect.h and projectile.y + projectile.radius > wall.rect.y:
                    # Check y coords
                    if projectile.x + projectile.radius > wall.rect.x and projectile.x - projectile.radius < wall.rect.x + wall.rect.w:
                        if projectile in hostileprojectiles:
                            hostileprojectiles.remove(projectile)

            # Check for collisions with gameObjects
            for gameObject in gameObjectList:
                # Check x coords
                if projectile.y - projectile.radius < gameObject.rect.y + gameObject.rect.h and projectile.y + projectile.radius > gameObject.rect.y:
                    # Check y coords
                    if projectile.x + projectile.radius > gameObject.rect.x and projectile.x - projectile.radius < gameObject.rect.x + gameObject.rect.w:
                        if projectile in hostileprojectiles:
                            hostileprojectiles.remove(projectile)

        # Remove projectiles when off screen
        else:
            hostileprojectiles.remove(projectile)

        # Draw the projectiles
        projectile.draw(screen)

    # Remove NPCs with HP <0
    for npc in player.npcList:
        if npc.health <= 0:
            player.available_targets.remove(npc)
            if npc.inventory != None:
                player.event_log.append("You pick up some items from a corpse.")
                player.inventory.append(npc.inventory)
            if npc.creatureClass == "Boss":
                stageSys.stageTransition(5)
            player.npcList.remove(npc)
            player.skills[2][3] += 1


    # Update north/south player world location
    if player.rect.top < 10:
        player.updateLocation("North")
    elif player.rect.bottom > 790:
        player.updateLocation("South")
    
    # Update east/west player world location
    if player.rect.left < 10:
        player.updateLocation("West")
    elif player.rect.right > 1490:
        player.updateLocation("East")
    
# GameObject interaction
# Handle game object interaction
def gameObjectHandler(segment, ev):
    for gameObject in gameObjectList:
        if gameObject.segment == segment:
            if not player.uiActive and not player.tuiActive:
                # Draw the object
                gameObject.draw()
            # Handle it
            playerDeltaX = (gameObject.rect.x + (gameObject.rect.w // 2)) - (player.rect.x + (player.rect.w // 2))
            playerDeltaY = (gameObject.rect.y + (gameObject.rect.h // 2)) - (player.rect.y + (player.rect.h // 2))
            # make sure player is within interaction range
            if -60 < abs(playerDeltaX) < 60 and -60 < abs(playerDeltaY) < 60:
                # to do when object is a container
                if gameObject.type == "Container":
                    # if its locked
                    if gameObject.locked == True:
                        # brute force unlock
                        if item_list[16] in player.inventory:
                            gameObject.text("E) Force Open")
                            if not player.uiActive and not player.tuiActive:
                                for event in ev:
                                    if event.type == pg.KEYUP and event.key == pg.K_e:
                                        openDoor.play()
                                        player.event_log.append("You force the container open.")
                                        player.skills[4][3] += 1
                                        gameObject.locked = False
                        # lockpick unlock
                        else:
                            if not player.uiActive and not player.tuiActive:
                                gameObject.text("E) Unlock")
                                for event in ev:
                                    if event.type == pg.KEYUP and event.key == pg.K_e:
                                        if item_list[15] in player.inventory:
                                            if random.randint(0, 7 - (player.skills[0][2] * 10)) == 0:
                                                openDoor.play()
                                                player.event_log.append("You unlocked the container.")
                                                player.skills[0][3] += 1
                                                player.inventory.remove(item_list[15])
                                                gameObject.locked = False
                                            else:
                                                player.event_log.append("You failed to unlock the container.")
                                                player.inventory.remove(item_list[15])
                                        else:
                                            player.event_log.append("You have no Bobby Pins.")
                    # if unlocked
                    else:
                        gameObject.text("E) Open")
                        if not player.uiActive and not player.tuiActive:
                            for event in ev:
                                if event.type == pg.KEYUP and event.key == pg.K_e:
                                    openDoor.play()
                                    if gameObject.inventory != None:
                                        player.tuiActive = True
                        # Open transfer UI
                        if player.tuiActive:                
                            player.transferUI(ev, gameObject.inventory)

                # to do when object is a door
                elif gameObject.type == "Door":
                    # if its locked
                    if gameObject.locked == True:
                        # brute force unlock
                        if item_list[16] in player.inventory:
                            if not player.uiActive and not player.tuiActive:
                                gameObject.text("E) Force Open")
                                for event in ev:
                                    if event.type == pg.KEYUP and event.key == pg.K_e:
                                        openDoor.play()
                                        player.event_log.append("You force the door open.")
                                        player.skills[4][3] += 1
                                        gameObject.locked = False
                        # lockpick unlock
                        else:
                            if not player.uiActive and not player.tuiActive:
                                gameObject.text("E) Unlock")
                                for event in ev:
                                    if event.type == pg.KEYUP and event.key == pg.K_e:
                                        if item_list[15] in player.inventory:
                                            if random.randint(0, 6 - (player.skills[0][2] * 10)) == 0:
                                                openDoor.play()
                                                player.event_log.append("You unlocked the door.")
                                                player.skills[0][3] += 1
                                                player.inventory.remove(item_list[15])
                                                gameObject.locked = False
                                            else:
                                                objectLocked.play()
                                                player.event_log.append("You failed to unlock the door.")
                                                player.inventory.remove(item_list[15])
                                        else:
                                            player.event_log.append("You have no Bobby Pins.")
                    # if unlocked
                    else:
                        gameObject.text("E) Use")
                        if not player.uiActive and not player.tuiActive:
                            for event in ev:
                                if event.type == pg.KEYUP and event.key == pg.K_e:
                                    openDoor.play()
                                    # swap width/height
                                    w = gameObject.rect.w
                                    h = gameObject.rect.h
                                    gameObject.rect.w = h
                                    gameObject.rect.h = w

# Draw trees
def drawTree(x, y, w, h):
    screen.blit(pg.transform.smoothscale(tree1, (w, h)), (x, y))

# # CLASSES # #
# Button handler class
class Button():
    def __init__(self, mainColor, borderColor):
        self.mainColor = mainColor
        self.borderColor = borderColor
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0

    # Draw button button
    def draw(self, screen, x, y, w, h, txt, txtSize, txtColor):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        pg.draw.rect(screen, self.borderColor, (self.x, self.y, self.w, self.h))
        pg.draw.rect(screen, self.mainColor, (self.x + 2, self.y + 2, self.w - 4, self.h - 4))

        text = buttonFont.render(txt, True, txtColor)
        screen.blit(text, (self.x + 5, self.y + (self.h // 2 - text.get_height() // 2 )))

    # Handle behaviour for the button (method returns True/False)
    def isActive(self, ev, keyPress):
        pos = pg.mouse.get_pos()
        for event in ev:
            # Handle mouse clicks
            if event.type == pg.MOUSEBUTTONDOWN:
                if pos[0] > self.x and pos[0] < self.x + self.w:
                    if pos[1] > self.y and pos[1] < self.y + self.h:
                        return True
            
            # Handle key input
            elif event.type == pg.KEYUP and event.key == keyPress:
                return True
        
        # Button default state
        return False

# Highly adaptive text drawing
class Text():
    def __init__(self):
        self.posX = 0
        self.posY = 0
        self.txtSize = 12
        self.txtColor = white
        self.txtBold = False
        self.txtItallic = False
        self.frameCounter = 0
        self.fadeFrame = 0
        self.fadeActive = True
    
    # Flexible text drawing
    def draw(self, surface, x, y, txt, size, color, opacity, bold=False, itallic=False):
        txtFont = pg.font.SysFont("lucidaconsole", size, bold, itallic)
        text = txtFont.render(txt, True, color)
        surf = pg.Surface(text.get_size()).convert_alpha()
        surf.fill((255, 255, 255, opacity))
        text.blit(surf, (0, 0), special_flags = pg.BLEND_RGBA_MULT)
        surface.blit(text, (x, y))

# # WALL (use function above game loop to draw)# #
class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        # Call the parent's constructor
        super().__init__()
 
        # Make a wall, of the size specified in the parameters
        self.image = pg.Surface([w, h])
        self.image.fill(color)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

# # MAP OBJECTS # #
# Container
class Container(pg.sprite.Sprite):
    def __init__(self, x, y, segment, type, contents, locked=False):
        # Init sprite
        super().__init__()

        self.type = "Container"
        self.default = pg.image.load(addressprefix + "\\misc\\woodCrate.png").convert_alpha()
        self.image = pg.transform.smoothscale(self.default, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.segment = segment
        self.inventory = contents
        self.locked = locked

    def draw(self):
        screen.blit(pg.transform.smoothscale(self.image, (50, 50)), (self.rect.x, self.rect.y))

    def text(self, txt):
        uiText.draw(screen, self.rect.x + self.rect.w, self.rect.y, txt, 18, white, 255, True)

# Door
class Door(pg.sprite.Sprite):
    def __init__(self, x, y, segment, type, contents=None, locked=False, w=None, h=None):
        # Init sprite
        super().__init__()

        self.type = "Door"
        self.image = pg.Surface([w, h])
        self.image.fill(doorBrown)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.w = w
        self.rect.h = h
        self.segment = segment
        self.inventory = None
        self.locked = locked

    def draw(self):
        self.image = pg.Surface([self.rect.w, self.rect.h])
        self.image.fill(doorBrown)
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def text(self, txt):
        uiText.draw(screen, self.rect.x, self.rect.y, txt, 18, white, 255, True)
        
# # PROJECTILES # #
# For player use
class Projectile(pg.sprite.Sprite):
    def __init__(self, x, y, radius, color, angle, damage, origin):
        super().__init__()
        self.x = x
        self.y = y
        self.x_change = 0
        self.y_change = 0
        self.angle = angle
        self.radius = radius
        self.color = color
        self.damage = damage
        self.origin = origin
        self.coords = [x + (radius // 2), y + (radius // 2)]
        
    # Draw the bullets on screen
    def draw(self, screen):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# For other game objects
class hostileProjectile(pg.sprite.Sprite):
    def __init__(self, x, y, radius, color, angle, damage, origin):
        self.x = x
        self.y = y
        self.x_change = 0
        self.y_change = 0
        self.angle = angle
        self.radius = radius
        self.color = color
        self.damage = damage
        self.origin = origin
        
    # Draw the bullets on screen
    def draw(self, screen):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# # NPC CLASS # #
class NPC(pg.sprite.Sprite):
    def __init__(self, locationX, locationY, angle, creatureType, creatureClass, alignment, health, shotRange, shotDamage, item, triggerRange, scale=1):
        global npcSpeed
        # Sprite init
        super().__init__()

        # Load images for human type
        self.defaultHuman = pg.image.load(addressprefix + "\\misc\\npcHuman.png") 
        human_leftForward = pg.image.load(addressprefix + "\\misc\\npcHuman-leftForward.png")
        human_rightForward = pg.image.load(addressprefix + "\\misc\\npcHuman-rightForward.png")
        self.humanAnimationImages = [human_leftForward, human_rightForward]

        # Load images for robot type
        self.defaultRobot = pg.image.load(addressprefix + "\\misc\\robot.png")

        # Active image variable
        self.image = pg.transform.rotate((pg.transform.smoothscale(self.defaultHuman, (50 * scale, 50 * scale))), 270)
        
        # Movement properties
        self.x_change = 0
        self.y_change = 0
        self.angle = angle
        self.rect = self.image.get_rect()
        self.rect.x = locationX
        self.rect.y = locationY
        self.speed = npcSpeed

        # Basic properties
        self.health = health
        self.accuracy = 0.8
        self.range = shotRange
        self.triggerRange = triggerRange
        self.damage = shotDamage
        self.alignment = alignment
        self.creatureType = creatureType
        self.creatureClass = creatureClass
        self.inventory = item
        self.aggravated = False
        self.target = None

        # Misc
        self.frameCounter = 0
        self.animationCounter = 0
        self.npcList = []
        self.scale = scale

    # Handle NPC shooting
    def shoot(self, ev):
        for event in ev:
            if event.type == enemyShootEvent:
                gunShot.play()
                hostileprojectiles.append(hostileProjectile(round(self.rect.x + (self.rect.w // 2)), round(self.rect.y + (self.rect.h // 2)), 4, black, self.angle, self.damage, "NPC"))
    # Move the NPC
    def move(self, moveDir):
        # movement handler
        if moveDir == "up":
            self.y_change = -self.speed
        elif moveDir == "down":
            self.y_change = self.speed
        elif moveDir == "left":
            self.x_change = -self.speed
        elif moveDir == "right":
            self.x_change = self.speed
        elif moveDir == "upLeft":
            self.y_change = -self.speed
            self.x_change = -self.speed
        elif moveDir == "upRight":
            self.y_change = -self.speed
            self.x_change = self.speed
        elif moveDir == "downLeft":
            self.y_change = self.speed
            self.x_change = -self.speed
        elif moveDir == "downRight":
            self.y_change = self.speed
            self.x_change = self.speed
        else:
            self.x_change = 0
            self.y_change = 0

    # Handle the NPC's behaviour in combat
    def combatBehaviour(self, ev):
        # Calculate distance between NPC and target (in x and y dimensions)
        deltaX = (self.rect.x + (self.rect.w // 2)) - (self.target.rect.x + (self.target.rect.w // 2))
        deltaY = (self.rect.y + (self.rect.h // 2)) - (self.target.rect.y + (self.target.rect.h // 2))
        
        # Start tracking target when in trigger range
        if -self.triggerRange < abs(deltaX) < self.triggerRange and -self.triggerRange < abs(deltaY) < self.triggerRange:
            # Track target and shoot when lined up
            if deltaX < 0 and -24 < deltaY < 24:
                if abs(deltaX) > self.range:
                    self.move("right")
                else:
                    self.angle = 0
                    self.shoot(ev)
            if deltaX > 0 and -24 < deltaY < 24:
                if abs(deltaX) > self.range:
                    self.move("left")
                else:
                    self.angle = 180
                    self.shoot(ev)
            if deltaY < 0 and -24 < deltaX < 24:
                if abs(deltaY) > self.range:
                    self.move("down")
                else:
                    self.angle = 270
                    self.shoot(ev)
            if deltaY > 0 and -24 < deltaX < 24:
                if abs(deltaY) > self.range:
                    self.move("up")
                else:
                    self.angle = 90
                    self.shoot(ev)

            # Special case targetting (diagonals)
            if deltaX >= 24 and deltaY <= -24:
                if abs(deltaX) > self.range or abs(deltaY) > self.range:
                    self.move("downLeft")
                else:
                    self.angle = 225
                    self.shoot(ev)
            if deltaX >= 24 and deltaY >= 24:
                if abs(deltaX) > self.range or abs(deltaY) > self.range:
                    self.move("upLeft")
                else:
                    self.angle = 135
                    self.shoot(ev)
            if deltaX <= -24 and deltaY >= 24:
                if abs(deltaX) > self.range or abs(deltaY) > self.range:
                    self.move("upRight")
                else:
                    self.angle = 45
                    self.shoot(ev)
            if deltaX <= -24 and deltaY <= -24:
                if abs(deltaX) > self.range or abs(deltaY) > self.range:
                    self.move("downRight")
                else:
                    self.angle = 315
                    self.shoot(ev)

    # Draw the NPC
    def draw(self, ev):
        # rotation handler
        if self.x_change < 0:
            if self.y_change < 0:
                self.angle = 135
            elif self.y_change > 0:
                self.angle = 225
            else:
                self.angle = 180
        elif self.x_change > 0:
            if self.y_change < 0:
                self.angle = 45
            elif self.y_change > 0:
                self.angle = 315
            else:
                self.angle = 0
        elif self.y_change < 0:
            self.angle = 90
        elif self.y_change > 0:
            self.angle = 270

        # Handle human walk animation
        if self.creatureType == "Human":
            # Don't animate when not moving
            if self.x_change == 0 and self.y_change == 0:
                self.image = self.defaultHuman
            
            # Animate while moving
            elif self.x_change != 0 or self.y_change != 0:
                self.frameCounter += 1
                if self.frameCounter == 11:
                    stepLeft.play()
                    self.image = self.humanAnimationImages[0]
                elif self.frameCounter == 23:
                    stepRight.play()
                    self.image == self.humanAnimationImages[1]
                elif self.frameCounter == 24:
                    self.frameCounter = 0

        # Robot type NPCs do not have walk animations
        elif self.creatureType == "Robot":
            self.image = self.defaultRobot

        # Make temp npcList without this npc in
        for npc in player.npcList:
            self.npcList.append(npc)
        self.npcList.remove(self)

        # Move the NPC left/right
        self.rect.x += self.x_change

        # Check if it collides with walls
        block_hit_list = pg.sprite.spritecollide(self, player.sprites, False)
        for block in block_hit_list:
            # Moving right
            if self.x_change > 0:
                self.rect.right = block.rect.left
            # Moving left
            else:
                self.rect.left = block.rect.right

        # Check if colliding other npcs
        npc_hit_list = pg.sprite.spritecollide(self, self.npcList, False)
        for npc in npc_hit_list:
            # Moving right
            if self.x_change > 0:
                self.rect.right = npc.rect.left
            # Moving left
            else:
                self.rect.left = npc.rect.right        

        # Check if colliding game objects
        gameObject_hit_list = pg.sprite.spritecollide(self, player.currentGameObjects, False)
        for gameObject in gameObject_hit_list:
            # Moving right
            if self.x_change > 0:
                self.rect.right = gameObject.rect.left
            # Moving left
            else:
                self.rect.left = gameObject.rect.right

        # Move the NPC up/down
        self.rect.y += self.y_change

        # Check if it collides with walls
        block_hit_list = pg.sprite.spritecollide(self, player.sprites, False)
        for block in block_hit_list:
            # Moving down
            if self.y_change > 0:
                self.rect.bottom = block.rect.top
            # Moving up
            else:
                self.rect.top = block.rect.bottom

        npc_hit_list = pg.sprite.spritecollide(self, self.npcList, False)
        for npc in npc_hit_list:
            # Moving down
            if self.y_change > 0:
                self.rect.bottom = npc.rect.top

            # Moving up
            else:
                self.rect.top = npc.rect.bottom

        # Check if colliding game objects
        gameObject_hit_list = pg.sprite.spritecollide(self, player.currentGameObjects, False)
        for gameObject in gameObject_hit_list:
            # Moving down
            if self.y_change > 0:
                self.rect.bottom = gameObject.rect.top
            # Moving up
            else:
                self.rect.top = gameObject.rect.bottom

        # Misc
        self.y_change = 0
        self.x_change = 0

        # Check if NPC is actively targetting
        if self.aggravated:
            # Ensure that the NPC has a target
            if not self.target == None:
                self.combatBehaviour(ev)

        # Make NPC actively target if alignment is changed
        elif self.alignment == "Hostile":
            self.aggravated = True
            self.target = player 

        # Draw the NPC
        screen.blit(pg.transform.rotate((pg.transform.smoothscale(self.image, (50 * self.scale, 50 * self.scale))), self.angle + 270), (self.rect.x,self.rect.y))
    
    # Check for collisions
    def hit(self, damage, origin):
        self.health -= damage
        if origin == "Player":
            self.alignment = "Hostile"
            self.aggravated = True
            self.target = player
    
# # PLAYER CLASS # #
class Player(pg.sprite.Sprite):
    global playerSpeed, playerHealth, playerActionPoints, playerMaxAP, playerSkills, playerInventory, location_list, bodyparts
    # Init attributes
    def __init__(self, locationX, locationY):
        # Sprite init
        super().__init__()

        # Health properties
        self.health = playerHealth
        self.actionPoints = playerActionPoints
        self.maxAP = playerMaxAP
        self.APlossRate = 1
        self.APgainRate = 1
        self.APgainIterator = 200
        self.hunger = 100
        self.thirst = 100
        self.bodyparts = bodyparts
        self.inPain = False
        self.injuryCount = 0
        self.drugDoses = 0
        self.maxDrugs = 3
        self.infected = False
        self.healthEffects = []
        self.canSprint = True

        # Gameplay properties
        self.skills = playerSkills
        self.speed = playerSpeed
        self.sprintBonus = 6
        self.evasion = 0.4
        self.accuracy = 0.8
        self.inventory = playerInventory
        self.inventoryQuantity = 0
        self.maxWeight = 50
        self.currentWeight = 0
        self.scrapMetal = 0
        self.sprites = None
        self.npcList = None

        # Combat properties
        self.equipped_weapon = None
        self.neededAmmo = None
        self.weaponDamage = 10
        self.loaded_rounds = 12
        self.available_targets = []
        self.targetAwarenessActive = False

        # StatusUI INV
        self.highlightMoveable = True
        self.highlightedItem = 0
        self.highlight_y = 160

        self.invDropUIactive = False
        self.invDropUnable = False
        self.invUseUIactive = False
        self.invUseUnable = False

        self.medKitActive = False
        self.medHighlightMoveable = True
        self.medHighlightedItem = 0
        self.medHighlight_y = 60
        
        # TransferUI
        self.leftHighlightMoveable = True
        self.leftHighlightedItem = 0
        self.leftHighlight_y = 90

        self.rightHighlightMoveable = False
        self.rightHighlightedItem = 0
        self.rightHighlight_y = 90

        # Display & mesh properties
        self.default = pg.image.load(addressprefix + "\\misc\\player.png").convert_alpha()
        self.animationImages = []
        leftForward = pg.image.load(addressprefix + "\\misc\\player-leftForward.png").convert_alpha()
        self.animationImages.append(leftForward)
        rightForward = pg.image.load(addressprefix + "\\misc\\player-rightForward.png").convert_alpha()
        self.animationImages.append(rightForward)
        self.image = pg.transform.rotate((pg.transform.smoothscale(self.default, (50, 50))), 270)
        self.frameCounter = 0
        self.animationCounter = 0

        # Movement properties
        self.x_change = 0
        self.y_change = 0
        self.angle = 0
        self.rect = self.image.get_rect()
        self.rect.x = locationX
        self.rect.y = locationY
        self.currentGameObjects = []

        # Navigation properties
        self.location_list = location_list
        self.visited_list = []
        self.current_location = 0

        # Event log properties
        self.event_log = ["Press [TAB] to toggle your inventory."]
        self.latest_event = 0
        self.num_events = 0

        # Misc properties
        self.last = pg.time.get_ticks()
        self.uiActive = False
        self.muiActive = True
        self.tuiActive = False
        self.painOpacity = 50
        self.failureCause = " "

    # Check for player injuries and adjust variables
    def healthCheck(self, ev):
        # Draw red filter on screen when player is in pain
        if self.inPain == True:
            # Draw transparent background for UI
            painCover = pg.Surface((1500, 800)).convert_alpha()
            painCover.fill([255, 0, 0, self.painOpacity])

            screen.blit(painCover, (0, 0, 0, 0))
        
        # Remove HP when wounded, depending on injury level 
        if self.injuryCount == 1:
            self.painOpacity = 50
            for event in ev:
                if event.type == healthEvent:
                    self.health -= 1

        elif self.injuryCount == 3:
            self.painOpacity = 100
            for event in ev:
                if event.type == healthEvent:
                    self.health -= 2

        elif self.injuryCount == 5:
            self.painOpacity = 150
            for event in ev:
                if event.type == healthEvent:
                    self.health -= 5

        # Health failure conditions
        if self.health <= 0 and not self.infected:
            self.failureCause = "Severe Internal Bleeding"
            stageSys.stageTransition(4)
        if self.health <= 0 and self.infected:
            self.failureCause = "Severe Infection"
            stageSys.stageTransition(4)

        # Update maxDrugs depending on endurance skill
        if 0 < self.skills[5][2] <= 0.1:
            self.maxDrugs = 3
        elif 0.1 < self.skills[5][2] <= 0.2:
            self.maxDrugs = 4
        elif 0.2 < self.skills[5][2] <= 0.3:
            self.maxDrugs = 5
        elif 0.3 < self.skills[5][2] <= 0.4:
            self.maxDrugs = 6
        elif 0.4 < self.skills[5][2] <= 0.5:
            self.maxDrugs = 7

        # Handle player chem doses
        if self.drugDoses > self.maxDrugs:
            self.failureCause = "Chem Overdose"
            stageSys.stageTransition(4)

        # Handle infection damage
        if self.infected:
            for event in ev:
                if event.type == healthEvent:
                    self.event_log.append("Your infection spreads.")
                    self.health -= 5

        # # CHECK LIMBS # #
        # Check head st[atus
        if self.bodyparts[0][1] == "Injured" and self.bodyparts[0][2] == False:
            if 0.8 < self.accuracy <= 1.0:
                self.accuracy = 0.8
            elif 0.6 < self.accuracy <= 0.8:
                self.accuracy = 0.6
            elif 0.4 < self.accuracy <= 0.6:
                self.accuracy = 0.4
            elif 0.2 < self.accuracy <= 0.4:
                self.accuracy = 0.2
            elif self.accuracy <= 0.2:
                self.accuracy = 0.1
            self.bodyparts[0][2] = True
        elif self.bodyparts[0][1] == "Destroyed":
            self.failureCause = "Severe Head Injury"
            stageSys.stageTransition(4)

        # Check torso status
        if self.bodyparts[1][1] == "Injured" and self.bodyparts[1][2] == False:
            if 0.8 < self.evasion <= 1.0:
                self.evasion = 0.8
            elif 0.6 < self.evasion <= 0.8:
                self.evasion = 0.6
            elif 0.4 < self.evasion <= 0.6:
                self.evasion = 0.4
            elif 0.2 < self.evasion <= 0.4:
                self.evasion = 0.2
            elif self.evasion <= 0.2:
                self.evasion = 0.1
            self.bodyparts[1][2] = True
        elif self.bodyparts[1][1] == "Destroyed":
            self.failureCause = "Severe Chest Injury"
            stageSys.stageTransition(4)

        # Check left arm status
        if self.bodyparts[2][1] == "Injured" and self.bodyparts[2][2] == False:
            self.accuracy = self.accuracy // 2 + 0.2
            self.bodyparts[2][2] = True
        elif self.bodyparts[2][1] == "Destroyed":
            self.accuracy = self.accuracy / 2
        
        # Check right arm status
        if self.bodyparts[3][1] == "Injured" and self.bodyparts[3][2] == False:
            self.accuracy = self.accuracy // 2 + 0.2
            self.bodyparts[3][2] = True
        elif self.bodyparts[3][1] == "Destroyed":
            self.accuracy = self.accuracy / 2
            
        # Check left leg status
        if self.bodyparts[4][1] == "Injured" and self.bodyparts[4][2] == False:
            self.speed -= (self.speed // 2) - 1
            self.sprintBonus -= self.sprintBonus // 2
            self.bodyparts[4][2] = True
        elif self.bodyparts[4][1] == "Destroyed":
            self.speed = (self.speed // 2) + 1
            self.canSprint = False

        # Check right leg status
        if self.bodyparts[5][1] == "Injured" and self.bodyparts[5][2] == False:
            self.speed -= (self.speed // 2) - 1
            self.sprintBonus -= self.sprintBonus // 2
            self.bodyparts[5][2] = True
        elif self.bodyparts[5][1] == "Destroyed":
            self.speed = (self.speed // 2) + 1
            self.canSprint = False
    
    # Tracks number of level up points per skill & ranks up when appropriate
    def skillsLevelUp(self):
        # All skills use the same scale
        for i in range(0, len(self.skills)):
            if self.skills[i][3] == 2 and self.skills[i][2] == 0.1:
                self.skills[i][2] = 0.2
                self.event_log.append("You leveled up in "+self.skills[i][0]+" (LVL "+str(round(self.skills[i][2] * 10))+").")
            elif self.skills[i][3] == 5 and self.skills[i][2] == 0.2:
                self.skills[i][2] = 0.3
                self.event_log.append("You leveled up in "+self.skills[i][0]+" (LVL "+str(round(self.skills[i][2] * 10))+").")
            elif self.skills[i][3] == 10 and self.skills[i][2] == 0.3:
                self.skills[i][2] = 0.4
                self.event_log.append("You leveled up in "+self.skills[i][0]+" (LVL "+str(round(self.skills[i][2] * 10))+").")
            elif self.skills[i][3] == 20 and self.skills[i][2] == 0.4:
                self.skills[i][2] = 0.5
                self.event_log.append("You leveled up in "+self.skills[i][0]+" (LVL "+str(round(self.skills[i][2] * 10))+").")
                
    # Auto update stats (thirst, hunger) and skills
    def updateNeeds(self, ev):
        # Prevent needs from updating when game paused
        if not self.uiActive:
            for event in ev:
                # Handle hunger updates
                if event.type == hungerEvent:
                    self.hunger -= 10

                    # Warn the player of their needs
                    if 80 <= self.hunger < 100:
                        if self.event_log[-1] is not "You are peckish from not eating.":
                            self.event_log.append("You are peckish from not eating.")
                    elif 60 <= self.hunger < 80:
                        if self.event_log[-1] is not "You are hungry from not eating.":
                            self.event_log.append("You are hungry from not eating.")
                    elif 40 <= self.hunger < 60:
                        if self.event_log[-1] is not "You are extremely hungry from not eating.":
                            self.event_log.append("You are extremely hungry from not eating.")
                    elif 20 <= self.hunger < 40:
                        if self.event_log[-1] is not "You are starving from not eating.":
                            self.event_log.append("You are starving from not eating.")
                    elif self.hunger <= 0:
                        self.failureCause = "Severe Starvation"
                        stageSys.stageTransition(4)

                # Handle thirst updates
                if event.type == thirstEvent:
                    self.thirst -= 10

                    # Warn the player of their needs
                    if 80 <= self.thirst < 100:
                        if self.event_log[-1] is not "You are parched from not drinking.":
                            self.event_log.append("You are parched from not drinking.")
                    elif 60 <= self.thirst < 80:
                        if self.event_log[-1] is not "You are thirsty from not drinking.":
                            self.event_log.append("You are thirsty from not drinking.")
                    elif 40 <= self.thirst < 60:
                        if self.event_log[-1] is not "You are very thirsty from not drinking.":
                            self.event_log.append("You are very thirsty from not drinking.")
                    elif 20 <= self.thirst < 40:
                        if self.event_log[-1] is not "You are dehydrated from not drinking.":
                            self.event_log.append("You are dehydrated from not drinking.")
                    elif self.thirst <= 0:
                        self.failureCause = "Severe Dehydration"
                        stageSys.stageTransition(4)

            # Make sure hunger, health, & thirst can't surpass their max values
            if self.hunger > 100:
                self.hunger = 100
            if self.thirst > 100:
                self.thirst = 100
            if self.health > 100:
                self.health = 100

        # Set max carry weight according to strength skill level
        if self.skills[4][2] == 0.1:
            self.maxWeight = 10
        elif self.skills[4][2] == 0.2:
            self.maxWeight = 20
        elif self.skills[4][2] == 0.3:
            self.maxWeight = 30
        elif self.skills[4][2] == 0.4:
            self.maxWeight = 40
        elif self.skills[4][2] == 0.5:
            self.maxWeight = 50

        # Set APgainIterator according to endurance skill level
        if self.skills[5][2] == 0.1:
            self.APgainIterator = 500
        elif self.skills[5][2] == 0.2:
            self.APgainIterator == 400
        elif self.skills[5][2] == 0.3:
            self.APgainIterator == 300
        elif self.skills[5][2] == 0.4:
            self.APgainIterator == 200
        elif self.skills[5][2] == 0.5:
            self.APgainIterator == 100

    # Handle shooting
    def shooting(self, ev):
        for event in ev:
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                if self.loaded_rounds != 0:
                    gunShot.play()
                    projectiles.append(Projectile(round(self.rect.x + (self.rect.w // 2)), round(self.rect.y + (self.rect.h // 2)), 4, black, self.angle, self.weaponDamage, "Player"))
                    self.loaded_rounds -= 1
                else:
                    if self.event_log[-1] is not "Your clip runs out of bullets.":
                        self.event_log.append("Your clip runs out of bullets.")

            if event.type == pg.KEYUP and event.key == pg.K_r:
                if self.neededAmmo in self.inventory:
                    gunReload.play()
                    self.event_log.append("Reloaded with "+self.neededAmmo[0])
                    self.inventory.remove(self.neededAmmo)
                    self.loaded_rounds = 12
                else:
                    if self.event_log[-1] is not "You do not have ammo for that gun.":
                        self.event_log.append("You do not have ammo for that gun.")

        # Draw shooting UI background
        shootUI = pg.Surface((260, 70)).convert_alpha()
        shootUI.fill(black_transparent)

        # Display weapon, ammo type, and loaded rounds
        uiText.draw(shootUI, 10, 10, self.equipped_weapon+" ("+self.neededAmmo[0]+")", 18, white, 255, True)
        pg.draw.rect(shootUI, black, [10, 40, 240, 20])
        if self.loaded_rounds == 0:
            uiText.draw(shootUI, 12, 42, "[R] to reload", 14, white, 255, True)
        else:
            for i in range(0, self.loaded_rounds):
                pg.draw.rect(shootUI, white, [12 + (20 * i), 42, 16, 16])
        
        if not self.uiActive and not self.tuiActive:
            # Draw the shooting UI
            screen.blit(shootUI, (50, 50, 260, 70))

    # UI to transfer objects from a container to inventory
    def transferUI(self, ev, otherInv):
        # Draw UI
        transferUI = pg.Surface((600, 520)).convert_alpha()
        transferUI.fill(black_transparent)
        
        pg.draw.rect(transferUI, black, [10, 10, 580, 500])

        # # Left side (player inventory) # #
        uiText.draw(transferUI, 20, 20, "Your Inventory", 24, white, 255, True, True)
        pg.draw.rect(transferUI, white, [20, 60, 260, 380])
        
        # Draw the table to hold inventory in
        uiText.draw(transferUI, 27, 65, "NAME", 16, black, 255, False, True)
        pg.draw.line(transferUI, black, (130, 60), (130, 440), 5)
        uiText.draw(transferUI, 140, 65, "WEIGHT", 16, black, 255, False, True)
        pg.draw.line(transferUI, black, (210, 60), (210, 440), 5)
        uiText.draw(transferUI, 220, 65, "VALUE", 16, black, 255, False, True)
        pg.draw.line(transferUI, black, (20, 90), (540, 90), 5)

        # Fill inventory table with entries
        if len(self.inventory) >= 1 and len(self.inventory) < 18:
            for i in range(0, len(self.inventory)):
                # Item name & quantity
                uiText.draw(transferUI, 27, 95 + (20 * i), self.inventory[i][0], 14, black, 255)
                # Weight
                uiText.draw(transferUI, 140, 95 + (20 * i), str(self.inventory[i][2]), 14, black, 255)
                # Value
                uiText.draw(transferUI, 220, 95 + (20 * i), str(self.inventory[i][3]), 14, black, 255)

        # Size of the item highlight
        leftItemHighlight = pg.Surface((260, 20)).convert_alpha()
        leftItemHighlight.fill([0, 150, 0, 150])

        # Associate physical locations on the GUI with an index location
        if self.leftHighlightMoveable:
            for event in ev:
                # DOWN arrow movement
                if event.type == pg.KEYUP and event.key == pg.K_DOWN:
                    # Check if going off the table and reset
                    if self.leftHighlight_y > 470:
                        self.leftHighlight_y = 450
                        self.leftHighlightedItem = 17
                    # Move the highlight and index value
                    else:
                        if self.leftHighlightedItem + 2 > len(self.inventory):
                            pass
                        else:
                            self.leftHighlightedItem += 1
                            self.leftHighlight_y = 90 + (20 * self.leftHighlightedItem)
                # UP arrow movement
                if event.type == pg.KEYUP and event.key == pg.K_UP:
                    # Check if going off the table and reset
                    if self.leftHighlight_y < 110:
                        self.leftHighlight_y = 90
                        self.leftHighlightedItem = 0
                    # Move the highlight and index value
                    else:
                        self.leftHighlight_y -= 20
                        self.leftHighlightedItem -= 1

            # Blit the selected item highlight
            transferUI.blit(leftItemHighlight, [20, self.leftHighlight_y, 260, 20])

        
        # # Right side (container inventory) # #
        uiText.draw(transferUI, 310, 20, "Container", 24, white, 255, True, True)
        pg.draw.rect(transferUI, white, [310, 60, 260, 380])

         # Draw the table to hold inventory in
        uiText.draw(transferUI, 317, 65, "NAME", 16, black, 255, False, True)
        pg.draw.line(transferUI, black, (420, 60), (420, 440), 5)
        uiText.draw(transferUI, 430, 65, "WEIGHT", 16, black, 255, False, True)
        pg.draw.line(transferUI, black, (500, 60), (500, 440), 5)
        uiText.draw(transferUI, 512, 65, "VALUE", 16, black, 255, False, True)
        pg.draw.line(transferUI, black, (310, 90), (570, 90), 5)

        # Fill inventory table with entries
        if len(otherInv) >= 1 and len(otherInv) < 18:
            for i in range(0, len(otherInv)):
                # Item name & quantity
                uiText.draw(transferUI, 317, 95 + (20 * i), otherInv[i][0], 14, black, 255)
                # Weight
                uiText.draw(transferUI, 430, 95 + (20 * i), str(otherInv[i][2]), 14, black, 255)
                # Value
                uiText.draw(transferUI, 512, 95 + (20 * i), str(otherInv[i][3]), 14, black, 255)

        # Size of the item highlight
        rightItemHighlight = pg.Surface((260, 20)).convert_alpha()
        rightItemHighlight.fill([0, 150, 0, 150])

        # Associate physical locations on the GUI with an index location
        if self.rightHighlightMoveable:
            for event in ev:
                # DOWN arrow movement
                if event.type == pg.KEYUP and event.key == pg.K_DOWN:
                    # Check if going off the table and reset
                    if self.rightHighlight_y > 470:
                        self.rightHighlight_y = 450
                        self.rightHighlightedItem = 17
                    # Move the highlight and index value
                    else:
                        if self.rightHighlightedItem + 2 > len(otherInv):
                            pass
                        else:
                            self.rightHighlightedItem += 1
                            self.rightHighlight_y = 90 + (20 * self.rightHighlightedItem)
                # UP arrow movement
                if event.type == pg.KEYUP and event.key == pg.K_UP:
                    # Check if going off the table and reset
                    if self.rightHighlight_y < 110:
                        self.rightHighlight_y = 90
                        self.rightHighlightedItem = 0
                    # Move the highlight and index value
                    else:
                        self.rightHighlight_y -= 20
                        self.rightHighlightedItem -= 1

            # Blit the selected item highlight
            transferUI.blit(rightItemHighlight, [310, self.rightHighlight_y, 260, 20])

        # Switch between left & right UI
        for event in ev:
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    self.leftHighlightMoveable = True
                    self.rightHighlightMoveable = False
                if event.key == pg.K_RIGHT:
                    self.leftHighlightMoveable = False
                    self.rightHighlightMoveable = True

        # Exit button
        tuiExit.draw(transferUI, 20, 450, 260, 50, " TAB) Cancel", 14, black)
        if tuiExit.isActive(ev, pg.K_TAB):
            self.tuiActive = False

        # Move item button
        tuiMove.draw(transferUI, 310, 450, 260, 50, " X) Move Item", 14, black)
        if self.leftHighlightMoveable:
            if len(self.inventory) != 0:
                if tuiMove.isActive(ev, pg.K_x):
                    otherInv.append(self.inventory[self.leftHighlightedItem])
                    del self.inventory[self.leftHighlightedItem]
                    if self.leftHighlightedItem > 0:
                        self.leftHighlight_y -= 20
                        self.leftHighlightedItem -= 1

        elif self.rightHighlightMoveable:
            if len(otherInv) != 0:
                if tuiMove.isActive(ev, pg.K_x):
                    self.inventory.append(otherInv[self.rightHighlightedItem])
                    del otherInv[self.rightHighlightedItem]
                    if self.rightHighlightedItem > 0:
                        self.rightHighlight_y -= 20
                        self.rightHighlightedItem -= 1

        # Draw the transfer UI
        screen.blit(transferUI, (50, 50, 0, 0))

    # Draws and updates the main game UI
    def drawUI(self, ev):
        # Left UI
        pg.draw.rect(screen, black, (50, 700, 150, 50))
        uiText.draw(screen, 55, 705, "HEALTH " + str(self.health), 20, white, 255, True)
        uiText.draw(screen, 55, 725, "ACTION " + str(self.actionPoints), 20, white, 255, True)

        # Right UI
        pg.draw.rect(screen, black, (1300, 700, 150, 50))
        uiText.draw(screen, 1305, 705, "HUNGER " + str(self.hunger), 20, white, 255, True)
        uiText.draw(screen, 1305, 725, "THIRST " + str(self.thirst), 20, white, 255, True)

        # Regen AP over time when depleted (when UI closed)
        if not self.uiActive and not self.targetAwarenessActive:
            if self.actionPoints < self.maxAP: 
                now = pg.time.get_ticks()
                if now - self.last >= self.APgainIterator:
                    self.last = now
                    self.actionPoints += self.APgainRate

        # Enable shooting when weapon is equipped
        if self.equipped_weapon != None:
            self.shooting(ev)

        # Target awareness UI
        if self.targetAwarenessActive:
            # Draw transparent background
            targetCover = pg.Surface((1500, 800)).convert_alpha()
            targetCover.fill([0, 0, 0, 30])

            # Highlight map targets
            for target in self.available_targets:
                if target.alignment == "Friendly":
                    pg.draw.rect(targetCover, green, [target.rect.x, target.rect.y, target.rect.w, target.rect.h], 2)
                    uiText.draw(targetCover, target.rect.x, target.rect.y + target.rect.h, "FRIENDLY", 12, green, 200, True)
                    uiText.draw(targetCover, target.rect.x, target.rect.y + target.rect.h + 10, "HP "+str(target.health), 12, green, 200, True)
                elif target.alignment == "Neutral":
                    pg.draw.rect(targetCover, blue, [target.rect.x, target.rect.y, target.rect.w, target.rect.h], 2)
                    uiText.draw(targetCover, target.rect.x, target.rect.y + target.rect.h, "NEUTRAL", 12, blue, 200, True)
                    uiText.draw(targetCover, target.rect.x, target.rect.y + target.rect.h + 10, "HP "+str(target.health), 12, blue, 200, True)
                elif target.alignment == "Hostile":
                    pg.draw.rect(targetCover, red, [target.rect.x, target.rect.y, target.rect.w, target.rect.h], 2)
                    uiText.draw(targetCover, target.rect.x, target.rect.y + target.rect.h, "HOSTILE", 12, red, 200, True)
                    uiText.draw(targetCover, target.rect.x, target.rect.y + target.rect.h + 10, "HP "+str(target.health), 12, red, 200, True)
                   
            # Toggle enhanced targetting off
            for event in ev:
                if event.type == pg.KEYDOWN and event.key == pg.K_q:
                    self.targetAwarenessActive = False

            screen.blit(targetCover, (0, 0, 0, 0))
            for event in ev:
                if event.type == targetAwareEvent:
                    self.actionPoints -= self.APlossRate
            if self.actionPoints <= 0:
                self.actionPoints = 0
                self.targetAwarenessActive = False
        else:
            for event in ev:
                if event.type == pg.KEYDOWN and event.key == pg.K_q:
                    self.targetAwarenessActive = True

        # Handle weight changes
        if self.inventoryQuantity < len(self.inventory):
            self.currentWeight = 0
            self.inventoryQuantity = len(self.inventory)
            for i in range(0, len(self.inventory)):
                self.currentWeight += self.inventory[i][2]

        # Level up when appropriate
        self.skillsLevelUp()

        # Inventory and status menu
        if self.uiActive and not self.tuiActive:
            # Toggle UI off
            for event in ev:
                if event.type == pg.KEYDOWN and event.key == pg.K_TAB:
                    self.uiActive = False
                    self.muiActive = True

            # Draw transparent background for UI
            statUICover = pg.Surface((1500, 800)).convert_alpha()
            statUICover.fill([0, 0, 0, 130])
            uiText.draw(statUICover, 700, 20, "[PAUSED]", 24, white, 255, True)
            screen.blit(statUICover, (0, 0, 0, 0))

            # Draw transparent background for UI
            statusUI = pg.Surface((600, 600)).convert_alpha()
            statusUI.fill(black_transparent)

            # Top Bar
            pg.draw.rect(statusUI, red, [10, 10, 110, 60])
            pg.draw.rect(statusUI, black, [120, 10, 470, 60])
            uiText.draw(statusUI, 22, 28, "STATS", 24, white, 255, True, True)
            uiText.draw(statusUI, 140, 32, "SCRAP METAL "+str(self.scrapMetal), 20, white, 255, True, True)
            uiText.draw(statusUI, 380, 32, "MAX WEIGHT "+str(self.maxWeight), 20, white, 255, True, True)

            # # LEFT BAR # #
            pg.draw.rect(statusUI, black, [10, 80, 120, 510])
            uiText.draw(statusUI, 15, 85, "NAUPLIUS", 20, white, 255, True)
            uiText.draw(statusUI, 20, 105, "'The finest", 14, white, 255, True, True)
            uiText.draw(statusUI, 20, 120, "in mobile", 14, white, 255, True, True)
            uiText.draw(statusUI, 20, 135, "computing!'", 14, white, 255, True, True)
        
            # Draw buttons
            statUIlog.draw(statusUI, 20, 160, 100, 40, "[1]LOG", 10, black)
            statUIinv.draw(statusUI, 20, 220, 100, 40, "[2]INV", 10, black)
            statUIstat.draw(statusUI, 20, 280, 100, 40, "[3]STAT", 10, black)
            statUIskill.draw(statusUI, 20, 340, 100, 40, "[4]SKILL", 10, black)
            statUImap.draw(statusUI, 20, 400, 100, 40, "[5]MAP", 10, black)
            statUIhelp.draw(statusUI, 20, 460, 100, 40, "[6]HELP", 10, black)

            # Lore text
            uiText.draw(statusUI, 23, 575, "Made in U.F.", 12, white, 255, True)

            # # MAIN BODY # #
            pg.draw.rect(statusUI, black, [140, 80, 450, 510])

            # Trigger LOG screen
            if statUIlog.isActive(ev, pg.K_1):
                for i in range(0, len(statUIactive)):
                    statUIactive[i] = False
                statUIactive [0] = True

            # Trigger INV screen
            if statUIinv.isActive(ev, pg.K_2):
                for i in range(0, len(statUIactive)):
                    statUIactive[i] = False
                statUIactive [1] = True

            # Trigger STAT screen
            if statUIstat.isActive(ev, pg.K_3):
                for i in range(0, len(statUIactive)):
                    statUIactive[i] = False
                statUIactive [2] = True
            
            # Trigger SKILL screen
            if statUIskill.isActive(ev, pg.K_4):
                for i in range(0, len(statUIactive)):
                    statUIactive[i] = False
                statUIactive [3] = True

            # Trigger MAP screen
            if statUImap.isActive(ev, pg.K_5):
                for i in range(0, len(statUIactive)):
                    statUIactive[i] = False
                statUIactive [4] = True

            # Trigger HELP screen
            if statUIhelp.isActive(ev, pg.K_6):
                for i in range(0, len(statUIactive)):
                    statUIactive[i] = False
                statUIactive [5] = True

            # Draw LOG screen
            if statUIactive[0]:
                uiText.draw(statusUI, 150, 85, "LOG", 20, white, 255, True)
                uiText.draw(statusUI, 160, 107, "A log of your recent activities.", 14, white, 255, True)
                pg.draw.rect(statusUI, white, (150, 130, 430, 450))

                if len(self.event_log) < 1:
                    uiText.draw(statusUI, 160, 140, "No events logged yet.", 18, black, 255)
                elif len(self.event_log) >= 1:
                    for i in range(0, len(self.event_log)):
                        uiText.draw(statusUI, 160, 140 + (20 * i), self.event_log[-i - 1], 18, black, 255)

            # Draw INV screen
            elif statUIactive[1]:
                # Title and description
                uiText.draw(statusUI, 150, 85, "INV", 20, white, 255, True)
                uiText.draw(statusUI, 160, 107, "A list of the items you are carrying.", 14, white, 255, True)
                uiText.draw(statusUI, 420, 85, "WEIGHT:"+str(self.currentWeight)+"/"+str(self.maxWeight), 18, white, 255, True)
                pg.draw.rect(statusUI, white, (150, 130, 430, 450))

                # Draw the table to hold inventory in
                uiText.draw(statusUI, 177, 135, "NAME", 16, black, 255, False, True)
                pg.draw.line(statusUI, black, (250, 130), (250, 580), 5)
                uiText.draw(statusUI, 292, 135, "DESCRIPTION", 16, black, 255, False, True)
                pg.draw.line(statusUI, black, (450, 130), (450, 580), 5)
                uiText.draw(statusUI, 457, 135, "WEIGHT", 16, black, 255, False, True)
                pg.draw.line(statusUI, black, (525, 130), (525, 580), 5)
                uiText.draw(statusUI, 530, 135, "VALUE", 16, black, 255, False, True)
                pg.draw.line(statusUI, black, (150, 157), (580, 157), 5)

                # Fill inventory table with entries
                if len(self.inventory) >= 1 and len(self.inventory) < 18:
                    for i in range(0, len(self.inventory)):
                        # Item name & quantity
                        uiText.draw(statusUI, 155, 165 + (20 * i), self.inventory[i][0], 14, black, 255)
                        # Description
                        uiText.draw(statusUI, 255, 165 + (20 * i), self.inventory[i][1], 14, black, 255)
                        # Weight
                        uiText.draw(statusUI, 460, 165 + (20 * i), str(self.inventory[i][2]), 14, black, 255)
                        # Value
                        uiText.draw(statusUI, 535, 165 + (20 * i), str(self.inventory[i][3]), 14, black, 255)

                # Size of the item highlight
                itemHighlight = pg.Surface((430, 20)).convert_alpha()
                itemHighlight.fill([0, 150, 0, 150])

                # Associate physical locations on the inv GUI with an index location
                if self.highlightMoveable:
                    for event in ev:
                        # DOWN arrow movement
                        if event.type == pg.KEYUP and event.key == pg.K_DOWN:
                            # Check if going off the table and reset
                            if self.highlight_y > 480:
                                self.highlight_y = 500
                                self.highlightedItem = 17
                            # Move the highlight and index value
                            else:
                                if self.highlightedItem + 2 > len(self.inventory):
                                    pass
                                else:
                                    self.highlightedItem += 1
                                    self.highlight_y = 160 + (20 * self.highlightedItem)
                        # UP arrow movement
                        if event.type == pg.KEYUP and event.key == pg.K_UP:
                            # Check if going off the table and reset
                            if self.highlight_y < 180:
                                self.highlight_y = 160
                                self.highlightedItem = 0
                            # Move the highlight and index value
                            else:
                                self.highlight_y -= 20
                                self.highlightedItem -= 1

                # Blit the selected item highlight
                statusUI.blit(itemHighlight, [150, self.highlight_y, 430, 20])

                # Bottom bar
                pg.draw.rect(statusUI, black, [150, 520, 430, 60])
                statUIinvDrop.draw(statusUI, 150, 530, 210, 50, " X) Drop Item", 14, black)
                statUIinvUse.draw(statusUI, 370, 530, 210, 50, " C) Use Item", 14, black)

                # Make item drop confirmation active
                if self.highlightMoveable:
                    if statUIinvDrop.isActive(ev, pg.K_x):
                        if self.inventory[self.highlightedItem][5]:
                            self.highlightMoveable = False
                            self.invDropUIactive = True
                        else:
                            self.highlightMoveable = False
                            self.invDropUnable = True

                # Make item use confirmation active
                if self.highlightMoveable:
                    if statUIinvUse.isActive(ev, pg.K_c):
                        if self.inventory[self.highlightedItem][4]:
                            self.highlightMoveable = False
                            self.invUseUIactive = True
                        else:
                            self.highlightMoveable = False
                            self.invUseUnable = True
                
                # Display item drop confirmation
                if self.invDropUIactive:
                    # Draw background
                    invDropUI = pg.Surface((300, 100)).convert_alpha()
                    invDropUI.fill(black_transparent)
                    pg.draw.rect(invDropUI, black, [10, 10, 280, 80])

                    # Draw text & buttons
                    uiText.draw(invDropUI, 20, 15, "Drop "+self.inventory[self.highlightedItem][0]+"?", 16, white, 255, True)
                    invDropAgree.draw(invDropUI, 20, 40, 125, 40, "E) Yes", 16, black)
                    invDropDisagree.draw(invDropUI, 155, 40, 125, 40, "Esc) No", 16, black)

                    # Delete item at index location
                    if invDropAgree.isActive(ev, pg.K_e):
                        self.currentWeight -= self.inventory[self.highlightedItem][2]
                        del self.inventory[self.highlightedItem]
                        self.highlightMoveable = True
                        self.invDropUIactive = False

                    # Return to INV
                    elif invDropDisagree.isActive(ev, pg.K_ESCAPE):
                        self.highlightMoveable = True
                        self.invDropUIactive = False

                    # Blit item drop confirmation UI (change 670 to 600 for center)
                    screen.blit(invDropUI, [670, 300, 0, 0])

                # Draw unable to drop UI
                if self.invDropUnable:
                    # Draw background
                    invUndropableUI = pg.Surface((300, 100)).convert_alpha()
                    invUndropableUI.fill(black_transparent)
                    pg.draw.rect(invUndropableUI, black, [10, 10, 280, 80])

                    # Draw text & buttons
                    uiText.draw(invUndropableUI, 20, 15, "You can't drop "+self.inventory[self.highlightedItem][0]+".", 14, white, 255, True)
                    invUndropable.draw(invUndropableUI, 20, 40, 260, 40, "E) Continue", 16, black)

                    # Handle the Continue button
                    if invUnusable.isActive(ev, pg.K_e):
                        self.invDropUnable = False
                        self.highlightMoveable = True

                    # Draw the UI
                    screen.blit(invUndropableUI, [670, 300, 0, 0])

                # Display item use confirmation
                if self.invUseUIactive:
                    # Draw background
                    invUseUI = pg.Surface((300, 100)).convert_alpha()
                    invUseUI.fill(black_transparent)
                    pg.draw.rect(invUseUI, black, [10, 10, 280, 180])

                    # Draw text & buttons
                    uiText.draw(invUseUI, 20, 15, "Use "+self.inventory[self.highlightedItem][0]+"?", 16, white, 255, True)
                    invUseAgree.draw(invUseUI, 20, 40, 125, 40, "E) Yes", 16, black)
                    invUseDisagree.draw(invUseUI, 155, 40, 125, 40, "Esc) No", 16, black)

                    # Handle using an item
                    if invUseAgree.isActive(ev, pg.K_e):
                        if self.inventory[self.highlightedItem][0] == "Med Kit":
                            if self.injuryCount > 0:
                                self.medKitActive = True
                                # Remove used item from inventory
                                del self.inventory[self.highlightedItem]
                            else:
                                self.event_log.append("You aren't injured.")
                                self.muiActive = True
                            

                        elif self.inventory[self.highlightedItem][0] == "Antibiotics":
                            if self.infected:
                                self.infected = False
                                self.event_log.append("Your infection is cured.")
                            else:
                                self.event_log.append("You take a dose of antibiotics.")
                            self.thirst -= 10
                            self.hunger -= 10             

                            # Remove used item from inventory
                            del self.inventory[self.highlightedItem]

                        elif self.inventory[self.highlightedItem][0] == "Bandage":
                            if self.health < 100:
                                self.health += 30
                            if self.injuryCount > 0:
                                self.injuryCount -= 2
                                if self.injuryCount <= 0:
                                    self.injuryCount = 1
                                    
                            # Remove used item from inventory
                            del self.inventory[self.highlightedItem]

                        elif self.inventory[self.highlightedItem][0] == "Painkillers":
                            self.event_log.append("You take a dose of Painkillers.")
                            if self.inPain:
                                self.inPain = False
                            self.thirst -= 10

                            # Remove used item from inventory
                            del self.inventory[self.highlightedItem]

                        elif self.inventory[self.highlightedItem][0] == "Clean Water":
                            self.event_log.append("You take a drink of water.")
                            self.thirst += 15

                            # Remove used item from inventory
                            del self.inventory[self.highlightedItem]

                        elif self.inventory[self.highlightedItem][0] == "Dirty Water":
                            self.event_log.append("You get an infection from Dirty Water.")
                            self.thirst += 10
                            if not self.infected:
                                self.infected = True

                            # Remove used item from inventory
                            del self.inventory[self.highlightedItem]

                        elif self.inventory[self.highlightedItem][0] == "Can of Spam":
                            self.event_log.append("You eat some food.")
                            self.hunger += 15
                            self.health += 10

                            # Remove used item from inventory
                            del self.inventory[self.highlightedItem]
                        
                        elif self.inventory[self.highlightedItem][0] == "Military MRE":
                            self.event_log.append("You eat some food.")
                            self.hunger += 15
                            self.health += 10

                            # Remove used item from inventory
                            del self.inventory[self.highlightedItem]
                        
                        elif self.inventory[self.highlightedItem][0] == "Cooked Meat":
                            self.event_log.append("You eat some food.")
                            self.hunger += 10

                            # Remove used item from inventory
                            del self.inventory[self.highlightedItem]
                            
                        elif self.inventory[self.highlightedItem][0] == "Old Candy Bar":
                            self.event_log.append("You get an infection from Old Candy Bar.")
                            self.hunger += 10
                            if not self.infected:
                                self.infected = True

                            # Remove used item from inventory
                            del self.inventory[self.highlightedItem]

                        elif self.inventory[self.highlightedItem][0] == "Raw Meat":
                            self.event_log.append("You get an infection from Raw Meat.")
                            self.hunger += 10
                            if not self.infected:
                                self.infected = True

                            # Remove used item from inventory
                            del self.inventory[self.highlightedItem]

                        elif self.inventory[self.highlightedItem][0] == "Nitro":
                            self.event_log.append("You take a dose of Nitro.")
                            self.thirst -= 10
                            self.drugDoses += 1
                            chemUsed = ["Nitro", "Increases AP refresh"]
                            self.healthEffects.append(chemUsed)
                            self.APgainRate = self.APgainRate + 3

                            # Remove used item from inventory
                            del self.inventory[self.highlightedItem]

                        elif self.inventory[self.highlightedItem][0] == "Grittle":
                            self.event_log.append("You take a dose of Grittle.")
                            self.thirst -= 10
                            self.drugDoses += 1
                            chemUsed = ["Grittle", "Increases max AP"]
                            self.healthEffects.append(chemUsed)
                            self.maxAP = self.maxAP + 50

                            # Remove used item from inventory
                            del self.inventory[self.highlightedItem]

                        elif self.inventory[self.highlightedItem][0] == "Bulkup":
                            self.event_log.append("You take a dose of Bulkup.")
                            self.thirst -= 10
                            self.drugDoses += 1
                            chemUsed = ["Bulkup", "Increases max weight"]
                            self.healthEffects.append(chemUsed)
                            self.maxWeight += 10

                            # Remove used item from inventory
                            del self.inventory[self.highlightedItem]

                        elif self.inventory[self.highlightedItem][0] == "Speed":
                            self.event_log.append("You take a dose of Speed.")
                            self.thirst -= 10
                            self.drugDoses += 1
                            chemUsed = ["Speed", "Increases max speed"]
                            self.healthEffects.append(chemUsed)
                            self.speed += 2

                            # Remove used item from inventory
                            del self.inventory[self.highlightedItem]

                        elif self.inventory[self.highlightedItem][0] == "Pistol":
                            if self.equipped_weapon != None:
                                self.event_log.append("You put away your "+self.equipped_weapon+".")
                                self.muiActive = True
                                self.equipped_weapon = None
                                self.neededAmmo = None
                                self.inventory[self.highlightedItem][5] = True
                            else:
                                self.event_log.append("You ready your hand gun.")
                                self.muiActive = True
                                self.equipped_weapon = "Pistol"
                                self.neededAmmo = item_list[17]
                                self.weaponDamage = 10
                                self.inventory[self.highlightedItem][5] = False

                        elif self.inventory[self.highlightedItem][0] == "Rifle":
                            if self.equipped_weapon != None:
                                self.event_log.append("You put away your "+self.equipped_weapon+".")
                                self.muiActive = True
                                self.equipped_weapon = None
                                self.neededAmmo = None
                                self.inventory[self.highlightedItem][5] = True
                            else:
                                self.event_log.append("You ready your rifle.")
                                self.muiActive = True
                                self.equipped_weapon = "Rifle"
                                self.neededAmmo = item_list[19]
                                self.weaponDamage = 15
                                self.inventory[self.highlightedItem][5] = False

                        elif self.inventory[self.highlightedItem][0] == "Carbine":
                            if self.equipped_weapon != None:
                                self.event_log.append("You put away your "+self.equipped_weapon+".")
                                self.muiActive = True
                                self.equipped_weapon = None
                                self.neededAmmo = None
                                self.inventory[self.highlightedItem][5] = True
                            else:
                                self.event_log.append("You ready your carbine.")
                                self.muiActive = True
                                self.equipped_weapon = "Carbine"
                                self.neededAmmo = item_list[18]
                                self.weaponDamage = 25
                                self.inventory[self.highlightedItem][5] = False

                        # Return to previous menu
                        self.highlightMoveable = True
                        self.invUseUIactive = False
                    
                    # Don't use an item
                    elif invUseDisagree.isActive(ev, pg.K_ESCAPE):
                        self.highlightMoveable = True
                        self.invUseUIactive = False

                    # Draw the menu
                    screen.blit(invUseUI, [670, 300, 0, 0])

                # Display med kit UI
                if self.medKitActive:
                    self.highlightMoveable = False
                    # Draw background
                    medKitUI = pg.Surface((300, 250)).convert_alpha()
                    medKitUI.fill(black_transparent)
                    pg.draw.rect(medKitUI, black, [10, 10, 280, 230])
                    pg.draw.rect(medKitUI, white, [20, 60, 260, 120])
                    uiText.draw(medKitUI, 20, 20, "SELECT A LIMB:", 18, white, 255)

                    # Print limb names and states
                    for i in range(0, len(self.bodyparts)):
                        uiText.draw(medKitUI, 25, 65 + (20 * i), self.bodyparts[i][0]+" - "+self.bodyparts[i][1], 14, black, 255)

                    # Size of med highlight
                    medHighlight = pg.Surface((260, 20)).convert_alpha()
                    medHighlight.fill([0, 150, 0, 150])

                    # Associate locations on the table with an index location
                    if self.medHighlightMoveable:
                        for event in ev:
                            if event.type == pg.KEYUP and event.key == pg.K_DOWN:
                                # Check if going off table
                                if self.medHighlight_y > 160:
                                    self.medHighlight_y = 160
                                    self.medHighlightedItem = 5
                                # Move highlight and index locations
                                else:
                                    if self.medHighlightedItem + 2 > len(self.bodyparts):
                                        pass
                                    else:
                                        self.medHighlight_y += 20
                                        self.medHighlightedItem += 1
                            elif event.type == pg.KEYUP and event.key == pg.K_UP:
                                # Check if going off table
                                if self.medHighlight_y < 80:
                                    self.medHighlight_y = 60
                                    self.medHighlightedItem = 0
                                # Move highlight and index locations
                                else:
                                    self.medHighlight_y -= 20
                                    self.medHighlightedItem -= 1

                    # Draw the highlight
                    medKitUI.blit(medHighlight, [20, self.medHighlight_y, 430, 20])

                    # Handle buttons
                    medKitHeal.draw(medKitUI, 20, 190, 120, 40, "X) Heal", 16, black)
                    if medKitHeal.isActive(ev, pg.K_x):
                        if self.bodyparts[self.medHighlightedItem][1] == "Healthy":
                            self.event_log.append("That limb is already healthy.")
                            self.muiActive = True
                        elif self.bodyparts[self.medHighlightedItem][1] == "Destroyed":
                            self.event_log.append("That limb has been destroyed.")
                            self.muiActive = True
                        else:
                            if random.randint(0, (5 - (self.skills[1][2] * 10))) == 0:
                                self.bodyparts[self.medHighlightedItem][1] = "Healthy"
                                self.event_log.append("You healed your "+self.bodyparts[self.medHighlightedItem][0])
                                self.muiActive = True
                                if self.health < 90:
                                    self.health = 90
                                if self.inPain:
                                    self.inPain = False
                                if self.injuryCount > 0:
                                    self.injuryCount -= 1
                                self.skills[1][3] += 1
                                self.highlightMoveable = True
                                self.medKitActive = False
                            else:
                                self.event_log.append("You failed to treat your "+self.bodyparts[self.medHighlightedItem][0])
                                self.muiActive = True
                                if self.health < 60:
                                    self.health = 60
                                if self.inPain:
                                    self.inPain = False
                                self.highlightMoveable = True
                                self.medKitActive = False
                            
                    medKitCancel.draw(medKitUI, 150, 190, 120, 40, "C) Cancel", 16, black)
                    if medKitCancel.isActive(ev, pg.K_c):
                        self.inventory.append(item_list[0])
                        self.highlightMoveable = True
                        self.medKitActive = False
                        
                    # Draw the medkit UI
                    screen.blit(medKitUI, [670, 300, 0, 0])

                # Display unable to use UI
                if self.invUseUnable:
                    # Draw background
                    invUnusableUI = pg.Surface((300, 100)).convert_alpha()
                    invUnusableUI.fill(black_transparent)
                    pg.draw.rect(invUnusableUI, black, [10, 10, 280, 80])

                    # Draw text & buttons
                    uiText.draw(invUnusableUI, 20, 15, "You can't use "+self.inventory[self.highlightedItem][0]+".", 14, white, 255, True)
                    invUnusable.draw(invUnusableUI, 20, 40, 260, 40, "E) Continue", 16, black)

                    # Handle the Continue button
                    if invUnusable.isActive(ev, pg.K_e):
                        self.invUseUnable = False
                        self.highlightMoveable = True

                    # Draw the UI
                    screen.blit(invUnusableUI, [670, 300, 0, 0])
                    
            # Draw STAT screen
            elif statUIactive[2]:
                # Title and description
                uiText.draw(statusUI, 150, 85, "STAT", 20, white, 255, True)
                uiText.draw(statusUI, 160, 107, "A summary of your health.", 14, white, 255, True)
                pg.draw.rect(statusUI, white, (150, 130, 430, 450))

                # Limb status
                uiText.draw(statusUI, 155, 135, "LIMBS", 20, black, 255)
                pg.draw.line(statusUI, black, [150, 160], [580, 160], 5)

                for i in range(0, len(self.bodyparts)):
                    uiText.draw(statusUI, 160, 165 + (25 * i), self.bodyparts[i][0], 18, black, 255)
                    pg.draw.line(statusUI, black, [150, 185 + (25 * i)], [580, 185 + (25 * i)], 2)
                    if self.bodyparts[i][1] == "Healthy":
                        uiText.draw(statusUI, 310, 165 + (25 * i), self.bodyparts[i][1], 18, darker_green, 255)
                    elif self.bodyparts[i][1] == "Injured":
                        uiText.draw(statusUI, 310, 165 + (25 * i), self.bodyparts[i][1], 18, darker_red, 255)
                    elif self.bodyparts[i][1] == "Destroyed":
                        uiText.draw(statusUI, 310, 165 + (25 * i), self.bodyparts[i][1], 18, black, 255)

                # Seperator (limb column and state column)
                pg.draw.line(statusUI, black, [300, 160], [300, 310], 5)

                # Seperator (limb section and effects section)
                pg.draw.rect(statusUI, black, [150, 310, 430, 30])
                
                # Health effects
                uiText.draw(statusUI, 155, 345, "EFFECTS", 20, black, 255)
                pg.draw.line(statusUI, black, [150, 370], [580, 370], 5)

                # Automatically append some effects when active
                if self.inPain:
                    if ["In pain", "Lowers visibility"] not in self.healthEffects:
                        healthEffect = ["In pain", "Lowers visibility"]
                        self.healthEffects.append(healthEffect)
                elif not self.inPain:
                    if ["In pain", "Lowers visibility"] in self.healthEffects:
                        self.healthEffects.remove(["In pain", "Lowers visibility"])
                if self.infected:
                    if ["Infected", "Periodically lose HP"] not in self.healthEffects:
                        healthEffect = ["Infected", "Periodically lose HP"]
                        self.healthEffects.append(healthEffect)
                elif not self.infected:
                    if ["Infected", "Periodically lose HP"] in self.healthEffects:
                        self.healthEffects.remove(["Infected", "Periodically lose HP"])
                if len(self.healthEffects) == 0:
                    uiText.draw(statusUI, 160, 375, "No health effects", 18, black, 255)
                else:
                    # Print list
                    for i in range(0, len(self.healthEffects)):
                        uiText.draw(statusUI, 160, 375 + (20 * i), "*"+self.healthEffects[i][0]+" - "+self.healthEffects[i][1], 18, black, 255)

            # Draw SKILL screen
            elif statUIactive[3]:
                # Title and description
                uiText.draw(statusUI, 150, 85, "SKILL", 20, white, 255, True)
                uiText.draw(statusUI, 160, 107, "Available skills and abilities.", 14, white, 255, True)
                pg.draw.rect(statusUI, white, (150, 130, 430, 450))

                for i in range(0, len(self.skills)):
                    uiText.draw(statusUI, 160, 135 + (60 * i), self.skills[i][0]+" - "+self.skills[i][1], 16, black, 255)
                    uiText.draw(statusUI, 160, 160 + (60 * i), "LVL "+str(round(self.skills[i][2] * 10)), 16, black, 255)
                    pg.draw.line(statusUI, black, [150, 185 + (60 * i)], [580, 185 + (60 * i)], 5)

            # Draw MAP screen
            elif statUIactive[4]:
                # Top bar
                uiText.draw(statusUI, 150, 85, "MAP", 20, white, 255, True)
                pg.draw.rect(statusUI, white, (150, 110, 430, 470))

                # Draw map & indicators
                statusUI.blit(pg.transform.smoothscale(fullMapImg, (410, 260)), (160, 120))
                uiText.draw(statusUI, 162, 122, "1", 12, black, 255)
                uiText.draw(statusUI, 298, 122, "2", 12, black, 255)
                uiText.draw(statusUI, 436, 122, "3", 12, black, 255)
                uiText.draw(statusUI, 162, 206, "4", 12, black, 255)
                uiText.draw(statusUI, 298, 206, "5", 12, black, 255)
                uiText.draw(statusUI, 436, 206, "6", 12, black, 255)
                uiText.draw(statusUI, 162, 293, "7", 12, black, 255)
                uiText.draw(statusUI, 298, 293, "8", 12, black, 255)
                uiText.draw(statusUI, 436, 293, "9", 12, black, 255)

                # "You are here" marker
                if self.current_location == 0:
                    uiText.draw(statusUI, 215, 235, "X", 28, black, 255, True)
                elif self.current_location == 1:
                    uiText.draw(statusUI, 215, 150, "X", 28, black, 255, True)
                elif self.current_location == 2:
                    uiText.draw(statusUI, 215, 325, "X", 28, black, 255, True)
                elif self.current_location == 3:
                    uiText.draw(statusUI, 350, 235, "X", 28, black, 255, True)
                elif self.current_location == 4:
                    uiText.draw(statusUI, 350, 150, "X", 28, black, 255, True)
                elif self.current_location == 5:
                    uiText.draw(statusUI, 350, 325, "X", 28, black, 255, True)
                elif self.current_location == 6:
                    uiText.draw(statusUI, 490, 150, "X", 28, black, 255, True)
                elif self.current_location == 7:
                    uiText.draw(statusUI, 490, 235, "X", 28, black, 255, True)
                elif self.current_location == 8:
                    uiText.draw(statusUI, 490, 325, "X", 28, black, 255, True)

                # Legend
                uiText.draw(statusUI, 165, 380, "X - Current location", 16, black, 255)
                uiText.draw(statusUI, 165, 400, "1 - "+location_list[1][0], 16, black, 255)
                uiText.draw(statusUI, 165, 420, "2 - "+location_list[4][0], 16, black, 255)
                uiText.draw(statusUI, 165, 440, "3 - "+location_list[6][0], 16, black, 255)
                uiText.draw(statusUI, 165, 460, "4 - "+location_list[0][0], 16, black, 255)
                uiText.draw(statusUI, 165, 480, "5 - "+location_list[3][0], 16, black, 255)
                uiText.draw(statusUI, 165, 500, "6 - "+location_list[7][0], 16, black, 255)
                uiText.draw(statusUI, 165, 520, "7 - "+location_list[2][0], 16, black, 255)
                uiText.draw(statusUI, 165, 540, "8 - "+location_list[5][0], 16, black, 255)
                uiText.draw(statusUI, 165, 560, "9 - "+location_list[8][0], 16, black, 255)

            # Draw HELP screen
            elif statUIactive[5]:
                # Title and description
                uiText.draw(statusUI, 150, 85, "HELP", 20, white, 255, True)
                uiText.draw(statusUI, 160, 107, "NAUPLIUS Mobile Computing Unit v2.1 rev. A", 14, white, 255, True)
                pg.draw.rect(statusUI, white, (150, 130, 430, 450))

                # Body (gameplay)
                uiText.draw(statusUI, 155, 135, "GAMEPLAY", 18, black, 255)
                uiText.draw(statusUI, 165, 165, "Your main goal is to survive and build up your character", 12, black, 255)
                uiText.draw(statusUI, 165, 185, "until you are strong enough to deal with the hostile A.I.", 12, black, 255)
                uiText.draw(statusUI, 165, 205, "east of the Military Compound. You can level up your skills", 12, black, 255)
                uiText.draw(statusUI, 165, 225, "simply by using them more often, and you can find useful", 12, black, 255)
                uiText.draw(statusUI, 165, 245, "items in crates scattered around the wasteland.", 12, black, 255)

                # Body (lore)
                uiText.draw(statusUI, 155, 290, "NAUPLIUS", 18, black, 255)
                uiText.draw(statusUI, 165, 320, "Named after the Greek figure known for being able to", 12, black, 255)
                uiText.draw(statusUI, 165, 340, "navigate using the stars during daylight, the NAUPLIUS", 12, black, 255)
                uiText.draw(statusUI, 165, 360, "Mobile Computer developed by the U.F. Armed Forces is ", 12, black, 255)
                uiText.draw(statusUI, 165, 380, "your ideal personal management solution. Included with", 12, black, 255)
                uiText.draw(statusUI, 165, 400, "the manager is an advanced Target Awareness System (Q)", 12, black, 255)
                uiText.draw(statusUI, 165, 420, "that allows the user to highlight all visible potential", 12, black, 255)
                uiText.draw(statusUI, 165, 440, "hostile encounters.", 12, black, 255)
           
           
            # Blit the UI on screen
            screen.blit(statusUI, (50, 50, 100, 100))

        # Toggle the UI on            
        else:
            if not self.tuiActive:
                for event in ev:
                    if event.type == pg.KEYDOWN and event.key == pg.K_TAB:
                        self.uiActive = True
                        self.muiActive = False

    # Display most recent log message
    def updateMiniLog(self, ev):
        # Toggle minilog UI
        for event in ev:
            if event.type == pg.KEYUP and event.key == pg.K_z:
                if self.muiActive == True:
                    self.muiActive = False
                elif self.muiActive == False:
                    self.muiActive = True

        # Draw UI background
        miniUI = pg.Surface((350, 50)).convert_alpha()
        miniUI.fill(black_transparent)

        # Check if there are events to show
        if len(self.event_log) < 1:
            uiText.draw(miniUI, 10, 17, "Press [Z] to toggle this menu.", 14, white, 255, True, False)
        elif len(self.event_log) >= 1:
            self.latest_event = self.event_log[-1]
            uiText.draw(miniUI, 10, 17, self.latest_event, 14, white, 255, True)
        
        # Blit the mini log to screen
        if self.muiActive:
            screen.blit(miniUI, (1100, 50, 350, 50))

    # Update the player's location (on the world map)
    def updateLocation(self, dirDepart):
        # Update based on northern departure
        if dirDepart == "North":
            next_location = location_list[self.current_location][1]
            if next_location == None:
                if "You can't go that way." is not self.event_log[-1]:
                    self.event_log.append("You can't go that way.")
                self.muiActive = True
            else:
                self.visited_list.append(self.current_location)
                self.current_location = next_location
                self.rect.bottom = 780
                self.event_log.append("You have entered "+str(location_list[self.current_location][0]+"."))
                projectiles.clear()
                hostileprojectiles.clear()
                self.sprites = None
                self.currentGameObjects = []
                if self.currentWeight > self.maxWeight:
                    self.skills[4][3] += 1
                if self.current_location not in self.visited_list:
                    uiText.fadeActive = True

        # Update based on eastern departure
        elif dirDepart == "East":
            next_location = location_list[self.current_location][2]
            if next_location == None:
                if "You can't go that way." is not self.event_log[-1]:
                    self.event_log.append("You can't go that way.")
                self.muiActive = True
            else:
                self.visited_list.append(self.current_location)
                self.current_location = next_location
                self.rect.left = 20
                self.event_log.append("You have entered "+str(location_list[self.current_location][0]+"."))
                projectiles.clear()
                hostileprojectiles.clear()
                self.sprites = None
                self.currentGameObjects = []
                if self.currentWeight > self.maxWeight:
                    self.skills[4][3] += 1
                if self.current_location not in self.visited_list:
                    uiText.fadeActive = True
        
        # Update based on southern departure
        elif dirDepart == "South":
            next_location = location_list[self.current_location][3]
            if next_location == None:
                if "You can't go that way." is not self.event_log[-1]:
                    self.event_log.append("You can't go that way.")
                self.muiActive = True
            else:
                self.visited_list.append(self.current_location)
                self.current_location = next_location
                self.rect.top = 20
                self.event_log.append("You have entered "+str(location_list[self.current_location][0]+"."))
                projectiles.clear()
                hostileprojectiles.clear()
                self.sprites = None
                self.currentGameObjects = []
                if self.currentWeight > self.maxWeight:
                    self.skills[4][3] += 1
                if self.current_location not in self.visited_list:
                    uiText.fadeActive = True

        # Update based on western departure
        elif dirDepart == "West":
            next_location = location_list[self.current_location][4]
            if next_location == None:
                if "You can't go that way." is not self.event_log[-1]:
                    self.event_log.append("You can't go that way.")
                self.muiActive = True
            else:
                self.visited_list.append(self.current_location)
                self.current_location = next_location
                self.rect.right = 1458
                self.event_log.append("You have entered "+str(location_list[self.current_location][0]+"."))
                projectiles.clear()
                hostileprojectiles.clear()
                self.sprites = None
                self.currentGameObjects = []
                if self.currentWeight > self.maxWeight:
                    self.skills[4][3] += 1
                if self.current_location not in self.visited_list:
                    uiText.fadeActive = True

    # Handle projectile collisions
    def combatHit(self, damage, origin):
        # Bullet has a chance to hit depending on evasion skill
        if random.randint(0, self.skills[3][2] * 10) == 0:
            randomLimb = random.randint(0, (len(self.bodyparts) - 1))
            self.health -= damage
            # Injure head
            if randomLimb == 0:
                if self.bodyparts[0][1] == "Healthy":
                    self.event_log.append("A bullet has injured your Head.")
                    self.injuryCount += 1
                    if not self.inPain:
                        self.inPain = True
                    self.bodyparts[0][1] = "Injured"
                elif self.bodyparts[0][1] == "Injured":
                    self.bodyparts[0][1] = "Destroyed"

            # Injure torso
            elif randomLimb == 1:
                if self.bodyparts[1][1] == "Healthy":
                    self.event_log.append("A bullet has injured your Torso.")
                    self.injuryCount += 1
                    if not self.inPain:
                        self.inPain = True
                    self.bodyparts[1][1] = "Injured"
                elif self.bodyparts[1][1] == "Injured":
                    self.bodyparts[1][1] = "Destroyed"

            # Injure left arm
            elif randomLimb == 2:
                if self.bodyparts[2][1] == "Healthy":
                    self.event_log.append("A bullet has injured your Left Arm.")
                    self.injuryCount += 1
                    self.bodyparts[2][1] = "Injured"
                elif self.bodyparts[2][1] == "Injured":
                    self.event_log.append("A bullet has destroyed your Left Arm.")
                    if not self.inPain:
                        self.inPain = True
                    self.bodyparts[2][1] = "Destroyed"

            # Injure right arm
            elif randomLimb == 3:
                if self.bodyparts[3][1] == "Healthy":
                    self.event_log.append("A bullet has injured your Right Arm.")
                    self.injuryCount += 1
                    self.bodyparts[3][1] = "Injured"
                elif self.bodyparts[3][1] == "Injured":
                    self.event_log.append("A bullet has destroyed your Right Arm.")
                    if not self.inPain:
                        self.inPain = True
                    self.bodyparts[3][1] = "Destroyed"

            # Injure left leg
            elif randomLimb == 4:
                if self.bodyparts[4][1] == "Healthy":
                    self.event_log.append("A bullet has injured your Left Leg.")
                    self.injuryCount += 1
                    self.bodyparts[4][1] = "Injured"
                elif self.bodyparts[4][1] == "Injured":
                    self.event_log.append("A bullet has destroyed your Left Leg.")
                    if not self.inPain:
                        self.inPain = True
                    self.bodyparts[4][1] = "Destroyed"
                            
            # Injure right leg
            elif randomLimb == 5:
                if self.bodyparts[5][1] == "Healthy":
                    self.event_log.append("A bullet has injured your Right Leg.")
                    self.injuryCount += 1
                    self.bodyparts[5][1] = "Injured"
                elif self.bodyparts[5][1] == "Injured":
                    self.event_log.append("A bullet has destroyed your Right Leg.")
                    if not self.inPain:
                        self.inPain = True
                    self.bodyparts[5][1] = "Destroyed"
        
        # Evade the bullet
        else:
            self.event_log.append("You evade a bullet.")
            self.skills[3][3] += 1

    # Update the player's position (on local map)
    def updatePos(self,screen,ev):
        # Get key presses
        pressed = pg.key.get_pressed()

        # Move up
        if pressed[pg.K_w]:
            if pressed[pg.K_LSHIFT] and self.currentWeight <= self.maxWeight and self.actionPoints > 0 and self.canSprint:
                self.y_change = -self.speed - self.sprintBonus
                self.actionPoints -= self.APlossRate
            else:
                if pressed[pg.K_LSHIFT] and self.currentWeight > self.maxWeight:
                    if self.event_log[-1] is not "You are overweight and can't run.":
                        self.event_log.append("You are overweight and can't run.")
                elif pressed[pg.K_LSHIFT] and not self.canSprint:
                    if self.event_log[-1] is not "You have an injury and can't run.":
                        self.event_log.append("You have an injury and can't run.")
                self.y_change = -self.speed

        # Move down
        if pressed[pg.K_s]:
            if pressed[pg.K_LSHIFT] and self.currentWeight <= self.maxWeight and self.actionPoints > 0 and self.canSprint:
                self.y_change = self.speed + self.sprintBonus
                self.actionPoints -= self.APlossRate
            else:
                if pressed[pg.K_LSHIFT] and self.currentWeight > self.maxWeight:
                    if self.event_log[-1] is not "You are overweight and can't run.":
                        self.event_log.append("You are overweight and can't run.")
                elif pressed[pg.K_LSHIFT] and not self.canSprint:
                    if self.event_log[-1] is not "You have an injury and can't run.":
                        self.event_log.append("You have an injury and can't run.")
                self.y_change = self.speed

        # Move left
        if pressed[pg.K_a]:
            if pressed[pg.K_LSHIFT] and self.currentWeight <= self.maxWeight and self.actionPoints > 0 and self.canSprint:
                self.x_change = -self.speed - self.sprintBonus
                self.actionPoints -= self.APlossRate
            else:
                if pressed[pg.K_LSHIFT] and self.currentWeight > self.maxWeight:
                    if self.event_log[-1] is not "You are overweight and can't run.":
                        self.event_log.append("You are overweight and can't run.")
                elif pressed[pg.K_LSHIFT] and not self.canSprint:
                    if self.event_log[-1] is not "You have an injury and can't run.":
                        self.event_log.append("You have an injury and can't run.")
                self.x_change = -self.speed

        # Move right
        if pressed[pg.K_d]:
            if pressed[pg.K_LSHIFT] and self.currentWeight <= self.maxWeight and self.actionPoints > 0 and self.canSprint:
                self.x_change = self.speed + self.sprintBonus
                self.actionPoints -= self.APlossRate
            else:
                if pressed[pg.K_LSHIFT] and self.currentWeight > self.maxWeight:
                    if self.event_log[-1] is not "You are overweight and can't run.":
                        self.event_log.append("You are overweight and can't run.")
                elif pressed[pg.K_LSHIFT] and not self.canSprint:
                    if self.event_log[-1] is not "You have an injury and can't run.":
                        self.event_log.append("You have an injury and can't run.")
                self.x_change = self.speed


        # window edge detection
        if self.rect.x + self.x_change >= 1500 or self.rect.x + self.x_change <= -10:
            self.x_change = 0
        if self.rect.y + self.y_change >= 800 or self.rect.y + self.y_change <= -10:
            self.y_change = 0 

        # rotation handler
        if self.x_change < 0:
            if self.y_change < 0:
                self.angle = 135
            elif self.y_change > 0:
                self.angle = 225
            else:
                self.angle = 180
        elif self.x_change > 0:
            if self.y_change < 0:
                self.angle = 45
            elif self.y_change > 0:
                self.angle = 315
            else:
                self.angle = 0
        elif self.y_change < 0:
            self.angle = 90
        elif self.y_change > 0:
            self.angle = 270

        # set to default animation when not moving
        if self.x_change == 0 and self.y_change == 0:
            self.image = self.default
            self.frameCounter = 0

        # use walking animation when moving
        elif self.x_change != 0 or self.y_change != 0:
            self.frameCounter += 1
            if self.frameCounter == 11:
                stepLeft.play()
                self.image = self.animationImages[0]
            elif self.frameCounter == 23:
                stepRight.play()
                self.image = self.animationImages[1]
            elif self.frameCounter == 24:
                self.frameCounter = 0
            
        # Move the player left/right
        self.rect.x += self.x_change
    
        # Check if player collides with something
        block_hit_list = pg.sprite.spritecollide(self, self.sprites, False)
        for block in block_hit_list:
            # Moving right
            if self.x_change > 0:
                self.rect.right = block.rect.left
            # Moving left
            else:
                self.rect.left = block.rect.right

        # Check for NPC collisions
        npc_hit_list = pg.sprite.spritecollide(self, self.npcList, False)
        for npc in npc_hit_list:
            # Moving right
            if self.x_change > 0:
                self.rect.right = npc.rect.left

            # Moving left
            else:
                self.rect.left = npc.rect.right
        
        # Handle game object collision and interaction
        for gameObject in gameObjectList:
            if gameObject.segment == self.current_location:
                self.currentGameObjects.append(gameObject)

        gameObject_hit_list = pg.sprite.spritecollide(self, self.currentGameObjects, False)
        for gameObject in gameObject_hit_list:
            # Moving right
            if self.x_change > 0:
                self.rect.right = gameObject.rect.left
            
            # Moving left
            else:
                self.rect.left = gameObject.rect.right

        # Move the player up/down
        self.rect.y += self.y_change

        # Check if player collides with a wall
        block_hit_list = pg.sprite.spritecollide(self, self.sprites, False)
        for block in block_hit_list:
            # Moving down
            if self.y_change > 0:
                self.rect.bottom = block.rect.top
            # Moving up
            else:
                self.rect.top = block.rect.bottom

        # Check if player collides with an NPC
        npc_hit_list = pg.sprite.spritecollide(self, self.npcList, False)
        for npc in npc_hit_list:
            # Moving down
            if self.y_change > 0:
                self.rect.bottom = npc.rect.top

            # Moving up
            else:
                self.rect.top = npc.rect.bottom

        # Handle game object collision and interaction
        gameObject_hit_list = pg.sprite.spritecollide(self, self.currentGameObjects, False)
        for gameObject in gameObject_hit_list:
            # Moving right
            if self.y_change > 0:
                self.rect.bottom = gameObject.rect.top
            
            # Moving left
            else:
                self.rect.top = gameObject.rect.bottom

        # Misc
        self.y_change = 0
        self.x_change = 0

        # draw the player
        screen.blit(pg.transform.rotate((pg.transform.smoothscale(self.image, (50, 50))), self.angle + 270), (self.rect.x,self.rect.y))
    
# # STAGE SYSTEM # #
class StageSystem():
    def __init__(self, stage):
        self.stage = stage
        self.event = []

    def stageTransition(self, stg):
        self.stage = stg

    def stageCheck(self, screen):
        if self.stage == 0:
            titleScreen(screen, self.event)
        elif self.stage == 1:
            gameIntro(screen, self.event)
        elif self.stage == 2:
            specialization(screen, self.event)
        elif self.stage == 3:
            mainGame(screen, self.event)
        elif self.stage == 4:
            playerDead(screen, self.event)
        elif self.stage == 5:
            victory(screen, self.event)
        elif self.stage == 10:
            instructionScreen(screen, self.event)

# # # CORE GAME CODE # # #
# Title screen
def titleScreen(screen, ev):
    screen.fill(black)
    # Title text
    uiText.draw(screen, 200, 300, "Aqua Adventure 3", 50, white, 255, True)
    uiText.draw(screen, 220, 360, "literally the greatest game", 24, white, 255, False, True)

    # Start game button
    startGameBtn.draw(screen, 300, 400, 300, 50, "1) Start Game", 10, black)
    if startGameBtn.isActive(ev, pg.K_1):
        stageSys.stageTransition(1)

    # Help menu button
    helpMenuBtn.draw(screen, 300, 460, 300, 50, "2) Instructions", 10, black)
    if helpMenuBtn.isActive(ev, pg.K_2):
        stageSys.stageTransition(10)

# Instruction screen
def instructionScreen(screen, ev):
    screen.fill(black)
    uiText.draw(screen, 200, 300, "Instructions", 50, white, 255, True)

    uiText.draw(screen, 220, 360, "Controls", 24, white, 255, True, True)
    uiText.draw(screen, 240, 390, "W), A), S), D) to move (in all axes)", 18, white, 255)
    uiText.draw(screen, 240, 410, "TAB) to open your inventory", 18, white, 255)
    uiText.draw(screen, 240, 430, "ARROWKEYS) to navigate inventory", 18, white, 255)
    uiText.draw(screen, 240, 450, "E) to interact", 18, white, 255)
    uiText.draw(screen, 240, 470, "SPACE) to shoot", 18, white, 255)
    uiText.draw(screen, 240, 490, "R) to reload", 18, white, 255)

    uiText.draw(screen, 220, 540, "Background", 24, white, 255, True, True)
    uiText.draw(screen, 240, 570, "Aqua Adventure 3 takes place in a post-apocalyptic coastal landscape, ", 18, white, 255)
    uiText.draw(screen, 240, 590, "4 years after the Earth's last war. You, a great war prophet, predicted this", 18, white, 255)
    uiText.draw(screen, 240, 610, "cataclysmic event and prepared accordingly. As an ex-government agent, you ", 18, white, 255)
    uiText.draw(screen, 240, 630, "know of the United Federation government's secret project - an advanced AI", 18, white, 255)
    uiText.draw(screen, 240, 650, "designed to control the Wastelands. You must destroy it.", 18, white, 255)
    
    backBtn.draw(screen, 200, 700, 150, 40, "1) Return", 12, black)
    if backBtn.isActive(ev, pg.K_1):
        stageSys.stageTransition(0)

# Game victory screen
def victory(screen, ev):
    screen.fill(black)
    uiText.draw(screen, 200, 300, "Victory!", 50, white, 255, True)

    uiText.draw(screen, 220, 360, "You have destroyed the evil AI ravaging the wasteland.", 24, white, 255, True, True)


# Game intro sequence
introCounter = 0
primaryFadeFrame = 0
secondaryFadeFrame = 0
tertiaryFadeFrame = 0
storyPhase = 0
def gameIntro(screen, ev):
    global introCounter, primaryFadeFrame, secondaryFadeFrame, tertiaryFadeFrame, storyPhase
    introCounter += 1
    screen.fill(black)

    # Fade in phase 0
    if 40 < introCounter < 280:
        storyPhase = 0
        primaryFadeFrame += 1
    if 140 < introCounter < 380:
        secondaryFadeFrame += 1
    if 240 < introCounter < 480:
        tertiaryFadeFrame += 1
    if 500 < introCounter < 740:
        primaryFadeFrame -= 1
    if 540 < introCounter < 780:
        secondaryFadeFrame -= 1
    if 580 < introCounter < 820:
        tertiaryFadeFrame -= 1

    # Fade in phase 1
    if 900 < introCounter < 1140:
        storyPhase = 1
        primaryFadeFrame += 1
    if 1040 < introCounter < 1280:
        secondaryFadeFrame += 1
    if 1100 < introCounter < 1340:
        tertiaryFadeFrame += 1
    if 1410 < introCounter < 1650:
        primaryFadeFrame -= 1
    if 1450 < introCounter < 1690:
        secondaryFadeFrame -= 1
    if 1490 < introCounter < 1730:
        tertiaryFadeFrame -= 1

    # Fade in phase 2
    if 1840 < introCounter < 2080:
        storyPhase = 2
        primaryFadeFrame += 1
    if 1940 < introCounter < 2180:
        secondaryFadeFrame += 1
    if 2040 < introCounter < 2280:
        tertiaryFadeFrame += 1
    if 2350 < introCounter < 2590:
        primaryFadeFrame -= 1
    if 2390 < introCounter < 2630:
        secondaryFadeFrame -= 1
    if 2430 < introCounter < 2670:
        tertiaryFadeFrame -= 1
    
    if introCounter > 2670:
        stageSys.stageTransition(2)

    # Story phase 0
    if storyPhase == 0:
        uiText.draw(screen, 200, 300, "2134", 50, white, primaryFadeFrame, True, True)
        uiText.draw(screen, 220, 360, "One day before Earth's final war", 24, white, secondaryFadeFrame, True, False)
        uiText.draw(screen, 240, 400, "You enter your personal survival shelter. Your neighbour calls you crazy.", 16, white, tertiaryFadeFrame, True)
        uiText.draw(screen, 240, 440, "He says nothing's going to happen. But you know otherwise.", 16, white, tertiaryFadeFrame, True)

    if storyPhase == 1:
        uiText.draw(screen, 200, 300, "2135", 50, white, primaryFadeFrame, True, True)
        uiText.draw(screen, 220, 360, "Two days after the war's end", 24, white, secondaryFadeFrame, True, False)
        uiText.draw(screen, 240, 400, "You still hear the chaos of the post-apocalypse outside of your shelter.", 16, white, tertiaryFadeFrame, True)
        uiText.draw(screen, 240, 440, "Your neighbour returns, begging to be let in. You leave him outside.", 16, white, tertiaryFadeFrame, True)

    if storyPhase == 2:
        uiText.draw(screen, 200, 300, "2139", 50, white, primaryFadeFrame, True, True)
        uiText.draw(screen, 220, 360, "Present day", 24, white, secondaryFadeFrame, True, False)
        uiText.draw(screen, 240, 400, "Your supplies start to run low. The outside world is finally quiet.", 16, white, tertiaryFadeFrame, True)
        uiText.draw(screen, 240, 440, "It's time to leave. You take your bare essentials and leave.", 16, white, tertiaryFadeFrame, True)

    introContinue.draw(screen, 200, 700, 150, 40, "E) Skip", 12, black)
    if introContinue.isActive(ev, pg.K_e):
        stageSys.stageTransition(2)


# Variable needed for specialization scene
global playerChoiceSpecial
playerChoiceSpecial = ["No skill selected.", None]

# Ask player to specialize in a skill
def specialization(screen, ev):
    global playerChoiceSpecial
    screen.fill(black)

    # UI text
    uiText.draw(screen, 200, 300, "SPECIALIZE", 50, white, 255, True)
    uiText.draw(screen, 220, 360, "Choose a skill to specialize in", 24, white, 255, True, True)
    uiText.draw(screen, 300, 400, "Your choice: "+playerChoiceSpecial[0], 20, white, 255)

    # Print avaiable skills on screen
    for i in range(0, len(playerSkills)):
        uiText.draw(screen, 300, 440 + (20 * i), str(i + 1)+") "+playerSkills[i][0], 18, white, 255, True)

    # Handle player choice
    for event in ev:
        if event.type == pg.KEYUP and event.key == pg.K_1:
            playerChoiceSpecial = ["Lockpick - Ability to open locked items, including doors and containers.", 0]
        elif event.type == pg.KEYUP and event.key == pg.K_2:
            playerChoiceSpecial = ["Medical - Ability to heal your injuries.", 1]
        elif event.type == pg.KEYUP and event.key == pg.K_3:
            playerChoiceSpecial = ["Shooting - Ability to shoot accurately.", 2]
        elif event.type == pg.KEYUP and event.key == pg.K_4:
            playerChoiceSpecial = ["Evasion - Ability to dodge and evade enemy attacks.", 3]
        elif event.type == pg.KEYUP and event.key == pg.K_5:
            playerChoiceSpecial = ["Strength - Ability to carry a large amount of items.", 4]
        elif event.type == pg.KEYUP and event.key == pg.K_6:
            playerChoiceSpecial = ["Endurance - Ability to sprint efficiently and use more chems.", 5]

    # Display button when player chooses a skill
    if playerChoiceSpecial != ["No skill selected.", None]:
        introSpecialize.draw(screen, 220, 600, 150, 40, "E) Confirm", 12, black)

        # Update skill and proceed to game
        if introSpecialize.isActive(ev, pg.K_e):
            playerSkills[playerChoiceSpecial[1]][2] = 0.3
            stageSys.stageTransition(3)    
    
# Handle inter-segment navigation and *stuff*
def mainGame(screen, ev):
    # Use player's current location to set scene
    if player.current_location == 0:
        Segment0(screen, ev)
    elif player.current_location == 1:
        Segment1(screen, ev)
    elif player.current_location == 2:
        Segment2(screen, ev)
    elif player.current_location == 3:
        Segment3(screen, ev)
    elif player.current_location == 4:
        Segment4(screen, ev)
    elif player.current_location == 5:
        Segment5(screen, ev)
    elif player.current_location == 6:
        Segment6(screen, ev)
    elif player.current_location == 7:
        Segment7(screen, ev)
    elif player.current_location == 8:
        Segment8(screen, ev)
    elif player.current_location == 9:
        BossFight(screen, ev)

# End of game
def playerDead(screen, ev):
    screen.fill(black)
    uiText.draw(screen, 200, 300, "YOU DIED", 50, white, 255, True)
    uiText.draw(screen, 220, 360, "Cause of death: "+player.failureCause, 24, white, 255, False, True)


# # SEGMENT FUNCTIONS # #
# Segment 0 (default)
def Segment0(screen, ev):
    # Draw segment background
    screen.blit(pg.transform.smoothscale(seg0Img, (1500, 800)), (0, 0))

    # # LEVEL DESIGN # #
    # Draw floors
    pg.draw.rect(screen, space_gray, [140, 390, 60, 100])
    pg.draw.rect(screen, black, [155, 405, 40, 40], 2)

    # Draw trees
    drawTree(800, 200, 150, 150)
    drawTree(400, 100, 150, 150)
    drawTree(500, 400, 150, 150)
    drawTree(1000, 600, 150, 150)
    
    # # # #

    # Draw walls
    s0_spriteList.update()
    s0_spriteList.draw(screen)

    # Load sprites & npcs for player
    player.sprites = s0_spriteList
    player.npcList = s0_npcList
    player.available_targets = s0_npcList

    # Draw NPCs
    if not player.uiActive:
        for npc in player.npcList:
            npc.draw(ev)

    # Call core segment code
    segmentCore(ev)

    # Handle game object interaction
    gameObjectHandler(0, ev)
            
# Segment 1
def Segment1(screen, ev):
    # Draw segment background
    screen.blit(pg.transform.smoothscale(seg1Img, (1500, 800)), (0, 0))

    # # LEVEL DESIGN # #



    # # # # #

    # Draw walls
    s1_spriteList.update()
    s1_spriteList.draw(screen)

    # Load sprites & npcs for player
    player.sprites = s1_spriteList
    player.npcList = s1_npcList
    player.available_targets = s1_npcList

    # Draw NPCs
    if not player.uiActive:
        for npc in s1_npcList:
            npc.draw(ev)

    # Call core segment code
    segmentCore(ev)

    # Handle game object interaction
    gameObjectHandler(1, ev)

# Segment 2
def Segment2(screen, ev):
    # Draw segment background
    screen.blit(pg.transform.smoothscale(seg2Img, (1500, 800)), (0, 0))

    # # LEVEL DESIGN # #
    pg.draw.rect(screen, floorBrown, [375, 250, 200, 400])
    pg.draw.rect(screen, floorBrown, [575, 450, 100, 200])


    drawTree(300, 100, 150, 150)
    drawTree(800, 300, 150, 150)
    drawTree(1000, 600, 150, 150)

    # # # # #

    # Draw walls
    s2_spriteList.update()
    s2_spriteList.draw(screen)

    # Load sprites & npcs for player
    player.sprites = s2_spriteList
    player.npcList = s2_npcList
    player.available_targets = s2_npcList

    # Draw NPCs
    if not player.uiActive:
        for npc in s2_npcList:
            npc.draw(ev)

    # Call core segment code
    segmentCore(ev)

    # Handle game object interaction
    gameObjectHandler(2, ev)

# Segment 3
def Segment3(screen, ev):
    # Draw segment background
    screen.blit(pg.transform.smoothscale(seg3Img, (1500, 800)), (0, 0))

    # # LEVEL DESIGN # #



    # # # # #

    # Draw walls
    s3_spriteList.update()
    s3_spriteList.draw(screen)

    # Load sprites & npcs for player
    player.sprites = s3_spriteList
    player.npcList = s3_npcList
    player.available_targets = s3_npcList

    # Draw NPCs
    if not player.uiActive:
        for npc in s3_npcList:
            npc.draw(ev)

    # Call core segment code
    segmentCore(ev)

    # Handle game object interaction
    gameObjectHandler(3, ev)

# Segment 4
def Segment4(screen, ev):
    # Draw segment background
    screen.blit(pg.transform.smoothscale(seg4Img, (1500, 800)), (0, 0))

    # # LEVEL DESIGN # #
    drawTree(100, 200, 150, 150)
    drawTree(300, 500, 150, 150)



    # # # # #

    # Draw walls
    s4_spriteList.update()
    s4_spriteList.draw(screen)

    # Load sprites & npcs for player
    player.sprites = s4_spriteList
    player.npcList = s4_npcList
    player.available_targets = s4_npcList

    # Draw NPCs
    if not player.uiActive:
        for npc in s4_npcList:
            npc.draw(ev)

    # Call core segment code
    segmentCore(ev)

    # Handle game object interaction
    gameObjectHandler(4, ev)

# Segment 5
def Segment5(screen, ev):
    # Draw segment background
    screen.blit(pg.transform.smoothscale(seg5Img, (1500, 800)), (0, 0))

    # # LEVEL DESIGN # #




    # # # # #

    # Draw walls
    s5_spriteList.update()
    s5_spriteList.draw(screen)

    # Load sprites & npcs for player
    player.sprites = s5_spriteList
    player.npcList = s5_npcList
    player.available_targets = s5_npcList

    # Draw NPCs
    if not player.uiActive:
        for npc in s5_npcList:
            npc.draw(ev)

    # Call core segment code
    segmentCore(ev)

    # Handle game object interaction
    gameObjectHandler(5, ev)

# Segment 6
def Segment6(screen, ev):
    # Draw segment background
    screen.blit(pg.transform.smoothscale(seg6Img, (1500, 800)), (0, 0))

    # # LEVEL DESIGN # #



    # # # # #

    # Draw walls
    s6_spriteList.update()
    s6_spriteList.draw(screen)

    # Load sprites & npcs for player
    player.sprites = s6_spriteList
    player.npcList = s6_npcList
    player.available_targets = s6_npcList

    # Draw NPCs
    if not player.uiActive:
        for npc in s6_npcList:
            npc.draw(ev)

    # Draw green transparent background
    radCover = pg.Surface((1500, 800)).convert_alpha()
    radCover.fill([0, 150, 0, 100])
    screen.blit(radCover, (0, 0, 0, 0))

    # Call core segment code
    segmentCore(ev)

    # Handle game object interaction
    gameObjectHandler(6, ev)

# Segment 7
def Segment7(screen, ev):
    # Draw segment background
    screen.blit(pg.transform.smoothscale(seg7Img, (1500, 800)), (0, 0))

    # # LEVEL DESIGN # #



    # # # # #

    # Draw walls
    s7_spriteList.update()
    s7_spriteList.draw(screen)

    # Load sprites & npcs for player
    player.sprites = s7_spriteList
    player.npcList = s7_npcList
    player.available_targets = s7_npcList

    # Draw NPCs
    if not player.uiActive:
        for npc in s7_npcList:
            npc.draw(ev)

    # Call core segment code
    segmentCore(ev)

    # Handle game object interactions
    gameObjectHandler(7, ev)

# Segment 8
def Segment8(screen, ev):
    # Draw segment background
    screen.blit(pg.transform.smoothscale(seg8Img, (1500, 800)), (0, 0))

    # # LEVEL DESIGN # #


    # # # # #

    # Draw walls
    s8_spriteList.update()
    s8_spriteList.draw(screen)

    # Load sprites & npcs for player
    player.sprites = s8_spriteList
    player.npcList = s8_npcList
    player.available_targets = s8_npcList

    # Draw NPCs
    if not player.uiActive:
        for npc in s8_npcList:
            npc.draw(ev)

    # Call core segment code
    segmentCore(ev)

    # Handle game object interaction
    gameObjectHandler(8, ev)

# Boss Fight (9)
def BossFight(screen, ev):
    # Draw segment background
    screen.fill(space_gray)

    # # LEVEL DESIGN # #




    # # # # #

    # Draw walls
    s9_spriteList.update()
    s9_spriteList.draw(screen)

    # Load sprites & npcs for player
    player.sprites = s9_spriteList
    player.npcList = s9_npcList
    player.available_targets = s9_npcList

    # Draw NPCs
    if not player.uiActive:
        for npc in s9_npcList:
            npc.draw(ev)

    # Call core segment code
    segmentCore(ev)

    # Handle game object interaction
    gameObjectHandler(9, ev)

# # # GAME CODE INIT # # #
# Main menu buttons
startGameBtn = Button(white, red)
helpMenuBtn = Button(white, red)
introContinue = Button(white, red)
introSpecialize = Button(white, red)
backBtn = Button(white, red)

# StatusUI main buttons
statUIlog = Button(white, red)
statUIinv = Button(white, red)
statUIstat = Button(white, red)
statUIskill = Button(white, red)
statUImap = Button(white, red)
statUIhelp = Button(white, red)

# StatusUI inv buttons
statUIinvDrop = Button(white, red)
statUIinvUse = Button(white, red)
invDropAgree = Button(white, red)
invDropDisagree = Button(white, red)
invUndropable = Button(white, red)
invUseAgree = Button(white, red)
invUseDisagree = Button(white, red)
invUnusable = Button(white, red)
medKitHeal = Button(white, red)
medKitCancel = Button(white, red)

# TransferUI buttons
tuiExit = Button(white, red)
tuiMove = Button(white, red)
tuiDrop = Button(white, red)

# StatusUI stat buttons
statUIstatHeal = Button(white, red)
healAgree = Button(white, red)
healDisagree = Button(white, red)
statUIstatMed = Button(white, red)

# Initialize text class
uiText = Text()

# Stage system
stageSys = StageSystem(stage)

# Player class
player = Player(145, 440) 

# Projectile list
projectiles = []
hostileprojectiles = []

# Full world map
global fullMapImg
fullMapImg = pg.image.load(addressprefix + "\\misc\\full_map.jpg").convert_alpha()

# Background images
global seg0Img
seg0Img = pg.image.load(addressprefix + "\\misc\\seg0.jpg").convert_alpha()
global seg1Img
seg1Img = pg.image.load(addressprefix + "\\misc\\seg1.jpg").convert_alpha()
global seg2Img
seg2Img = pg.image.load(addressprefix + "\\misc\\seg2.jpg").convert_alpha()
global seg3Img
seg3Img = pg.image.load(addressprefix + "\\misc\\seg3.jpg").convert_alpha()
global seg4Img
seg4Img = pg.image.load(addressprefix + "\\misc\\seg4.jpg").convert_alpha()
global seg5Img
seg5Img = pg.image.load(addressprefix + "\\misc\\seg5.jpg").convert_alpha()
global seg6Img
seg6Img = pg.image.load(addressprefix + "\\misc\\seg6.jpg").convert_alpha()
global seg7Img
seg7Img = pg.image.load(addressprefix + "\\misc\\seg7.jpg").convert_alpha()
global seg8Img
seg8Img = pg.image.load(addressprefix + "\\misc\\seg8.jpg").convert_alpha()

# # TIMERS # #
# Define a new event in pygame for each thing to time (SPECIAL FUNCTION)
hungerEvent = pg.USEREVENT + 1
thirstEvent = pg.USEREVENT + 2
healthEvent = pg.USEREVENT + 3
enemyShootEvent = pg.USEREVENT + 4
bossShootEvent = pg.USEREVENT + 5
targetAwareEvent = pg.USEREVENT + 6
npcSpeakEvent = pg.USEREVENT + 7

# Set the timers
pg.time.set_timer(hungerEvent, hungerIterator)
pg.time.set_timer(thirstEvent, thirstIterator)
pg.time.set_timer(healthEvent, healthIterator)
pg.time.set_timer(enemyShootEvent, enemyShootIterator)
pg.time.set_timer(bossShootEvent, bossShootIterator)
pg.time.set_timer(targetAwareEvent, targetAwareIterator)
pg.time.set_timer(npcSpeakEvent, npcSpeakIterator)

# # SPRITE STUFF # #
# Init wall lists for each segment
s0_spriteList = pg.sprite.Group()
s1_spriteList = pg.sprite.Group()
s2_spriteList = pg.sprite.Group()
s3_spriteList = pg.sprite.Group()
s4_spriteList = pg.sprite.Group()
s5_spriteList = pg.sprite.Group()
s6_spriteList = pg.sprite.Group()
s7_spriteList = pg.sprite.Group()
s8_spriteList = pg.sprite.Group()
s9_spriteList = pg.sprite.Group()

# Init NPC lists for each segment
s0_npcList = pg.sprite.Group()
s1_npcList = pg.sprite.Group()
s2_npcList = pg.sprite.Group()
s3_npcList = pg.sprite.Group()
s4_npcList = pg.sprite.Group()
s5_npcList = pg.sprite.Group()
s6_npcList = pg.sprite.Group()
s7_npcList = pg.sprite.Group()
s8_npcList = pg.sprite.Group()
s9_npcList = pg.sprite.Group()

# Easy function to produce walls
def drawWall(segment, x, y, w, h, color):
    wall = Wall(x, y, w, h, color)
    if segment == 0:
        s0_spriteList.add(wall)
    elif segment == 1:
        s1_spriteList.add(wall)
    elif segment == 2:
        s2_spriteList.add(wall)
    elif segment == 3:
        s3_spriteList.add(wall)
    elif segment == 4:
        s4_spriteList.add(wall)
    elif segment == 5:
        s5_spriteList.add(wall)
    elif segment == 6:
        s6_spriteList.add(wall)
    elif segment == 7:
        s7_spriteList.add(wall)
    elif segment == 8:
        s8_spriteList.add(wall)
    elif segment == 9:
        s9_spriteList.add(wall)

# Sound effects
gunShot = pg.mixer.Sound(addressprefix + "\\sounds\\gunshot.wav")
openDoor = pg.mixer.Sound(addressprefix + "\\sounds\\unlockDoor.wav")
objectLocked = pg.mixer.Sound(addressprefix + "\\sounds\\doorLocked.wav")
gunReload = pg.mixer.Sound(addressprefix + "\\sounds\\reload.wav")
stepLeft = pg.mixer.Sound(addressprefix + "\\sounds\\leftStep.wav")
stepRight = pg.mixer.Sound(addressprefix + "\\sounds\\rightStep.wav")

# # LEVEL DESIGN # #
# Segment 0 (player spawns at (100, 400))
# Draw some walls
drawWall(0, 1120, 150, 10, 80, black)
drawWall(0, 840, 90, 160, 10, black)
drawWall(0, 1220, 400, 10, 110, black)

# Old Shelter Walls
drawWall(0, 140, 390, 70, 10, black)
drawWall(0, 140, 390, 10, 100, black)
drawWall(0, 140, 490, 70, 10, black)

# Shelter door
shelterDoor = Door(200, 400, 0, "Door", None, False, 10, 90)
gameObjectList.append(shelterDoor)

# Game start container
oldShelterContItems = [
    item_list[22],
    item_list[19],
    item_list[19],
    item_list[0]
]
oldShelterContainer = Container(145, 340, 0, "Container", oldShelterContItems, True)
gameObjectList.append(oldShelterContainer)

# Segment 1
# Draw some walls
drawWall(1, 420, 100, 10, 60, black)
drawWall(1, 350, 240, 10, 90, black)
drawWall(1, 335, 450, 10, 110, black)
drawWall(1, 740, 80, 110, 10, black)
drawWall(1, 830, 200, 90, 10, black)
drawWall(1, 1230, 130, 10, 130, black)

# old rectangle thing
drawWall(1, 650, 370, 100, 60, black)

contItems = [ 
    item_list[random.randint(0, 17)],
    item_list[random.randint(0, 17)],
    item_list[random.randint(0, 17)],
    item_list[16]
]
northCoastContainer = Container(670, 320, 1, "Container", contItems)
gameObjectList.append(northCoastContainer)

# Robot swarm
ncRobot1 = NPC(650, 300, 0, "Robot", "Basic", "Hostile", 75, 150, 2, item_list[random.randint(0, 18)], 500)
ncRobot2 = NPC(800, 290, 180, "Robot", "Basic", "Hostile", 75, 150, 2, item_list[random.randint(0, 18)], 500)
ncRobot3 = NPC(725, 240, 270, "Robot", "Basic", "Hostile", 75, 150, 2, item_list[16], 500)

s1_npcList.add(ncRobot1, ncRobot2, ncRobot3)

# Segment 2
# Draw some house walls
drawWall(2, 375, 250, 200, 10, black)
drawWall(2, 375, 250, 10, 400, black)
drawWall(2, 575, 250, 10, 300, black)
drawWall(2, 450, 450, 145, 10, black)
scHouseDoor = Door(595, 450, 2, "Door", None, False, 80, 10)
gameObjectList.append(scHouseDoor)
drawWall(2, 675, 450, 10, 210, black)
drawWall(2, 375, 650, 300, 10, black)

contItems = [
    item_list[random.randint(0, 17)],
    item_list[random.randint(0, 17)],
]
s2_cont1 = Container(525, 460, 2, "Container", contItems)
gameObjectList.append(s2_cont1)

contItems = [
    item_list[random.randint(0, 17)],
    item_list[random.randint(0, 17)]
]
s2_cont2 = Container(525, 400, 2, "Container", contItems)
gameObjectList.append(s2_cont2)

contItems = [
    item_list[random.randint(0, 17)],
    item_list[random.randint(0, 17)]
]
s2_cont3 = Container(385, 260, 2, "Container", contItems)
gameObjectList.append(s2_cont3)

s2_npc = NPC(450, 400, 180, "Human", "Basic", "Hostile", 40, 100, 8, None, 100)
s2_npcList.add(s2_npc)


# # Segment 3 # #
contItems = [
    ["Rifle", "A .308cal rifle", 10, 100, True, True],
    [".308cal mag", "A .308 magazine", 1, 70, False, True],
    [".308cal mag", "A .308 magazine", 1, 70, False, True],
    [".308cal mag", "A .308 magazine", 1, 70, False, True],
    ["Military MRE", "Restores hunger", 2, 50, True, True],
    ["Clean Water", "Restores thirst", 1, 25, True, True],
    ["Painkillers", "Removes pain blindness", 0.5, 20, True, True],
    ["Antibiotics", "Treats infections", 1, 75, True, True]
]
s3_cont = Container(670, 500, 3, "Container", contItems, True)
gameObjectList.append(s3_cont)

# # Segment 7 # #
# Right border walls
drawWall(7, 1480, 0, 20, 350, black)
drawWall(7, 1480, 450, 20, 350, black)

# # Boss Fight # #
# Border walls
drawWall(9, 0, 0, 1500, 20, black)
drawWall(9, 1480, 0, 20, 800, black)
drawWall(9, 0, 780, 1500, 20, black)
drawWall(9, 0, 0, 20, 350, black)
drawWall(9, 0, 450, 20, 350, black)

# NPCs first wave
f1_npc1 = NPC(200, 200, 270, "Robot", "Basic", "Hostile", 200, 200, 10, item_list[random.randint(0, 18)], 200)
f1_npc2 = NPC(200, 550, 90, "Robot", "Basic", "Hostile", 200, 200, 10, item_list[random.randint(0, 18)], 200)
s9_npcList.add(f1_npc1, f1_npc2)

# Interior wall 1
drawWall(9, 500, 0, 20, 350, black)
drawWall(9, 500, 450, 20, 350, black)

bossDoor1 = Door(505, 350, 9, "Door", None, True, 10, 100)
gameObjectList.append(bossDoor1)

# NPCs second wave
f2_npc1 = NPC(600, 200, 270, "Robot", "Basic", "Hostile", 250, 250, 15, item_list[random.randint(0, 18)], 200)
f2_npc2 = NPC(850, 200, 270, "Robot", "Basic", "Hostile", 250, 250, 15, item_list[random.randint(0, 18)], 200)
f2_npc3 = NPC(600, 550, 90, "Robot", "Basic", "Hostile", 250, 250, 15, item_list[random.randint(0, 18)], 200)
f2_npc4 = NPC(850, 550, 90, "Robot", "Basic", "Hostile", 250, 250, 15, item_list[random.randint(0, 18)], 200)
s9_npcList.add(f2_npc1, f2_npc2, f2_npc3, f2_npc4)

# Interior wall 2
drawWall(9, 1000, 0, 20, 350, black)
drawWall(9, 1000, 450, 20, 350, black)

bossDoor2 = Door(1005, 350, 9, "Door", None, True, 10, 100)
gameObjectList.append(bossDoor2)

# Final wave
boss = NPC(1350, 350, 180, "Robot", "Boss", "Hostile", 500, 200, 25, None, 250, 2)

f3_npc1 = NPC(1100, 200, 270, "Robot", "Basic", "Hostile", 300, 300, 15, item_list[random.randint(0, 18)], 200)
f3_npc2 = NPC(1250, 200, 270, "Robot", "Basic", "Hostile", 300, 300, 15, item_list[random.randint(0, 18)], 200)
f3_npc3 = NPC(1400, 200, 270, "Robot", "Basic", "Hostile", 300, 300, 15, item_list[random.randint(0, 18)], 200)
f3_npc4 = NPC(1100, 550, 90, "Robot", "Basic", "Hostile", 300, 300, 15, item_list[random.randint(0, 18)], 200)
f3_npc5 = NPC(1250, 550, 90, "Robot", "Basic", "Hostile", 300, 300, 15, item_list[random.randint(0, 18)], 200)
f3_npc6 = NPC(1400, 550, 90, "Robot", "Basic", "Hostile", 300, 300, 15, item_list[random.randint(0, 18)], 200)
s9_npcList.add(f3_npc1, f3_npc2, f3_npc3, f3_npc4, f3_npc5, f3_npc6, boss)

# # # MAIN LOOP # # #
while not done:

    # Capture events in stageSys
    stageSys.event = pg.event.get()

    # Main event loop
    for event in stageSys.event:
        #print(event)
        if event.type == pg.QUIT:
            done = True # if user clicks close, it will end the main loop

    # Check which stage is active
    stageSys.stageCheck(screen)

    # Update the screen at a defined fps
    pg.display.flip()
    clock.tick(60)

# Close the window and quit the game
pg.quit()

