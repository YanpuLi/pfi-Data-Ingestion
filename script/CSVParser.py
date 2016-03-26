import csv
import json

def csv_parsing_file(input_file, fileName, jsonPath):
   
    def parseMeta(count, array):
        strName = "MetaData%i"%(count-1)
        output[strName] = {}
        for i in range(1,len(array)):
            output[strName][array[i][0]] = array[i][1]

    input_data = open(input_file, 'r')
    intermediate = []
    output = {}
    try:
        reader = csv.reader(input_data)
        reader = list(reader)
 
        # count: num of sections, countLine: num of rows
        count = 0
        countLine = 0

        for row in reader:     
            countLine = countLine + 1
      
            #splitting raw data into sections by using blank line as deliminator
            if row[0] != '' and countLine != len(reader):
                intermediate.append(row)
            
            elif row[0] != '' and countLine == len(reader): 
                output['MetaDataLast'] = {}
                for i in range(1,(len(intermediate)+1)):
                    if i < len(intermediate):
                        output['MetaDataLast'][intermediate[i][0]] = intermediate[i][1]
                    else:
                        output['MetaDataLast'][row[0]] = row[1]
              
            else:  
                count = count +1
                if ('Sample Table' in intermediate[0]):
                    output['ExperimentData'] = {}
                    output['ExperimentData']['Title'] = intermediate[0]
                    output['ExperimentData']['Unit'] = intermediate[2]
                    output['ExperimentData']['Content'] = []
                    exper = {}
                    for i in range(3,len(intermediate)):
                        for j in range(len(intermediate[1])):             
                            exper[intermediate[1][j]] = intermediate[i][j]
                        output['ExperimentData']['Content'].append(exper)
                        exper = {}
                    intermediate = []
                else:
                    parseMeta(count, intermediate)
                    intermediate = []
        print (jsonPath+fileName+'.json')
        with open((jsonPath+fileName+'.json'),'w') as outfile:
            json.dump(output, outfile, indent = 4)
    
                    
                        
                
    finally:
        input_data.close()

