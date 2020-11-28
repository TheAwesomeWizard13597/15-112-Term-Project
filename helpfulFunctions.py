
##############################################
#intended to create a set of helpful functions for testing purposes
#And for conciseness
##############################################
import math, sys
import numpy as np
# Obtained from class notes
def findInstallLibrary(library):
    print(f'"{sys.executable}" -m pip install '+library)

def make2dList(rows, cols):
    return [ ([None] * cols) for row in range(rows) ]

# Helper function for print2dList.
# This finds the maximum length of the string
# representation of any item in the 2d list
def maxItemLength(a):
    maxLen = 0
    for row in range(len(a)):
        for col in range(len(a[row])):
            maxLen = max(maxLen, len(repr(a[row][col])))
    return maxLen

def print2dList(a):
    if a == []:
        print([])
        return
    print()
    rows, cols = len(a), len(a[0])
    maxCols = max([len(row) for row in a])
    fieldWidth = max(maxItemLength(a), len(f'col={maxCols-1}'))
    rowLabelSize = 5 + len(str(rows-1))
    rowPrefix = ' '*rowLabelSize+' '
    rowSeparator = rowPrefix + '|' + ('-'*(fieldWidth+3) + '|')*maxCols
    print(rowPrefix, end='  ')
    # Prints the column labels centered
    for col in range(maxCols):
        print(f'col={col}'.center(fieldWidth+2), end='  ')
    print('\n' + rowSeparator)
    for row in range(rows):
        # Prints the row labels
        print(f'row={row}'.center(rowLabelSize), end=' | ')
        # Prints each item of the row flushed-right but the same width
        for col in range(len(a[row])):
            print(repr(a[row][col]).center(fieldWidth+1), end=' | ')
        # Prints out missing cells in each column in case the list is ragged
        missingCellChar = chr(10006)
        for col in range(len(a[row]), maxCols):
            print(missingCellChar*(fieldWidth+1), end=' | ')
        print('\n' + rowSeparator)
    print()



#Self-coded
def distance(x0, y0, x1, y1):
    return(math.sqrt((x0-x1)**2 + (y0-y1)**2))

#Takes two tuples of four elements each and returns if the rectangles made
#By the tuples of coordinates intersect
def rectangleIntersect(rect1Dim, rect2Dim):
    rect1xR, rect1yB, rect1xL, rect1yT = rect1Dim
    rect2xR, rect2yB, rect2xL, rect2yT = rect2Dim
    if rect1xR <= rect2xL or rect2xR <= rect1xL:
        return False
    if rect1yB <= rect2yT or rect2yB <= rect1yT:
        return False
    return True


def linefit(x0, x1, y0, y1):
    pass
#Takes three tuples, lineStart and lineEnd are (x, y) coordinates, rectDim has four elements
def lineInRectangle(lineStart, lineEnd, rectDim):
    rectx0, recty0, rectx1, recty1 = rectDim
    xCoords = [lineStart[0], lineEnd[0]]
    yCoords = [lineStart[1], lineEnd[1]] #bound lines
    coefficients = np.polyfit(xCoords, yCoords, 1) #Write this myself :)
    if rectx0 * coefficients[0] + coefficients[1] > recty0:
        checker = 1
    else:
        checker = -1

    for x, y in [(rectx0, recty1), (rectx1, recty1), (rectx1, recty0)]:
        if x * coefficients[0] + coefficients[1] < y and checker == 1:
            return True
        if x * coefficients[0] + coefficients[1] > y and checker == -1:
            return True
    return False

def lineInRectangle2(lineStart, lineEnd, rectDim):
    dx = (lineStart[0] - lineEnd[0])/10
    dy = (lineStart[1] - lineEnd[1])/10
    for i in range(10):
        if pointInRectangle((lineStart[0] + dx*i, lineStart[1] + dy*i), rectDim):
            return True
    return False

def pointInRectangle(pointCoords, rectCoords):
    rectx0, recty0, rectx1, recty1 = rectCoords
    if rectx0 < pointCoords[0] < rectx1 and recty0 < pointCoords[1] < recty1:
        return True
    return False

    


##############################################
#intended to create a set of helpful functions for testing purposes
#And for conciseness
#Programmed by Ryan Bao Testing Part 2
#ABCDEFG
##############################################
import math
import sys
# Obtained from class notes
def findInstallLibrary(library):
    print(f'"{sys.executable}" -m pip install '+library)

def make2dList(rows, cols):
    return [ ([None] * cols) for row in range(rows) ]

# Helper function for print2dList.
# This finds the maximum length of the string
# representation of any item in the 2d list
def maxItemLength(a):
    maxLen = 0
    for row in range(len(a)):
        for col in range(len(a[row])):
            maxLen = max(maxLen, len(repr(a[row][col])))
    return maxLen

def print2dList(a):
    if a == []:
        print([])
        return
    print()
    rows, cols = len(a), len(a[0])
    maxCols = max([len(row) for row in a])
    fieldWidth = max(maxItemLength(a), len(f'col={maxCols-1}'))
    rowLabelSize = 5 + len(str(rows-1))
    rowPrefix = ' '*rowLabelSize+' '
    rowSeparator = rowPrefix + '|' + ('-'*(fieldWidth+3) + '|')*maxCols
    print(rowPrefix, end='  ')
    # Prints the column labels centered
    for col in range(maxCols):
        print(f'col={col}'.center(fieldWidth+2), end='  ')
    print('\n' + rowSeparator)
    for row in range(rows):
        # Prints the row labels
        print(f'row={row}'.center(rowLabelSize), end=' | ')
        # Prints each item of the row flushed-right but the same width
        for col in range(len(a[row])):
            print(repr(a[row][col]).center(fieldWidth+1), end=' | ')
        # Prints out missing cells in each column in case the list is ragged
        missingCellChar = chr(10006)
        for col in range(len(a[row]), maxCols):
            print(missingCellChar*(fieldWidth+1), end=' | ')
        print('\n' + rowSeparator)
    print()

        
def thunk():
    return(False)

