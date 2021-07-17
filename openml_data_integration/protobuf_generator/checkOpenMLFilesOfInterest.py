# date: 2021.07.17
# author: Raul Saavedra raul.saavedra.felipe@iais.fraunhofer.de

from utils import *
import sys
import checkOpenMLFile


def checkOpenMLFilesOfInterest(argv):
    createSubfolders = False
    try:
        if argv[0] == "--s":
           createSubfolders = True
    except:
        pass
    OpenMLFiles = get_file_Nums_of_interest()
    print(f'# of Datasets of interest: {len(OpenMLFiles)}\n')
    print(f'Dataset IDs: {OpenMLFiles}\n\n')
    for i in OpenMLFiles:
        rc = checkOpenMLFile.PullData(i, createSubfolders)


if __name__ == '__main__':
    checkOpenMLFilesOfInterest(sys.argv[1:])
