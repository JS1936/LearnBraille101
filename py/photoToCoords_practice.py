import imghdr
import os
from PIL import Image
from itertools import product

# Global variables:
# Picture-Specific
avg_dot_base_diameter = 0  # default
ratio = 0  # default

# Dot Base Diameter (mm)
min_dot_base_diameter = 1.5
max_dot_base_diameter = 1.6

# Distance Between Two Dots in the Same Cell (mm)
min_distance_between_two_dots_in_the_same_cell = 2.3
max_distance_between_two_dots_in_the_same_cell = 2.5

# Distance Between Corresponding Dots In Adjacent Cell (mm)
min_distance_between_corresponding_dots_in_adjacent_cells = 6.1
max_distance_between_corresponding_dots_in_adjacent_cells = 7.6

# Not using dot height

# Distance Between Corresponding Dots from One Cell Directly Below (mm)
min_distance_between_corresponding_dots_in_one_cell_directly_below = 10.0
max_distance_between_corresponding_dots_in_one_cell_directly_below = 10.2



#Note: still need to get leftmost dot.
#^Start with that row for initial testing, don't bother moving upward to left_top.
cells = []


# try feeding it in knowing whether it's col1 or col2 (when doing append, just do num + 3 if col2)
def predictCellDots(peaks, pixels2, img2, ratio, w, h, isCol1, cell):
    # look at height vals for the row
    # and establish acceptable "borders" between row1, row2, row3
    print("PREDICT CELL DOTS")
    first_peak = peaks[0]
    leftmost_col = first_peak[0]
    leftmost_rows = first_peak[1]
    leftmost_dot = [leftmost_col, leftmost_rows[0]]
    print("leftmost_dot = " + str(leftmost_dot))

    jump_down_amt = max_distance_between_two_dots_in_the_same_cell * ratio
    print("jump_down_amt = " + str(jump_down_amt))
    # 17 + 11(1.5) = 17 + 11 + 5.5 = 33.5. If val is > 22.5 and val < 33.5
    cell.append(1)


    index = 1
    while index < len(leftmost_rows):
        dot2_expect = leftmost_rows[index - 1] + 11
        dot2_possible = leftmost_rows[index]
        print("dot expected near: " + str(dot2_expect))
        print("dot found at: " + str(dot2_possible))
        # lower bound and upper bound
        if (dot2_possible > (dot2_expect - (jump_down_amt/2))) and (dot2_possible < (dot2_expect + (jump_down_amt/2))):
            if isCol1 == True:
                cell.append(index + 1)
            else:
                cell.append(index + 4)
        index += 1

    # try to get a sense of col2
    #jump_over_amt = max_distance_between_corresponding_dots_in_adjacent_cells * ratio
    #dot_expect = leftmost_col + jump_over_amt
    #dot_lowerBound = dot_expect - (jump_over_amt/2)
    #dot_upperBound = dot_expect + (jump_over_amt/2)

    #print("jump_over_amt    = " + str(jump_over_amt))
    #print("leftmost_col     = " + str(leftmost_col))
    #print("dot_expect       = " + str(dot_expect))
    #print("dot_lowerBound   = " + str(dot_lowerBound))
    #print("dot_upperBound   = " + str(dot_upperBound))
    #col2_topDot = [leftmost_col, leftmost_rows[0] + jump_over_amt]
    #print("col2_topDot = " + str(col2_topDot))

    print("cell = " + str(cell))


    return 0
def drawPredictionGrid(peaks, pixels2, img2, ratio, w, h): #peaks? dots?
    print("drawPredictionGrid in progress")

    first_peak = peaks[0]
    leftmost_col = first_peak[0]
    leftmost_rows = first_peak[1]
    leftmost_dot = [leftmost_col, leftmost_rows[0]]
    print("leftmost_dot = " + str(leftmost_dot))
    pixels2[leftmost_col, leftmost_rows[0]] = (0, 255, 0) # tiny green dot


    #leftmost =
    # draw col1row1's (jump rightward 6.0*ratio each time)
    print("ratio = " + str(ratio))

    #pixels2[leftmost_col+ jump_amt, leftmost_rows[0]] = (0, 255, 0)
    #img2.show()
    #exit(0)

    jump_amt = max_distance_between_corresponding_dots_in_adjacent_cells * ratio
    jump_down_amt = max_distance_between_two_dots_in_the_same_cell * ratio
    #jump_amt2 = min_distance_between_corresponding_dots_in_adjacent_cells * ratio
    print("jump_across_amt = " + str(jump_amt))
    print("jump_down_amt = " + str(jump_down_amt))
    indexW = leftmost_col
    #indexW2 = leftmost_rows[0]
    indexH = leftmost_rows[0]
    while indexW < w: # revisit this
        print("indexW = " + str(indexW) + "; w = " + str(w) + "; h = " + str(h))
        pixels2[indexW, indexH] = (0, 255, 0)  # tiny green dot
        pixels2[indexW -1, indexH] = (0, 255, 0)
        pixels2[indexW + 1, indexH] = (0, 255, 0)

        if (indexH + jump_down_amt) < h:
            pixels2[indexW - 1, indexH + jump_down_amt] = (0, 255, 0)
        if (indexH + 2*jump_down_amt) < h:
            pixels2[indexW + 1, indexH + (jump_down_amt * 2)] = (0, 255, 0)
        #pixels2[indexW2, indexH] = (255, 0, 0) # tiny red dot

        indexW += (jump_amt)  # is that okay? # int(jump_amt)


    #img2.show()
    # from leftmost, move down by 2.3*ratio, then do the same thing to do col1srow2's

    # repeat again for col1row3s
    # --------------------------
    # now need to do col2s: repeat the whole previous process, but move to col2 instead of col1
    # "offset"

    indexW = leftmost_col + jump_down_amt
    while indexW < w:  # revisit this
        print("indexW = " + str(indexW) + "; w = " + str(w))
        pixels2[indexW, indexH] = (128, 0, 128)  # tiny purple dot
        pixels2[indexW - 1, indexH] = (128, 0, 128)





        if (indexH + jump_down_amt) < h:
            pixels2[indexW - 1, indexH + jump_down_amt] = (128, 0, 128)
        if (indexH + 2 * jump_down_amt) < h:
            pixels2[indexW + 1, indexH + (jump_down_amt * 2)] = (128, 0, 128)
        # pixels2[indexW2, indexH] = (255, 0, 0) # tiny red dot

        indexW += (jump_amt)  # is that okay? # int(jump_amt)
    #img2.show()
    return 0

def saveOriginalFile(filename, dir_in):
    name, ext = os.path.splitext(filename)
    img = Image.open(os.path.join(dir_in, filename))

    # try this
    #rgb_img = img.convert('RGB')
    #rgb_img.save(filename + ".jpg")

    return img
    #return rgb_img

