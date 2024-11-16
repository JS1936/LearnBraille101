"""
    Given a single-braille-line testcase,
    store the cell makeup of each cell in the list "cells".
"""
import math
import sys

# global vars with default values
#testcase = -1
#img_h = -1
#img_w = -1
#avg_dot_diameter = -1
#avg_distance_between_adjacent_dots = -1

# Added: 5to10cells testcase with updated coord results
testcase0 = {
    21: [11.5, 24.5, 44.0],
    33: [24.5],
    62: [17.0],
    73: [24.5],
    120: [12.5, 25.0],
    161: [11.5],
    181: [28.0],
    225: [11.0, 22.5, 36.5],
    266: [21.0],
    286: [12.5],
    306: [8.5, 21.0],
    321: [7.5, 20.5],
    348: [7.0, 20.0],
    367: [24.0]
}

# 5to10cells testcase
testcase1 = {
    18: [13.0, 25.5, 38.0],
    32: [25.0],
    58: [12.5],
    72: [24.5],
    123: [10.5, 23.5],
    163: [10.5],
    177: [22.5],
    228: [9.5, 22.0, 34.5],
    268: [20.5],
    282: [8.0],
    308: [7.5, 20.5],
    322: [7.0, 20.0],
    349: [7.0, 20.0],
    364: [18.5]
}
#combo's attempt:
#thriceConsolidated = {21: [11.5, 24.5, 37.5, 44.0], 22: [11.0, 31.0, 43.5], 36: [30.5], 61: [11.0, 17.0], 76: [29.5], 127: [22.0, 29.0], 168: [14.5], 181: [21.0, 28.0], 232: [14.0, 20.0, 33.0], 272: [26], 286: [6.5, 12.5], 313: [12.5, 25.0], 327: [11.5, 24.5], 354: [11.0, 24.5], 367: [17.5, 24.0], 18: [13.0, 25.5, 38.0], 32: [25.0], 57: [13.0], 72: [24.5], 123: [10.5, 23.5], 163: [10.5], 176: [23.5], 228: [9.5, 22.0, 34.5], 268: [20.5], 282: [8.0], 308: [7.5, 20.5], 322: [7.0, 20.0], 349: [7.0, 20.0], 363: [19.0]}
#avg dot diameter = 12.256578947368421

testcase2 = {
    63: [40.5, 187.5],
    296: [40.5, 194.0],
    377: [40.5, 107.0]
}

# "Testcases" testcase
# NOTE: Starting dots have errors in them
# need better duplicate postive rulouts
# created from using "combo".
# "combo" creation does not properly get rid of "too close in h", "too close in w" duplicates
# current results: [[6], [6, 5, 6], [2, 3], [3, 2], [2, 2], [2, 3, 1], [1, 2], [1, 2, 3, 6], [6, 7]]
# this turns into... "Bebbealbv"  --> not good
testcase_sheet_title = {
    206: [43.5],
    228: [22.0, 29.0, 35.5, 43.5],  # should not have four! Presumably the 29.0 is out of place?
    230: [43.5],
    241: [15.5, 28.5],
    262: [14.5],
    276: [28.5],
    297: [42.0],
    310: [14.0],
    331: [13.5],
    345: [13.5],
    366: [12.5],
    401: [26.5, 40.5],
    415: [12.5],
    436: [12.0],
    450: [25.5],
    471: [26.5, 33.0, 39.5],
    474: [40],
    484: [12.0]
}
#avg dot diameter = 11.38

cols = dict()
def print_testcase(testcase):
    for key in testcase:
        values = testcase[key]
        print(str(key) + ": " + str(values))

#def print_globals():
    #print("-------Globals:---------")
    #print("\ttestcase = " + str(testcase))
    #print("\timg_h = " + str(img_h))
    #print("\timg_w = " + str(img_w))
    #print("\tavg_dot_diamter = " + str(avg_dot_diameter))
    #print("\tavg_distance_between_adjacent_dots = " + str(avg_distance_between_adjacent_dots))


