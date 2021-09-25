import unittest

from WaterSortPuzzle import Vial, VialSet, Move, LIGHT_BLUE, DARK_BLUE, GREEN, LIGHT_GREEN, Liquid, PINK, UNKNOWN
from WaterSortPuzzleSolver import validAndUsefulMove


class TestLiquid(unittest.TestCase):

    def testEqualBetweenDifferentObjects(self):
        liq1 = Liquid("0xFFFFFF", "color1")
        liq2 = Liquid("0xFFFFFF", "color1")

        self.assertEqual(liq2, liq1)


class TestSolver(unittest.TestCase):

    def testValidMoveEmptyToEmpty(self):
        vial1 = Vial(1, startEmpty=True)
        vial2 = Vial(2, startEmpty=True)

        self.assertEqual(False, validAndUsefulMove(vial1, vial2))

    def testValidMoveColorToEmpty(self):
        vial1 = Vial(1, startEmpty=True)
        vial2 = Vial(2, startEmpty=True)
        vial1.push(LIGHT_BLUE)

        self.assertEqual(False, validAndUsefulMove(vial1, vial2))

    def testValidMoveDifferentColors(self):
        vial1 = Vial(1, startEmpty=True)
        vial2 = Vial(2, startEmpty=True)
        vial1.push(LIGHT_BLUE)
        vial2.push(DARK_BLUE)

        self.assertEqual(False, validAndUsefulMove(vial1, vial2))

    def testValidMoveSameColors(self):
        vial1 = Vial(1, startEmpty=True)
        vial2 = Vial(2, startEmpty=True)
        vial1.push(LIGHT_BLUE)
        vial2.push(LIGHT_BLUE)

        self.assertEqual(True, validAndUsefulMove(vial1, vial2))

    def testValidMoveInsufficientSpace(self):
        vial1 = Vial(1, startEmpty=True)
        vial2 = Vial(2, startEmpty=True)
        vial1.push(DARK_BLUE)
        vial1.push(LIGHT_BLUE)
        vial1.push(LIGHT_BLUE)
        vial2.push(LIGHT_BLUE)
        vial2.push(LIGHT_BLUE)

        self.assertEqual(False, validAndUsefulMove(vial2, vial1))

    def testValidMoveWithFullToVial(self):
        vial1 = Vial(1, LIGHT_BLUE, DARK_BLUE, LIGHT_GREEN, GREEN)
        vial2 = Vial(2, startEmpty=True)
        vial2.push(LIGHT_BLUE)

        self.assertEqual(False, validAndUsefulMove(vial2, vial1))

    def testValidMoveWithSingleColorNonFullFromVial(self):
        vial1 = Vial(1, startEmpty=True)
        vial2 = Vial(2, startEmpty=True)
        vial2.push(LIGHT_BLUE)
        vial2.push(LIGHT_BLUE)
        vial2.push(LIGHT_BLUE)

        self.assertEqual(False, validAndUsefulMove(vial2, vial1))


class TestMove(unittest.TestCase):

    def testMoveWithSingleColor(self):
        vial1 = Vial(1, LIGHT_BLUE, DARK_BLUE, LIGHT_GREEN, GREEN)
        vial2 = Vial(2, startEmpty=True)

        move = Move(vial1, vial2)
        self.assertEqual(True, vial2.isEmpty())
        self.assertEqual(True, vial1.isFull())

        move.execute()
        self.assertEqual(True, vial2.isSingleColor() and not vial2.isFull())
        self.assertEqual(DARK_BLUE, vial1.peek())

    def testMoveWithMultipleBlocks(self):
        vial1 = Vial(1, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, DARK_BLUE)
        vial2 = Vial(2, startEmpty=True)

        move = Move(vial1, vial2)
        self.assertEqual(True, vial2.isEmpty())
        self.assertEqual(True, vial1.isFull())

        move.execute()
        self.assertEqual(True, vial2.isSingleColor() and not vial2.isFull())
        self.assertEqual(DARK_BLUE, vial1.peek())
        self.assertEqual(LIGHT_BLUE, vial2.peek())

    def testUndoMove(self):
        vial1 = Vial(1, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, GREEN)
        vial2 = Vial(2, startEmpty=True)

        move = Move(vial1, vial2)
        self.assertEqual(True, vial2.isEmpty())
        self.assertEqual(True, vial1.isFull())
        move.undo()
        # Undo shouldn't do anything if not executed yet
        self.assertEqual(True, vial2.isEmpty())
        self.assertEqual(True, vial1.isFull())

        move.execute()
        self.assertEqual(True, vial2.isSingleColor() and not vial2.isFull())
        self.assertEqual(GREEN, vial1.peek())
        self.assertEqual(LIGHT_BLUE, vial2.peek())

        move.undo()
        self.assertEqual(True, vial2.isEmpty())
        self.assertEqual(True, vial1.isFull())


