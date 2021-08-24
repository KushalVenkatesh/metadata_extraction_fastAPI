import re
import json
import os

# the function read each line and return metadata as key and value
def get_metadata_in_one_line(line):
    s = re.sub('\t+', '\t', line)
    s = s.replace('\n','\t')
    result = s.split('\t')[:-1]
    return result

# get file extention and base folder of the file
def get_file_information(path, file):
    completedFileName, fileExtention = os.path.splitext(os.path.join(path,file))
    folderName = os.path.basename(path)
    return fileExtention, folderName

def eModul_metadata(filePath, fileName ):
    data = open(r"{}\{}".format(filePath,fileName),'r')
    # get type of the file and name of base folder
    fileExtention, experimentName = get_file_information(filePath, fileName)

    if fileExtention == '.dat':
        fileExtention = 'DATFILE'
    elif fileExtention == '.csv':
        fileExtention = 'CSVFile'
    elif fileExtention == '.cad':
        fileExtention = 'CADFILE'
    else:
        fileExtention = 'DocumentFile'

    dataType = {
        'data type': fileExtention
    }

    # read data file line by line
    lines = data.readlines()
    # get empty lines (where start and end the header)
    emptyLineIndex = []
    for lineIndex in range(len(lines)):
        if len(lines[lineIndex]) == 1:
            emptyLineIndex.append(lineIndex)

    # service information of the experiment, it should be in between the first two empty lines
    serviceInformation = []
    for ind in range(emptyLineIndex[0]+1,emptyLineIndex[1]):
        serviceInformation.append(get_metadata_in_one_line(lines[ind]))

    # generate service information dictionary
    serviceInformationDict = {'Bediener Information':{
        serviceInformation[0][1].replace(':','').strip():serviceInformation[0][2],
        'Zeitpunkt':serviceInformation[0][4],
    }}
    for i in range(len(serviceInformation)-2):
        
        serviceInformationDict['Bediener Information'][serviceInformation[i+1][0].replace(':','').strip()] = serviceInformation[i+1][1]

    # data collection dictionary
    dataCollectionInformationDict = {
        'Datenerfassung': {
            get_metadata_in_one_line(lines[emptyLineIndex[1]+1])[1].replace(':',''):get_metadata_in_one_line(lines[emptyLineIndex[1]+1])[2],
            'Zeitpunkt':get_metadata_in_one_line(lines[emptyLineIndex[1]+1])[4]
        }
    }

    # columns name and unit

    columnsDict = { 'Column Data': {
        'Columns Name':get_metadata_in_one_line(lines[emptyLineIndex[1]+2]),
        'Column Unit':get_metadata_in_one_line(lines[emptyLineIndex[1]+3])
        }
        
    }

    # aggregate the metadata
    metadata = [dataType, serviceInformationDict,dataCollectionInformationDict,columnsDict]
    # jsonData = json.dumps(serviceInformationDict,ensure_ascii=False)
    
    return metadata