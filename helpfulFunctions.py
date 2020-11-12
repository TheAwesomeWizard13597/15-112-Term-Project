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



#Self-coded
def distance(x0, y0, x1, y1):
    return(math.sqrt((x0-x1)**2 + (y0-y1)**2))

#Takes two tuples of four elements each and returns if the rectangles made
#By the tuples of coordinates intersect
def pointInRectangle(rect1Dim, rect2Dim): 
    rect1x0, rect1y0, rect1x1, rect1y1 = rect1Dim
    rect2x0, rect2y0, rect2x1, rect2y1 = rect2Dim
    if rect1x0 < rect2x0 < rect1x1 and rect1y0 < rect2y0 < rect1y1:
        return True
    if rect1x0 < rect2x1 < rect1x1 and rect1y0 < rect2y0 < rect1y1:
        return True
    if rect1x0 < rect2x0 < rect1x1 and rect1y0 < rect2y1 < rect1y1:
        return True
    if rect1x0 < rect2x1 < rect1x1 and rect1y0 < rect2y1 < rect1y1:
        return True
    return False

        
    

findInstallLibrary('')