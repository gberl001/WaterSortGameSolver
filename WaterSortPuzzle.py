from PIL import Image, ImageFont, ImageDraw


class Liquid:
    def __init__(self, color, name):
        self.color = color
        self.name = name

    def getColor(self):
        return self.color

    def getName(self):
        return self.name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Liquid):
            return self.__key() == other.__key()
        return NotImplemented

    def __hash__(self):
        return hash(self.__key())

    def __key(self):
        return self.color, self.name


# Colors
LIGHT_BLUE = Liquid("#00FFFF", "Light Blue")
DARK_BLUE = Liquid("#0000FF", "Dark Blue")
YELLOW = Liquid("#FFFF00", "Yellow")
ORANGE = Liquid("#FF9900", "Orange")
LIGHT_GREEN = Liquid("#00FF00", "Light Green")
GREEN = Liquid("#93C47D", "Green")
DARK_GREEN = Liquid("#274E13", "Dark Green")
GRAY = Liquid("#999999", "Gray")
PURPLE = Liquid("#9900FF", "Purple")
RED = Liquid("#CC0000", "Red")
BROWN = Liquid("#783F04", "Brown")
PINK = Liquid("#E06666", "Pink")
UNKNOWN = Liquid("#000000", "Unknown")


class Move:
    def __init__(self, fromVial, toVial):
        self.fromVial = fromVial
        self.toVial = toVial
        self.amtMoved = 0

    def execute(self):
        for i in range(0, self.fromVial.topColorCount()):
            self.amtMoved += 1
            self.toVial.push(self.fromVial.pop())

    def undo(self):
        if self.amtMoved > 0:
            for i in range(0, self.amtMoved):
                self.fromVial.push(self.toVial.pop())
            self.amtMoved = 0

    def getFromVial(self):
        return self.fromVial

    def getToVial(self):
        return self.toVial

    def moveHeuristic(self):
        totalHeuristic = 0
        # We don't want to move from a full single color to an empty vial, that's a lateral move
        if self.fromVial.isFull and self.fromVial.isSingleColor():
            totalHeuristic += 10000
        # Favor not putting it in an empty vial
        if self.toVial.isEmpty():
            totalHeuristic += 500
        # Favor moving to a vial with more of the color than the from vial
        if self.fromVial.topColorCount() > self.toVial.topColorCount():
            totalHeuristic += 200

        return totalHeuristic

    def shallowCopy(self):
        return Move(self.fromVial.shallowCopy(), self.toVial.shallowCopy())

    def drawImage(self):
        image = Image.new('RGB', (200, 200), color='#CCCCCC')

        # Setup
        fnt = ImageFont.truetype("calibri.ttf", size=25)
        w = h = 30

        # Draw the From Vial
        vial1Text = ImageDraw.Draw(image)
        vial1Text.text((35, 170), str(self.fromVial.getId()), font=fnt, fill=(0, 0, 0))
        x = 25
        y = 145
        for color in self.fromVial.colors:
            y -= h
            shape = [(x, y), (x + w, y + h)]
            img = ImageDraw.Draw(image)
            img.rectangle(shape, fill=color.getColor())

        # Draw the From Vial
        vial2Text = ImageDraw.Draw(image)
        vial2Text.text((145, 170), str(self.toVial.getId()), font=fnt, fill=(0, 0, 0))
        x = 135
        y = 145
        for color in self.toVial.colors:
            y -= h
            shape = [(x, y), (x + w, y + h)]
            img = ImageDraw.Draw(image)
            img.rectangle(shape, fill=color.getColor())

        return image

    def __str__(self):
        return str(self.fromVial.getId()) + " (" + str(self.fromVial.peek()) + ") --> " + str(
            self.toVial.getId()) + " (" + str(self.toVial.peek()) + ")"

    def __lt__(self, other):
        if isinstance(other, Move):
            return self.moveHeuristic() < other.moveHeuristic()
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Move):
            return self.moveHeuristic() <= other.moveHeuristic()
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Move):
            return self.moveHeuristic() >= other.moveHeuristic()
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Move):
            return self.moveHeuristic() > other.moveHeuristic()
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveHeuristic() == other.moveHeuristic()
        return NotImplemented


