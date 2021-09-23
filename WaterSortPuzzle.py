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

    def __str__(self):
        return str(self.fromVial.getId()) + " (" + self.fromVial.peek() + ") --> " + str(
            self.toVial.getId()) + " (" + self.toVial.peek() + ")"

    def __lt__(self, other):
        return self.moveHeuristic() < other.moveHeuristic()

    def __le__(self, other):
        return self.moveHeuristic() <= other.moveHeuristic()

    def __ge__(self, other):
        return self.moveHeuristic() >= other.moveHeuristic()

    def __gt__(self, other):
        return self.moveHeuristic() > other.moveHeuristic()

    def __eq__(self, other):
        return self.moveHeuristic() == other.moveHeuristic()


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

    # Create a score based on how close to a complete separation we are
    def computeGoalHeuristic(self):
        totalHeuristic = 0
        for vial in self.vialList:
            # If a vial is full of a single color, don't add points as this is our goal
            if not (vial.isSingleColor() and vial.isFull()):
                colorSet = set()
                for color in vial.colors:
                    colorSet.add(color)
                totalHeuristic += len(colorSet)
                del colorSet

        return totalHeuristic

    def validate(self, isQuestionPuzzle=False):
        retVal = True
        # Dictionary of color counts
        colors = {}

        print("There are " + str(len(self.vialList)) + " vials in the game")
        print("There are " + str(len(self.vialList[0])) + " colors in each vial")

        for vial in self.vialList:
            for color in vial:
                # Don't count unknown colors
                if color is UNKNOWN:
                    continue
                # Check if the color is in the dict
                if color in colors.keys():
                    colors[color] = colors[color] + 1
                else:
                    colors[color] = 1

        # Check for any color that does not equal 4
        for colorName in colors.keys():
            if colors[colorName] != 4 and not isQuestionPuzzle:
                print(colorName + " has an invalid count (" + str(colors[colorName]) + ")")
                retVal = False
            elif isQuestionPuzzle and colors[colorName] > 4:
                print(colorName + " has more than 4 colors (" + str(colors[colorName]) + ")")
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

    def __init__(self, vialId, color1="", color2="", color3="", color4=""):
        if color1 == "" and (color2 != "" or color3 != "" or color4 != ""):
            print("Error, either all colors must be provided or no colors for an empty vial")

        self.vialId = vialId

        if color1 == "":
            self.colors = []
        else:
            self.colors = [color4, color3, color2, color1]

        self.maxSize = 4
        self.index = len(self.colors)

    def isEmpty(self):
        return len(self.colors) == 0

    def isFull(self):
        return len(self.colors) == self.maxSize

    def push(self, item):
        if self.isFull():
            print("The vial is already full")
        else:
            self.colors.append(item)

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
        retVal += self.colors[3] + ", " if len(self.colors) > 3 else "empty, "
        retVal += self.colors[2] + ", " if len(self.colors) > 2 else "empty, "
        retVal += self.colors[1] + ", " if len(self.colors) > 1 else "empty, "
        retVal += self.colors[0] if len(self.colors) > 0 else "empty"

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


# Colors
LBLUE = "lBlue"
DBLUE = "dBlue"
YELLOW = "Yellow"
ORANGE = "Orange"
LGREEN = "lGreen"
GREEN = "Green"
DGREEN = "dGreen"
GRAY = "Gray"
PURPLE = "Purple"
RED = "Red"
BROWN = "Brown"
PINK = "Pink"
UNKNOWN = "Unknown"


class Liquid:
    def __init__(self, color):
        self.color = color

    def getColor(self):
        return self.color
