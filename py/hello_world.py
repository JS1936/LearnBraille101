# hello_world.py

# def main():
#     print("Hello, World!")

# if __name__ == "__main__":
#     main()


import sys
from PIL import Image
from cellsToText_practice import cellsToText

import json



# def process_cells(cells):
#     """
#     Processes the list of cells.
    
#     Args:
#         cells (list): A list of cell values.
#     """
#     print("Processing Cells:")
#     for cell in cells:
#         print(cell)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python hello_world.py <cells_json>")
        sys.exit(1)


    #print("Welcome to hello_world.py")
    # Get the JSON string from the command line argument
    cells_json = sys.argv[1]
    
    # Convert the JSON string back to a list
    cells = json.loads(cells_json)

    # Process the cells
    #process_cells(cells)

    #######

    output_text = cellsToText(cells)
    print("output_text = " + str(output_text))

    # Call cellsToText
    #cellsToText(cells)
