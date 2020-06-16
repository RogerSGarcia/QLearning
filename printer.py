from pprint import pprint


def printMaze(maze):
    s = ""
    even = True
    for row in maze:
        for element in row:
            if even:
                if element == 0:
                    s = s + "   "
                if element == 1:
                    s = s + " - "
                if element == 2:
                    s = s + " * "
                if element == 3:
                    s = s + " X "
            if not even:
                if element == 0:
                    s = s + "   "
                if element == 1:
                    s = s + " | "
                if element == 2:
                    s = s + " * "
                if element == 3:
                    s = s + " X "
        even = not even
        s = s + '\n'
    print(s)
