import os, sys, time
import pathlib, http.client, urllib.parse, re


# some constants
pageHtmlFormat = """<html>\n<head><title>Facts About Numbers</title></head>\n<body>\n<center><h1>Facts About Numbers</h1></center>\n<hr>\n[$ITEMS]\n<hr>\n<center>[$FOOT]</center>\n</body>\n</html>"""
pageItemHtmlFormat = """<h3>The Number [$NUM]</h3>\n[$LINKS]<br><br>\n"""
pageItemLinkFormat = """<a href="[$LINKURL]">[$LINK]</a><br>\n"""
pageFootHtmlFormat = """[$PLINK]&nbsp;&nbsp;&nbsp;&nbsp;Page [$PNUM]&nbsp;&nbsp;&nbsp;&nbsp;[$NLINK]"""


# Function to create output directory
def prepareFolder(name):

    # Get current working directory
    root = pathlib.Path.cwd()
    
    # Get current timestamp for naming folder
    timestamp = str(time.time())
    folderPath = os.path.join(root, f"{name} {timestamp}")
    print(f"New folder created:\n{folderPath}\n")
    
    # Create output folder
    os.mkdir(folderPath)

    # return path of newly created folder
    return folderPath


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
def saveOutputFile(outputPath, name, data):
    
    # Get output file path
    filePath = os.path.join(outputPath, str(name) + '.html')

    # Write data to output file
    with open(filePath, 'wb') as F:
        F.write(data)


# Function to compute the content of each page
# for every number which needs to be mentioned on the page, this function will check the search result of the number and find wikipedia links
# these links are then collected, and formatted into a neat looking html page
def processPage(pageContent, tempPath, pageNum, hasPrev, hasNext):
    
    itemDataHtml = []

    for record in pageContent:

        linkDataHtml = []

        with open(os.path.join(tempPath, str(record) + '.html'), 'r') as F:

            data = F.read()
            
            allWikiLinks = re.findall('https://[a-z]+.wikipedia.[a-z]+/wiki/[a-zA-Z_0-9()%]*', data)
            allWikiLinksSet = set()
            for link in allWikiLinks:
                while link != urllib.parse.unquote(link):
                    link = urllib.parse.unquote(link)
                allWikiLinksSet.add('https://' + urllib.parse.quote(link[8:]))
            allWikiLinks = list(sorted(list(allWikiLinksSet)))

            for link in allWikiLinks:
                linkDataHtml.append(pageItemLinkFormat.replace('[$LINK]', link).replace('[$LINKURL]', link))
            
        itemDataHtml.append(pageItemHtmlFormat.replace('[$NUM]', str(record)).replace('[$LINKS]', ''.join(linkDataHtml)))
    
    footDataHtml = pageFootHtmlFormat.replace('[$PNUM]', str(pageNum)).replace('[$PLINK]', pageItemLinkFormat.replace('<br>\n', '').replace('[$LINK]', 'Previous').replace('[$LINKURL]', f'Page%20{pageNum - 1}.html') if hasPrev else '').replace('[$NLINK]', pageItemLinkFormat.replace('<br>\n', '').replace('[$LINK]', 'Next').replace('[$LINKURL]', f'Page%20{pageNum + 1}.html') if hasNext else '')
    
    return bytes(pageHtmlFormat.replace('[$ITEMS]', ''.join(itemDataHtml)).replace('[$FOOT]', footDataHtml), 'utf-8')
