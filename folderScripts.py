import os
import re
import pprint
import sys
import shutil

os.chdir("C:\\mockTestScript\\Clients")
listOfClients = os.listdir(os.getcwd())

clientRoot = "C:\\mockTestScript\\Clients\\"
individTemplatePath = "C:\\mockTestScript\\templates\\File Structure Ind XXXX Last, First & Spouse\\2017 XXXX"
businessTemplatePath = "C:\\mockTestScript\\templates\\File Structure BUS XXXX Business Name\\123117 XXXX"
businessTemplatePathNotYear = "C:\\mockTestScript\\templates\\File Structure BUS XXXX Business Name"
newBusinessPath = "C:\\mockTestScript\\clients\\File Structure BUS XXXX Business Name"
fullIndividualTemplate = "C:\\mockTestScript\\templates\\File Structure Ind XXXX Last, First & Spouse"
newIndClientLocation = "C:\\mockTestScript\\clients\\File Structure Ind XXXX Last, First & Spouse"

def getClientID(arg):
    for client in listOfClients:
        clientID = client[0:4]
        regex = re.compile(clientID)
        mo = regex.search(arg)
        if mo != None:
            matchString = mo.group()
            if matchString == clientID:
                return clientID

def replaceXInPath(clientID, pathname):
    regex = re.compile(r'[X]{4}')
    return regex.sub(clientID, pathname)

# We need to present user with screen that offers select options based on use cases
# User needs to create a new client
# User needs to add an additional year to existing clients
# User should be asked to specify whether this is business or individual should it affect program flow


def recursiveWalk(rootDir, clientID):
    try:
        for entry in os.listdir(rootDir):
            newPath = os.path.join(rootDir, entry)
            finalPath = replaceXInPath(clientID, newPath)
            os.rename(newPath, finalPath)
            recursiveWalk(finalPath, clientID)

    except OSError as e:
        print(e, file=sys.stderr)


def checkClientForX():
    print("Please enter the ID of the Client you would like to inspect.")
    checkID = input()
    for dir in os.listdir(clientRoot):
        if dir[0:4] == checkID:
            newPath = os.path.join(clientRoot, dir)
            recursiveWalk(newPath, dir[0:4])


def isBusClient(clientPath):
    clientRegex = re.compile(r'\d{6}(\s)([X]{4}|\d{4})')
    if clientRegex.search(clientPath):
        return True
    else:
        return False

def isIndividualClient(clientPath):
    clientRegex = re.compile(r'\d{4}(\s)([X]{4}|\d{4})')
    if clientRegex.search(clientPath):
        return True
    else:
        return False

def afterCopy(pathname, oldYear, newYear, clientID):
    regex = re.compile(r'' + oldYear + '[X]{4}')

    for currentFolder, subFolder, fileName in os.walk(pathname):
        if regex.search(currentFolder):
            newPath = regex.sub(newYear + " " + clientID, currentFolder)
            os.rename(currentFolder, newPath + " ")
        elif regex.search(str(fileName)):
            file = ''.join(fileName)
            fullFilePath = os.path.join(currentFolder, file)
            newPath = regex.sub(newYear + " " + clientID, fullFilePath)
            os.rename(fullFilePath, newPath)




def addNewYear():
    # determine whether we are adding to an individual or business client
    # get the latest year from correct template and increment by one
    # copy to respective client
    # replace 'XXXX' in newly added directory with client ID
    # move on to the next client repeating for each client

    busClients = []
    individClient = []
    print("Please Enter the desired year for Business Clients e.g. 123116")
    businessBaseName = input()
    print("Please Enter the desired year for Individual Clients i.e. 2016")
    individBaseName = input()
    for client in os.listdir(clientRoot):
        subDirs = os.path.join(clientRoot, client)
        for dir in os.listdir(subDirs):
            if isBusClient(dir):
                busClients.append(client)
            elif isIndividualClient(dir):
                individClient.append(client)
            else:
                print("Not a valid Client")

            if client in busClients:
                baseName = os.path.basename(businessTemplatePath)
                clientID = client[0:5]
                beforeIncrement = baseName[0:7]
                baseName = baseName.replace(beforeIncrement, businessBaseName+ " ")
                finalName = clientRoot + client + "\\" + str(baseName)
                if not os.path.exists(finalName):
                    shutil.copytree(businessTemplatePath, finalName)
                afterCopy(finalName, beforeIncrement, businessBaseName, clientID)


            elif client in individClient:
                baseName = os.path.basename(individTemplatePath)
                clientID = client[0:5]
                beforeIncrement = baseName[0:5]
                baseName = baseName.replace(beforeIncrement, individBaseName+ " ")
                finalName = clientRoot + client + "\\" + str(baseName)
                if not os.path.exists(finalName):
                    shutil.copytree(individTemplatePath, finalName)
                afterCopy(finalName, beforeIncrement, individBaseName, clientID)





    busClients = sorted(set(busClients))
    individClient = sorted(set(individClient))
    pprint.pprint(individClient)
    pprint.pprint(busClients)




def createNewClient():
    # Present user with option to choose Bus/Ind
    print("Is this a new Individual Client or Business client? ((b) for Business or (c) for ind. client")
    answer = input()

    answer = str.capitalize(answer)

    if answer == "B":
        print("Please enter the Business ID number for the new client")
        id = input()
        print("Please enter the name of the business")
        busName = input()
        #Get file structure from templates
        shutil.copytree(businessTemplatePathNotYear,newBusinessPath)

        baseName = id + " " + busName
        newName = clientRoot + baseName + "\\"
        os.rename(newBusinessPath, newName)

        #replace X's with user entered id number
        recursiveWalk(newName, id)

    elif answer == "C":
        print("Please enter the Individual Client ID number for the new Client")
        individID = input()

        print("Please enter the individual's name")
        indName = input()

        shutil.copytree(fullIndividualTemplate,newIndClientLocation)

        dirName = individID + " " + indName
        newIndivName = clientRoot + dirName + "\\"
        os.rename(newIndClientLocation, newIndivName)
        recursiveWalk(dirName, individID)

        # Same as above only utilize the individual template


    else:
        print("The option you selected is not valid.")


def presentScreen():
    print("Please choose an option below based on what you are trying to do.")
    print("\nWould you like to create a new client?---Type N---to create a new client")
    print("Would you like to add a year to existing clients?----Type Y---to add a year to existing clients")
    print("Would you like to replace Xs for a specific Client by ID?----Type I----to check a specific Client")
    print("If you would like to exit, type----E----.")
    print("\nFyi: Client Root Directory: " + clientRoot + "\n" "Directory year: "
          + individTemplatePath + "\n" + "Template Paths: " + fullIndividualTemplate)

presentScreen()
userChoice = input()
userChoice = str.capitalize(userChoice)


while userChoice != "E":
    if userChoice == "N":
        createNewClient()
    elif userChoice == "Y":
        addNewYear()
    elif userChoice == "I":
        checkClientForX()
    elif userChoice == "E":
        exit()
    presentScreen()
    userChoice = input()
    userChoice = str.capitalize(userChoice)