class TestVial(unittest.TestCase):

    def testEmptySpaceHalfFull(self):
        vial = Vial(1, LIGHT_BLUE, DARK_BLUE, LIGHT_GREEN, GREEN)
        vial.pop()
        vial.pop()

        self.assertEqual(2, vial.emptySpace())

    def testEmptySpaceFullyEmpty(self):
        vial = Vial(1, startEmpty=True)

        self.assertEqual(4, vial.emptySpace())

    def testTopColorCountSingle(self):
        vial = Vial(1, LIGHT_BLUE, DARK_BLUE, LIGHT_GREEN, GREEN)

        self.assertEqual(1, vial.topColorCount())

    def testTopColorCountColorDouble(self):
        vial = Vial(1, LIGHT_BLUE, LIGHT_BLUE, LIGHT_GREEN, GREEN)

        self.assertEqual(2, vial.topColorCount())

    def testTopColorCountColorDiscontinuous(self):
        vial = Vial(1, LIGHT_BLUE, DARK_BLUE, LIGHT_GREEN, LIGHT_BLUE)

        self.assertEqual(1, vial.topColorCount())

    def testTopColorCountColorWithContinuousAndDiscontinuous(self):
        vial = Vial(1, LIGHT_BLUE, LIGHT_BLUE, LIGHT_GREEN, LIGHT_BLUE)

        self.assertEqual(2, vial.topColorCount())

    def testIterator(self):
        colors = [LIGHT_BLUE, DARK_BLUE, LIGHT_GREEN, GREEN]
        vial = Vial(1, colors[0], colors[1], colors[2], colors[3])

        count = 0
        for color in vial:
            self.assertEqual(colors[count], color)
            count += 1

        self.assertEqual(4, count)

        # Do the same again to ensure the index was reset
        count = 0
        for color in vial:
            self.assertEqual(colors[count], color)
            count += 1

        self.assertEqual(4, count)

    def testGetId(self):
        vial = Vial(49, startEmpty=True)

        self.assertEqual(vial.getId(), 49)

    def testEmptyVialCreation(self):
        vial = Vial(1, startEmpty=True)
        self.assertEqual(True, vial.isEmpty())
        self.assertEqual(False, vial.isFull())

    def testFullVial(self):
        vial = Vial(1, LIGHT_BLUE, DARK_BLUE, LIGHT_GREEN, GREEN)

        self.assertEqual(True, vial.isFull())
        self.assertEqual(False, vial.isEmpty())

    def testPushSingleColorIntoVial(self):
        vial = Vial(1, startEmpty=True)
        vial.push(LIGHT_BLUE)

        self.assertEqual(False, vial.isFull())
        self.assertEqual(False, vial.isEmpty())
        self.assertEqual(LIGHT_BLUE, vial.peek())
        self.assertEqual(LIGHT_BLUE, vial.pop())

    def testLastColorShowsInPeekAndPop(self):
        vial = Vial(1, startEmpty=True)
        vial.push(LIGHT_BLUE)
        vial.push(DARK_BLUE)

        self.assertEqual(False, vial.isFull())
        self.assertEqual(False, vial.isEmpty())
        self.assertEqual(DARK_BLUE, vial.peek())
        self.assertEqual(DARK_BLUE, vial.pop())

    def testIsSingleColorTrue(self):
        vial = Vial(1, startEmpty=True)
        vial.push(LIGHT_BLUE)
        vial.push(LIGHT_BLUE)

        self.assertEqual(True, vial.isSingleColor())

    def testIsSingleColorFalse(self):
        vial = Vial(1, startEmpty=True)
        vial.push(LIGHT_BLUE)
        vial.push(DARK_BLUE)

        self.assertEqual(False, vial.isSingleColor())

    def testIsSingleColorBeforeAndAfterPop(self):
        vial = Vial(1, startEmpty=True)
        vial.push(LIGHT_BLUE)
        vial.push(LIGHT_BLUE)
        vial.push(DARK_BLUE)
        vial.push(LIGHT_BLUE)

        self.assertEqual(False, vial.isSingleColor())

        vial.pop()
        self.assertEqual(False, vial.isSingleColor())

        vial.pop()
        self.assertEqual(True, vial.isSingleColor())

    def testSetColors(self):
        vial = Vial(1, startEmpty=True)
        colors = [LIGHT_BLUE, DARK_BLUE, LIGHT_GREEN, GREEN]
        vial.setColors(colors)

        self.assertEqual(GREEN, vial.pop())
        self.assertEqual(LIGHT_GREEN, vial.pop())
        self.assertEqual(DARK_BLUE, vial.pop())
        self.assertEqual(LIGHT_BLUE, vial.pop())

    def testStringOutputFullVial(self):
        vial = Vial(1, LIGHT_BLUE, DARK_BLUE, LIGHT_GREEN, GREEN)
        self.assertEqual(
            "1 - <" + str(LIGHT_BLUE) + ", " + str(DARK_BLUE) + ", " + str(LIGHT_GREEN) + ", " + str(GREEN) + ">",
            str(vial))

    def testStringOutputEmptyVial(self):
        vial = Vial(1, startEmpty=True)
        self.assertEqual("1 - <empty, empty, empty, empty>", str(vial))

    def testStringOutputAfterPop(self):
        vial = Vial(1, LIGHT_BLUE, DARK_BLUE, LIGHT_GREEN, GREEN)
        vial.pop()
        vial.pop()
        self.assertEqual("1 - <empty, empty, " + str(LIGHT_GREEN) + ", " + str(GREEN) + ">", str(vial))

    def testShallowCopy(self):
        vial = Vial(1, LIGHT_BLUE, DARK_BLUE, LIGHT_GREEN, GREEN)

        self.assertEqual(LIGHT_BLUE, vial.peek())
        vialCopy = vial.shallowCopy()
        self.assertEqual(LIGHT_BLUE, vialCopy.peek())


