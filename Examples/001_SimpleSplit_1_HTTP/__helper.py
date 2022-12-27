import os, sys, time
import pathlib, http.client


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


# Function to search for the number on google
def googleSearchNumber(num):
    
    # Search for the number on google and get the results
    connection = http.client.HTTPConnection('www.google.com')
    connection.request('GET', f"/search?q={num}")
    response = connection.getresponse()
    responseData = response.read()
    connection.close()

    # Return the results of the google search
    return responseData


# Function to save data to output file
def saveOutputFile(outputPath, num, data):
    
    # Get output file path
    filePath = os.path.join(outputPath, str(num) + '.html')

    # Write data to output file
    with open(filePath, 'wb') as F:
        F.write(data)