def tile2(filename, dir_in, dir_out, d):

    # Open img from filename
    print("filename = " + str(filename))
    name, ext = os.path.splitext(filename)
    desired_ext = ".png"
    img = Image.open(os.path.join(dir_in, name + desired_ext)) # filename
    w, h = img.size
    img.show()
    print("image size = " + str(img.size))
    print("w = " + str(w))
    print("h = " + str(h))
    pixel_values = list(img.getdata())

    # Split img into pieces (like a puzzle) and do dot detection. After, do reassembly.
    grid = product(range(0, h - h % d, d), range(0, w - w % d, d))
    for i, j in grid:
        # save image piece
        box = (j, i, j + d, i + d)
        out = os.path.join(dir_out, f'{name}_{i}_{j}{desired_ext}') #ext #i = height, j = width
        img.crop(box).save(out)

        # for each tile, do dot detection
        curr_tile = tile(out, dir_in, dir_out, d)
        curr_tile.save(out)


    # take care of "leftovers"
    print("h - h % d = " + str(h - h % d))
    print("w - w % d = " + str(w - w % d))
    print("h % d = " + str(h % d))
    print("w % d = " + str(w % d))
    tile_rightmost_start = w - w % d
    tile_lowest_start = h - h % d

    # height of picture does not split evenly by divider d. Catch/save leftovers
    if h % d != 0:
        curr_w = 0
        while curr_w < w:
            print("h = " + str(h) + ", curr_w = " + str(curr_w))
            print("--> tile_lowest_start = " + str(tile_lowest_start))

            #box = (j, i, j + d, i + d)
            box = (curr_w, tile_lowest_start, curr_w + d, h)
            out = os.path.join(dir_out, f'{name}_{tile_lowest_start}_{curr_w}{desired_ext}') #ext
            print("out = " + str(out))
            img.crop(box).save(out)
            #img.show()

            # for each tile, do dot detection
            curr_tile = tile(out, dir_in, dir_out, d)
            curr_tile.save(out)
            #curr_tile.show()
            curr_w += d

    # width of picture does not split evenly by divider d. Catch/save leftovers
    # note: bottom right corner may get saved twice (written over once)
    #       if both w and h split unevenly by divider d
    # note: remember to double check this
    if w % d != 0:
        curr_h = 0
        while curr_h < h:
            print("w = " + str(w) + ", curr_h = " + str(curr_h))
            print("--> tile_rightmost_start = " + str(tile_rightmost_start))
            #box = (j, i, j + d, i + d)
            box = (tile_rightmost_start, curr_h, w, curr_h + d)
            out = os.path.join(dir_out, f'{name}_{curr_h}_{tile_rightmost_start}{desired_ext}') #ext
            print("out = " + str(out))
            img.crop(box).save(out)
            #img.show()

            # for each tile, do dot detection
            curr_tile = tile(out, dir_in, dir_out, d)
            curr_tile.save(out)
            curr_h += d

    # reassemble the image from its dot-detected parts
    reassembled_img = reassembleThePicture(img, name, dir_out, d, grid) # could instead call per tile
    reassembled_img.show()

    # HERE: use reassembled image (green and black indicate dots) to read cells
    dots_keyW = dict()
    black_keyW = dict() # turn it into a dictionary...
    black_keyH = dict()
    green_keyW = dict()
    reassembled_pixels = reassembled_img.load()
    for i in range(reassembled_img.size[0]):  # for every pixel:        # w
        for j in range(reassembled_img.size[1]):  # h
            curr_pixel = reassembled_pixels[i, j]
            #print("curr_pixel = " + str(curr_pixel))
            r,g,b,a = curr_pixel
            sum = r + g + b
            if sum == 0: # "black" #opt--> <50
                #print("found a black dot!")

                # update black_keyW
                if i not in black_keyW.keys():
                    black_keyW.setdefault(i, [])
                black_keyW[i].append(j)

                # update black_keyH
                if j not in black_keyH.keys():
                    black_keyH.setdefault(j, [])
                black_keyH[j].append(i)
            #if g = 255 sum > 240 and sum < 260: # should be 255 exactly, but... (?)
            if r == 0 and g == 255 and b == 0:
                #print("found a green dot!")
                # update green_keyW
                if i not in green_keyW.keys():
                    green_keyW.setdefault(i, [])
                green_keyW[i].append(j)

                #print(i,j)
                #exit(0)
            #print("curr_pixel = " + str(curr_pixel))
    #print("black_keyW = " + str(black_keyW))
    #print("black_keyH = " + str(black_keyH))
    #print("green_keyW = " + str(green_keyW))
    reassembled_img.show()
    avgDiameter = calculateAvgDotDiameter(reassembled_img) # REVISIT / FIX
    # estimate the avg distance between

    standard_min_distance_between_6High_2Low = 5.4 # 11.0 - 2*2.5 # 10.0 - 4.6 = 5.4
    diameterRatio = avgDiameter / min_dot_base_diameter
    print("diameterRatio = " + str(diameterRatio))
    avg6H2LDiff = diameterRatio * 5.4
    print("avg6H2LDiff = " + str(avg6H2LDiff))

    #       average dot diameter        average 6High 2Low diff
    #       --------------------    =   ------------------------
    #       standard dot diameter       standard 6High 2Low diff
    #
    #
    #   Therefore, average6High2Low diff = (averageDotDiameter * standard62) / standard dot diameter
    #
    print("averageDiameter = " + str(avgDiameter))
    #average6High2LowDiff = (avgDiameter * standard_min_distance_between_6High_2Low) / min_dot_base_diameter
    print("average6High2LowDiff = " + str(avg6H2LDiff))
    #exit(0)


    combo = black_keyW.copy()
    for key in green_keyW.keys():
        values = green_keyW[key]
        if key not in combo:
            combo.setdefault(key, [])
        for value in values:
            combo[key].append(value)
        combo[key].sort()
    combo_sorted = dict(sorted(combo.items())) # revisit this
    # try this--> LOOK
    #green_keyW = combo
    green_keyW.clear()
    green_keyW = combo_sorted.copy()#black_keyW.copy()


    # Try isolating the black so that it is one pixel per dot
    """
    black = {   
                21: [10, 11, 12, 13, 24, 25, 37, 38, 44], 
                22: [11, 31, 43, 44], 
                23: [16, 17, 18, 29, 30, 42, 43],
                24: [15, 16, 17, 29, 30, 41, 42, 43], 
                36: [30, 31], 
                37: [29, 30, 31], 
                38: [29, 30], 
                61: [10, 11, 12, 17],
                62: [10, 11, 16, 17, 18], 
                63: [16, 17], 
                64: [16, 17], 
                76: [29, 30], 
                77: [28, 29, 30], 
                127: [22, 29],
                128: [14, 15, 28, 29], 
                168: [14, 15], 
                181: [21, 28], 
                182: [27, 28], 
                183: [26, 27], 
                232: [14, 20, 33],
                233: [13, 14, 26, 27, 39, 40], 
                234: [13, 25, 26, 37, 38, 39], 
                272: [26], 
                273: [26], 
                274: [25],
                286: [6, 7, 12, 13], 
                287: [11, 12, 13], 
                313: [12, 13, 25], 
                314: [11, 12, 23, 24, 25],
                327: [11, 12, 24, 25], 
                328: [11, 24], 329: [23, 24], 
                353: [4, 11, 12], 
                354: [10, 11, 12, 24, 25],
                355: [10, 11, 23, 24, 25], 
                356: [10], 367: [17, 18, 24], 
                368: [23, 24, 25], 369: [23, 24, 25],
                370: [21, 22, 23, 24]}
    """
    combo_consolidated, avgDotDiameter = consolidate_all(combo_sorted)
    #combo_consolidated, avgDotDiameter = consolidate_all(green_keyW)
    #consolidatedGreen, avgDotDiameter = consolidate(green_keyW)

    #exit(0)
    ###drawLines(reassembled_img, thriceConsolidated, estimated_distance_between_corresponding_dots_in_one_cell_directly_below)
    #drawLinesHorizontal(reassembled_img, thriceConsolidated, estimated_distance_between_corresponding_dots_in_one_cell_directly_below)


    reassembled_img_withOrange = markDots(combo_consolidated, reassembled_img)

    return combo_consolidated # added,  should return coords

    ###sorted_swapped = swap(combo_consolidated, avgDotDiameter)
    ###drawLinesHorizontal2(reassembled_img, sorted_swapped, avg6H2LDiff)

