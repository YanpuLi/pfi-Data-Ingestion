import xmltodict
import operator
import pandas as pd
import json
from datetime import datetime
import sys, os


def xml_parsing_file(input_file, fileName, jsonPath):
	start=datetime.now()
	with open(input_file) as fd:
		doc = xmltodict.parse(fd.read())
	output = {}
	output['MetaData'] = {}
	output['MetaData']['ExperimentId'] = doc['Experiment']['@Name']
	output['MetaData']['StartTimeLocal'] = doc['Experiment']['@StartTimeLocal']
	output['MetaData']['Duration'] = doc['Experiment']['@Duration']
	output['MetaData']['User'] = doc['Experiment']['@User']

	output['ExperimentData'] = {}
	output['ExperimentData']['Unit'] = {}
	output['ExperimentData']['Content'] = []
	record = {}
	attributeList = []
	count = {}

	# generating output content: meta, unit
	for i in range(len(doc['Experiment']['Trends']['Trend'])):
		output['ExperimentData']['Unit'][doc['Experiment']['Trends']['Trend'][i]['@Name']] = doc['Experiment']['Trends']['Trend'][i]['@Unit']
		attributeList.append(doc['Experiment']['Trends']['Trend'][i]['@Name'])
		count[doc['Experiment']['Trends']['Trend'][i]['@Name']+ '/' +str(i)] = len(doc['Experiment']['Trends']['Trend'][i]['V'])

	# extracting all the attributes values putting in out, json format
	out = {}
	temp = {}
	for i in range(len(doc['Experiment']['Trends']['Trend'])):
		out[doc['Experiment']['Trends']['Trend'][i]['@Name']] = []
		for j in range(len(doc['Experiment']['Trends']['Trend'][i]['V'])):
			temp[doc['Experiment']['Trends']['Trend'][i]['@Name']] = doc['Experiment']['Trends']['Trend'][i]['V'][j]['#text']
			temp['Time'] = doc['Experiment']['Trends']['Trend'][i]['V'][j]['@T']
			out[doc['Experiment']['Trends']['Trend'][i]['@Name']].append(temp)
			temp = {}

	# doing outer merge of all attributes values
	pd1 = pd.DataFrame(out[attributeList[0]])
	for i in range(1, len(attributeList)):
		pd2 = pd.DataFrame(out[attributeList[i]])
		pd1 = pd.merge(pd1, pd2, how = 'outer', on = 'Time')
	pd1.fillna(0, inplace= True)

	tempValueDict = {}
	output['ExperimentData']['Content'] = []
	for i in range(len(pd1)):
		for j in attributeList:
			tempValueDict[j] = pd1.loc[i][j]
		tempValueDict['Time'] = pd1.loc[i]['Time']
		output['ExperimentData']['Content'].append(tempValueDict)

		tempValueDict = {}

	if not os.path.isdir(jsonPath):
		os.makedirs(jsonPath)
	with open((jsonPath+fileName+'.json'),'w') as outfile:
		json.dump(output, outfile, indent = 4)

	print datetime.now()-start