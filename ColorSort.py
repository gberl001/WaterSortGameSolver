import cv2
import numpy as np
from matplotlib import pyplot as plt
from math import sqrt
from WaterSortPuzzle import Vial, LIGHT_BLUE, DARK_BLUE, YELLOW, ORANGE, LIGHT_GREEN, GREEN, DARK_GREEN, GRAY, PURPLE, \
    RED, BROWN, PINK, Move, VialSet, UNKNOWN
from WaterSortPuzzleSolver import getGameResult


def getVials(path, getEmpty=True):
    stx = 0
    vials = []
    gameMoves = []
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(
        threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    i = 0
    count = 0
    _, stx, _ = img.shape
    colordict = {(26, 26, 26): "Empty", (229, 163, 85): LIGHT_BLUE, (195, 47, 59): DARK_BLUE, (87, 217, 240): YELLOW,
                 (65, 140, 232): ORANGE, (125, 214, 97): LIGHT_GREEN, (14, 151, 120): GREEN, (52, 100, 18): DARK_GREEN,
                 (102, 100, 99): GRAY, (145, 43, 115): PURPLE, (35, 42, 199): RED, (8, 74, 125): BROWN,
                 (125, 92, 236): PINK, (53, 50, 48): UNKNOWN, (255, 255, 255): UNKNOWN}
    COLORS = [
        (26, 26, 26),   # Empty
        (229, 163, 85),  # Light Blue
        (195, 47, 59),  # Dark Blue
        (87, 217, 240),  # Yellow
        (65, 140, 232),  # Orange
        (125, 214, 97),  # Light Green
        (14, 151, 120),  # Green
        (52, 100, 18),  # Dark Green
        (102, 100, 99),  # Gray
        (145, 43, 115),  # Purple
        (35, 42, 199),  # Red
        (8, 74, 125),  # Brown
        (125, 92, 236),  # Pink
        (53, 50, 48),  # Unknown
        (255, 255, 255),  # Unknown
    ]


    def closest_color(b, g, r):
        color_diffs = []
        for color in COLORS:
            cb, cg, cr = color
            color_diff = sqrt(abs(b - cb)**2 + abs(g - cg)**2 + abs(r - cr)**2)
            color_diffs.append((color_diff, color))
        return min(color_diffs)[1]


    for contour in contours:

        if i == 0:
            i = 1
            continue

        approx = cv2.approxPolyDP(
            contour, 0.01 * cv2.arcLength(contour, True), True)

        try:
            x, y, w, h = cv2.boundingRect(approx)
            if h > 150:
                try:
                    if y - sty < -50:
                        _, stx, _ = img.shape
                except:
                    pass
                if -400 < x-stx < -20:
                    sty = y
                    stx = x
                    newim = img[y:y+h, x:x+w]
                    cv2.drawContours(img, [contour], 0, (0, 0, 255), 10)
                    cv2.putText(img, 'vial', (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    vials.append(newim)
        except:
            pass


    gameVialSet = VialSet()
    questionGame = False


    for i, vial in enumerate(vials):
        colors = []
        h, w, _ = vial.shape
        pos = [vial[int(h * 0.17), w - 25], vial[int(h * 0.51), w - 25], vial[int(h * 0.68), w - 25],
               vial[int(h * 0.93), w - 25]]
        for p in pos:
            (b, g, r) = p
            close = closest_color(b, g, r)
            final = colordict[close]
            colors.append(final)
            if final == UNKNOWN:
                questionGame = True

        if final == "Empty":
            if getEmpty:
                gameVialSet.addVial(Vial(len(vials) - i, startEmpty=True))
        else:
            gameVialSet.addVial(Vial(len(vials) - i, colors[0], colors[1], colors[2], colors[3]))
    return gameVialSet


def solve(gameVialSet, gameMoves, questionGame):
    getGameResult(gameVialSet, gameMoves, isQuestionPuzzle=questionGame)
    print("\nSolution:")
    """most_recent_file = max((os.path.join(root,f) for root,_,the_files in os.walk(path) for f in the_files if f.lower().endswith(".cpp")),key=os.path.getctime)
    """
    for qualityMove in gameMoves:
        print(qualityMove)