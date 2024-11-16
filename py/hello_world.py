import sys
from PIL import Image
from cellsToText_practice import cellsToText
from coordsToCells_practice import testcase_one
from photoToCoords_practice import getCoords

from coordsToCells_practice import testcase_none
from coordsToCells_practice import testcase_zero
import json

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python hello_world.py <image's local_file_path>")
        sys.exit(1)


    # Get image
    local_file_path = sys.argv[1]
    print("\nlocal_file_path = " + local_file_path + "\n")
    img = Image.open(local_file_path)
    img.show()


    # Get coords
    coords = getCoords(img, local_file_path)
    print("coords DONE: " + str(coords))


    # Get cells
    cells = testcase_zero(coords)
    print("(testcase_zero) cells --> " + str(cells))


    # Get text
    output_text = cellsToText(cells)
    print("output_text = " + str(output_text))


# Removed:
#path_pieces = local_file_path.split("/")
#print("\npath_pieces = " + str(path_pieces))


# Note: could write the "receipts" to a file 
# and display that to the user as way of showing work
# EX: similar to ==> output_file = open("HTML_write_example.html", "w")