import pygame, sys, random

pygame.font.init()
myfont = pygame.font.Font('/Users/julianbesems/Library/Fonts/HELR45W.ttf', 28)

colours = []
colours.append([228, 197, 73])
colours.append([185, 0, 37])
colours.append([78, 87, 111])
colours.append([12, 63, 50])
colours.append([236, 110, 0])
colours.append([68, 22, 33])
colours.append([143, 149, 160])
colours.append([185, 197, 201])
colours.append([35, 127, 125])
colours.append([149, 132, 103])
colours.append([0, 44, 125])
colours.append([0, 160, 213])
colours.append([166, 202, 87])
colours.append([228, 166, 156])

class Graphics:
    screen_width = 2560 #1500 #1400 #2000 #1440
    screen_height = 1600 #1000 #800 #1143 #823

    portLx = int(0.4015 * screen_width)
    portLy = int(0.158 * screen_height)
    portRx = portLx + int(0.20667 * screen_width)
    portRy = portLy + int(0.64 * screen_height)

    padding = int(0.0322 * (portRx - portLx))
    width = 2 * padding
    height = 13 * padding

    def __init__(self, port, groups):
        self._port = port
        self._groups = groups
        self._screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)

    class Background(pygame.sprite.Sprite):
        def __init__(self, image_file, location):
            pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
            self.image = pygame.image.load(image_file)
            self.rect = self.image.get_rect()
            self.rect.left, self.rect.top = location

    class Ship(pygame.sprite.Sprite):
        def __init__(self, image_file, location, home, exit, screen):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(image_file)
            self.rect = self.image.get_rect()
            self.rect.left, self.rect.top = location
            self.screen = screen
            self.home = home
            self.exit = exit
            self.cargo_height = 0
            self.topC = 0
            self.max_capacity = 3000

        def getColour(self, dock):
            if dock.ship.colour == None:
                return pygame.Color('black')
            else:
                return dock.ship.colour

        def getHeight(self, ship):
            if not ship == None:
                height = int(len(ship.containers)/self.max_capacity * 0.7 * self.rect.height)
                return height
            else:
                return 0

        def update(self, dock):
            if not dock.ship == None:
                self.max_capacity = dock.ship.max_capacity
                self.screen.blit(self.image, self.position(dock.ship))
                self.topC= self.rect.top + int(self.rect.height * 0.2)
                leftC = self.rect.left + int(self.rect.width * 0.1)
                widthC = int(self.rect.width * 0.8)
                self.cargo_height = self.getHeight(dock.ship)
                pygame.draw.rect(self.screen, self.getColour(dock), (leftC, self.topC, widthC, self.cargo_height))

        def position(self, ship):
            step = 6
            if ship.status == "docked" or ship.status == "loading":
                self.rect.left, self.rect.top = self.home
                return self.rect
            elif ship.status == "arriving1":
                self.rect.left, self.rect.top = self.exit
                ship.status = "arriving2"
                return self.rect
            elif ship.status == "arriving2":
                if self.rect.top > self.home[1]:
                    self.rect.top -= step
                    return self.rect
                elif (self.home[0] - step -1 < self.rect.left and self.rect.left < self.home[0] + step -1 and self.home[1] - step -1 < self.rect.top and self.rect.top < self.home[1] + step -1):
                    ship.status = "docked"
                    #print("docked")
                    self.rect.left, self.rect.top = self.home
                    return self.rect
                elif self.home[0] > self.rect.left :
                    self.rect.left += step
                    return self.rect
                elif self.home[0] < self.rect.left :
                    self.rect.left -= step
                    return self.rect
            elif ship.status == "leaving1":
                self.rect.left, self.rect.top = self.home
                ship.status = "leaving2"
                return self.rect
            elif ship.status == "leaving2":
                if self.exit[0] -step > self.rect.left:
                    self.rect.left += step
                    return self.rect
                elif self.exit[0] + step < self.rect.left :
                    self.rect.left -= step
                    return self.rect
                elif self.exit[1] - step -1 < self.rect.top:
                    ship.status = "left"
                    #print("left")
                    self.rect.left, self.rect.top = self.exit
                    return self.rect
                if self.rect.top < self.exit[1]:
                    self.rect.top += step
                    return self.rect
            else:
                self.rect.left, self.rect.top = self.exit
                return self.rect

    class Lorry:
        def __init__(self,pointlist):
            self._pointlist = pointlist
            self._col = pygame.Color('black')

        def update(self,pointlist):
            pygame.draw.polygon(screen, self._col, pointlist)

    def draw_screen(self, screen):
        pygame.init()
        pygame.display.set_caption('Dock')

        pygame.draw.lines(screen, pygame.Color('black'), False, [(0,self.screen_height/10),
        (self.screen_width/5,self.screen_height/10),(self.screen_width/5,self.screen_height-(self.screen_height/10)),
        (self.screen_width-(self.screen_width/5),self.screen_height-(self.screen_height/10)),
        (self.screen_width-(self.screen_width/5),self.screen_height/10),
        (self.screen_width, self.screen_height/10)])

    def update_stack(self, stackG, stackP):
        colour = int(255 - (len(stackP.containers)/(stackP.max+1))*155)
        stackG.update(pygame.Color(colour, colour, colour))

    def getShipColour(self, dock):
        if dock.ship == None:
            return pygame.Color(255, 255, 255)
        else:
            colour = int(255 - (len(dock.ship.containers)/(3000+1))*255)
            return pygame.Color(colour, colour, colour)

    def drawNeStack(self, i, eStackLx, eStackLy, ships, dateThreshold):
        stacksX = eStackLx
        stacksY = eStackLy + 3 * self.width
        cw = int(0.28 * self.padding)
        ch = int(0.83 * self.padding)
        for stack in self._port.ne_stacks:
            if stack.name == str(i):
                for w in range(10):
                    for h in range(28):
                        if dateThreshold < 1:
                            height = stack.image[h][w].height
                            colour = stack.image[h][w].colour
                        else:
                            height = stack.image[h][w].checkDates(self._port.date, dateThreshold)
                            if height > 5:
                                height = 5
                            colour = stack.image[h][w].getColour(stack.image[h][w].group, height)
                        if not colour == pygame.Color(255, 255, 255):
                            pygame.draw.rect(self._screen, colour, (stacksX + stack.x * 3.9 * self.padding + w * cw, stacksY + stack.y * 26 * self.padding + h * ch, cw, ch))
                        if stack.image[h][w].new:
                            start_pos = (stacksX + stack.x * 3.85 * self.padding + w * cw, stacksY + stack.y * 25 * self.padding + h * ch)
                            if (not stack.image[h][w].group == None) and stack.image[h][w].group.activity == "outbound":
                                end_pos = (self.portLx, self.portLy - 12 * self.padding)
                                pygame.draw.line(self._screen, stack.image[h][w].group.colour,  start_pos, end_pos)
                            elif(not stack.image[h][w].group == None and not stack.image[h][w].group.ship == None):
                                end_pos = (ships[stack.image[h][w].group.ship.dock.name].rect.left + self.padding, ships[stack.image[h][w].group.ship.dock.name].rect.top + self.padding)
                                pygame.draw.line(self._screen, stack.image[h][w].group.colour,  start_pos, end_pos)
                            stack.image[h][w].new = False
                        elif stack.image[h][w].removed:
                            start_pos = (stacksX + stack.x * 3.85 * self.padding + w * cw, stacksY + stack.y * 25 * self.padding + h * ch)
                            gr = stack.image[h][w].pr_group
                            if (not gr == None) and gr.activity == "inbound":
                                end_pos = (self.portRx + 2 * self.padding, self.portLy - self.padding)
                                pygame.draw.line(self._screen, stack.image[h][w].getColour(gr, 3),  start_pos, end_pos)
                            elif(not gr == None and not gr.ship == None and gr.activity == "outbound" and gr.ship.status == "loading"):
                                end_pos = (ships[gr.ship.dock.name].rect.left + self.padding, ships[gr.ship.dock.name].topC+ ships[gr.ship.dock.name].cargo_height)
                                pygame.draw.line(self._screen, stack.image[h][w].getColour(gr, 3),  start_pos, end_pos)
                            stack.image[h][w].removed = False

    def exportNeStack(self, i, eStackLx, eStackLy, ships, exports, stack, counter):
        stacksX = eStackLx
        stacksY = eStackLy + 3 * self.width
        cw = int(0.28 * self.padding)
        ch = int(0.83 * self.padding)
        expCw = 2430
        expCh = 12200
        expHeight = 2590
        stack = stack
        file = open("Exports/export" + str(exports) + "_" + str(counter) + ".csv", "w+")
        for w in range(10):
            for h in range(28):
                if not stack.image[h][w].colour == pygame.Color(255, 255, 255):
                    x = str(int(w * expCw))
                    y = str(int(h * expCh))
                    colour = stack.image[h][w].group.colour
                    r = str(colour.r)
                    g = str(colour.g)
                    b = str(colour.b)
                    a = str(colour.a)
                    if stack.image[h][w].height >= 1:
                        file.write(x + ", " + y + ", " + str(0) + ", " + r + ", " + g + ", " + b + ", " + a + "\n")
                    if stack.image[h][w].height >= 2:
                        file.write(x + ", " + y + ", " + str(expHeight) + ", " + r + ", " + g + ", " + b + ", " + a + "\n")
                    if stack.image[h][w].height >= 3:
                        file.write(x + ", " + y + ", " + str(int(2 * expHeight)) + ", " + r + ", " + g + ", " + b + ", " + a + "\n")
                    if stack.image[h][w].height >= 4:
                        file.write(x + ", " + y + ", " + str(int(3 * expHeight)) + ", " + r + ", " + g + ", " + b + ", " + a + "\n")
                    if stack.image[h][w].height >= 5:
                        file.write(x + ", " + y + ", " + str(int(4 * expHeight)) + ", " + r + ", " + g + ", " + b + ", " + a + "\n")
        file.close()

    def checkPos(self, eStackLx, eStackLy, pos):
        stacksX = eStackLx
        stacksY = eStackLy
        cw = int(0.28 * self.padding)
        ch = int(0.83 * self.padding)

        dy = self.screen_height - 3 * self.padding
        dx1 = (int((self.screen_width/2) - 14 * self.padding))
        dx2 = dx1 + 27 * self.padding

        cx = 5 * self.padding
        cy1 = (int((self.screen_height/2) - 5 * self.padding))
        cy2 = cy1 + 20 * self.padding

        ex = 5 * self.padding
        ey1 = (int((self.screen_height/2) - 30 * self.padding))
        ey2 = ey1 + 20 * self.padding

        for i in range(self._port.nr_non_empty_stacks):
            for stack in self._port.ne_stacks:
                if stack.name == str(i):
                    if pygame.Rect(stacksX + stack.x * 3.9 * self.padding, stacksY + stack.y * 26 * self.padding, 10 * cw, 28 * ch).collidepoint(pos):
                        return stack, pos
        if pygame.Rect(dx1 - 3 * self.padding, dy - 1 * self.padding, 30 * self.padding, 2*self.padding).collidepoint(pos):
            return "dateThresh", pos
        if pygame.Rect(cx - 1 * self.padding, cy1 - 3 * self.padding, 2 * self.padding, 23*self.padding).collidepoint(pos):
            return "capacityThresh", pos
        if pygame.Rect(ex - 1 * self.padding, ey1 - 3 * self.padding, 2 * self.padding, 23*self.padding).collidepoint(pos):
            return "emptyC", pos
        return None, None

    def drawEStack(self, eStackLx, eStackLy, dateThreshold):
        cw = int(0.28 * self.padding)
        ch = int(0.83 *  self.padding)
        stack = self._port.e_stack
        for w in range (36):
            for h in range(15):
                if dateThreshold < 1:
                    height = stack.image[h][w].height
                    colour = stack.image[h][w].colour
                else:
                    height = stack.image[h][w].checkDates(self._port.date, dateThreshold)
                    if height > 5:
                        height = 5
                    colour = stack.image[h][w].getColour(stack.image[h][w].group, height)
                pygame.draw.rect(self._screen, colour, (eStackLx + w * ch, eStackLy + h * cw, ch, cw))

    def drawIso(self, rect, pos, stack, stacksX, stacksY, moving, scale, coordinates):
        sw = 10 * int(0.28 * self.padding)
        diffYl = int(scale * self.padding)
        diffXl = int(4.6 * diffYl)
        diffYr = int(0.2 * diffYl)
        diffXr = int(1.2 * diffYl)
        axoHeight = int(1.2 * diffYl)

        startX = int(0.928 * self.screen_width)
        startY = int(0.09 * self.screen_height)
        width = int(2.8 * self.padding)
        height = int(0.7 * self.padding)

        if moving:
            axoMCornerX = coordinates[0]
            axoMCornerY = coordinates[1]
        else:
            axoMCornerX = startX - 13 * diffXr
            axoMCornerY = startY + 28 * width

        if moving:
            sy = pos
        else:
            sy = int(28 * (pos[1] - rect.top)/(rect.bottom - rect.top))

        if sy > 25:
            sy = 25

        if moving:
            offset = 27
        else:
            offset = sy+2

        for i in range(30):
            if i == 27:
                y = sy + 1
            elif i == 28:
                y = sy + 2
            elif i == 1 or i%3 == 0:
                y = sy
            elif i == 2 or i%3 == 1:
                y = sy + 1
            elif i%3 == 2:
                y = sy + 2

            if i == 0 or i == 2 or i == 5:
                x = 9
            elif i == 1 or i == 4 or i == 8:
                x = 8
            elif i == 3 or i == 7 or i == 11:
                x = 7
            elif i == 6 or i == 10 or i == 14:
                x = 6
            elif i == 9 or i == 13 or i == 17:
                x = 5
            elif i == 12 or i == 16 or i == 20:
                x = 4
            elif i == 15 or i == 19 or i == 23:
                x = 3
            elif i == 18 or i == 22 or i == 26:
                x = 2
            elif i == 21 or i == 25 or i == 28:
                x = 1
            elif i == 24 or i == 27 or i == 29:
                x = 0

            if not stack.image[y][x].group == None:
                colourA = stack.image[y][x].getColour(stack.image[y][x].group, 5)
                colourB = stack.image[y][x].getColour(stack.image[y][x].group, 4)
                colourC = stack.image[y][x].getColour(stack.image[y][x].group, 3)
                if not colourA == pygame.Color(255, 255, 255):
                    axH = int(stack.image[y][x].height * axoHeight)
                    cornerA1x = axoMCornerX - (offset - y)*diffXl + x*diffXr
                    cornerA1y =  axoMCornerY - (offset - y)*diffYl - x*diffYr

                    cornerA1 = (cornerA1x, cornerA1y)
                    cornerA2 = (cornerA1x - diffXl, cornerA1y - diffYl)
                    cornerA3 = (cornerA1x - diffXl, cornerA1y - diffYl - axH)
                    cornerA4 = (cornerA1x, cornerA1y - axH)
                    cornerB1 = (cornerA1x + diffXr, cornerA1y - diffYr)
                    cornerB2 = (cornerA1x + diffXr, cornerA1y - diffYr - axH)
                    cornerC1 = (cornerA1x - diffXl + diffXr, cornerA1y - diffYl - diffYr - axH)

                    pygame.draw.polygon(self._screen, colourA, [cornerA1, cornerA2, cornerA3, cornerA4] )
                    pygame.draw.polygon(self._screen, colourB, [cornerA1, cornerA4, cornerB2, cornerB1] )
                    pygame.draw.polygon(self._screen, colourC, [cornerA4, cornerA3, cornerC1, cornerB2] )
        if not moving:
            rect2 = pygame.Rect(rect.left, rect.top + sy * int(0.83 * self.padding), sw, 3 * int(0.83 * self.padding))
            pygame.draw.rect(self._screen, pygame.Color(0,0,0), rect2, 1)

    def drawAllAxo(self, eStackLx, eStackLy):
        diffYl = int( self.padding)
        diffXl = int(4.6 * diffYl)
        diffYr = int(0.2 * diffYl)
        diffXr = int(1.2 * diffYl)

        baseX1 = self.screen_width/3 - self.padding
        baseY1 = self.screen_height/2 + 2 * self.padding

        baseX2 = baseX1 + 9 * diffXl
        baseY2 = baseY1 + 9 * diffYl

        stacksX = eStackLx
        stacksY = eStackLy + 3 * self.width
        sw = 10 * int(0.28 * self.padding)
        sh = 28 * int(0.83 * self.padding)
        order = [7,6,5,4,3,2,1,0,15,14,13,12,11,10,9,8]
        for i in order:
            for stack in self._port.ne_stacks:
                if int(stack.name) == i:
                    rect = pygame.Rect(stacksX + stack.x * 3.9 * self.padding, stacksY + stack.y * 26 * self.padding, sw, sh)
                    for i in range(9):
                        if int(stack.name) < 8:
                            self.drawIso(rect, i*3, stack, stacksX, stacksY, True, 0.3, [baseX1 + int(stack.name) * 5 * diffXr, baseY1 - int(stack.name) * 5 * diffYr])
                        else:
                            self.drawIso(rect, i*3, stack, stacksX, stacksY, True, 0.3, [baseX2 + (int(stack.name)-8) * 5 * diffXr, baseY2 - (int(stack.name)-8) * 5 * diffYr])

    def drawNeSection(self, i, eStackLx, eStackLy):
        stacksX = eStackLx
        stacksY = eStackLy + 3 * self.width
        sw = 10 * int(0.28 * self.padding)
        sh = 28 * int(0.83 * self.padding)
        width = int(2.8 * self.padding)
        height = int(0.7 * self.padding)
        startX = int(0.928 * self.screen_width)
        startY = int(0.09 * self.screen_height)


        diffYl = self.padding
        diffXl = int(4.6 * diffYl)
        diffYr = int(0.2 * diffYl)
        diffXr = int(1.2 * diffYl)
        axoHeight = int(1.2 * diffYl)

        axoMCornerX = startX - 13 * diffXr
        axoMCornerY = startY + 28 * width

        for stack in self._port.ne_stacks:
            if stack.name == str(i):
                rect = pygame.Rect(stacksX + stack.x * 3.9 * self.padding, stacksY + stack.y * 26 * self.padding, sw, sh)
                pos = pygame.mouse.get_pos()
                if rect.collidepoint(pos):
                    for i in range(28):
                        for j in range(5):
                            if not stack.image[i][4-j].group == None:
                                colour = stack.image[i][4-j].getColour(stack.image[i][4-j].group, j+1)
                                if not colour == pygame.Color(255, 255, 255):
                                    pygame.draw.rect(self._screen, colour, (startX, startY + i * width, stack.image[i][4-j].height * height, width) )
                                    text = str(len(stack.containers))
                                    cInStack = myfont.render(text, False, (0,0,0))
                                    self._screen.blit(cInStack, (startX, startY - int(2.5 * self.padding)))
                    self.drawIso(rect, pos, stack, stacksX, stacksY, False, 1 , 0)
                    self.showContent(pos, stack,stacksX, stacksY)

    def showContent(self, pos, stack, stacksX, stacksY):
        contents = []
        w = int(0.28 * self.padding)
        h = int(0.83 * self.padding)
        sx = stacksX + stack.x * 3.9 * self.padding
        sy = stacksY + stack.y * 26 * self.padding
        px = pos[0] - sx
        py = pos[1] - sy
        cx = int((px/w)//1)
        cy = int((py/h)//1)
        if cx < 0:
            cx = 0
        if cy < 0:
            cy = 0
        pygame.draw.rect(self._screen, pygame.Color(255, 0, 0), (stacksX + stack.x * 3.9 * self.padding + cx * w, stacksY + stack.y * 26 * self.padding + cy * h, w, h))
        contents = stack.image[cy][cx].contents
        if not len(contents) == 0:
            content = contents[-1]
        else:
            content = ""
        if not content == "":
            ContentImage = self.Background("Contents/" + content + ".png", [3* self.padding, 3 * self.padding])
            self._screen.blit(ContentImage.image, ContentImage.rect)

    def printGroups(self, group):
        return str(": " + str(len(group.containers)))

    def dateCounter(self):
        totContainers = self._port.nr_containers.counter
        date = int(totContainers / 1500000 * 365)
        hour = int((totContainers / 1500000 * 365) * 24 - date * 24)
        dateText = myfont.render("Day " + str(date) + ", Hour " + str(hour), False, (0,0,0))
        self._screen.blit(dateText, (int((self.screen_width/2) - 14 * self.padding), self.screen_height - 10 * self.padding))
        self._port.date = date*24 + hour

    def dateThresholdF(self, pos):
        x1 = (int((self.screen_width/2) - 14 * self.padding))
        val = ((pos[0] - x1) / (27*self.padding)) * 240
        if val < 0:
            val = 0
        return val

    def capacityThresholdF(self, pos):
        y1 = (int((self.screen_height/2) - 5 * self.padding))
        val = ((pos[1] - y1) / (20*self.padding)) * 3999 + 1001
        if val < 1001:
            val = 1001
        return val

    def emptyCF(self, pos):
        y1 = (int((self.screen_height/2) - 30 * self.padding))
        val = ((pos[1] - y1) / (20*self.padding)) * 100
        if val < 0:
            val = 0
        return val

    def dateSlider(self, dateThresholdText, dateThreshold):
        y = self.screen_height - 3 * self.padding
        x1 = (int((self.screen_width/2) - 14 * self.padding))
        x2 = x1 + 27 * self.padding
        self._screen.blit(dateThresholdText, (x1, y - 3 * self.padding))
        pygame.draw.line(self._screen, pygame.Color('black'),  (x1, y), (x2, y))
        pygame.draw.circle(self._screen, False, (int(x1 + (dateThreshold/240) * 27 * self.padding), y), self.padding)
        hourSliderText = myfont.render(str(int(dateThreshold)), False, (0,0,0))
        self._screen.blit(hourSliderText, (int(x1 + (dateThreshold/240) * 27 * self.padding), y + self.padding))

    def capacitySlider(self, capacityText, capacityUpperBound):
        x = 5 * self.padding
        y1 = (int((self.screen_height/2) - 5 * self.padding))
        y2 = y1 + 20 * self.padding
        self._screen.blit(capacityText, (x - 4 * self.padding, y1 - 3 * self.padding))
        pygame.draw.line(self._screen, pygame.Color('black'),  (x, y1), (x, y2))
        pygame.draw.circle(self._screen, False, (x, int(y1 + ((capacityUpperBound-1001)/4000) * 20 * self.padding)), self.padding)
        capacitySliderText = myfont.render(str(int(capacityUpperBound)), False, (0,0,0))
        self._screen.blit(capacitySliderText, (x + int(1.5*self.padding), int(y1 - self.padding  + (capacityUpperBound-1001)/4000 * 20 * self.padding)))

    def emptyCSlider(self, emptyChanceText, emptyChance):
        x = 5 * self.padding
        y1 = (int((self.screen_height/2) - 30 * self.padding))
        y2 = y1 + 20 * self.padding
        self._screen.blit(emptyChanceText, (x - 4 * self.padding, y1 - 3 * self.padding))
        pygame.draw.line(self._screen, pygame.Color('black'),  (x, y1), (x, y2))
        pygame.draw.circle(self._screen, False, (x, int(y1 + (emptyChance/100) * 20 * self.padding)), self.padding)
        emptyCSliderText = myfont.render(str(int(emptyChance))+"%", False, (0,0,0))
        self._screen.blit(emptyCSliderText, (x + int(1.5*self.padding), int(y1 - self.padding  + (emptyChance/100) * 20 * self.padding)))


    def display(self):
        clock = pygame.time.Clock()
        self._screen.fill(pygame.Color('white'))
        self.draw_screen(self._screen)

        dateThreshold = 0
        dateThresholdText = myfont.render("Stationary in hours: ", False, (0,0,0))

        capacityUpperBound = 3000
        capacityText = myfont.render("Max capacity: ", False, (0,0,0))

        emptyChance = 20
        emptyChanceText = myfont.render("Empty %: ", False, (0,0,0))

        minEmptyContainers = 0
        prevEmptyContainers = 0

        padding = self.padding
        width = self.width
        height = self.height

        portLx = self.portLx
        portLy = self.portLy
        portRx = self.portRx
        portRy = self.portRy
        portWidth = portRx - portLx
        portHeight = portRy - portLy
        eStackLx = portLx + padding
        eStackLy = portLy + padding
        eStackRx = portRx - padding
        eStackRy = eStackLy + 3 * width
        ship1x = portLx - int(4.3 * padding)
        ship1y = int(eStackRy + 2.5 * width)

        Background = self.Background('background2560.png', [0,0])
        Cars = []
        for i in range(11):
            Cars.append(self.Background(str('Cars/' + str(i) + '.png'), [0,0]))

        ThreadingImage = self.Background('threading.png', [155,10])
        StackingImage = self.Background('StackingAlgorithm.png', [130,10])
        EmptyStackImage = self.Background('EmptyStack.png', [40,8])
        axoBackground = self.Background('axoBackground2560.png', [0,0])

        ships = []
        ship1 = self.Ship('Ship2560.png', [0,0], [ship1x, ship1y],
                [ship1x - 9 * padding, self.screen_height], self._screen)
        ships.append(ship1)
        ship2 = self.Ship('Ship2560.png', [0,0], [ship1x, ship1y + height],
                [ship1x - 6 * padding, self.screen_height], self._screen)
        ships.append(ship2)
        ship3 = self.Ship('Ship2560.png', [0,0], [ship1x, ship1y + 2 * height],
                [ship1x - 3 * padding, self.screen_height], self._screen)
        ships.append(ship3)
        ship4 = self.Ship('Ship2560.png', [0,0], [ship1x + portWidth + int(7.3 * padding), ship1y + 0.4 * height],
                [ship1x + portWidth + int(16.3 * padding), self.screen_height], self._screen)
        ships.append(ship4)
        ship5 = self.Ship('Ship2560.png', [0,0], [ship1x + portWidth + int(7.3 * padding), ship1y + 1.4 * height],
                [ship1x + portWidth + int(13.3 * padding), self.screen_height], self._screen)
        ships.append(ship5)
        ship6 = self.Ship('Ship2560.png', [0,0], [ship1x + portWidth + int(7.3 * padding), ship1y + 2.4 * height],
                [ship1x + portWidth + int(10.3 * padding), self.screen_height], self._screen)
        ships.append(ship6)
        ship7 = self.Ship('Ship2560.png', [0,0], [ship1x + portWidth + int(7.3 * padding), ship1y + 3.4 * height],
                [ship1x + portWidth + int(7.3 * padding), self.screen_height], self._screen)
        ships.append(ship7)

        car = 0
        exports = 0
        exp_handled = False
        counter = 0
        clicked = None
        file = ''

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            self._screen.fill([255, 255, 255])
            self._screen.blit(Background.image, Background.rect)
            self._screen.blit(Cars[car].image, Cars[car].rect)

            grHeader = myfont.render("Groups:", False, (0,0,0))
            self._screen.blit(grHeader, (int(1.5 * self.padding), int(0.67 * self.screen_height)))

            for group in self._groups:
                text = self.printGroups(group)
                groupText = myfont.render(text, False, (0,0,0))
                self._screen.blit(groupText, (3 * self.padding, 2 * group.name * self.padding + 2 * self.padding + int(0.67 * self.screen_height)))
                pygame.draw.rect(self._screen, colours[group.name], (int(1.5 * self.padding), 2 * group.name * self.padding + int(2.1 * self.padding) + int(0.67 * self.screen_height), self.padding, int(1.5 * self.padding)))

            for i in range(len(ships)):
                ships[i].update(self._port.docks[i])

            self.drawEStack(eStackLx, eStackLy, dateThreshold)

            for i in range(self._port.nr_non_empty_stacks):
                self.drawNeStack(i, eStackLx, eStackLy, ships, dateThreshold)

            for i in range(self._port.nr_non_empty_stacks):
                self.drawNeSection(i, eStackLx, eStackLy)

            if pygame.Rect(portLx - 10 * self.padding, 0, 20 * self.padding, portLy).collidepoint(pygame.mouse.get_pos()):
                self._screen.blit(StackingImage.image, StackingImage.rect)

            if pygame.Rect(2 * self.padding, int(0.67 * self.screen_height), 10 * self.padding, int(0.25 * self.screen_height)).collidepoint(pygame.mouse.get_pos()):
                self._screen.blit(ThreadingImage.image, ThreadingImage.rect)

            if clicked == None:
                if pygame.mouse.get_pressed()[0]:
                    clicked, pos = self.checkPos(eStackLx, eStackLy, pygame.mouse.get_pos())
                    exp_handled = pygame.mouse.get_pressed()[0]
            elif clicked == "dateThresh":
                dateThreshold = self.dateThresholdF(pos)
                clicked = None
            elif clicked == "capacityThresh":
                capacityUpperBound = self.capacityThresholdF(pos)
                self._port.max_capacity = int(capacityUpperBound)
                clicked = None
            elif clicked == "emptyC":
                emptyChance = self.emptyCF(pos)
                self._port.emptyC = int(emptyChance)
                clicked = None
            else:
                stack = clicked
                cText = myfont.render(str(counter), False, (0,0,0))
                self._screen.blit(cText, (20, 20))
                if counter < 100:
                    for i in range(self._port.nr_non_empty_stacks):
                        self.exportNeStack(i, eStackLx, eStackLy, ships, exports, stack, counter)
                    counter +=1
                elif counter == 100:
                    counter = 0
                    exports +=1
                    clicked = None

            self.dateCounter()

            self.dateSlider(dateThresholdText, dateThreshold)

            self.capacitySlider(capacityText, capacityUpperBound)

            self.emptyCSlider(emptyChanceText, emptyChance)

            if prevEmptyContainers > len(self._port.e_stack.containers) and minEmptyContainers == 0 and self._port.date > 240:
                minEmptyContainers = len(self._port.e_stack.containers)

            prevEmptyContainers = len(self._port.e_stack.containers)

            if len(self._port.e_stack.containers) < minEmptyContainers:
                minEmptyContainers = len(self._port.e_stack.containers)

            cw = int(0.28 * self.padding)
            ch = int(0.83 *  self.padding)
            if pygame.Rect(eStackLx, eStackLy, ch * 35, cw * 15).collidepoint(pygame.mouse.get_pos()):
                minEConText = myfont.render(str(minEmptyContainers), False, (0,0,0))
                EconNr = myfont.render(str(len(self._port.e_stack.containers)), False, (0,0,0))
                self._screen.blit(EmptyStackImage.image, EmptyStackImage.rect)
                self._screen.blit(minEConText, (31 * self.padding, 5 * self.padding))
                self._screen.blit(EconNr, (eStackLx - 7 * self.padding, eStackLy))

            if pygame.Rect(self.screen_width - 9 * self.padding, self.screen_height - 5 * self.padding, 5 * self.padding,  5 * self.padding).collidepoint(pygame.mouse.get_pos()):
                self._screen.blit(axoBackground.image, axoBackground.rect)
                self.drawAllAxo(eStackLx, eStackLy)

            pygame.display.update()
            if car < 10:
                car += 1
            else:
                car = 0
            clock.tick(200)
