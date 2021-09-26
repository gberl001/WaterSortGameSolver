import sys
from math import floor
import __main__
# FIXME: import __main__ is a hack to gain access to the "window" variable created in __main__

from PyQt5.QtGui import QPainter, QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QDialog, QLabel

import WaterSortPuzzleSolver as PuzzleSolver
from WaterSortPuzzle import LIGHT_BLUE, DARK_BLUE, YELLOW, ORANGE, LIGHT_GREEN, GREEN, DARK_GREEN, GRAY, PURPLE, RED, \
    BROWN, PINK, UNKNOWN, VialSet, Vial

colors = [LIGHT_BLUE, DARK_BLUE, YELLOW, ORANGE, LIGHT_GREEN, GREEN, DARK_GREEN, GRAY, PURPLE, RED, BROWN, PINK,
          UNKNOWN]

vialSet = VialSet()
colorCount = 0
isQuestionGame = False

class ColorSelectionDialog(QDialog):

    def __init__(self, msg, vialList, vialNum):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(QLabel(msg))

        self.initButtonSubmit()
        self.vialList = vialList
        self.vialNum = vialNum
        self.setWindowTitle("Select a Color")
        self.btnGrid = QWidget()
        self.initButtonGrid()
        self.colorsAdded = 0

    def initButtonSubmit(self):
        submitLayout = QGridLayout()
        btnSubmit = QPushButton("Submit")
        btnUndo = QPushButton("Undo")
        btnSubmit.clicked.connect(lambda: self.btnSubmit())
        btnUndo.clicked.connect(lambda: self.btnUndo())
        submitLayout.addWidget(btnUndo, 1, 1, 1, 1)
        submitLayout.addWidget(btnSubmit, 1, 2, 1, 1)
        self.layout.addLayout(submitLayout)

    def initButtonGrid(self):
        btnLayout = QGridLayout()
        self.layout.addLayout(btnLayout)

        btnCnt = 0
        for i in range(0, 4):
            for j in range(0, 4):
                if btnCnt >= len(colors):
                    break
                btn = QPushButton(str(i) + str(j))
                btn.setText(str(colors[btnCnt]))
                btn.clicked.connect(lambda state, x=btnCnt: self.buttonClicked(x))
                if colors[btnCnt] == UNKNOWN:
                    btn.setStyleSheet("background-color : " + str(colors[btnCnt].getColor()) + "; color: white;")
                else:
                    btn.setStyleSheet("background-color : " + str(colors[btnCnt].getColor()))
                btnLayout.addWidget(btn, i, j)
                btnCnt += 1

    def buttonClicked(self, position):
        self.colorsAdded += 1
        vial = self.vialList.getVial(self.vialNum)

        # Remove the unknown color(s) and add the selected color
        for i in range(0, self.colorsAdded):
            vial.pop()
        for i in range(0, self.colorsAdded):
            vial.push(colors[position])

        print("Added " + str(colors[position]) + " to vial " + str(self.vialList.getVial(self.vialNum)))
        __main__.window.repaint()

    def btnSubmit(self):
        self.done(0)

    def btnUndo(self):
        vial = self.vialList.getVial(self.vialNum)
        # Replace the colors added with unknown colors
        for i in range(0, self.colorsAdded):
            vial.pop()
        for i in range(0, self.colorsAdded):
            vial.push(UNKNOWN)

        self.colorsAdded = 0