class VialSet:

    def __init__(self):
        self.vialList = []
        self.index = 0

    def addVial(self, vial):
        self.vialList.append(vial)

    def getVial(self, index):
        for vial in self.vialList:
            if vial.getId() == index:
                return vial

    def shallowCopy(self):
        vialsCopy = VialSet()
        for vial in self.vialList:
            vialsCopy.addVial(vial.shallowCopy())
        return vialsCopy

    def getVials(self):
        return self.vialList

    def getEmptyVialCount(self):
        retVal = 0
        for vial in self.vialList:
            if vial.isEmpty():
                retVal += 1
        return retVal

    def removeVial(self, vialId):
        self.vialList.remove(self.getVial(vialId))

    def validate(self, isQuestionPuzzle=False):
        retVal = True
        # Dictionary of color counts
        colors = {}

        print("There are " + str(len(self.vialList)) + " vials in the game")
        print("There are " + str(len(self.vialList[0])) + " colors in each vial")
        expectedColorCount = (len(self.vialList) - 2) * 4
        actualColorCnt = 0

        for vial in self.vialList:
            for color in vial:
                actualColorCnt += 1
                # Don't count unknown colors
                if color == UNKNOWN:
                    continue
                # Check if the color is in the dict
                if color in colors.keys():
                    colors[color] = colors[color] + 1
                else:
                    colors[color] = 1

        # Check for any color that does not equal 4
        for color in colors.keys():
            if colors[color] != 4 and not isQuestionPuzzle:
                print(str(color) + " has an invalid count (" + str(colors[color]) + ")")
                retVal = False
            elif isQuestionPuzzle and colors[color] > 4:
                print(str(color) + " has more than 4 colors (" + str(colors[color]) + ")")
                retVal = False

        # Check for empty vial(s)
        emptyCnt = 0
        for vial in self.vialList:
            if vial.isEmpty():
                emptyCnt += 1
        if emptyCnt != 2:
            print("There are " + str(emptyCnt) + " empty vials.")
            retVal = False

        # Check that there are the expected amount of colors
        if actualColorCnt == len(self.vialList) * 4:
            print("It looks like you might have forgotten to use the startEmpty=True parameter for your empty vials")
            retVal = False
        elif actualColorCnt < expectedColorCount:
            print(str(actualColorCnt) + " is not enough colors for " + str(len(self.vialList) - 2) + " filled vials.")
            retVal = False
        elif actualColorCnt > expectedColorCount:
            print(str(actualColorCnt) + " is too many colors for " + str(len(self.vialList) - 2) + " filled vials.")
            retVal = False

        return retVal

    def __len__(self):
        return len(self.vialList)

    def __iter__(self):
        return VialSetIterator(self)

    def __str__(self):
        retVal = ""
        for vial in self.vialList:
            retVal += str(vial) + "\n"

        return retVal

    def __reversed__(self):
        return reversed(self.vialList)


class Vial:

    def __init__(self, vialId, color1=UNKNOWN, color2=UNKNOWN, color3=UNKNOWN, color4=UNKNOWN, startEmpty=False):
        self.vialId = vialId

        if startEmpty:
            self.colors = []
        else:
            self.colors = [color4, color3, color2, color1]

        self.maxSize = 4
        self.index = len(self.colors)

    def isEmpty(self):
        return len(self.colors) == 0

    def isFull(self):
        return len(self.colors) == self.maxSize

    def push(self, color):
        if self.isFull():
            print("The vial is already full")
        else:
            self.colors.append(color)

    def pop(self):
        return self.colors.pop()

    def peek(self):
        if len(self.colors) > 0:
            return self.colors[len(self.colors) - 1]
        else:
            return ""

    def emptySpace(self):
        return self.maxSize - len(self.colors)

    # Get the number of spaces that the top color takes up
    def topColorCount(self):
        topColor = self.peek()
        cnt = 0
        for color in reversed(self.colors):
            if topColor == color:
                cnt += 1
            else:
                break

        return cnt

    def getId(self):
        return self.vialId

    def setColors(self, colors):
        self.colors = colors

    def isSingleColor(self):
        colors = set()
        for element in self.colors:
            colors.add(element)

        return len(colors) <= 1

    def shallowCopy(self):
        shallowCopy = Vial(self.vialId)
        shallowCopy.setColors(self.colors.copy())
        return shallowCopy

    def __len__(self):
        return len(self.colors)

    def __iter__(self):
        return VialIterator(self)

    def __str__(self):
        retVal = str(self.vialId) + " - <"
        retVal += str(self.colors[3]) + ", " if len(self.colors) > 3 else "empty, "
        retVal += str(self.colors[2]) + ", " if len(self.colors) > 2 else "empty, "
        retVal += str(self.colors[1]) + ", " if len(self.colors) > 1 else "empty, "
        retVal += str(self.colors[0]) if len(self.colors) > 0 else "empty"

        return retVal + ">"


class VialSetIterator:
    def __init__(self, vialSet):
        self.vialSet = vialSet
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index > len(self.vialSet):
            raise StopIteration

        return self.vialSet.getVials()[self.index - 1]


class VialIterator:
    def __init__(self, vial):
        self.vial = vial
        self.index = len(self.vial.colors)

    def __iter__(self):
        return self

    def __next__(self):
        self.index -= 1
        if self.index < 0:
            raise StopIteration

        return self.vial.colors[self.index]