class TestVialSet(unittest.TestCase):

    def testVialSetIterator(self):
        vialSet = VialSet()

        vialsList = [Vial(1, LIGHT_BLUE, DARK_BLUE, LIGHT_GREEN, GREEN), Vial(2, LIGHT_BLUE, DARK_BLUE, LIGHT_GREEN, GREEN),
                     Vial(3, LIGHT_BLUE, DARK_BLUE, LIGHT_GREEN, GREEN), Vial(4, LIGHT_BLUE, DARK_BLUE, LIGHT_GREEN, GREEN),
                     Vial(5, startEmpty=True)]

        for vial in vialsList:
            vialSet.addVial(vial)

        i = 0
        for vial in vialSet:
            self.assertEqual(vialsList[i], vial)
            i += 1

        self.assertEqual(5, i)

    def testAddVial(self):
        vialSet = VialSet()
        self.assertEqual(vialSet.getVial(1), None)

        vial = Vial(1)
        vialSet.addVial(vial)

        self.assertEqual(vial, vialSet.getVial(1))

    def testShallowCopy(self):
        vialSet = VialSet()
        vial = Vial(1, startEmpty=True)
        vialSet.addVial(vial)

        # Make a copy
        vialSetCopy = vialSet.shallowCopy()

        self.assertNotEqual(vialSet, vialSetCopy)

        # Also assert the vial in the original set is the same and the vial in the copied set is not the same
        self.assertEqual(vial, vialSet.getVial(1))
        self.assertNotEqual(vial, vialSetCopy.getVial(1))

        # Now assert that they are the same shallow copy
        copiedVial = vialSetCopy.getVial(1)
        self.assertEqual(vial.getId(), copiedVial.getId())
        self.assertEqual(vial.isEmpty(), copiedVial.isEmpty())

    def testHeuristicPerfectGame(self):
        vialSet = VialSet()

        vialsList = [Vial(1, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE), Vial(2, DARK_BLUE, DARK_BLUE, DARK_BLUE, DARK_BLUE),
                     Vial(3, LIGHT_GREEN, LIGHT_GREEN, LIGHT_GREEN, LIGHT_GREEN), Vial(4, GREEN, GREEN, GREEN, GREEN),
                     Vial(5, startEmpty=True)]
        for vial in vialsList:
            vialSet.addVial(vial)

        self.assertEqual(0, vialSet.computeGoalHeuristic())

    def testHeuristicCloseGame(self):
        vialSet = VialSet()
        vial5 = Vial(5, startEmpty=True)
        vial1 = Vial(1, startEmpty=True)
        vial1.push(LIGHT_BLUE)
        vial1.push(LIGHT_BLUE)
        vial1.push(LIGHT_BLUE)
        vial5.push(LIGHT_BLUE)

        vialsList = [vial1, Vial(2, DARK_BLUE, DARK_BLUE, DARK_BLUE, DARK_BLUE),
                     Vial(3, LIGHT_GREEN, LIGHT_GREEN, LIGHT_GREEN, LIGHT_GREEN), Vial(4, GREEN, GREEN, GREEN, GREEN),
                     vial5]
        for vial in vialsList:
            vialSet.addVial(vial)

        # Two vials have a single color but are NOT full so we should get a point for each
        self.assertEqual(2, vialSet.computeGoalHeuristic())

    def testHeuristicAnotherCloseGame(self):
        vialSet = VialSet()
        vial5 = Vial(5, startEmpty=True)
        vial1 = Vial(1, startEmpty=True)
        vial2 = Vial(2, startEmpty=True)
        for i in range(0, 3):
            vial1.push(LIGHT_BLUE)
            vial2.push(DARK_BLUE)
        vial5.push(LIGHT_BLUE)
        vial5.push(DARK_BLUE)

        vialsList = [vial1, vial2,
                     Vial(3, LIGHT_GREEN, LIGHT_GREEN, LIGHT_GREEN, LIGHT_GREEN), Vial(4, GREEN, GREEN, GREEN, GREEN),
                     vial5]
        for vial in vialsList:
            vialSet.addVial(vial)

        # Two vials have a single color but are NOT full and one vial has two colors so we should get 4
        originalHeuristic = vialSet.computeGoalHeuristic()
        self.assertEqual(4, originalHeuristic)

        # Move one of the colors over and confirm we have a better score
        vial2.push(vial5.pop())
        self.assertLess(vialSet.computeGoalHeuristic(), originalHeuristic)

    def testValidGameMoreThanFourColors(self):
        vialSet = VialSet()
        vialSet.addVial(Vial(1, LIGHT_BLUE, LIGHT_BLUE, DARK_BLUE, DARK_BLUE))
        vialSet.addVial(Vial(2, LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE, DARK_BLUE))
        vialSet.addVial(Vial(3, startEmpty=True))
        vialSet.addVial(Vial(4, startEmpty=True))

        self.assertFalse(vialSet.validate())

    def testValidGameLessThanFourColors(self):
        vialSet = VialSet()
        vialSet.addVial(Vial(1, LIGHT_BLUE, LIGHT_BLUE, DARK_BLUE, DARK_BLUE))
        vialSet.addVial(Vial(2, LIGHT_BLUE, PINK, DARK_BLUE, DARK_BLUE))
        vialSet.addVial(Vial(3, startEmpty=True))
        vialSet.addVial(Vial(4, startEmpty=True))

        self.assertFalse(vialSet.validate())

    def testValidGameNoEmptyVials(self):
        vialSet = VialSet()
        vialSet.addVial(Vial(1, LIGHT_BLUE, LIGHT_BLUE, DARK_BLUE, DARK_BLUE))
        vialSet.addVial(Vial(2, LIGHT_BLUE, LIGHT_BLUE, DARK_BLUE, DARK_BLUE))

        self.assertFalse(vialSet.validate())

    def testValidGameNotEnoughEmptyVials(self):
        vialSet = VialSet()
        vialSet.addVial(Vial(1, LIGHT_BLUE, LIGHT_BLUE, DARK_BLUE, DARK_BLUE))
        vialSet.addVial(Vial(2, LIGHT_BLUE, LIGHT_BLUE, DARK_BLUE, DARK_BLUE))
        vialSet.addVial(Vial(3, startEmpty=True))

        self.assertFalse(vialSet.validate())

    def testValidGameTooManyEmptyVials(self):
        vialSet = VialSet()
        vialSet.addVial(Vial(1, LIGHT_BLUE, LIGHT_BLUE, DARK_BLUE, DARK_BLUE))
        vialSet.addVial(Vial(2, LIGHT_BLUE, LIGHT_BLUE, DARK_BLUE, DARK_BLUE))
        vialSet.addVial(Vial(3, startEmpty=True))
        vialSet.addVial(Vial(4, startEmpty=True))
        vialSet.addVial(Vial(5, startEmpty=True))

        self.assertFalse(vialSet.validate())

    def testValidGameQuestionPuzzle(self):
        vialSet = VialSet()
        vialSet.addVial(Vial(1, LIGHT_BLUE, UNKNOWN, UNKNOWN, UNKNOWN))
        vialSet.addVial(Vial(2, LIGHT_BLUE, UNKNOWN, UNKNOWN, UNKNOWN))
        vialSet.addVial(Vial(3, LIGHT_BLUE, UNKNOWN, UNKNOWN, UNKNOWN))
        vialSet.addVial(Vial(4, LIGHT_BLUE, UNKNOWN, UNKNOWN, UNKNOWN))
        vialSet.addVial(Vial(5, startEmpty=True))
        vialSet.addVial(Vial(6, startEmpty=True))

        self.assertTrue(vialSet.validate(isQuestionPuzzle=True))

    def testValidateForgotStartEmptyParameter(self):
        vialSet = VialSet()
        vialSet.addVial(Vial(1, LIGHT_BLUE, UNKNOWN, UNKNOWN, UNKNOWN))
        vialSet.addVial(Vial(2, LIGHT_BLUE, UNKNOWN, UNKNOWN, UNKNOWN))
        vialSet.addVial(Vial(3, LIGHT_BLUE, UNKNOWN, UNKNOWN, UNKNOWN))
        vialSet.addVial(Vial(4, LIGHT_BLUE, UNKNOWN, UNKNOWN, UNKNOWN))
        vialSet.addVial(Vial(5))
        vialSet.addVial(Vial(6))

        self.assertFalse(vialSet.validate(isQuestionPuzzle=True))

    def testValidGameQuestionPuzzleNotEnoughEmptyVials(self):
        vialSet = VialSet()
        vialSet.addVial(Vial(1, LIGHT_BLUE, UNKNOWN, UNKNOWN, UNKNOWN))
        vialSet.addVial(Vial(2, LIGHT_BLUE, UNKNOWN, UNKNOWN, UNKNOWN))
        vialSet.addVial(Vial(3, LIGHT_BLUE, UNKNOWN, UNKNOWN, UNKNOWN))
        vialSet.addVial(Vial(4, LIGHT_BLUE, UNKNOWN, UNKNOWN, UNKNOWN))
        vialSet.addVial(Vial(5, startEmpty=True))

        self.assertFalse(vialSet.validate(isQuestionPuzzle=True))

    def testValidGameQuestionPuzzleTooManyEmptyVials(self):
        vialSet = VialSet()
        vialSet.addVial(Vial(1, LIGHT_BLUE, UNKNOWN, UNKNOWN, UNKNOWN))
        vialSet.addVial(Vial(2, LIGHT_BLUE, UNKNOWN, UNKNOWN, UNKNOWN))
        vialSet.addVial(Vial(3, LIGHT_BLUE, UNKNOWN, UNKNOWN, UNKNOWN))
        vialSet.addVial(Vial(4, LIGHT_BLUE, UNKNOWN, UNKNOWN, UNKNOWN))
        vialSet.addVial(Vial(5, startEmpty=True))
        vialSet.addVial(Vial(6, startEmpty=True))
        vialSet.addVial(Vial(7, startEmpty=True))

        self.assertFalse(vialSet.validate(isQuestionPuzzle=True))