class ColorSelectionGrid(QWidget):
    def __init__(self):
        super(ColorSelectionGrid, self).__init__()
        self.initButtonGrid()

    def initButtonGrid(self):
        btnLayout = QGridLayout()
        self.setLayout(btnLayout)

        btnCnt = 0
        for i in range(0, 4):
            for j in range(0, 4):
                if btnCnt >= len(colors):
                    break
                btn = QPushButton(str(i) + str(j))
                btn.setText(str(colors[btnCnt]))
                btn.clicked.connect(lambda state, x=btnCnt: self.buttonClicked(x))
                if colors[btnCnt] == UNKNOWN:
                    btn.setStyleSheet("background-color : " + str(colors[btnCnt].getColor()) + "; color: white;")
                else:
                    btn.setStyleSheet("background-color : " + str(colors[btnCnt].getColor()))
                btnLayout.addWidget(btn, i, j)
                btnCnt += 1

    def buttonClicked(self, position):
        global colors, colorCount

        # Figure out the vial
        vialNum = floor(colorCount / 4) + 1

        # See if we need to create a vial
        if len(vialSet) < vialNum:
            vialSet.addVial(Vial(vialNum, startEmpty=True))
            print(str(vialSet))

        # Add the color to the vial
        vialSet.getVial(vialNum).push(colors[position])
        print("Added " + str(colors[position]) + " to vial " + str(vialSet.getVial(vialNum)))

        window.repaint()
        colorCount += 1


class PictureCanvas(QWidget):
    def __init__(self):
        super(PictureCanvas, self).__init__()
        self.setGeometry(30, 30, 200, 300)

    def paintEvent(self, event):
        global isQuestionGame

        painter = QPainter(self)
        pixmap = QPixmap("./lib/Koala.png")
        painter.drawPixmap(self.rect(), pixmap)

        # Update the vial colors
        vialNum = 0
        for vial in vialSet:
            x = 10 + vialNum * 30
            vialNum += 1

            colorNum = 0
            for color in vial.colors:
                if color == UNKNOWN:
                    isQuestionGame = True
                y = 10 + (100 - colorNum * 25)
                painter.fillRect(x, y, 25, 25, QColor(color.getColor()))
                colorNum += 1

        painter.end()


class SetupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.btnGrid = ColorSelectionGrid()
        # self.btnGrid = QWidget()
        self.actionButtons = QWidget()
        self.pictureCanvas = PictureCanvas()
        self.image = QPixmap("./lib/Koala.png")
        # self.initButtonGrid()
        self.initActionButtons()

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.btnGrid)
        self.mainLayout.addWidget(self.pictureCanvas)
        self.mainLayout.addWidget(self.actionButtons)

        self.setWindowTitle("Color Selection")
        self.setGeometry(50, 50, 200, 500)

    def initActionButtons(self):
        btnLayout = QGridLayout()
        self.actionButtons.setLayout(btnLayout)

        btnSolve = QPushButton("Solve!")
        btnUndo = QPushButton("Undo")
        btnSolve.clicked.connect(lambda: self.solveTheGame())
        btnUndo.clicked.connect(lambda: self.undo())
        btnLayout.addWidget(btnUndo, 0, 0, 1, 1)
        btnLayout.addWidget(btnSolve, 0,1, 1, 1)

    # Remove the last color
    def undo(self):
        global colorCount
        vial = vialSet.getVial(len(vialSet))
        vial.pop()
        colorCount -= 1
        if vial.isEmpty():
            vialSet.removeVial(vial.getId())
        window.repaint()

    def solveTheGame(self):
        global colorCount
        # Add two empty vials
        vialSet.addVial(Vial(len(vialSet) + 1, startEmpty=True))
        vialSet.addVial(Vial(len(vialSet) + 1, startEmpty=True))

        # Make sure it's a valid game
        if not vialSet.validate(isQuestionGame):
            exit(1)

        gameMoves = []
        # PuzzleSolver.startGameWithSpecificStartingVial(
        #     vialSet, gameMoves, vialSet.getVial(10), isQuestionPuzzle=isQuestionGame)
        PuzzleSolver.getGameResult(vialSet, gameMoves, isQuestionPuzzle=isQuestionGame)

        # Print the solution steps
        print("\nSolution:")
        for qualityMove in gameMoves:
            print(qualityMove)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SetupWindow()
    window.show()
    sys.exit(app.exec_())
