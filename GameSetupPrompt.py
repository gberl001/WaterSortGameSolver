import sys
from math import floor

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon, QPainter, QPixmap, QPen, QColor, QBrush
from PyQt5.QtCore import pyqtSlot, Qt

from WaterSortPuzzle import LIGHT_BLUE, DARK_BLUE, YELLOW, ORANGE, LIGHT_GREEN, GREEN, DARK_GREEN, GRAY, PURPLE, RED, \
    BROWN, PINK, UNKNOWN, VialSet, Vial
import WaterSortPuzzleSolver as PuzzleSolver

colors = [LIGHT_BLUE, DARK_BLUE, YELLOW, ORANGE, LIGHT_GREEN, GREEN, DARK_GREEN, GRAY, PURPLE, RED, BROWN, PINK,
          UNKNOWN]

vialSet = VialSet()
colorCount = 0
isQuestionGame = False


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
        self.btnGrid = QWidget()
        self.btnExecute = QWidget()
        self.pictureCanvas = PictureCanvas()
        self.image = QPixmap("./lib/Koala.png")
        self.initButtonGrid()
        self.initGoButton()

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.btnGrid)
        self.mainLayout.addWidget(self.pictureCanvas)
        self.mainLayout.addWidget(self.btnExecute)

        self.setWindowTitle("Color Selection")
        self.setGeometry(50, 50, 200, 500)

    def initGoButton(self):
        btnLayout = QGridLayout()
        self.btnExecute.setLayout(btnLayout)

        btn = QPushButton("Solve!")
        btn.clicked.connect(lambda: self.solveTheGame())
        btnLayout.addWidget(btn, 0, 0, 1, 1)

    def initButtonGrid(self):
        btnLayout = QGridLayout()
        self.btnGrid.setLayout(btnLayout)

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

        self.pictureCanvas.repaint()
        colorCount += 1

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
