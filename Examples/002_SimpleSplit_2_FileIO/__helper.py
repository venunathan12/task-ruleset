import os, sys, time
import pathlib


# Some constants
svgFormat = svgFormat = """<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n<svg width="600" height="600" xmlns="http://www.w3.org/2000/svg">\n<rect width="600" height="600" stroke="black" stroke-width="2" fill="white" />\n[$DATA]\n</svg>"""
svgPointFormat = """<circle cx="[$X]" cy="[$Y]" r="3" stroke="black" stroke-width="0" fill="red" />"""


# Function to create output directory
def prepareOutputFolder():

    # Get current working directory
    root = pathlib.Path.cwd()
    print(f"Currently running from:\n{root}\n")
    
    # Get current timestamp for naming output folder
    timestamp = str(time.time())
    outFolderPath = os.path.join(root, f"Output {timestamp}")
    print(f"Output will be saved in:\n{outFolderPath}\n")
    
    # Create output folder
    os.mkdir(outFolderPath)

    # return path of newly created folder
    return outFolderPath


# Function to get list of input files
def getListOfFilesToProcess():
    
    # Get input directory
    inputFolderPath = os.path.join(pathlib.Path.cwd(), 'Input')
    print(f"Reading input files from:\n{inputFolderPath}\n")

    # Get list of input files
    inputFilesList = [item for item in os.listdir(inputFolderPath)]
    print(f"{len(inputFilesList)} files will be processed.")
    for item in inputFilesList:
        print(item)
    print()

    # return list of input files
    return inputFilesList


# Function to process file
def processFile(fileName):
    
    # Get path to input file
    filePath = os.path.join(pathlib.Path.cwd(), 'Input', fileName)

    # Read data from input file
    fileData = None
    with open(filePath, 'r') as F:
        fileData = F.read()
    
    # Prepare results
    points = []

    # If file was read successfully
    if fileData is not None:

        # For every line in the file
        for line in fileData.split('\n'):
            if line != '' and ',' in line:

                # Plot one point based on the line
                x, y = map(lambda c: str(int(float(c) * 300 + 300)), line.split(','))
                points.append(svgPointFormat.replace('[$X]', x).replace('[$Y]', y))

    # Collect all points
    result = svgFormat.replace('[$DATA]', '\n'.join(points))

    # return processed data for this file
    return result


# Function to save data to output file
def saveOutputFile(outputPath, fileName, data):
    
    # Get output file path
    filePath = os.path.join(outputPath, fileName + '.svg')

    # Write data to output file
    with open(filePath, 'w') as F:
        F.write(data)