def column(testcase, key, dividers):
    """
    Allows col1 values. If col2, the value will get updated later on.
    - len 1 or 2: use height to determine number
    - len 3: 1,2,3
    """
    values = testcase[key]
    print(str(key) + ": " + str(values))

    if key not in cols:
        cols.setdefault(key, [])

    if len(values) == 1:  # 1 value. Look at the height
        number = get_single_dot_123(values[0], dividers)
        cols[key].append(number)
        print("1 value: " + str(number) + "\n")

    elif len(values) == 2:
        num_index0 = get_single_dot_123(values[0], dividers)
        num_index1 = get_single_dot_123(values[1], dividers)
        cols[key].append(num_index0)
        cols[key].append(num_index1)
        print("2 values: " + str(num_index0) + ", " + str(num_index1) + "\n")

    elif len(values) == 3:  # full column
        cols[key].append(1)
        cols[key].append(2)
        cols[key].append(3)

    else: # len(values) is 0
        print("Error: len(values) = 0")

# Iterate through cols. If latest num > curr num: that's a new cell.
# If diff > 14, they're not in the same cell.
cells = [] # No keys

def getCellsFromCols(cols, avg_distance_between_adjacent_dots):

    # Iterate through cols. Find "cells" and append them to cells list.
    # Large gap means [], a space.
    # Small gap means same cell.
    # Between those means adjacent/different cells.

    col1to2_buffer = avg_distance_between_adjacent_dots * float(2.5 / 1.6)  # ~21, 22. was float(20/14)
    gap_start = (avg_distance_between_adjacent_dots * 7.6) / 2.5    # alternative: 6.1 instead of 7.6
    ###print("gap_start = " + str(gap_start))
    print(cols)
    keys_list = list(cols.keys())
    start_key = keys_list[0]
    #cells.append(cols[start_key])
    index = 0
    while index < len(keys_list) - 1:
        curr_key = keys_list[index]
        next_key = keys_list[index + 1]
        diff = abs(next_key - curr_key)
        print()

        #print("[diff = " + str(diff) + "] curr = " + str(curr_key) + ", next = " + str(next_key))
        #print("curr values = " + str(cols[curr_key]))
        #print("next values = " + str(cols[next_key]))
        
        if diff >= gap_start:
            #print("SPACE")
            cells.append([])
        elif diff < col1to2_buffer:
            #print("SAME CELL")
            join = cols[curr_key] + cols[next_key]  # join two lists
            #print("join = " + str(join) + " | cells = " + str(cells))
            cells.append(join)

            # Check for space that might get missed when you "jump"
            if (index + 1) < len(keys_list) - 1:
                next_next_key = keys_list[index + 2]
                diff2 = abs(next_key - next_next_key)
                if diff2 >= gap_start:
                    cells.append([])

            # "Jump"
            index += 1
        else:
            #print("DIFF CELLS")
            cells.append(cols[curr_key])
            #

        #print("cells = " + str(cells))
        index += 1

def becomeCol2(key): # does this preserve the changes?
    """
    Valid col1 values are 1, 2, and 3.
    Valid col2 values are 4, 5, and 6.
    A col1 value + 3 is the corresponding col2 value. EX: 1 --> 4.
    """
    #print("key = " + str(key))
    #print("values = " + str(cols[key]))
    new_values = []  # used in order to preserve changes made and transfer them back to cols
    for value in cols[key]:
        new_values.append(value + 3)
    cols[key].clear()
    cols[key] = new_values