#print(green_keyW)
# Use avgDotDiameter to rule out redundancies...
# For each peak, check surroundings... remove keys as needed until no longer applies
# Expect to remove: 15, 22, 199, 127, 224, 232, 305, 353
# Assumption for now: maximum of 3 rows
#previously named "consolidateAgain(twiceConsolidated, avgDotDiameter)"
def round4_consolidate(twiceConsolidated, avgDotDiameter):

    print("twiceConsolidated = " + str(twiceConsolidated))
    #exit(0)
    avgDotRadius = avgDotDiameter / 2
    print("\navgDotDiameter = " + str(avgDotDiameter))
    print("avgDotRadius   = " + str(avgDotRadius))  # EX: for 2cell screenshot, avgDotRadius is 46.30666...
    keys_list = list(twiceConsolidated.keys())
    print("keys_list = " + str(keys_list))

    keys_index = 1
    keys_to_remove = [] #what if you did keys to keep instead of keys to remove
    #keys_to_keep = []
    while keys_index < (len(keys_list) - 1):
        """
            1. Look for keys close enough (diff is <= avgDotRadius)
            2. Within keys close enough, determine which key to keep (keep whichever has more vals)
        """

        # get curr, prev, and next keys
        curr_key = keys_list[keys_index]
        prev_key = keys_list[keys_index - 1]
        next_key = keys_list[keys_index + 1]

        # get curr, prev, and next length (number of values)
        curr_len = len(twiceConsolidated[curr_key])
        prev_len = len(twiceConsolidated[prev_key])
        next_len = len(twiceConsolidated[next_key])

        # get absolute difference between prev key and curr key, between curr key and next key
        curr_prev_key_diff = abs(prev_key - curr_key)
        curr_next_key_diff = abs(curr_key - next_key)

        # print
        print("\ncurr_key = " + str(curr_key) + "(" + str(curr_len) + ")")
        #print("prev_key = " + str(prev_key) + "(" + str(prev_len) + ")")
        #print("next_key = " + str(next_key) + "(" + str(next_len) + ")")
        print("avgDotRadius = " + str(avgDotRadius)) #~9 for 5to10cells
        #print("curr_prev_key_diff = " + str(curr_prev_key_diff))
        #print("curr_next_key_diff = " + str(curr_next_key_diff))

        # same cell.
        if curr_prev_key_diff < avgDotRadius:  # same cell. Keep whichever picks up more dots (up to 3) # was avgDotRadius
                if curr_len >= prev_len:
                    keys_to_remove.append(prev_key)
                    print("expect to remove key (prev) " + str(prev_key))
                else:
                    keys_to_remove.append(curr_key)
                    print("expect to remove key (curr) " + str(curr_key))
        #else:
        #    print("Found a key to keep! Key: " + str(curr_key))
        #    keys_to_keep.append(prev_key)
        #    exit(0)
        if curr_key in keys_to_remove:
            curr_key = prev_key

        print("keys_list = " + str(keys_list))
        #print("keys_to_remove = " + str(keys_to_remove))
        #5to10cells:
        #keys_list = [15, 18, 21, 22, 34, 57, 61, 63, 73, 119, 124, 164, 176, 181, 182, 224, 229, 269, 282, 286, 287,
        #             305, 308, 313, 322, 327, 329, 351, 356, 363, 367, 369]
        #exit(0)
        # changed from if to while
        while abs(curr_key - next_key) <= avgDotRadius:#radius? # if or while?
                print("curr_key = " + str(curr_key) + ", next_key = " + str(next_key) + ", keys_index = " + str(keys_index))
                print("curr = " + str(twiceConsolidated[curr_key]))
                print("next = " + str(twiceConsolidated[next_key])) # this has 4 when it should have max 3. That means something is wrong with the choosing of keys EARLIER.

                curr_len = len(twiceConsolidated[curr_key]) # added 8/30, effects not checked
                next_len = len(twiceConsolidated[next_key]) # added 8/30, effects not checked
                if curr_len >= next_len:  # is this correct? Should it be next_len >= curr_len? Does it matter?
                    print("curr_len > next_len and diff <= avgDotRadius, so add next_key to keys_to_remove")
                    keys_to_remove.append(next_key)
                    #del twiceConsolidated[next_key] #added
                    next_key = keys_list[keys_index + 1] # try this
                    keys_index += 1  # want to skip over next_key in keys_list
                else:
                    print("curr_len < next_len and diff <= avgDotRadius, so add curr_key to keys_to_remove")
                    keys_to_remove.append(curr_key)
                    keys_index += 1
                    curr_key = keys_list[keys_index]
                    next_key = keys_list[keys_index + 1]

                if keys_index + 1 == len(keys_list):
                    break
                #else:
                #    next_key = keys_list[keys_index + 1]
                    #exit(0)
                #if curr_key == 228:
                #    exit(0)
                #keys_index += 1 # LOOK HERE PLEASE
        #print(twiceConsolidated)
        #print(keys_to_remove)
        keys_index += 1


        """
        if curr_len >= prev_len:
            if abs(curr_key - prev_key) < avgDotRadius: # was avgDotRadius * 2 # was avgDotRadius
                keys_to_remove.append(prev_key)
                #print("deleting key " + str(prev_key))
                #del twiceConsolidated[prev_key]
        if curr_len >= next_len:
            if abs(curr_key - next_key) < avgDotRadius: # was avgDotRadius * 2 # was avgDotRadius
                #print("deleting key " + str(next_key))
                #del twiceConsolidated[next_key]
                keys_to_remove.append(next_key)
                keys_index += 1
        """


    # Remember to deal with the last one...
    print("keys_to_remove = " + str(keys_to_remove))
    #print("keys_to_keep = " + str(keys_to_keep))
    index = 0
    while index < len(keys_to_remove):
        key = keys_to_remove[index]
        print("key to remove= " + str(key))
        print("twiceConsolidated.keys() = " + str(twiceConsolidated.keys()))
        if key in twiceConsolidated.keys():
            del twiceConsolidated[key]
        index += 1

    #exit(0)
    # loop through one more time just in case
    index = 0
    keys_list = list(twiceConsolidated.keys())
    while index < len(keys_list) - 1:
        curr_key = keys_list[index]
        next_key = keys_list[index + 1]
        diff = abs(curr_key - next_key)
        if diff < avgDotRadius:
            #print("diff is less than avg dot radius! curr_key = " + str(curr_key) + ", next_key = " + str(next_key))
            #print("diff = " + str(diff) + ", avgDotRadius = " + str(avgDotRadius))
            #exit(0)
            curr_len = len(twiceConsolidated[curr_key])
            next_len = len(twiceConsolidated[next_key])
            if next_len >= curr_len:
                del twiceConsolidated[curr_key]
            else:
                del twiceConsolidated[next_key]
                index += 1

        index += 1

    # loop through again just in case (for each key, check for "too close" values, or too many values)
    # ADD HERE

    #for key in keys_to_remove:
    #    print("key = " + str(key))
    #    print("twiceConsolidated.keys() = " + str(twiceConsolidated.keys()))
    #    del twiceConsolidated[key]
    #for key in twiceConsolidated:
    #    values = twiceConsolidated[key]
    #    print(str(key) + " | " + str(values))

    # ADDED 9/23/2024: (deals with potential "too close" for last and second to last keys)
    keys_list = list(twiceConsolidated.keys())
    last = keys_list[-1]
    second_last = keys_list[-2]
    print("last = " + str(keys_list[-1]))
    print("second_last = " + str(keys_list[-2]))
    last_diff = abs(last - second_last)
    if last_diff < avgDotRadius:
        numValues_last = len(twiceConsolidated[last])
        numValues_second_last = len(twiceConsolidated[second_last])
        if numValues_last == numValues_second_last:
            del twiceConsolidated[last] # favor keeping lhs
            #twiceConsolidated.remove(second_last) # favor keeping rhs
        elif numValues_last > numValues_second_last:
            del twiceConsolidated[second_last]
            #twiceConsolidated.remove(second_last)
        else:
            del twiceConsolidated[last]
            #twiceConsolidated.remove(last)
    print("last_diff = " + str(last_diff))
    print("twiceConsolidated = " + str(twiceConsolidated))


    # go through looking for excess len
    keys_list = list(twiceConsolidated.keys())
    for key in keys_list:
        values = twiceConsolidated[key]
        if len(values) > 3:
            print("key " + str(key) +" has ERROR: > 3 values")
        values_list = list(values)
        index = 0
        while index < len(values) - 1:
            # compare curr and next value
            diff = abs(values_list[index] - values_list[index + 1])
            print("diff = " + str(diff) + ", radius = " + str(avgDotRadius))
            if diff < avgDotRadius:
                print("before-> " + str(values))
                values.remove(values_list[index])
                print("after--> " + str(values))
                twiceConsolidated[key] = values
                #values_list.remove(values_list[index])

            index += 1

    #exit(0)
    #exit(0)
    return twiceConsolidated

def markDots(thriceConsolidated, reassembled_img):
    pixels = reassembled_img.load()
    for key in thriceConsolidated.keys():
        values = thriceConsolidated[key]
        for value in values:
            pixels[key, value] = (255, 165, 0) # orange

    reassembled_img.show()
    return reassembled_img

