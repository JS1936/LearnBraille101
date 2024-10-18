from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import time
from bs4 import BeautifulSoup
import requests


# EX is from 5to10cells png
#note: index 2 cell WAS 0, changed to [], same for index cell 5
cells = [[1, 2, 3, 5], [1, 5], [], [1, 2], [1, 5], [], [1, 2, 3], [2, 4], [1, 2, 4, 5], [1, 2, 5]]



def cellsToEnglishText_using_abcbraille():
    print("Hi")

    output_text = ""
    # Set up the WebDriver (this example uses Chrome)
    driver = webdriver.Chrome()
    try:
        driver.get("https://abcbraille.com/braille")  # Open the website
        time.sleep(2) # Let the page load
        print("OK_1")

        # Send each cell into textbox to get translated
        for cell in cells:
            #print("CELL = " + str(cell))
            for dot in cell:
                #print("--dot = " + str(dot))
                # Access + click/select the label element
                label = driver.find_element(By.CSS_SELECTOR, 'label.cell-dot[for="dot1' + str(dot) + '"]')
                label.click()
            #print("clicked all dots for single cell. Now add the cell...")
            button_add = driver.find_element(By.ID, "btn_add")
            button_add.click()


        # Find and click the "Translate Braille" button
        chunk = driver.find_element(By.ID, "inputtextform")
        #print("chunk = " + str(chunk))
        button_translate_braille = chunk.find_element(By.CSS_SELECTOR, ".btn.btn-primary.btn-block")
        button_translate_braille.click()

        # Store results. The id of result/output textbox is "translate_output"
        textbox = driver.find_element(By.ID, "translate_output")
        output_text = textbox.text
        print("TEXT = " + str(textbox.text))

        print("OK_2")
        time.sleep(10)

    except:
        print("FAILED")
        exit(1)

    #EXAMPLE:
    # Create HTML file to store and display output_text to the user
    # NOTE: This would only write to the local file... how would this work remotely...?
    output_file = open("HTML_write_example.html", "w")
    output_file.size = 0

    # Write output_text to HTML file
    output_file.write(
        "<!DOCTYPE html>"
        "\n<html>"
        "\n     <head>"
        "\n         <title>Conversion Output</title>"
        "\n     </head> "
        "\n     <body>"
        "\n         <h1>Conversion Output</h1> "
        "\n         <h2>Results: " + str(output_text) + "</h2> "
        "\n     </body>"
        "\n</html>")

    # Saving the data into the HTML file
    output_file.close()
