from PriorityQueue import PriorityQueue
from WaterSortPuzzle import Vial, LBLUE, DBLUE, YELLOW, ORANGE, LGREEN, GREEN, DGREEN, GRAY, PURPLE, \
    RED, BROWN, PINK, Move, VialSet

import sys

sys.setrecursionlimit(10000)


def gameOver(vialSet):
    for vial in vialSet:
        if not vial.isEmpty() and not vial.isFull():
            return False
        if vial.isFull() and not vial.isSingleColor():
            return False

    return True


def getGameResult(vialSet, recordedMoves):
    if gameOver(vialSet):
        print("Game Complete!")
        return True

    possibleGameMoves = getPossibleGameMoves(vialSet)
    if len(possibleGameMoves) == 0:
        print("Exhausted this attempt")
        print(vialSet)
        print("------------------------------------------")

    while not possibleGameMoves.empty():
        gameMove = possibleGameMoves.get2()
        # Perform the move, then recurse, then undo the move
        print("Attempting move " + str(gameMove))
        recordedMoves.append(str(gameMove))
        gameMove.execute()
        if getGameResult(vialSet, recordedMoves):
            return True
        gameMove.undo()
        recordedMoves.pop()


def getPossibleGameMoves(vialSet):
    possibleGameMoves = PriorityQueue()
    for fromVial in vialSet:
        for toVial in vialSet:
            # Skip pouring into itself
            if fromVial == toVial:
                continue

            if validAndUsefulMove(fromVial, toVial):
                move = Move(fromVial, toVial)
                possibleGameMoves.put2(move)

    return possibleGameMoves


def validAndUsefulMove(fromVial, toVial):
    # Ensure from vial is not empty
    if fromVial.isEmpty():
        return False
    # Ensure the colors are the same
    if not toVial.isEmpty() and toVial.peek() != fromVial.peek():
        return False
    # Ensure the toVial is not full
    if toVial.isFull():
        return False
    # Either dump all of the color or don't bother
    if toVial.emptySpace() < fromVial.topColorCount():
        return False

    return True


# My best attempt at some sort of intelligent way to compute a better move, lower score is better
def heuristic(thisVial, thatVial):
    result = 0

    # Best case scenario is pouring single color into single color with the smaller getting the higher value
    if thatVial.isSingleColor() and thisVial.isSingleColor():
        result += thisVial.topColorCount() * 10

    # Second best case scenario is pouring a color into one of a single color, better score if there is continuous color
    if thatVial.isSingleColor():
        result += 20 / thisVial.topColorCount()

    # Scenario: If pouring thisVial into thatVial doesn't pour all of the color out of thisVial (pointless move)
    if thatVial.emptySpace() >= thisVial.topColorCount():
        result -= 20
    else:
        result += 100


if __name__ == "__main__":

    gameVialSet = VialSet()

    # Add the vials
    gameVialSet.addVial(Vial(1, DBLUE, DGREEN, LBLUE, LBLUE))
    gameVialSet.addVial(Vial(2, PURPLE, PINK, GREEN, LGREEN))     # Unsure
    gameVialSet.addVial(Vial(3, ORANGE, PURPLE, RED, BROWN))
    gameVialSet.addVial(Vial(4, ORANGE, PINK, RED, ORANGE))
    gameVialSet.addVial(Vial(5, DGREEN, RED, YELLOW, DBLUE))
    gameVialSet.addVial(Vial(6, YELLOW, DGREEN, BROWN, LGREEN))     # Unsure
    gameVialSet.addVial(Vial(7, BROWN, PURPLE, RED, ORANGE))     # Unsure
    gameVialSet.addVial(Vial(8, LGREEN, PURPLE, PINK, GREEN))     # Unsure
    gameVialSet.addVial(Vial(9, GREEN, GRAY, LBLUE, DBLUE))
    gameVialSet.addVial(Vial(10, BROWN, YELLOW, GRAY, DGREEN))     # Unsure
    gameVialSet.addVial(Vial(11, GRAY, YELLOW, LGREEN, DBLUE))     # Unsure
    gameVialSet.addVial(Vial(12, GREEN, LBLUE, PINK, GRAY))     # Unsure
    gameVialSet.addVial(Vial(10))
    gameVialSet.addVial(Vial(11))

    # Make sure it's a valid game
    if not gameVialSet.validate():
        exit(1)

    gameMoves = []
    getGameResult(gameVialSet, gameMoves)

    # Print the solution steps
    for qualityMove in gameMoves:
        print(qualityMove)
