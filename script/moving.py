#!/usr/bin/python
#
'''
python moving.py --src WIP sourcePath --dst raw Path --jdst json storing Path
'''
from CSVParser import csv_parsing_file
from XMLParser import xml_parsing_file
import sys, os, shutil
import argparse
import glob


parser = argparse.ArgumentParser(description='file moving')
parser.add_argument('--src', action='store', dest='src', help='store the sourcePath')
parser.add_argument('--dst', action='store',dest='dst',help='store the destinationPath')
parser.add_argument('--jdst', action='store',dest='jdst',help='store the json file')
result = parser.parse_args()

'''
def generateDstFolder(root, format, srcPath, dstPath):
    for f in glob.glob("%s/*.%s"%(root, format)):
            src = f
            dst = f
            dst = dstPath + dst[len(srcPath):-(len(f.split('/')[len(f.split('/'))-1])+1)] + '/2'
            # identify if the storing folder exist, if not, new one first
            if not os.path.isdir(dst):
                os.makedirs(dst)
                shutil.move(src, dst)

def movingFile(srcPath, dstPath):
    for root, dirs, files in os.walk(result.src):
        format = 'csv'
        generateDstFolder(root, format, srcPath, dstPath)
'''

def movingFile(srcPath, dstPath):
    files = os.listdir(srcPath)
    for f in files:
        src = srcPath+'/'+f
        dst = dstPath 
    
        if not os.path.isdir(dst):
            os.makedirs(dst)
        shutil.move(src, dst)


         

    '''
    root: absolute path for each root folder
    dirs: folder names included in the root
    files: file names included in the root
    src = srcPath+'/'+item
    dst = dstPath +'/'+item
    shutil.move(src, dst)

    if files.endswith(".csv"):

    mkdir: new a folder
    makedirs: duoji folder
    '''

movingFile(result.src, result.dst)

flagXML = False
flagCSV = False
flagXLS = False
for root, dirs, files in os.walk(result.dst):
    #print "{} in {}".format(len(files), root)
    for f in glob.glob("%s/*.xml"%root):
        para = f.split('/')
        xml_parsing_file(f, para[len(para)-1][:-4], result.jdst)
        flagXML = True
    if flagXML == False:
        for f in glob.glob("%s/*.csv"%root):
           para = f.split('/')
           xls_parsing_file(f, para[len(para)-1][:-4], result.jdst)
           flagXLS = True
        if flagXLS == False:
            for f in glob.glob("%s/*.csv"%root):
                para = f.split('/')
                # f is for path+filename.csv, para[len(para)-1][:-4] is for filename, result.jdst is for json folder path
                csv_parsing_file(f, para[len(para)-1][:-4], result.jdst)
                flagCSV = True

    flagXML = False
    flagCSV = False
    flagXLS = False


    