# ALTERNATIVE: for every green dot, count forward as far as you can staying green and track the lengths
def calculateAvgDotDiameter(reassembled_img):
    print("--calculate average dot diameter--")
    pixels = reassembled_img.load()
    w, h = reassembled_img.size


    start = -1
    end = -1
    radii = []
    for i in range(reassembled_img.size[0]):  # for every pixel:        # w
        for j in range(reassembled_img.size[1]):  # h

            if j > 0:
                curr_pixel = pixels[i, j]
                prev_pixel = pixels[i, j-1]
                #print("prev_pixel (" + str(i) + ", " + str(j-1) + ")= " + str(prev_pixel))
                #print("curr_pixel (" + str(i) + ", " + str(j) + ")= " + str(curr_pixel))

                if prev_pixel[0] != 0 or prev_pixel[1] != 255 or prev_pixel[2] != 0: # pixel is not green
                    if curr_pixel[0] == 0 and curr_pixel[1] == 255 and curr_pixel[2] == 0: # pixel is green
                        print("found a green pixel! start of the diameter")
                        start = j
                        #exit(0)

                    else:
                        #print("still looking for the start of the diameter")
                        start = -1
                if prev_pixel[0] == 0 and prev_pixel[1] == 255 and prev_pixel[2] == 0: # prev pixel is green
                    if curr_pixel[0] == 0 and curr_pixel[1] == 255 and curr_pixel[2] == 0:  # curr pixel is green
                        #print("the diameter continues")

                        # special case: reached picture border
                        if j == h:
                            end = j
                            if start != -1 and end != -1:  # is this if-statement even needed?
                                radius = abs(end - start + 1)
                                radii.append(radius)
                            start = -1
                            end = -1

                    else: # curr pixel is not green
                        print("end of the diameter")
                        end = j
                        if start != -1 and end != -1: # is this if-statement even needed?
                            radius = abs(end - start + 1)
                            radii.append(radius)
                        start = -1
                        end = -1
        #exit(0)
    print("radii = " + str(radii))
    sum = 0
    for radius in radii:
        sum += radius
    avg_radius = sum / len(radii) # Note: approximation
    #avg_diameter = avg_radius * 2
    avg_diameter = int(avg_radius) * 2

    print("avg radius = " + str(avg_radius))
    print("avg diameter = " + str(avg_diameter))

    return avg_diameter


def round3_consolidate(combo_r2_post):

    # Setup
    combo_r3 = combo_r2_post.copy()
    key_index = 0
    start = 0
    keys_list = list(combo_r2_post.keys())
    r3_dict = dict()

    # Navigate through keys_list. Update twiceConsolidated.
    while key_index < len(keys_list) - 1:

        # Setup
        curr_key = keys_list[key_index]
        next_key = keys_list[key_index + 1]
        curr_values = combo_r3[curr_key]
        next_values = combo_r3[next_key]
        # print("start key = " + str(keys_list[start]) + ", curr_key = " + str(curr_key) + ", next_key = " + str(next_key))

        # Consecutive keys
        if curr_key + 1 == next_key:
            # print("curr_key = " + str(curr_key) + ", curr_values = " + str(curr_values) + ", next_values = " + str(next_values))

            # Curr and next have different number of values
            if len(curr_values) != len(next_values):
                width = abs(start - key_index)
                if start == key_index:
                    r3_dict[curr_key] = combo_r3[curr_key]
                    start = key_index + 1
                else:
                    keepIndex = abs(int(start + width / 2))  # (key_index-1) / 2))
                    keepKey = keys_list[keepIndex]
                    r3_dict[keepKey] = combo_r3[keepKey]
                    start = key_index + 1
        else:
            startKey = keys_list[start]
            endKey = keys_list[key_index] - 1
            if abs(startKey - endKey) == 1:
                r3_dict[startKey] = combo_r3[startKey]
            else:
                width = abs(start - key_index)
                keepIndex = abs(int((start + width / 2)))
                keepKey = keys_list[keepIndex]
                r3_dict[keepKey] = combo_r3[keepKey]
            start = key_index + 1#int((abs(start - key_index)/2)+1) #was +1
           # key_index += int((abs(start - key_index)/2)) #added
        key_index += 1

    # Catch ending section
    keepIndex = int(start + abs(start - key_index) / 2)
    keepKey = keys_list[keepIndex]
    #print("keepKey = " + str(keepKey))
    keyDiff = abs(keepKey - keys_list[keepIndex - 1])
    #print("keyDiff = " + str(keyDiff))
    #exit(0)
    r3_dict[keepKey] = combo_r3[keepKey]

    # keep for now
    # print("twiceConsolidated = " + str(twiceConsolidated))
    # exit(0)
    return r3_dict, combo_r3
# ^Start trying to consolidate further, focusing on consecutive keys with same-length, same-areas


def round2_consolidate(combo_r1_post, avgDotDiameter):
    """
    Round 2: For each key, remove "too close" values (diff<radius).

    Example: values in key 21 in 5to10cells png would go from [11.5, 24.5, 37.5, 44.0] --> [11.5, 24.5, 44.0].

    Note: When removing a value, favors keeping rhs.
    """
    floor_avgDotDiameter = int(avgDotDiameter)
    print("floor_avgDotDiameter = " + str(floor_avgDotDiameter))
    #exit(0)

    combo_r2 = combo_r1_post.copy()
    for key in combo_r2:
        values = combo_r2[key]
        values_index = 0
        while values_index < len(values) - 1:
            diff = abs(values[values_index] - values[values_index + 1])
            if diff < floor_avgDotDiameter/2: #added:/2(??) # REVISIT THIS
                values.remove(values[values_index])
                values_index -= 1
            values_index += 1
        combo_r2[key] = values
    return combo_r2

def consolidate_all(combo_w):
    """
        Round 1: For each key, remove "too close" values (consecutive)
        Round 2: For each key, remove "too close" values (diff<radius).
        Round 3: For dictionary, remove consecutive KEYS, keeping whichever has the most values. If tie, keep "avg" one.
        Round 4: For dictionary, remove non-consecutive but still "too close" KEYS, keeping whichever has the most
                values. If tie, keep "avg" one.
    """

    # Round 1
    combo_r1_post, avgDotDiameter = round1_consolidate(combo_w)
    print("combo_r1_post = " + str(combo_r1_post))

    # Round 2
    combo_r2_post = round2_consolidate(combo_r1_post, avgDotDiameter)
    print("combo_r2_post   = " + str(combo_r2_post))
    print("keys = " + str(combo_r2_post.keys()))
    #exit(0)

    # Round 3
    r3_dict, combo_r3_post = round3_consolidate(combo_r2_post) # In round4, watch out for last key possibly being "too close" to prev key
    print("combo_r3_post   = " + str(combo_r3_post))
    save_r3_post = combo_r3_post.copy()

    # Round 4
    ratio = min_distance_between_two_dots_in_the_same_cell / min_dot_base_diameter
    estimated_distance_between_two_dots_in_the_same_cell = ratio * avgDotDiameter
    print("avgDotRadius = " + str(avgDotDiameter / 2))
    print("estimated_distance_between_two_dots_in_the_same_cell = " + str(
        estimated_distance_between_two_dots_in_the_same_cell))
    print("estimated half distance between to same-cell dots: " + str(
        estimated_distance_between_two_dots_in_the_same_cell / 2))
    combo_r4_post = round4_consolidate(combo_r3_post,
                                          estimated_distance_between_two_dots_in_the_same_cell)  # was avgDotDiameter, was est without /2
    print("combo original  = " + str(combo_w))
    print("combo_r1_post   = " + str(combo_r1_post))
    print("combo_r2_post   = " + str(combo_r2_post))
    print("save_r3_post    = " + str(save_r3_post))
    print("combo_r3_post   = " + str(combo_r3_post))
    print("combo_r4_post = " + str(combo_r4_post))
    print(len(combo_r4_post.keys()))


    return combo_r4_post, avgDotDiameter
    #len = len(thriceConsolidated)
    #print("len = " + str(len))

    #FIX: (combo_original). combo_r1_post shows only 114 :(
    #372: [34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47,
    #
    #       101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111,
    #      112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127],
    # For each key, remove "too close" values.
    #
