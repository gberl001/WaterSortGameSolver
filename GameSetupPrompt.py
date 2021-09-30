import __main__
# FIXME: import __main__ is a hack to gain access to the "window" variable created in __main__
import sys
from math import floor

from PyQt5.QtGui import QPainter, QPixmap, QColor, QFont, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QDialog, QLabel, QFileDialog

import ColorSort as PictureAnalyzer
import WaterSortPuzzleSolver as PuzzleSolver
from WaterSortPuzzle import LIGHT_BLUE, DARK_BLUE, YELLOW, ORANGE, LIGHT_GREEN, GREEN, DARK_GREEN, GRAY, PURPLE, RED, \
    BROWN, PINK, UNKNOWN, VialSet, Vial

colors = [LIGHT_BLUE, DARK_BLUE, YELLOW, ORANGE, LIGHT_GREEN, GREEN, DARK_GREEN, GRAY, PURPLE, RED, BROWN, PINK,
          UNKNOWN]
guiVialSet = VialSet()
colorCount = 0
isQuestionGame = False


class ColorSelectionDialog(QDialog):

    def __init__(self, msg, vialList, vialNum, moves):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.moves = moves

        self.vialList = vialList
        self.vialNum = vialNum
        self.setWindowTitle("Select a Color")

        # Add the list of moves to make for the current situation
        self.displayMoves()

        # Add Button selection grid to the dialog
        self.btnGrid = QWidget()
        self.initButtonGrid()
        self.colorsAdded = 0

        # Add the message to the dialog
        messageFont = QFont()
        messageFont.setBold(True)
        lblMessage = QLabel(msg)
        lblMessage.setFont(messageFont)
        self.layout.addWidget(lblMessage)

        # Show buttons at the bottom of the dialog
        self.initButtonSubmit()

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

    def displayMoves(self):
        moveLayout = QVBoxLayout()

        titleFont = QFont()
        titleFont.underline()
        titleFont.setPointSize(12)
        lblTitle = QLabel("Steps to perform:")
        lblTitle.setFont(titleFont)
        moveLayout.addWidget(lblTitle)

        for move in self.moves:
            moveLayout.addWidget(QLabel(str(move)))

        __main__.window.displayMoveArrow(self.moves[len(self.moves) - 1])

        self.layout.addLayout(moveLayout)

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
        removedColor = None
        for i in range(0, self.colorsAdded):
            removedColor = vial.pop()
        for i in range(0, self.colorsAdded):
            vial.push(UNKNOWN)

        self.colorsAdded = 0
        print("Removed " + str(removedColor) + " from vial " + str(self.vialList.getVial(self.vialNum)))
        __main__.window.repaint()


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
        global colors, colorCount, guiVialSet

        # Figure out the vial
        vialNum = floor(colorCount / 4) + 1

        # See if we need to create a vial
        if len(guiVialSet) < vialNum:
            guiVialSet.addVial(Vial(vialNum, startEmpty=True))
            print(str(guiVialSet))

        # Add the color to the vial
        guiVialSet.getVial(vialNum).push(colors[position])
        # print("Added " + str(colors[position]) + " to vial " + str(guiVialSet.getVial(vialNum)))

        self.parent().repaint()
        colorCount += 1


class PictureCanvas(QWidget):
    def __init__(self):
        super(PictureCanvas, self).__init__()
        self.setGeometry(30, 30, 200, 300)
        self.lastMove = None

    def displayMoveArrow(self, move):
        self.lastMove = move

    def paintEvent(self, event):
        global isQuestionGame, guiVialSet
        xOffset = 10
        yOffset = 10
        colorSquareSize = 25
        spaceBetweenVials = 5

        painter = QPainter(self)
        pixmap = QPixmap("./lib/Koala.png")
        painter.drawPixmap(self.rect(), pixmap)

        # Update the vial colors
        vialNum = 0
        for vial in guiVialSet:
            x = xOffset + vialNum * (colorSquareSize + spaceBetweenVials)
            vialNum += 1

            colorNum = 0
            for color in vial.colors:
                if color == UNKNOWN:
                    isQuestionGame = True
                y = yOffset + (100 - colorNum * colorSquareSize)
                painter.fillRect(x, y, colorSquareSize, colorSquareSize, QColor(color.getColor()))
                colorNum += 1

        # Paint the last move arrow
        if self.lastMove is not None:
            # Find the location of vialFrom and vialTo
            fromId = self.lastMove.getFromVial().getId()
            toId = self.lastMove.getToVial().getId()

            xFrom = floor(xOffset + fromId * (colorSquareSize + spaceBetweenVials) -
                          (colorSquareSize + spaceBetweenVials) / 2)
            xTo = floor(xOffset + toId * (colorSquareSize + spaceBetweenVials) -
                        (colorSquareSize + spaceBetweenVials) / 2)

            arrowPen = QPen()
            arrowPen.setColor(QColor("#000000"))
            arrowPen.setWidth(2)
            painter.setPen(arrowPen)

            # Draw the arrow
            if xFrom < xTo:
                arrowOffset = -5
            else:
                arrowOffset = +5
            painter.drawLine(xFrom, 35, xTo, 35)
            painter.drawLine(xTo + arrowOffset, 30, xTo, 35)
            painter.drawLine(xTo + arrowOffset, 40, xTo, 35)

        painter.end()


class SetupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.btnGrid = ColorSelectionGrid()
        # Create the widgets
        self.lblMessage = QLabel()
        self.actionButtons = QWidget()
        self.pictureCanvas = PictureCanvas()

        self.image = QPixmap("./lib/Koala.png")
        self.initActionButtons()

        # Main layout is a vertical layout, each item added is below the previous items
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        # Add file selection button at the top
        self.initFileButton()
        # Next add the color selection button grid
        self.mainLayout.addWidget(self.btnGrid)
        # Next add the vial set image
        self.mainLayout.addWidget(self.pictureCanvas)
        # Next add the action buttons, and the message box
        self.mainLayout.addWidget(self.actionButtons)

        self.setWindowTitle("Color Selection")
        self.setGeometry(50, 50, 200, 500)

    def initFileButton(self):
        btnFile = QPushButton("Open image...")
        btnFile.clicked.connect(lambda: self.selectAFile())
        self.mainLayout.addWidget(btnFile)

    def displayMoveArrow(self, move):
        self.pictureCanvas.displayMoveArrow(move)

    def initActionButtons(self):
        btnLayout = QGridLayout()
        self.actionButtons.setLayout(btnLayout)

        # Add the action buttons
        btnSolve = QPushButton("Solve!")
        btnUndo = QPushButton("Undo")
        btnSolve.clicked.connect(lambda: self.solveTheGame())
        btnUndo.clicked.connect(lambda: self.undo())
        btnLayout.addWidget(btnUndo, 0, 0, 1, 1)
        btnLayout.addWidget(btnSolve, 0, 1, 1, 1)

        # Add the message section
        self.lblMessage.setStyleSheet("color: red")
        btnLayout.addWidget(self.lblMessage, 1, 0, 1, 2)

    def selectAFile(self):
        global colorCount, guiVialSet
        file, check = QFileDialog.getOpenFileName(None, "Select Image", "", "All Files (*)")
        if check:
            guiVialSet = PictureAnalyzer.getVials(file, getEmpty=False)
            self.parent().repaint()

    # Remove the last color
    def undo(self):
        global colorCount, guiVialSet
        vial = guiVialSet.getVial(len(guiVialSet))
        vial.pop()
        colorCount -= 1
        if vial.isEmpty():
            guiVialSet.removeVial(vial.getId())
        self.parent().repaint()

    def solveTheGame(self):
        global colorCount, guiVialSet
        # Ensure there are two empty vials
        for i in range(2 - guiVialSet.getEmptyVialCount()):
            guiVialSet.addVial(Vial(len(guiVialSet) + 1, startEmpty=True))

        # Make sure it's a valid game
        if guiVialSet.validate(isQuestionGame):
            self.lblMessage.setText("")
            moves = []
            result = PuzzleSolver.getGameResult(guiVialSet, moves, isQuestionPuzzle=isQuestionGame)

            if result:
                self.lblMessage.setText("Success: Solution Found")

            # Print the solution steps
            print("\nSolution:")
            for move in moves:
                print(move)

            PuzzleSolver.displaySolutionSteps(moves)
        else:
            self.lblMessage.setText("Invalid game, check your entry and try again")

        window.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SetupWindow()
    window.show()
    sys.exit(app.exec_())
