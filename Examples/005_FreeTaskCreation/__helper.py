import os, sys, time
import pathlib


# The list which stores all values of x
# This list gets modified as the simulation progresses
Xs = []

# Some constants
svgFormat = svgFormat = """<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n<svg width="400" height="400" xmlns="http://www.w3.org/2000/svg">\n<rect width="400" height="400" stroke="black" stroke-width="2" fill="white" />\n[$DATA]\n</svg>"""
svgPointFormat = """<circle cx="[$X]" cy="[$Y]" r="3" stroke="black" stroke-width="0" fill="red" />"""
summaryHtmlFormat = """<html>\n    <head>\n        <title>Simulation Summary</title>\n        <script>\n            \n            let currentSliderValue = null;\n\n            function onLoad()\n            {\n                document.getElementById("slider").value = 0;\n                onSliderChange(); updateImage();\n            }\n            function onSliderChange()\n            {\n                currentSliderValue = document.getElementById("slider").value;\n                document.getElementById("iterNum").textContent = currentSliderValue;\n                updateImage();\n            }\n\n            function updateImage()\n            {\n                document.getElementById("plot").setAttribute("src", `Iteration ${currentSliderValue}.svg`);\n            }\n\n        </script>\n    </head>\n    <body onload="onLoad()">\n        <center>\n            <h1>Simulation Summary</h1>\n            <hr>\n            <img id="plot" />\n            <hr>\n            Iteration: <span id="iterNum"></span><br>\n            <input id="slider" type="range" oninput="onSliderChange()" step="[$STEP]" max="[$MAX]"/> \n        </center>\n    </body>\n</html>\n"""


# The function which updated the values of x
def iterate():

    global Xs
    
    # Create copy of the list for new values
    NXs = Xs.copy()
    LenXs = len(Xs)

    for i in range(LenXs):

        idx1 = (LenXs + i) % LenXs
        idx2 = (LenXs + i + 1) % LenXs
        idx3 = (LenXs + i + 3) % LenXs
        idx4 = (LenXs + i - 2) % LenXs

        # Compute the new values of x
        NXs[i] = Xs[idx1] + Xs[idx2] - Xs[idx3] - Xs[idx4]
    
    # Normalize the new values of x
    MaxX, MinX = max(NXs), min(NXs)
    for i in range(LenXs):
        NXs[i] = (NXs[i] - MinX) / (MaxX - MinX)

    # Update the values of x
    Xs = NXs

    return


# Function to create directory
def prepareFolder(name):

    # Get current working directory
    root = pathlib.Path.cwd()
    
    # Get current timestamp for naming folder
    timestamp = str(time.time())
    folderPath = os.path.join(root, f"{name} {timestamp}")
    print(f"New folder created:\n{folderPath}\n")
    
    # Create folder
    os.mkdir(folderPath)

    # return path of newly created folder
    return folderPath


# Function to plot the values of x to a file
def plot(Xs, iterNum, outFolder):
    
    # Prepare results
    numPoints = len(Xs)
    points = []

    # For every value of x
    for i, x in enumerate(Xs):
        
        # Plot one point based on the value
        x, y = map(lambda c: str(int(float(c) * 400)), [i / numPoints, x])
        points.append(svgPointFormat.replace('[$X]', x).replace('[$Y]', y))

    # Collect all points
    result = svgFormat.replace('[$DATA]', '\n'.join(points))

    # Write the results to a file
    with open(os.path.join(outFolder, f'Iteration {iterNum}.svg'), 'w') as F:
        F.write(result)

    return


# Function to prepare a html page to view all the plots
def collectPlots(maxIteration, poltEveryNthIteration, outputPath):

    # Write the html content to a file
    with open(os.path.join(outputPath, 'Simulation Summary.html'), 'w') as F:
        F.write(summaryHtmlFormat.replace('[$MAX]', str(maxIteration)).replace('[$STEP]', str(poltEveryNthIteration)))
