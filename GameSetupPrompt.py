import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon, QPainter, QPixmap, QPen
from PyQt5.QtCore import pyqtSlot, Qt

from WaterSortPuzzle import LIGHT_BLUE, DARK_BLUE, YELLOW, ORANGE, LIGHT_GREEN, GREEN, DARK_GREEN, GRAY, PURPLE, RED, \
    BROWN, PINK, UNKNOWN

colors = [LIGHT_BLUE, DARK_BLUE, YELLOW, ORANGE, LIGHT_GREEN, GREEN, DARK_GREEN, GRAY, PURPLE, RED, BROWN, PINK,
          UNKNOWN]

#
# class ColorButtonGrid(QWidget):
#
#     def __init__(self):
#         super(ColorButtonGrid, self).__init__()
#         self.layout = QGridLayout()
#         self.setLayout(self.layout)
#
#         btnCnt = 0
#         for i in range(0, 4):
#             for j in range(0, 4):
#                 if btnCnt >= len(colors):
#                     break
#                 btn = QPushButton(str(i) + str(j))
#                 btn.setText(str(colors[btnCnt]))
#                 btn.clicked.connect(lambda state, x=btnCnt: self.buttonClicked(x))
#                 if colors[btnCnt] == UNKNOWN:
#                     btn.setStyleSheet("background-color : " + str(colors[btnCnt].getColor()) + "; color: white;")
#                 else:
#                     btn.setStyleSheet("background-color : " + str(colors[btnCnt].getColor()))
#                 self.layout.addWidget(btn, i, j)
#                 btnCnt += 1
#
#     def buttonClicked(self, position):
#         global colors
#         print(str(colors[position]) + " was clicked!")
#
#
# class PictureCanvas(QWidget):
#     def __init__(self):
#         super(PictureCanvas, self).__init__()
#         self.setGeometry(30, 30, 200, 300)
#
#     def paintEvent(self, event):
#         painter = QPainter(self)
#         pixmap = QPixmap("./lib/Koala.png")
#         painter.drawPixmap(self.rect(), pixmap)
#         pen = QPen(Qt.red, 3)
#         painter.setPen(pen)
#         painter.drawLine(10, 10, self.rect().width() - 10, 10)


class SetupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.btnGrid = QWidget()
        self.pictureCanvas = QWidget()
        self.initButtonGrid()
        self.initPictureCanvas()

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.btnGrid)
        self.mainLayout.addWidget(self.pictureCanvas)

        self.setWindowTitle("Color Selection")
        self.setGeometry(50, 50, 200, 500)

    def initPictureCanvas(self):
        self.pictureCanvas.setGeometry(30, 30, 200, 300)
        painter = QPainter(self.pictureCanvas)
        pixmap = QPixmap("./lib/Koala.png")
        painter.drawPixmap(self.pictureCanvas.rect(), pixmap)

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

    def paintEvent(self, event):
        painter = QPainter(self.pictureCanvas)
        # pixmap = QPixmap("./lib/Koala.png")
        # painter.drawPixmap(self.picture.rect(), pixmap)
        pen = QPen(Qt.red, 3)
        painter.setPen(pen)
        painter.drawLine(10, 10, self.pictureCanvas.rect().width() - 10, 10)

    def buttonClicked(self, position):
        global colors
        print(str(colors[position]) + " was clicked!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SetupWindow()
    window.show()
    sys.exit(app.exec_())
