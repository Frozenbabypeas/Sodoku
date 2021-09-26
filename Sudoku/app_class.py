import pygame, sys, requests
import pygame, sys
import requests
from bs4 import BeautifulSoup
from settings import *
from buttonclass import *

#initialise the game
class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.grid = finishedBoard
        self.selected = None
        self.mousePos = None
        self.state = "playing"
        self.finished = False
        self.cellChanged = False
        self.playingbuttons = []
        self.lockedCells = []
        self.incorrectCells = []
        self.font = pygame.font.SysFont("comicsansms", cellsize//2)
        self.grid = []
        self.load()

        pygame.display.set_caption("Sudoku")
        icon = pygame.image.load("Sudoku\Digital.png")
        pygame.display.set_icon(icon)
        
#initialise the loop so the game doesn't close straight away
    def run(self):
        while self.running:
            if self.state == "playing":
                self.playing_events()
                self.playing_update()
                self.playing_draw()
        pygame.quit()
        sys.exit()

#update the game on changes        
    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            #user clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouseongrid()
                if selected:
                    self.selected = selected
                else: #if mouse if off the grid, check to see if mouse is on a button
                    self.selected = None
                    for button in self.playingbuttons:
                        if button.highlighted:
                            button.click()

            #user types
            if event.type == pygame.KEYDOWN:
                if self.selected != None and self.selected not in self.lockedCells:
                    if self.isInt(event.unicode):
                        #cell changed
                        self.grid[self.selected[1]][self.selected[0]] = int(event.unicode)
                        self.cellChanged = True

    def playing_update(self):
        self.mousePos = pygame.mouse.get_pos()
        for button in self.playingbuttons:
            button.update(self.mousePos)

        #check to see if board has been filled in to finsih the game
        if self.cellChanged:
            self.incorrectCells = []
            if self.allCellsDone():
                #check if board is correct
                self.checkAllCells()
                if len(self.incorrectCells) == 0:
                    self.finished = True
    
#draw the background
    def playing_draw(self):
        self.window.fill(WHITE)

        #drawing the buttons
        for button in self.playingbuttons:
            button.draw(self.window)

        #drawing the grid
        if self.selected:
            self.drawSelection(self.window, self.selected) 
        
        self.shadeLockedCells(self.window, self.lockedCells)
        self.shadeIncorrectCells(self.window, self.incorrectCells)
        self.drawnumbers(self.window)
        self.drawgrid(self.window)
        pygame.display.update()    
        self.cellChanged = False

#board checking functions
    def allCellsDone(self):
        for row in self.grid:
            for number in row:
                if number == 0:
                    return False
        return True    

    def checkAllCells(self):
        self.checkRows()
        self.checkCols()
        self.checkSmallGrid()

    def checkSmallGrid(self):
        for x in range(3):
            for y in range(3):
                possibles = [1,2,3,4,5,6,7,8,9]
                #print("re-setting possibles")
                for i in range(3):
                    for j in range (3):
                        #print(x * 3 + i, y * 3 + j)
                        xidx = x * 3 + i
                        yidx = y * 3 + j
                        if self.grid[yidx][xidx] in possibles:
                            possibles.remove(self.grid[yidx][xidx])
                        else:
                            if [xidx, yidx] not in self.lockedCells and [xidx, yidx] not in self.incorrectCells:
                                self.incorrectCells.append([xidx, yidx])
                            if [xidx, yidx] in self.lockedCells:
                                for k in range(3):
                                    for l in range (3):
                                        xidx2 = x * 3 + k
                                        yidx2 = y * 3 + l
                                        if self.grid[yidx2][xidx2] == self.grid[yidx][xidx] and [xidx2, yidx2] not in self.lockedCells:
                                            self.incorrectCells.append([xidx2, yidx2])


    def checkRows(self):
        for yidx, row in enumerate(self.grid):
            possibles = [1,2,3,4,5,6,7,8,9]
            for xidx in range(9):
                if self.grid[yidx][xidx] in possibles:
                    possibles.remove(self.grid[yidx][xidx])
                else:
                    if [xidx, yidx] not in self.lockedCells and [xidx, yidx] not in self.incorrectCells:
                        self.incorrectCells.append([xidx, yidx])
                    if [xidx,yidx] in self.lockedCells:
                        for k in range(9):
                            if self.grid[yidx][k] == self.grid[yidx][xidx] and [k, yidx] not in self.lockedCells:
                                self.incorrectCells.append([k, yidx])

    def checkCols(self):
        for xidx in range(9):
            possibles = [1,2,3,4,5,6,7,8,9]
            for yidx, row in enumerate(self.grid):
                if self.grid[yidx][xidx] in possibles:
                    possibles.remove(self.grid[yidx][xidx])
                else:
                    if [xidx, yidx] not in self.lockedCells and [xidx, yidx] not in self.incorrectCells:
                        self.incorrectCells.append([xidx, yidx])
                    if [xidx, yidx] in self.lockedCells:
                        for k, row in enumerate(self.grid):
                            if self.grid[k][xidx] == self.grid[yidx][xidx] and [xidx, k] not in self.lockedCells:
                                self.incorrectCells.append([xidx, k])

#difficulties in game
    def getPuzzle(self, difficulty):
        #difficulty passed in as a string with one digit, 1 to 4
        html_doc = requests.get("https://nine.websudoku.com/?level={}".format(difficulty)).content
        soup = BeautifulSoup(html_doc, 'html.parser')
        ids = ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 
        'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 
        'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 
        'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 
        'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 
        'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 
        'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68', 
        'f70', 'f71', 'f72', 'f73', 'f74', 'f75', 'f76', 'f77', 'f78', 
        'f80', 'f81', 'f82', 'f83', 'f84', 'f85', 'f86', 'f87', 'f88']
        data = []
        for cid in ids:
            data.append(soup.find("input", id = cid))
        board = [[0 for x in range (9)] for x in range (9)]
        for index, cell in enumerate(data):
                try:
                    board[index//9][index % 9] = int(cell["value"])
                except:
                    pass
        self.grid = board
        self.load()

#draw locked cells
    def shadeIncorrectCells(self, window, locked):
        for cell in locked:
            pygame.draw.rect(window, INCORRECTCELLCOLOUR, (cell[0] * cellsize + gridPos[0], cell[1] * cellsize + gridPos[1], cellsize, cellsize))

    def shadeLockedCells(self, window, locked):
        for cell in locked:
            pygame.draw.rect(window, LOCKEDCELLCOLOUR, (cell[0] * cellsize + gridPos[0], cell[1] * cellsize + gridPos[1], cellsize, cellsize))

#draw numbers
    def drawnumbers(self, window):
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num != 0:
                    pos = [xidx * cellsize + gridPos[0], yidx * cellsize + gridPos[1]]
                    self.textToscreen(window, str(num), pos)

#mouse click selection
    def drawSelection(self, window, pos):
        pygame.draw.rect(window, LIGHTBLUE, ((pos[0] * cellsize) + gridPos[0], (pos[1] * cellsize) + gridPos[1], cellsize, cellsize))

#draw the grid
    def drawgrid(self, window):
        pygame.draw.rect(window, BLACK, (gridPos[0], gridPos[0], WIDTH -150, HEIGHT - 150), 4)
        for x in range(9):
            pygame.draw.line(window, BLACK, (gridPos[0] + (x * cellsize), gridPos[0]), (gridPos[0] + (x * cellsize), gridPos[0] + 450), 2 if x %3 == 0 else 1) #vertical lines with padding after 3
            pygame.draw.line(window, BLACK, (gridPos[0], gridPos[0] + (x * cellsize)), (gridPos[0] + 450, gridPos[0] + (x * cellsize)), 2 if x %3 == 0 else 1) #horiztonal lines with padding after 3

#defining grid level with mouse click
    def mouseongrid(self):
        if self.mousePos[0] <gridPos[0] or self.mousePos[1] < gridPos[1]:
            return False
        if self.mousePos[0] > gridPos[0] + gridsize or self.mousePos[1] > gridPos[1] + gridsize:
            return False
        return ((self.mousePos[0] - gridPos[0])//cellsize, (self.mousePos[1] - gridPos[1])//cellsize)

#button build    
    def loadbuttons(self):
        self.playingbuttons.append(button(  20, 40, WIDTH//7, 40,
                                            function=self.checkAllCells,
                                            colour=(27,142,207),
                                            text="Check"))
        self.playingbuttons.append(button(  140, 40, WIDTH//7, 40,
                                            colour=(117,172,112),
                                            function=self.getPuzzle,
                                            params="1",
                                            text="Easy"))
        self.playingbuttons.append(button(  WIDTH//2-(WIDTH//7)//2, 40, WIDTH//7, 40,
                                            colour=(204,197,110),
                                            function=self.getPuzzle,
                                            params="2",
                                            text="Medium"))
        self.playingbuttons.append(button(  380, 40, WIDTH//7, 40,
                                            colour=(199,129,48),
                                            function=self.getPuzzle,
                                            params="3",
                                            text="Hard"))
        self.playingbuttons.append(button(  500, 40, WIDTH//7, 40,
                                            colour=(207,68,68),
                                            function=self.getPuzzle,
                                            params="4",
                                            text="Evil"))

#number build
    def textToscreen(self, window, text, pos):
        font = self.font.render(text, False, BLACK)
        fontWidth = font.get_width()
        fontHeight = font.get_height()
        pos[0] += (cellsize - fontWidth)//2
        pos[1] += (cellsize - fontHeight)//2
        window.blit(font, pos)

    def load(self):
        self.playingbuttons = []
        self.loadbuttons()
        self.lockedCells = []
        self.incorrectCells = []
        self.finished = False

        #setting locked cells from original board
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num != 0:
                    self.lockedCells.append([xidx,yidx])
    
    #check to see if input is an integrer
    def isInt(self, string):
        try:
            int(string)
            return True
        except:
            return False