# Remember to calculate avg dot diameter while doing this
# If avg dot diameter calculation turns out to be not accurate (/not accurate enough), go back to doing the shadow-black calculation
def round1_consolidate(combo):
    print("combo = " + str(combo))

    combo_r1 = combo.copy()

    # For each combo_r1 key, empty its values. The keys still exist.
    for key in combo_r1:
        combo_r1[key] = []

    # For each combo_r1 key, update its values.
    for key in combo_r1:
        combo_r1 = track_consecutive_values(combo, combo_r1, key)
        #if key == 372:
        #    print("key is 372 done. combo_r1 is now: " + str(combo_r1))
    #exit(0)
    print("combo___ = " + str(combo))
    print("combo_r1 = " + str(combo_r1)) #here, 372 has 2 values (good)
    #exit(0)

    diffsAvg = calculate_avg_dot_diameter(combo_r1)
    print("round1_consolidate's diffsAvg = " + str(diffsAvg))

    # REMOVED: Start trying to consolidate further, focusing on consecutive keys with same-length, same-areas
    # TODO: review here
    #exit(0)
    return combo_r1, diffsAvg # was avgDotDiameter

def track_consecutive_values(combo, combo_r1, key):
    """temp: pass in combo also"""

    values = combo[key]
    consecutiveValuesSum = values[0]
    numConsecutiveValues = 1
    startIndex = 0
    currIndex = 1

    if key == 372:
        print("key is 372")
        print("values: " + str(values))
        #exit(0)

    while currIndex < len(values):
        #print("currIndex = " + str(currIndex))
        currVal = values[currIndex]
        prevVal = values[currIndex - 1]

        if prevVal + 1 == currVal:
            consecutiveValuesSum += currVal
            numConsecutiveValues += 1
        else:
            print("jump. currVal = " + str(currVal))

            avgVal = consecutiveValuesSum / numConsecutiveValues
            #print("avgVal = " + str(avgVal))
            combo_r1[key].append(avgVal)
            consecutiveValuesSum = currVal
            numConsecutiveValues = 1

        if currIndex + 1 == len(values):
            print("[end] jump. currVal = " + str(currVal))
            avgVal = consecutiveValuesSum / numConsecutiveValues
            #print("avgVal = " + str(avgVal))
            combo_r1[key].append(avgVal)
            #return combo_r1 #remove this?
            #print("combo_key values are: " + str(combo_r1[key])) #[40.5, 114.0]
            #consecutiveValuesSum = currVal
            #numConsecutiveValues = 1

        currIndex += 1

    if len(values) == 1:
        combo_r1[key].append(values[0])

    #if key == 372:
    #    exit(0)
    return combo_r1

#def calculate_avg_distance_between_adjacent_same_column_dots(combo_r1):
def calculate_avg_dot_diameter(combo_r1):

    diffsSum = 0
    diffsCount = 0

    for key in combo_r1:
        values = combo_r1[key]
        if len(values) > 1:
            diff1 = abs(values[0] - values[1])
            diffsSum += diff1
            diffsCount += 1
        if len(values) == 3:
            diff2 = abs(values[1] - values[2])
            diffsSum += diff2
            diffsCount += 1
    diffsAvg = diffsSum / diffsCount

    middle_standard_distance_between_two_dots_in_the_same_cell = (
            min_distance_between_two_dots_in_the_same_cell +
            max_distance_between_two_dots_in_the_same_cell) / 2
    middle_standard_dot_base_diameter = (min_dot_base_diameter + max_dot_base_diameter) / 2


    # REVISIT THIS:
    avgDotDiameter = (diffsAvg / middle_standard_distance_between_two_dots_in_the_same_cell) * middle_standard_dot_base_diameter #???
    print("diffsAvg = " + str(diffsAvg))
    print("avgDotDiameter = " + str(avgDotDiameter))
    #exit(0)
    # FIX THIS
    #adjustedAvgDotDiameter = calculate_avg_dot_diameter(diffsAvg)
    #print("adjustedAvgDotDiameter = " + str(adjustedAvgDotDiameter))
    #exit(0) # 5to10: avg 78.01666...

    return diffsAvg
    #return avgDotDiameter # TODO: which one?

'''
min_distance_between_two_dots_in_the_same_cell = 2.3
max_distance_between_two_dots_in_the_same_cell = 2.5

min_dot_base_diameter = 1.5
max_dot_base_diameter = 1.6

NOTE: calculating avg dot diameter with ratio ends up with exact same result as just 
getting calculate_avg_distance_between_adjacent_same_column_dots and using that
EX: 12.256578947368421
'''
"""def calculate_avg_dot_diameter(avgDistanceBetweenAdjacentSameColDots):
    middle_standard_distance_between_two_dots_in_the_same_cell = (
            min_distance_between_two_dots_in_the_same_cell +
            max_distance_between_two_dots_in_the_same_cell) / 2
    middle_standard_dot_base_diameter = (min_dot_base_diameter + max_dot_base_diameter) / 2
    avgDotDiameter = (avgDistanceBetweenAdjacentSameColDots / middle_standard_distance_between_two_dots_in_the_same_cell) * middle_standard_dot_base_diameter
    print("avgDotDiameter = " + str(avgDotDiameter))
    return avgDotDiameter"""


'''ALTERNATIVE OPTION for calculate avg dot diameter given combo_r1:
    for key in combo_r1:
        values = combo_r1[key]
        index = 1
        while index < len(values):
            diff = abs(values[index] - values[index-1])
            diffsSum += diff
            diffsCount += 1
            index += 1
'''
def readHorizontalLine(reassembled_img, curr_h):
    print("--read horizontal line: curr_h = " + str(curr_h))
    pixels2 = reassembled_img.load()  # create the pixel map
    w = reassembled_img.size[0]
    h = reassembled_img.size[1]

    dots = []
    green = []
    black = []
    for curr_w in range(w):
            # look for green pixels
            r,g,b,a = pixels2[curr_w,curr_h] # current pixel
            #print("(" + str(curr_h) + ", " + str(curr_w) + ") = " + str(pixels2[curr_w, curr_h]))
            if r == 0 and g == 255 and b == 0:
                print("found a green dot!")
            if r == 255 and g == 255 and b == 255:
                print("found a black dot!")
            # look for black pixels

    #green = []
    #black = []

# orange: big contrast between adjacent cells (a "catch-all")
def addOrangeOverlay(img2, pixels2):
    for i in range(img2.size[0]):  # for every pixel:        # w
        for j in range(img2.size[1]):  # h
            curr_pixel = pixels2[i, j]
            curr_pixel_sum = curr_pixel[0] + curr_pixel[1] + curr_pixel[2]

            # turn a pixel orange if adjacent cell (one rightward or one downward) has sum diff > 100
            if (i + 1) in range(img2.size[0]):
                next_pixel = pixels2[i + 1, j]
                next_pixel_sum = next_pixel[0] + next_pixel[1] + next_pixel[2]
                if abs(curr_pixel_sum - next_pixel_sum) > 100:
                    pixels2[i, j] = (255, 165, 0)  # orange
            if (j + 1) in range(img2.size[1]):
                next_pixel = pixels2[i, j + 1]
                next_pixel_sum = next_pixel[0] + next_pixel[1] + next_pixel[2]
                if abs(curr_pixel_sum - next_pixel_sum) > 100:
                    pixels2[i, j] = (255, 165, 0)  # orange
    return img2
# Note: could also look for pixel sum difference (adj or diagonal)
# black: shadows
# green: bright white
# orange: big contrast between adjacent cells (a "catch-all")
# what if search orange, then green, then black (rather than current green, black, orange)

