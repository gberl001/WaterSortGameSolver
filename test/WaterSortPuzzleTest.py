import unittest

from WaterSortPuzzle import Vial, VialSet, Move
from WaterSortPuzzleSolver import validAndUsefulMove


class TestSolver(unittest.TestCase):

    def testValidMoveEmptyToEmpty(self):
        vial1 = Vial(1)
        vial2 = Vial(2)

        self.assertEqual(False, validAndUsefulMove(vial1, vial2))

    def testValidMoveColorToEmpty(self):
        vial1 = Vial(1)
        vial2 = Vial(2)
        vial1.push("color1")

        self.assertEqual(False, validAndUsefulMove(vial1, vial2))

    def testValidMoveDifferentColors(self):
        vial1 = Vial(1)
        vial2 = Vial(2)
        vial1.push("color1")
        vial2.push("color2")

        self.assertEqual(False, validAndUsefulMove(vial1, vial2))

    def testValidMoveSameColors(self):
        vial1 = Vial(1)
        vial2 = Vial(2)
        vial1.push("color1")
        vial2.push("color1")

        self.assertEqual(True, validAndUsefulMove(vial1, vial2))

    def testValidMoveInsufficientSpace(self):
        vial1 = Vial(1)
        vial2 = Vial(2)
        vial1.push("color2")
        vial1.push("color1")
        vial1.push("color1")
        vial2.push("color1")
        vial2.push("color1")

        self.assertEqual(False, validAndUsefulMove(vial2, vial1))

    def testValidMoveWithFullToVial(self):
        vial1 = Vial(1, "color1", "color2", "color3", "color4")
        vial2 = Vial(2)
        vial2.push("color1")

        self.assertEqual(False, validAndUsefulMove(vial2, vial1))

    def testValidMoveWithSingleColorNonFullFromVial(self):
        vial1 = Vial(1)
        vial2 = Vial(2)
        vial2.push("color1")
        vial2.push("color1")
        vial2.push("color1")

        self.assertEqual(False, validAndUsefulMove(vial2, vial1))


class TestMove(unittest.TestCase):

    def testMoveWithSingleColor(self):
        vial1 = Vial(1, "color1", "color2", "color3", "color4")
        vial2 = Vial(2)

        move = Move(vial1, vial2)
        self.assertEqual(True, vial2.isEmpty())
        self.assertEqual(True, vial1.isFull())

        move.execute()
        self.assertEqual(True, vial2.isSingleColor() and not vial2.isFull())
        self.assertEqual("color2", vial1.peek())

    def testMoveWithMultipleBlocks(self):
        vial1 = Vial(1, "color1", "color1", "color1", "color4")
        vial2 = Vial(2)

        move = Move(vial1, vial2)
        self.assertEqual(True, vial2.isEmpty())
        self.assertEqual(True, vial1.isFull())

        move.execute()
        self.assertEqual(True, vial2.isSingleColor() and not vial2.isFull())
        self.assertEqual("color4", vial1.peek())
        self.assertEqual("color1", vial2.peek())

    def testUndoMove(self):
        vial1 = Vial(1, "color1", "color1", "color1", "color4")
        vial2 = Vial(2)

        move = Move(vial1, vial2)
        self.assertEqual(True, vial2.isEmpty())
        self.assertEqual(True, vial1.isFull())
        move.undo()
        # Undo shouldn't do anything if not executed yet
        self.assertEqual(True, vial2.isEmpty())
        self.assertEqual(True, vial1.isFull())

        move.execute()
        self.assertEqual(True, vial2.isSingleColor() and not vial2.isFull())
        self.assertEqual("color4", vial1.peek())
        self.assertEqual("color1", vial2.peek())

        move.undo()
        self.assertEqual(True, vial2.isEmpty())
        self.assertEqual(True, vial1.isFull())


