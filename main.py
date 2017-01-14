from gapiMain import *

#Graphics
SPACING = 64
X_ROW = 8
Y_ROW = 8

#Textures
RED = ImgLoad("Red.png")
CYAN = ImgLoad("Cyan.png")

#Codes
EDGE = 0
FOE  = 1
FREE = 2
FRI  = 3
OPEN = (FOE, FREE)

#Keys
M_SELECT = 1

def PosToTup(pos):
    return (pos[0]//SPACING, pos[1]//SPACING)

class World(dWorld):
    # Screen Vars
    this = None
    caption = "Chess"
    size = (X_ROW*SPACING, Y_ROW*SPACING)
    done = False
    exitKeys = (269,)
    def __init__(self):
        World.this = self
        self.fps = 25
        self.player = -1
        self.selected = None
        self.board = set()
        self.markers = set()
        self.active = set()
        
    def PostInit(self):
        self.GenPawns()
        self.GenKnights()
        self.GenRooks()
        self.GenBishops()
        self.GenQueens()
        self.GenKings()
        self.GenMarkers()

    def OnKeyDown(self, kKey):
        if kKey == 27:
            self.selected = None
            self.ClearMarkers()

    def OnClick(self, mPos, mKey):
        if mKey == M_SELECT:
            if self.selected == None:
                self.ClearMarkers()
                self.EngineClick(mPos, mKey)
                self.SetMarkers()
                return
            x, y = PosToTup(mPos)
            p = self.PieceAt(self.player, x, y)
            if (x, y) in self.selected.valid:
                if p == FOE:
                    self.KillAt(x, y)
                self.selected.Move(x, y)
                self.SwitchPlayer()
                self.ClearMarkers()
            if p == FRI:
                self.ClearMarkers()
                self.selected = self.GetAt(x, y)
                self.SetMarkers()

    def PieceAt(self, n, x, y):
        if x > X_ROW or x < 0 or y > Y_ROW or y < 0:
            return EDGE
        for piece in self.board:
            if (piece.x, piece.y) == (x, y):
                if n == piece.owner:
                    return FRI
                return FOE
        return FREE

    def KillAt(self, x, y):
        for piece in self.board:
            if (piece.x, piece.y) == (x, y):
                piece.Dead()

    def GetAt(self, x, y):
        for piece in self.board:
            if (piece.x, piece.y) == (x, y):
                return piece

    def IsKingSafeAt(self, n, x, y):
        for piece in self.board:
            if piece.owner != n:
                if (x, y) in piece.valid:
                    return False
        return True

    def SwitchPlayer(self):
        self.selected = None
        self.player = -self.player

    def SetMarkers(self):
        tmp = set()
        if self.selected != None:
            for item, marker in zip(self.selected.valid, self.markers):
                tmp.add(marker)
                marker.render = True
                marker.pos = item[0]*SPACING, item[1]*SPACING
                p = self.PieceAt(self.selected.owner, item[0], item[1])
                if p == FREE:
                    marker.texture = CYAN
                elif p == FOE:
                    marker.texture = RED
                self.active.add(marker)
        for item in tmp:
            self.markers.remove(item)
            
    def ClearMarkers(self):
        tmp = set()
        for marker in self.active:
            tmp.add(marker)
            marker.render = False
            self.markers.add(marker)
        for item in tmp:
            self.active.remove(item)

    def GenPawns(self):
        for n, y in zip((1, -1), (1, X_ROW-2)):
            for x in range(X_ROW):
                self.board.add(Pawn(n, x, y))

    def GenKnights(self):
        self.board.add(Knight( 1, 1, 0))
        self.board.add(Knight( 1, 6, 0))
        self.board.add(Knight(-1, 1, 7))
        self.board.add(Knight(-1, 6, 7))

    def GenRooks(self):
        self.board.add(Rook( 1, 0, 0))
        self.board.add(Rook( 1, 7, 0))
        self.board.add(Rook(-1, 0, 7))
        self.board.add(Rook(-1, 7, 7))

    def GenBishops(self):
        self.board.add(Bishop( 1, 2, 0))
        self.board.add(Bishop( 1, 5, 0))
        self.board.add(Bishop(-1, 2, 7))
        self.board.add(Bishop(-1, 5, 7))

    def GenQueens(self):
        self.board.add(Queen( 1, 3, 0))
        self.board.add(Queen(-1, 4, 7))        

    def GenKings(self):
        self.board.add(King( 1, 4, 0))
        self.board.add(King(-1, 3, 7))
        
    def GenMarkers(self):
        for i in range(32):
            marker = Element((-64, -64), RED)
            marker.render = False
            self.markers.add(marker)

class Piece(Element):
    isNew = True
    select = True
    def __init__(self, owner, x, y):
        self.owner = owner
        if owner == -1:
            self.texture = self.wtexture
        elif owner == 1:
            self.texture = self.btexture
        self.x = x
        self.y = y
        self.pos = (x*SPACING, y*SPACING)
        self.Init()

    def OnClick(self, mPos, mKey):
        if mKey == M_SELECT and self.owner == World.this.player:
            World.this.selected = self

    def Update(self):
        self.SetValid()

    def Move(self, x, y):
        self.x = x
        self.y = y
        self.pos = (x*SPACING, y*SPACING)
        self.isNew = False

    def Dead(self):
        self.render = False
        self.x = -1
        self.y = -1
        self.pos = (-1*SPACING, -1*SPACING)

class Pawn(Piece):
    wtexture = ImgLoad("PawnWhite.png")
    btexture = ImgLoad("PawnBlack.png")
    def SetValid(self):
        self.valid = set()
        self.Front()
        self.Flanks()

    def Front(self):
        x, y = self.x, self.y+self.owner
        p = World.this.PieceAt(self.owner, x, y)
        if p == FREE:
            self.valid.add((x, y))
            if self.isNew:
                x, y = self.x, self.y+self.owner*2
                p = World.this.PieceAt(self.owner, x, y)
                if p == FREE:
                    self.valid.add((x, y))

    def Flanks(self):
        x, y = self.x-1, self.y+self.owner
        p = World.this.PieceAt(self.owner, x, y)
        if p == FOE:
            self.valid.add((x, y))
        x, y = self.x+1, self.y+self.owner
        p = World.this.PieceAt(self.owner, x, y)
        if p == FOE:
            self.valid.add((x, y))

class Knight(Piece):
    wtexture = ImgLoad("KnightWhite.png")
    btexture = ImgLoad("KnightBlack.png")
    def SetValid(self):
        self.valid = set()
        for x, y in zip((-1, 1, 2, 2, -1, 1, -2, -2), (2, 2, 1, -1, -2, -2, -1, 1)):
            p = World.this.PieceAt(self.owner, self.x+x, self.y+y)
            if p == FREE or p == FOE:
                self.valid.add((self.x+x, self.y+y))

class Rook(Piece):
    wtexture = ImgLoad("RookWhite.png")
    btexture = ImgLoad("RookBlack.png")
    def SetValid(self):
        self.valid = set()
        for x, y in zip((-1, 1, 0, 0), (0, 0, -1, 1)):
            p = World.this.PieceAt(self.owner, self.x+x, self.y+y)
            n = 1
            while p == FREE:
                self.valid.add((self.x+(x*n), self.y+(y*n)))
                n += 1
                p = World.this.PieceAt(self.owner, self.x+(x*n), self.y+(y*n))
            if p == FOE:
                self.valid.add((self.x+(x*n), self.y+(y*n)))

class Bishop(Piece):
    wtexture = ImgLoad("BishopWhite.png")
    btexture = ImgLoad("BishopBlack.png")
    def SetValid(self):
        self.valid = set()
        for x, y in zip((-1, 1, -1, 1), (1, 1, -1, -1)):
            p = World.this.PieceAt(self.owner, self.x+x, self.y+y)
            n = 1
            while p == FREE:
                self.valid.add((self.x+(x*n), self.y+(y*n)))
                n += 1
                p = World.this.PieceAt(self.owner, self.x+(x*n), self.y+(y*n))
            if p == FOE:
                self.valid.add((self.x+(x*n), self.y+(y*n)))
            
class King(Piece):
    wtexture = ImgLoad("KingWhite.png")
    btexture = ImgLoad("KingBlack.png")
    def SetValid(self):
        self.valid = set()
        for x, y in zip((0, 1, 1, 1, 0, -1, -1, -1), (1, 1, 0, -1, -1, -1, 0, 1)):
            p = World.this.PieceAt(self.owner, self.x+x, self.y+y)
            if p in OPEN:
                self.valid.add((self.x+x, self.y+y))
        tmp = set()
        for v in self.valid:
            if not World.this.IsKingSafeAt(self.owner, *v):
                tmp.add(v)
        for item in tmp:
            self.valid.remove(item)
            
class Queen(Piece):
    wtexture = ImgLoad("QueenWhite.png")
    btexture = ImgLoad("QueenBlack.png")
    def SetValid(self):
        self.valid = set()
        for x, y in zip((-1, 1, -1, 1, -1, 1, 0, 0), (1, 1, -1, -1, 0, 0, -1, 1)):
            p = World.this.PieceAt(self.owner, self.x+x, self.y+y)
            n = 1
            while p == FREE:
                self.valid.add((self.x+(x*n), self.y+(y*n)))
                n += 1
                p = World.this.PieceAt(self.owner, self.x+(x*n), self.y+(y*n))
            if p == FOE:
                self.valid.add((self.x+(x*n), self.y+(y*n)))
                    
            
w = World().Run()