def findWhite(filename, img2, pixels2, avg):
    white = [] # coordinates of pixels that are white (or very close to it)
    sum = 0

    for i in range(img2.size[0]):  # for every pixel:        # w
        for j in range(img2.size[1]):  # h
            curr_pixel = pixels2[i, j]
            curr_pixel_sum = curr_pixel[0] + curr_pixel[1] + curr_pixel[2]

            # turn a pixel orange if adjacent cell (one rightward or one downward) has sum diff > 100
            """
            if (i+1) in range(img2.size[0]):
                next_pixel = pixels2[i+1, j]
                next_pixel_sum = next_pixel[0] + next_pixel[1] + next_pixel[2]
                if abs(curr_pixel_sum - next_pixel_sum) > 100:
                    pixels2[i,j] = (255, 165, 0) # orange
            if (j+1) in range(img2.size[1]):
                next_pixel = pixels2[i, j+1]
                next_pixel_sum = next_pixel[0] + next_pixel[1] + next_pixel[2]
                if abs(curr_pixel_sum - next_pixel_sum) > 100:
                    pixels2[i,j] = (255, 165, 0) # orange
            """
            if curr_pixel_sum > 675:  # change this to a percentage, maybe? #was 650
                # print("(" + str(i) + ", " + str(j) + ") --> greater than average! (" + str(curr_pixel_sum) + ")")
                pixels2[i, j] = (0, 255, 0)  # green
                white.append([i, j])
            if curr_pixel_sum < avg / 1.5:
                pixels2[i,j] = (0, 0, 0) # black # good for catching ones that get missed by the 650



            sum += curr_pixel_sum
    avg = sum / (img2.size[0] * img2.size[1])
    print("avg = " + str(avg))
    return img2


def reassembleThePicture(original_image, filename, dir_out, d, grid):

    # Create new image
    print("\n\noriginal_image.mode = " + str(original_image.mode))
    desired_ext = ".png"
    print("reassemble the picture!")
    name, ext = os.path.splitext(filename)
    w, h = original_image.size
    new_image = Image.new("RGBA", (w, h), ) # THIS WORKS FOR basic embossed (rgb) #RGB or RGBA?
    print("new_image.mode = " + str(new_image.mode)) #RGB

    # Note: not JPG. Instead, PNG. JPG result is pixelated/fuzzy.
    new_image.save(dir_out + "/" + filename + "_reassembled" + desired_ext)
    print("h - h % d = " + str(h - h % d))
    print("w - w % d = " + str(w - w % d))

    #exit(0)


    grid = product(range(0, h - h % d, d), range(0, w - w % d, d))
    #grid = product(range(0, tile_lowest_start, d), range(0, tile_rightmost_start, d))
    #for i, j in grid:
    #    print(i, j)
    for i, j in grid:
        print("i = " + str(i) + ", j = " + str(j))
        box = (j, i, j + d, i + d)
        curr_filename = str(name) + "_" + str(i) + "_" + str(j) + desired_ext #".jpg? .png?"
        print("curr_filename = " + str(curr_filename))
        curr_img = Image.open(str(dir_out) + "/" + curr_filename)
        print("curr_img.mode = " + str(curr_img.mode))

        #curr_img.show() # oops

        curr_img.save(dir_out + "/" + curr_filename)
        new_image.paste(curr_img, box) #i, j? j, i?


    # take care of "leftovers"
    print("h % d = " + str(h % d))
    print("w % d = " + str(w % d))
    tile_rightmost_start = w - (w % d)
    tile_lowest_start = h - (h % d)
    print("tile_rightmost_start = " + str(tile_rightmost_start))
    if h % d != 0:
        print("HERE, w = " + str(w) + ", h = " + str(h))
        curr_w = 0
        while curr_w < tile_rightmost_start: # prev: curr_w < w
            #print("tile_lowest_start = " + str(tile_lowest_start))
            print("curr_w = " + str(curr_w) + ", w = " + str(w))
            box = (curr_w, tile_lowest_start, curr_w + d, h)
            curr_filename = str(name) + "_" + str(tile_lowest_start) + "_" + str(curr_w) + desired_ext#".jpg", .png?
            curr_img = Image.open(str(dir_out) + "/" + curr_filename)
            curr_img.save(dir_out + "/" + curr_filename)

            #curr_img.show()
            #print("curr_img.mode = " + str(curr_img.mode))  # RGB?
            #print("new_img.mode  = " + str(new_image.mode))
            #exit(0)
            # LOOK;
            # check mode
            # check dimensions?

            new_image.paste(curr_img, box) # ValueError: images do not match # no error this time
            #exit(0)
            curr_w += d
    #exit(0)
    if w % d != 0:
        print("HERE")
        curr_h = 0
        while curr_h < h:
            print("tile_rightmost_start = " + str(tile_rightmost_start))
            print("curr_h = " + str(curr_h))
            box = (tile_rightmost_start, curr_h, w, curr_h + d)
            curr_filename = str(name) + "_" + str(curr_h) + "_" + str(tile_rightmost_start) + desired_ext
            curr_img = Image.open(str(dir_out) + "/" + curr_filename)
            curr_img.save(dir_out + "/" + curr_filename)

            #curr_img.show()
            new_image.paste(curr_img, box)
            curr_h += d
    print("new_image.mode = " + str(new_image.mode))
    new_image.save(dir_out + "/" + filename + "_reassembled" + desired_ext) # png or jpg?
    #new_image.show()
    # example: Embossed_Braille_114_38.jpg

    #assembled_img = new_image
    return new_image
def findAvgRGB(filename, img2, pixels2):
    sum = 0
    low = 255 * 3
    high = 0
    for i in range(img2.size[0]):  # for every pixel:        # w
        for j in range(img2.size[1]):  # h
            curr_pixel = pixels2[i, j]
            curr_pixel_sum = curr_pixel[0] + curr_pixel[1] + curr_pixel[2]
            sum += curr_pixel_sum
            if curr_pixel_sum > high:
                high = curr_pixel_sum
            if curr_pixel_sum < low:
                low = curr_pixel_sum
    avg = sum / (img2.size[0] * img2.size[1])
    print("avg = " + str(avg))
    print("low = " + str(low))
    print("high= " + str(high))
    img2 = findWhite(filename, img2, pixels2, avg)
    #img2.show() #pixeltion seems okay here
    return avg, img2
def tile(filename, dir_in, dir_out, d):
    #print("---tile FUNCTION---")
    name, ext = os.path.splitext(filename)
    #print("---1 REACHED---")
    img = Image.open(os.path.join(dir_in, filename))
    # Is the absolute path not being passed in?
    #print("---2 REACHED---")
    w, h = img.size
    #print("---3 REACHED---")

    print("image size = " + str(img.size))
    print("w = " + str(w))
    print("h = " + str(h))
    pixel_values = list(img.getdata())
    pixel_sums = []
    for pixel in pixel_values:
        pixel_sums.append(pixel[0] + pixel[1] + pixel[2])

    picture_sum = 0
    for pixel_sum in pixel_sums:
        picture_sum += pixel_sum
    print("picture_sum = " + str(picture_sum))
    avg = picture_sum / len(pixel_values)
    print("avg = " + str(avg))

    img2 = img.copy()

    pixels2 = img2.load()  # create the pixel map
    avgRGB_clean, img2 = findAvgRGB(filename, img2, pixels2)
    print("avgRGB_clean = " + str(avgRGB_clean))
    ###avgJump = findAvgJump(peaks)
    ###peaks = removeMiniJumps(peaks, avgJump) # re-add later
    print("avg_dot_base_diameter = " + str(avg_dot_base_diameter))
    #img2.show() #pixelation seems okay by here
    return img2
def searchBlack(black, dictionary):
    print("searchBlack")

    print("len of black: " + str(len(black)))
    print("len of dict:  " + str(len(dictionary.values())))

    sum = 0
    for key in dictionary.keys():
        sum += len(dictionary[key])

    print("num keys = " + str(len(dictionary.keys())))
    print("sum = " + str(sum))

    for key in dictionary.keys():
        values = dictionary[key]
        for value in values:
            if [key, value] in black:
                black.remove([key, value])
                #print("REMOVING!")
                #exit(0)

    print("updated black len: " + str(len(black))) # why are there 733 remaining??
    print(dictionary)

