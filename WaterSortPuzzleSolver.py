from PriorityQueue import PriorityQueue
from WaterSortPuzzle import Vial, LBLUE, DBLUE, YELLOW, ORANGE, LGREEN, GREEN, DGREEN, GRAY, PURPLE, \
    RED, BROWN, PINK, Move, VialSet, UNKNOWN

import sys

sys.setrecursionlimit(10000)


def gameOver(vialSet):
    for vial in vialSet:
        if not vial.isEmpty() and not vial.isFull():
            return False
        if vial.isFull() and not vial.isSingleColor():
            return False

    return True


def startGameWithSpecificStartingVial(vialSet, recordedMoves, startingVial, isQuestionPuzzle=False):
    possibleGameMoves = PriorityQueue()
    for toVial in vialSet:
        # Skip pouring into itself
        if startingVial == toVial:
            continue

        if validAndUsefulMove(startingVial, toVial):
            move = Move(startingVial, toVial)
            possibleGameMoves.put2(move)

    # Make the first round of moves but let getGameResult() take over after that
    while not possibleGameMoves.empty():
        gameMove = possibleGameMoves.get2()
        # Perform the move, then recurse, then undo the move
        # print("Attempting move " + str(gameMove) + " at level " + str(len(recordedMoves)))
        recordedMoves.append(str(gameMove))
        gameMove.execute()
        if getGameResult(vialSet, recordedMoves, isQuestionPuzzle):
            return True
        gameMove.undo()
        recordedMoves.pop()
        del gameMove


def getGameResult(vialSet, recordedMoves, isQuestionPuzzle=False):
    if gameOver(vialSet):
        print("Game Complete with " + str(len(recordedMoves)) + " moves!")
        return True

    if isQuestionPuzzle:
        checkForUnknown(vialSet, recordedMoves)

    possibleGameMoves = getPossibleGameMoves(vialSet)
    # if len(possibleGameMoves) == 0:
    #     print("Exhausted this attempt")
        # print(vialSet)
        # print("------------------------------------------")

    while not possibleGameMoves.empty():
        gameMove = possibleGameMoves.get2()
        # Perform the move, then recurse, then undo the move
        # print("Attempting move " + str(gameMove) + " at level " + str(len(recordedMoves)))
        recordedMoves.append(str(gameMove))
        gameMove.execute()
        if getGameResult(vialSet, recordedMoves, isQuestionPuzzle):
            return True
        gameMove.undo()
        recordedMoves.pop()
        del gameMove


def checkForUnknown(vialSet, moves):
    for vial in vialSet:
        # Check for unknown color
        if vial.peek() == UNKNOWN:
            for move in moves:
                print(move)
            print()

            # Replace the unknown color with the reported color
            # TODO: Sometimes two colors pop up, allow comma separated for these cases
            reportedColor = input("What color is in vial " + str(vial.getId()) + "?")
            colors = reportedColor.split(",")
            for color in colors:
                vial.pop()
                vial.push(color)

            # Print new color map
            print("The new reported colors:")
            print(vialSet)


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
    # Don't dump all from one back into another (endless recursion will result)
    if fromVial.isSingleColor() and toVial.isEmpty():
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
    isQuestionGame = False

    # Add the vials
    gameVialSet.addVial(Vial(1, DBLUE, DGREEN, LBLUE, LBLUE))
    gameVialSet.addVial(Vial(2, PURPLE, PINK, GREEN, GRAY))
    gameVialSet.addVial(Vial(3, ORANGE, PURPLE, RED, BROWN))
    gameVialSet.addVial(Vial(4, ORANGE, PINK, RED, ORANGE))
    gameVialSet.addVial(Vial(5, DGREEN, RED, YELLOW, DBLUE))
    gameVialSet.addVial(Vial(6, YELLOW, DGREEN, BROWN, DGREEN))
    gameVialSet.addVial(Vial(7, BROWN, PURPLE, RED, LGREEN))
    gameVialSet.addVial(Vial(8, LGREEN, PURPLE, PINK, LGREEN))
    gameVialSet.addVial(Vial(9, GREEN, GRAY, LBLUE, DBLUE))
    gameVialSet.addVial(Vial(10, BROWN, YELLOW, GRAY, GREEN))
    gameVialSet.addVial(Vial(11, GRAY, YELLOW, LGREEN, DBLUE))
    gameVialSet.addVial(Vial(12, GREEN, LBLUE, PINK, ORANGE))
    gameVialSet.addVial(Vial(13))
    gameVialSet.addVial(Vial(14))

    # Make sure it's a valid game
    if not gameVialSet.validate(isQuestionGame):
        exit(1)

    gameMoves = []
    # startGameWithSpecificStartingVial(gameVialSet, gameMoves, gameVialSet.getVial(10), isQuestionPuzzle=isQuestionGame)
    getGameResult(gameVialSet, gameMoves, isQuestionPuzzle=isQuestionGame)

    # Print the solution steps
    print("\nSolution:")
    for qualityMove in gameMoves:
        print(qualityMove)