class TestVial(unittest.TestCase):

    def testEmptySpaceHalfFull(self):
        vial = Vial(1, "color1", "color2", "color3", "color4")
        vial.pop()
        vial.pop()

        self.assertEqual(2, vial.emptySpace())

    def testEmptySpaceFullyEmpty(self):
        vial = Vial(1)

        self.assertEqual(4, vial.emptySpace())

    def testTopColorCountSingle(self):
        vial = Vial(1, "color1", "color2", "color3", "color4")

        self.assertEqual(1, vial.topColorCount())

    def testTopColorCountColorDouble(self):
        vial = Vial(1, "color1", "color1", "color3", "color4")

        self.assertEqual(2, vial.topColorCount())

    def testTopColorCountColorDiscontinuous(self):
        vial = Vial(1, "color1", "color2", "color3", "color1")

        self.assertEqual(1, vial.topColorCount())

    def testTopColorCountColorWithContinuousAndDiscontinuous(self):
        vial = Vial(1, "color1", "color1", "color3", "color1")

        self.assertEqual(2, vial.topColorCount())

    def testIterator(self):
        vial = Vial(1, "color1", "color2", "color3", "color4")

        count = 0
        for color in vial:
            count += 1
            self.assertEqual("color" + str(count), color)

        self.assertEqual(4, count)

        # Do the same again to ensure the index was reset
        count = 0
        for color in vial:
            count += 1
            self.assertEqual("color" + str(count), color)

        self.assertEqual(4, count)

    def testGetId(self):
        vial = Vial(49)

        self.assertEqual(vial.getId(), 49)

    def testEmptyVialCreation(self):
        vial = Vial(1)
        self.assertEqual(True, vial.isEmpty())
        self.assertEqual(False, vial.isFull())

    def testFullVial(self):
        vial = Vial(1, "color1", "color2", "color3", "color4")

        self.assertEqual(True, vial.isFull())
        self.assertEqual(False, vial.isEmpty())

    def testPushSingleColorIntoVial(self):
        vial = Vial(1)
        vial.push("color1")

        self.assertEqual(False, vial.isFull())
        self.assertEqual(False, vial.isEmpty())
        self.assertEqual("color1", vial.peek())
        self.assertEqual("color1", vial.pop())

    def testLastColorShowsInPeekAndPop(self):
        vial = Vial(1)
        vial.push("color1")
        vial.push("color2")

        self.assertEqual(False, vial.isFull())
        self.assertEqual(False, vial.isEmpty())
        self.assertEqual("color2", vial.peek())
        self.assertEqual("color2", vial.pop())

    def testIsSingleColorTrue(self):
        vial = Vial(1)
        vial.push("color1")
        vial.push("color1")

        self.assertEqual(True, vial.isSingleColor())

    def testIsSingleColorFalse(self):
        vial = Vial(1)
        vial.push("color1")
        vial.push("color2")

        self.assertEqual(False, vial.isSingleColor())

    def testIsSingleColorBeforeAndAfterPop(self):
        vial = Vial(1)
        vial.push("color1")
        vial.push("color1")
        vial.push("color2")
        vial.push("color1")

        self.assertEqual(False, vial.isSingleColor())

        vial.pop()
        self.assertEqual(False, vial.isSingleColor())

        vial.pop()
        self.assertEqual(True, vial.isSingleColor())

    def testSetColors(self):
        vial = Vial(1)
        colors = ["color1", "color2", "color3", "color4"]
        vial.setColors(colors)

        self.assertEqual("color4", vial.pop())
        self.assertEqual("color3", vial.pop())
        self.assertEqual("color2", vial.pop())
        self.assertEqual("color1", vial.pop())

    def testStringOutputFullVial(self):
        vial = Vial(1, "color1", "color2", "color3", "color4")
        self.assertEqual("1 - <color1, color2, color3, color4>", str(vial))

    def testStringOutputEmptyVial(self):
        vial = Vial(1)
        self.assertEqual("1 - <empty, empty, empty, empty>", str(vial))

    def testStringOutputAfterPop(self):
        vial = Vial(1, "color1", "color2", "color3", "color4")
        vial.pop()
        vial.pop()
        self.assertEqual("1 - <empty, empty, color3, color4>", str(vial))

    def testShallowCopy(self):
        vial = Vial(1, "color1", "color2", "color3", "color4")

        self.assertEqual("color1", vial.peek())
        vialCopy = vial.shallowCopy()
        self.assertEqual("color1", vialCopy.peek())


class TestVialSet(unittest.TestCase):

    def testVialSetIterator(self):
        vialSet = VialSet()

        vialsList = [Vial(1, "color1", "color2", "color3", "color4"), Vial(2, "color1", "color2", "color3", "color4"),
                     Vial(3, "color1", "color2", "color3", "color4"), Vial(4, "color1", "color2", "color3", "color4"),
                     Vial(5)]

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
        vial = Vial(1)
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

        vialsList = [Vial(1, "color1", "color1", "color1", "color1"), Vial(2, "color2", "color2", "color2", "color2"),
                     Vial(3, "color3", "color3", "color3", "color3"), Vial(4, "color4", "color4", "color4", "color4"),
                     Vial(5)]
        for vial in vialsList:
            vialSet.addVial(vial)

        self.assertEqual(0, vialSet.computeGoalHeuristic())

    def testHeuristicCloseGame(self):
        vialSet = VialSet()
        vial5 = Vial(5)
        vial1 = Vial(1)
        vial1.push("color1")
        vial1.push("color1")
        vial1.push("color1")
        vial5.push("color1")

        vialsList = [vial1, Vial(2, "color2", "color2", "color2", "color2"),
                     Vial(3, "color3", "color3", "color3", "color3"), Vial(4, "color4", "color4", "color4", "color4"),
                     vial5]
        for vial in vialsList:
            vialSet.addVial(vial)

        # Two vials have a single color but are NOT full so we should get a point for each
        self.assertEqual(2, vialSet.computeGoalHeuristic())

    def testHeuristicAnotherCloseGame(self):
        vialSet = VialSet()
        vial5 = Vial(5)
        vial1 = Vial(1)
        vial2 = Vial(2)
        for i in range(0, 3):
            vial1.push("color1")
            vial2.push("color2")
        vial5.push("color1")
        vial5.push("color2")

        vialsList = [vial1, vial2,
                     Vial(3, "color3", "color3", "color3", "color3"), Vial(4, "color4", "color4", "color4", "color4"),
                     vial5]
        for vial in vialsList:
            vialSet.addVial(vial)

        # Two vials have a single color but are NOT full and one vial has two colors so we should get 4
        originalHeuristic = vialSet.computeGoalHeuristic()
        self.assertEqual(4, originalHeuristic)

        # Move one of the colors over and confirm we have a better score
        vial2.push(vial5.pop())
        self.assertLess(vialSet.computeGoalHeuristic(), originalHeuristic)