def identifyRow(peaks, avgDotDiameter, img2, w, h, pixels2):
    print()
    border_top_middle = h / 3
    border_middle_bottom = 2 * h / 3
    border_middleground1 = (border_top_middle + border_middle_bottom) / 2
    border_middleground2 = (border_middle_bottom + h) / 2
    print("border_top_middle    = " + str(border_top_middle))
    print("border_middle_bottom = " + str(border_middle_bottom))
    print("border_middleground1    = " + str(border_middleground1))
    print("border_middleground2    = " + str(border_middleground2))



    borders = [border_top_middle, border_middle_bottom]
    middlegrounds = [border_middleground1, border_middleground2]
    for i in range(img2.size[0]):
        for border in borders:
            pixels2[i, border] = (255, 255, 0) # yellow
        for middleground in middlegrounds:
            pixels2[i, middleground] = (255, 128, 0) # orange

    # if 1 peak has > 3 entries, that's a problem...(fix later)
    for peak in peaks:
        for height in peak[1]:
            dot = [peak[0], height]
            print("peak = " + str(peak))
            if dot[1] < int(middlegrounds[0]):
                print("1 or 4")
            elif dot[1] < int(middlegrounds[1]):
                print("2 or 5")
            else:
                print("3 or 6")

    #img2.show()


# Now, if adjacent keys are closer than avgJump, get rid of one of them (does it matter which one…?)
def removeMiniJumps(peaks, avgJump):
    index = 0
    #count_duplicates = 0
    #count_nonduplicates = 0
    while index < len(peaks):
        print(peaks[index])
        if index > 0:
            curr_peak = peaks[index]
            prev_peak = peaks[index - 1]
            print("curr_peak = " + str(curr_peak))
            curr_key = curr_peak[0]
            prev_key = prev_peak[0]
            if abs(curr_key - prev_key) < (avgJump)/2: # fix this # is abs even needed?
                print("We found a duplicate!")
                peaks.remove(peaks[index])
                #exit(0)
                #index -= 1 # in case of multiple consecutive duplicates
                #count_duplicates += 1
            #else:
                #count_nonduplicates += 1
        index += 1
    print("peaks being returned: " + str(peaks))
    #print("count_duplicates    = " + str(count_duplicates))
    #print("count_nonduplicates = " + str(count_nonduplicates))
    #exit(0)
    return peaks

def findAdjacentDuplicates(peaks, img2, pixels2):
    index = 0
    while index < len(peaks) - 1:
        print(peaks[index])
        curr_peak = peaks[index]
        next_peak = peaks[index + 1]

        curr_key = curr_peak[0]
        next_key = curr_key[0]

        curr_values = curr_peak[1]
        next_values = next_peak[1]

        # for each overlap value, remove the lower one
        for next_value in next_values:
            if next_value in curr_values: # overlap!
                curr_values.remove(next_value)
                pixels2[curr_key, next_value] = (255, 255, 255) # white
                print("OVERLAP!")

        curr_peak = [curr_key, curr_values]
        peaks[index] = curr_peak

def findAvgDotDiameter(peaks):
    index = 0
    sum = 0 # per dot
    avg = 0
    numDots = 0
    diameters = [] #[index, diameter]

    while index < len(peaks):
        print("peaks[index] = " + str(peaks[index]))
        print("index = " + str(index))
        curr_peak = peaks[index]
        key = curr_peak[0]
        values = curr_peak[1]
        valueIndex = 0
        start = values[0]
        no_jump_sum = 0
        no_jump_count = 0
        no_jump_avg = 0
        no_jump_avgValues = []
        while valueIndex < len(values):
            curr_value = values[valueIndex]
            print("===> " + str(curr_value) + "( no_jump_sum = " + str(no_jump_sum) + ")")
            no_jump_sum += curr_value
            no_jump_count += 1

            if valueIndex > 0 and valueIndex + 1 < len(values) and curr_value != (values[valueIndex - 1] + 1):
                end = curr_value
                diameter = end - start
                print("diameter = " + str(diameter))
                diameters.append([valueIndex, diameter])
                sum += diameter
                no_jump_sum -= curr_value
                no_jump_count -= 1
                print("no_jump_sum = " + str(no_jump_sum))
                print("no_jump_count = " + str(no_jump_count))

                no_jump_avg = int(no_jump_sum / no_jump_count)
                print("no_jump_avg = " + str(no_jump_avg))
                no_jump_avgValues.append(no_jump_avg)

                print("We found a jump!")
                numDots += 1
                start = values[valueIndex + 1]
                no_jump_sum = curr_value
                no_jump_count = 1

                #sumJump += curr_value - values[valueIndex - 1]
            if valueIndex + 1 == len(values): # No next dot, so no jump, but still a dot
                end = curr_value
                diameter = end - start
                print("-diameter = " + str(diameter))
                sum += diameter
                numDots += 1
                print("-no_jump_sum = " + str(no_jump_sum))
                print("-no_jump_count = " + str(no_jump_count))

                no_jump_avg = int(no_jump_sum / no_jump_count)
                print("-no_jump_avg = " + str(no_jump_avg))
                no_jump_avgValues.append(no_jump_avg)
                no_jump_sum = 0
            valueIndex += 1

        print(peaks[index])
        #key_ = curr_peak[0]
        value_ = no_jump_avgValues
        peaks[index] = [key, value_]  # EX: maximum of 3 dots
        #print("(updated) peaks[" + str(index) + "] = " + str(peaks[index]))
        # peaks[index] =  #fix here
        index += 1

    print("sum of diameters = " + str(sum))
    print("num dots = " + str(numDots))
    avg = sum / numDots
    print("avg diameter = " + str(avg))
    print("peaks:")
    print(peaks)
    return avg, peaks
def findAvgJump(peaks):

    index = 0
    sumJump = 0
    numJumps = 0
    while index < len(peaks):
        print(peaks[index])
        curr_peak = peaks[index]
        key = curr_peak[0]
        values = curr_peak[1]
        valueIndex = 0
        while valueIndex < len(values):
            curr_value = values[valueIndex]
            print("===> " + str(curr_value))
            if valueIndex > 0 and curr_value != (values[valueIndex - 1] + 1):
                print("We found a jump!")
                numJumps += 1
                sumJump += curr_value - values[valueIndex - 1]
            valueIndex += 1

        index += 1
    print("numJumps = " + str(numJumps))
    print("sumJump  = " + str(sumJump))
    avgJump = sumJump / numJumps
    print("avgJump = " + str(avgJump))
    return avgJump

# Identify peak of bell curve.
def findPeak(dictionary):
    print("dictionary = " + str(dictionary)) # 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47
    numKeys = len(dictionary.keys())
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    index = 0
    peaksFound = 0
    peaks = []
    while index < len(keys):
        curr_key = keys[index]
        print("curr_key = " + str(curr_key))
        curr_values = values[index]
        print("curr_values = " + str(curr_values))
        key_values = dictionary.get(curr_key)
        print("key_values  = " + str(key_values))
        #print("index = " + str(index) + ". Curr key =  " + str(curr_key))
        if index > 0 and index < (numKeys - 1): # is it okay to put both bounds here? # current key is not the first or the last key
            # compare number of values: key vs (key -1)
            if len(curr_values) > len(values[index-1]) and len(curr_values) >= len(values[index+1]):
                # current is peak or "low peak"
                print("PEAK! found at key = " + str(curr_key))
                peaksFound += 1
                peaks.append([curr_key, curr_values])                       #### FIND


                # get the surrounding ones just in case
                # upper
                surroundings_index = index
                while surroundings_index < (numKeys - 1) and surroundings_index < (index + 5):
                    peaks.append([keys[surroundings_index], values[surroundings_index]])
                    surroundings_index += 1
                    print("surroundings! key " + str(surroundings_index) + " found from key = " + str(curr_key))
                # lower
                surroundings_index = index
                while surroundings_index > 0 and surroundings_index > (index - 5):
                    peaks.append([keys[surroundings_index], values[surroundings_index]])
                    surroundings_index -= 1
                    print("surroundings! key " + str(surroundings_index) + " found from key = " + str(curr_key))
        index += 1
    print("peaksFound = " + str(peaksFound))
    return peaks

