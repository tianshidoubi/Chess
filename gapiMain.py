
import pygame
import ctypes

from collections import deque
from time import clock as clk

def ImgLoad(name):
    return pygame.image.load("Textures/"+name)

class GAPIError(Exception):
    pass

class Global:
    SCREEN_SIZE = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)

class Event:
    reject = False
    def __init__(self, name):
        self.name = name
        self.reject = False

    def Cancel(self):
        self.reject = True

    def Rejected(self):
        return self.reject

class dWorld:
    # Engine Vars
    screenStack = deque
    selectStack = deque
    mouseStack = deque
    flush = list()
    # Screen Vars
    fps = 10
    frame = 0
    screen = pygame.Surface
    caption = "pygameWindow"
    background = pygame.image.load("gapi/deftex.png")
    icon = pygame.image.load("gapi/icon32.png")
    size = (256, 256)
    done = False
    exitKeys = (269, 27)

    def OnExitTry(self, e):
        pass

    def OnExit(self):
        pygame.display.quit()

    def OnClick(self, mPos, mKey):
        self.EngineClick(mPos, mKey)

    def OnMouseUp(self, mPos, mKey):
        pass

    def OnKeyDown(self, kKey):
        print(kKey)

    def OnKeyUp(self, kKey):
        pass

    def OnFrame(self):
        pass

    def OnLogic(self):
        pass

    def PreInit(self):
        pass

    def PostInit(self):
        pass

    def OnFlush(self):
        for item in self.flush:
            if item[1] == "l":
                getattr(self, item[0]).append(item[2])
            elif item[1] == "r":
                getattr(self, item[0]).appendleft(item[2])
            else:
                raise GAPIError("Cannot flush with direction {}"
                                .format(item[2]))
        dWorld.flush = set()
        
    def EngineClick(self, mPos, mKey):
        CLK_EVE = Event("MOUSE_CATCH")
        for item in self.selectStack:
            if item.ThisInside(mPos):
                item.OnClick(mPos, mKey)
        return True

    def CheckForExit(self, kKey):
        for key in self.exitKeys:
            if int(key) == int(kKey):
                self.done = True

    def Blit(self):
        for item in self.screenStack:
            item.Update()
            item.Draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYDOWN:
                self.OnKeyDown(event.key)
                self.CheckForExit(event.key)
            elif event.type == pygame.KEYUP:
                self.OnKeyUp(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.OnClick(pygame.mouse.get_pos(), event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.OnMouseUp(pygame.mouse.get_pos(), event.button)

    def flip():
        pygame.display.flip()
    
    def Init(self):
        self.PreInit()
        self.screenStack = deque()
        self.selectStack = deque()
        self.mouseStack = deque()
        self.screen = pygame.display.set_mode(self.size)
        Element.surface = self.screen
        pygame.display.set_caption(self.caption)
        pygame.display.set_icon(self.icon)
        pygame.init()
        pygame.font.init()

    def Run(self):
        self.Init()
        clock = pygame.time.Clock()
        Element((0, 0), self.background)
        self.PostInit()
        while True:
            clock.tick(self.fps)
            self.OnFlush()
            self.Blit()
            self.OnFrame()
            dWorld.flip()
            self.frame += 1
            if self.done:
                EXE_EVE = Event("EXIT")
                self.OnExitTry(EXE_EVE)
                if not EXE_EVE.Rejected():
                    self.OnExit()
                    break

    def Time(self):
        return self.frames / self.fps
    
class Element:
    surface = pygame.Surface
    pos = tuple
    size = tuple
    _texture = pygame.Surface
    points = tuple
    render = True
    select = False
    mouse = False
    def __init__(self, pos, texture):
        self.pos = pos
        self.texture = texture
        self.Init()
        
    def OnClick(self, mPos, mKey):
        pass

    def ThisInside(self, mPos):
        if mPos[0] > self.pos[0] and mPos[0] < self.pos[0] + self.size[0]:
            if mPos[1] > self.pos[1] and mPos[1] < self.pos[1] + self.size[1]:
                return True
        return False

    def Init(self):
        self.OnChange()
        dWorld.flush.append(("screenStack", "l", self))
        if self.select:
            dWorld.flush.append(("selectStack", "r", self))
        if self.mouse:
            dWorld.flush.append(("mouseStack", "r", self))

    def OnChange(self):
        self.size = self.texture.get_size()

    def Update(self):
        pass

    def Draw(self):
        if self.render:
            Element.surface.blit(self.texture, self.pos)

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, texture):
        self._texture = texture
        self.OnChange()

    @staticmethod
    def getSurface(size, col):
        surf = pygame.Surface(size)
        surf.fill(col)
        return surf

    @staticmethod
    def flattenTier(tier):
        pass


































