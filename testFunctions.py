import numpy as np
from helpfulFunctions import *

print('Testing Line in Rectangle!')
assert(lineInRectangle((0, 0), (5, 5), (3, 3, 7, 7))== True)
assert(lineInRectangle((0, 0), (5, 5), (2, 0, 3, 1)) == False)
assert(pointInRectangle((1, 1), (0, 0, 2, 2)) == True)
assert(pointInRectangle((3, 3), (0, 0, 2, 2)) == False)
print('Passed!')