# For a single dot in a testcase, determine the location id (a number [1,6]) within a cell.
def get_single_dot_123456(testcase, key, avg_distance_between_adjacent_dots): # cols, key? # added avg_distance...

    """
    The following measurements help determine the location id of a dot in a cell:
        1. shortest:    same-cell col1 to col2 distance

    If a dot is found to belong in col1, its dot id remains unchanged (1, 2, or 3).
    If a dot is found to belong in col2, becomeCol2 is called on it to update its dot id.
    """

    keys_list = list(cols.keys())
    print(keys_list)

    col1to2_buffer = avg_distance_between_adjacent_dots * float(2.5 / 1.6)  # was float(20/14)
    ###print("col1to2_buffer = " + str(col1to2_buffer))
    index = -1  # default

    # Get index from key
    if key in keys_list:
        index = keys_list.index(key)

    # If last index, do not call becomeCol2. It should already be updated. Current method updates NEXT index.
    if index == len(keys_list) - 1:  # last one
        return False
    else:
        # Not last index. If "too close" update NEXT index's value.

        # get distance from curr col to next col
        diff = abs(keys_list[index] - keys_list[index + 1])

        # same cell ("too close")
        if diff <= col1to2_buffer: # try this
            # index is col1, index + 1 is col2
            ###print("[key = " + str(key) + "] diff " + str(diff) + " < col1to2_buffer " + str(col1to2_buffer) + " ==> SAME CELL!")
            becomeCol2(keys_list[index+1])
            return True  # same cell
        else:
            return False  # not same cell
        #print("avg_distance_between_adjacent_dots = " + str(avg_distance_between_adjacent_dots))
        #print("diff = " + str(diff) + "\n")
        #exit(0)

# For each dot in the given testcase, get the location id (a number [1,6]) within a cell.
def get_all_dots_123456(testcase, avg_distance_between_adjacent_dots): #added avg_distance...

    skipNext = False
    for key in testcase:
        if(skipNext):
            skipNext = False
        else:
            skipNext = get_single_dot_123456(testcase, key, avg_distance_between_adjacent_dots)

# For a dot of height "height", determines which row of a cell it falls into.
# Returns 1, 2, or 3.
# Note: The actual dot id may end up being 4, 5, or 6.
def get_single_dot_123(height, dividers):
    if height < dividers[0]:
        return 1
    elif height < dividers[1]:
        return 2
    else: # height > dividers[1]
        return 3


# Assumption: exactly 1 line of cells
# Note: revisit whether img_h and avg_dot_diameter are needed or not.
def get_dividers(img_h, testcase, avg_dot_diameter, avg_distance_between_adjacent_dots):
    # look for dot highest in the picture (lowest value)
    uppermost = get_uppermost_h(testcase)
    bottommost = get_bottommost_h(testcase)
    ###print("uppermost  = " + str(uppermost))
    ###print("bottommost = " + str(bottommost))

    #middle_line = (uppermost + avg_distance_between_adjacent_dots)
    # top_middle_divider = (uppermost + middle_line) / 2
    # middle_bottom_divider = (middle_line + bottommost) / 2
    middle_line = abs(uppermost - bottommost) /2 #+ avg_distance_between_adjacent_dots)

    top_middle_divider = (uppermost + middle_line - avg_dot_diameter/2)
    middle_bottom_divider = (bottommost - avg_dot_diameter/2)
    ###print("middle_line           = " + str(middle_line))
    ###print("top_middle_divider    = " + str(top_middle_divider))
    ###print("middle_bottom divider = " + str(middle_bottom_divider))
    return [top_middle_divider, middle_bottom_divider]


def get_uppermost_h(testcase):
    """
    The top of the page starts at height 0.
    Therefore, the lowest value numerically is the highest one on the page.
    Given a testcase (keys, with up to 3 values per key), return the lowest (uppermost) value.
    """
    uppermost = sys.maxsize  # was img_h
    for key in testcase:
        values = testcase[key]
        for value in values:
            if value < uppermost:
                uppermost = value
    return uppermost
def get_bottommost_h(testcase):
    """
    The top of the page starts at height 0.
    Therefore, the highest value numerically is the lowest one on the page.
    Given a testcase (keys, with up to 3 values per key), return the highest (bottommost) value.
    """
    bottommost = 0
    for key in testcase:
        values = testcase[key]
        for value in values:
            if value > bottommost:
                bottommost = value
    return bottommost