# Defining main function
# TODO: accept file path, use that file
def getCoords(img, photo_path):
    #uploads/downloaded_example_photo.png
    abs_path = os.path.abspath(photo_path)
    abs_path_pieces = abs_path.split("/")
    
    filename = abs_path_pieces[-1]
    #dir_in = abs_path.replace(filename,'')
    
    print("photoPath = " + str(photo_path))
    print("abs_path   = " + str(abs_path))
    dir_in = '/'.join(abs_path_pieces[0:(len(abs_path_pieces)-1)])
    dir_out = str(dir_in + "/tiles")
    
    print("\nfilename = " + filename)       # OK
    print("\ndir_in   = " + str(dir_in))    # OK
    print("\ndir_out  = " + dir_out)        # OK

    #exit(0)

     # Calculate d
    original_file = saveOriginalFile(filename, dir_in)
    d = int(original_file.width / 4)
    print(d)

    # Convert
    combo_consolidated = tile2(filename, dir_in, dir_out, d) # 38

    return combo_consolidated # expect: returns coords
    
    #return "returning from getCoords..."


def main():
    print("main")

    # Set dir_in, dir_out
    dir_in = "/Users/jenniferstibbins/PycharmProjects/example/testHoughCircles"
    dir_out = "/Users/jenniferstibbins/PycharmProjects/example/testHoughCircles/Tiles"

    # List out filenames for testing
    test_filenames = ["Embossed_Braille.png",
                      "Embossed_Braille_subsection_2cells.png",
                      "Embossed_Braille_subsection_5to10cells.png",
                      "Embossed_Braille_7rows_dark.png",
                      "Embossed_Braille_FullPage.png",
                      "Embossed_CustomTestcases_title_straightened.png",
                      "Embossed_Braille_FullPage_www_line_straightened.png"]

    # Set filename
    #filename = "Embossed_Braille.png"                      # OK
    #filename = "Embossed_Braille_subsection_2cells.png"    # OK     <-- fails as of 9/23
    filename = "Embossed_Braille_subsection_5to10cells.png" # OK <-- watch out for key 21, 4 vals
    #filename = "Embossed_Braille_7rows_dark.png"           # OK
    #filename = "Embossed_Braille_FullPage.png"             # OK but border not clear. 987 x 956. EDIT: with green 675, misses some dots (and false positives from doublesided-ness)
    #filename =  "Embossed_CustomTestcases_title_straightened.png"
    #filename = "Embossed_Braille_FullPage_www_line_straightened.png"
    ###filename = "Embossed_CustomTestcases_title_straightened.png" #"Testcases", 1 line

    # Calculate d
    original_file = saveOriginalFile(filename, dir_in)
    d = int(original_file.width / 4)
    print(d)

    # Convert
    tile2(filename, dir_in, dir_out, d) # 38

    # 2cells: combo_r4_post = {58: [40.5, 187.5], 285: [40.5, 194.0], 379: [40.5, 107.0]}
    # 5to10cells:  {21: [11.5, 24.5, 37.5, 44.0], 33: [24.5], 62: [10.5, 17.0], 73: [24.5], 120: [12.5, 25.0], 161: [11.5], 181: [21.0, 28.0], 225: [11.0, 22.5, 36.5], 266: [21.0], 286: [6.5, 12.5], 306: [8.5, 21.0], 321: [7.5, 20.5], 348: [7.0, 20.0], 367: [17.5, 24.0]}
    #   - Note: key 21 currently has 4 values instead of 3. Values at indices 2 and 3 are too close


def swap(thriceConsolidated, avgDotDiameter):
    #keys = thriceConsolidated.keys()
    print("original = " + str(thriceConsolidated.items()))
    swapped = dict()
    for key, values in thriceConsolidated.items():
        for value in values:
            if value not in swapped.keys():
                swapped.setdefault(value, [])
            swapped[value].append(key)
    sorted_swapped = dict(sorted(swapped.items()))#sort(swapped)#swapped.sort()
    print("sorted_swapped = " + str(sorted_swapped))
    print("avg dot diameter = " + str(avgDotDiameter))
    return sorted_swapped
    #exit(0)
    #for key in sorted_swapped.keys():
    #    print(str(key))

# has some extra "jumps"...
def drawLinesHorizontal2(reassembled_img, sorted_swapped, distance):
    print("HERE")
    keys_list = list(sorted_swapped.keys()) # height values, NOT width values
    if len(keys_list) < 2:
        return

    w, h = reassembled_img.size
    pixels = reassembled_img.load()

    curr_index = 1
    num_diffs = 1
    sum_diffs = abs(keys_list[curr_index] - keys_list[curr_index - 1])

    while curr_index < len(keys_list) -1:
        diffCurrPrev = abs(keys_list[curr_index] - keys_list[curr_index - 1])
        diffCurrNext = abs(keys_list[curr_index] - keys_list[curr_index + 1])
        curr = keys_list[curr_index]
        next = keys_list[curr_index +1]
        if abs(curr - next) >= distance * 0.5:#9: # change the 9 so that it scales to work for each picture
            print("\ndiffCurrNext = " + str(diffCurrNext))
            print("diffCurrPrev = " + str(diffCurrPrev))
            print("next value = " + str(keys_list[curr_index+1]) + " --> That's a jump!")

            drawHeight = int((keys_list[curr_index] + keys_list[curr_index + 1]) / 2)
            index_w = 0
            while index_w < w:
                pixels[index_w, drawHeight] = (0, 0, 0)
                index_w += 1
        curr_index += 1
    reassembled_img.show()
def drawLinesHorizontal(reassembled_img, thriceConsolidated, estimated_distance_between_corresponding_dots_in_one_cell_directly_below):
    keys = list(thriceConsolidated.keys())

    # Find dot closest to top of picture
    w, h = reassembled_img.size
    min = h
    for key in thriceConsolidated.keys():
        values = thriceConsolidated[key]
        for value in values:
            if value < min:
                print("key = " + str(key) + ", value = " + str(value))
                min = value
    print("min = " + str(min))


    # Start with highest dot
    pixels = reassembled_img.load()
    index_w = 0
    while index_w < w:
        pixels[index_w, min] = (255, 165, 0)
        index_w += 1


    index_h = min + estimated_distance_between_corresponding_dots_in_one_cell_directly_below/2 # why /2?
    while index_h < h:
        index_w = 0
        while index_w < w:
            pixels[index_w, index_h] = (255, 165, 0)
            index_w += 1
        index_h += estimated_distance_between_corresponding_dots_in_one_cell_directly_below/2
        index_w += 1
    #new_h = min + estimated_distance_between_corresponding_dots_in_one_cell_directly_below/2



    #startKey = keys[0] # width
    #values = thriceConsolidated[startKey]
    #startValue = values[0]
    #startCoord = startKey,startValue
    #print("startCoord = " + str(startCoord))
    """
    print("startKey = " + str(startKey))
    pixels = reassembled_img.load()
    w, h = reassembled_img.size
    print(w,h)
    curr_h = 0

    for key in keys:
        print("key = " + str(key))
        curr_h = 0
        while curr_h < h:
            pixels[key, curr_h] = (0, 0, 0)
            curr_h += 1
    # repetitive...
    for key in keys:
        values = thriceConsolidated[key]
        for value in values:
            curr_w = 0
            while curr_w < w:
                pixels[curr_w, value] = (255, 255, 255)
                curr_w += 1
    """

    reassembled_img.show()
# find uppermost dot and do 10mm * ratio down and draw a line across the picture in blue for each
def drawLines(reassembled_img, thriceConsolidated, estimated_distance_between_corresponding_dots_in_one_cell_directly_below):
    keys = list(thriceConsolidated.keys())
    startKey = keys[0] # width
    print("startKey = " + str(startKey))
    pixels = reassembled_img.load()
    w, h = reassembled_img.size
    print(w,h)
    curr_h = 0

    for key in keys:
        print("key = " + str(key))
        curr_h = 0
        while curr_h < h:
            pixels[key, curr_h] = (255, 255, 255)
            curr_h += 1
    # repetitive...
    """for key in keys:
        values = thriceConsolidated[key]
        for value in values:
            curr_w = 0
            while curr_w < w:
                pixels[curr_w, value] = (255, 255, 255)
                curr_w += 1
    """

    reassembled_img.show()

# Using the special variable
# __name__
if __name__ == "__main__":
    main()