def columns(testcase, dividers):
    #print(testcase)
    for key in testcase:
        column(testcase, key, dividers)
        #exit(0)

# testcase_none: ERROR - not working
def testcase_none(img, coords):

    width, height = img.size
    print("testcase_none")
    print("(coordsToCells) coords = " + str(coords))
    avg_dot_diameter = 7
    avg_distance_between_adjacent_dots = 12
    return do_testcase(height, coords, avg_dot_diameter, avg_distance_between_adjacent_dots) # added "return"


def testcase_zero(coords):
    """
    Tests Embossed_Braille_subsection_5to10cells.png
    Result: cells = [[1, 2, 3, 5], [1, 5], [], [1, 2], [1, 5], [], [1, 2, 3], [2, 4], [1, 2, 4, 5], [1, 2, 5]]
    """
    testcase = 0
    img_h = 62
    img_w = 385
    avg_dot_diameter = 9
    avg_distance_between_adjacent_dots = 14

    do_testcase(img_h, coords, avg_dot_diameter, avg_distance_between_adjacent_dots)
    return cells
    #ranges = getRowRanges(testcase0, avg_dot_diameter)
    #print("ranges = " + str(ranges))

def testcase_one():
    """
    Tests Embossed_Braille_subsection_5to10cells.png
    Result: cells = [[1, 2, 3, 5], [1, 5], 0, [1, 2], [1, 5], 0, [1, 2, 3], [2, 4], [1, 2, 4, 5], [1, 2, 5]]

    WRONG   cells = [[1, 2, 3, 5], [1, 5], 0, [1, 2], [1], [1, 5], 0, [1, 2, 3], [2], [2, 4], [1, 2, 4, 5], [1, 2, 5]]
    """
    testcase = 1
    img_h = 62
    img_w = 385
    avg_dot_diameter = 10
    avg_distance_between_adjacent_dots = 14

    do_testcase(img_h, testcase1, avg_dot_diameter, avg_distance_between_adjacent_dots)
    ranges = getRowRanges(testcase1, 10)
    print("ranges = " + str(ranges))

def testcase_two():
    """
    Tests Embossed_Braille_subsection_2cells.png
    cells = [[1, 3], [1, 3, 4, 6]]
    """
    testcase = 2
    img_h = 282
    img_w = 429
    avg_dot_diameter = 70   # guess
    avg_distance_between_adjacent_dots = 80  # guess
    do_testcase(img_h, testcase2, avg_dot_diameter, avg_distance_between_adjacent_dots)


def do_testcase(img_h, testcase, avg_dot_diameter, avg_distance_between_adjacent_dots):
    print("----------")
    print_testcase(testcase)

    print("----------")
    dividers = get_dividers(img_h, testcase1, avg_dot_diameter, avg_distance_between_adjacent_dots)
    print("dividers = " + str(dividers))
    columns(testcase, dividers)

    print("----------")
    print("cols = " + str(cols))
    get_all_dots_123456(testcase, avg_distance_between_adjacent_dots)

    print("----------")
    print("cols = " + str(cols))
    # print_testcase(cols)

    print("----------")
    print("avg_distance_between_adjacent_dots = " + str(avg_distance_between_adjacent_dots))
    getCellsFromCols(cols, avg_distance_between_adjacent_dots)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("HELLO")
    #testcase_zero(coords)
    #testcase_one()
    #testcase_two()

# Needs work:
# get_dividers -- messy
# get_single_dot_123456 -- is still hardcoded
# getCellsFromCols -- is still hardcoded
# column -- works but is unclear with naming





# Needs work:
# get_dividers -- messy
# get_single_dot_123456 -- is still hardcoded
# getCellsFromCols -- is still hardcoded
# column -- works but is unclear with naming