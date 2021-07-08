# date: 2021.03.29
# author: Han Tran (htran@know-center.at)

import sys
from utils import *

def main(argv):
    # get DataID from input
    try:
        idx = int(argv[0])
    except:
        idx = 42563 # if not provided from Terminal
        #idx = 61

    # get file_name for output
    try:
        file_name = argv[1]
    except:
        file_name = 'model'+str(idx)+'.proto' # if not provided from Terminal

    # get file_name for output
    try:
        output_folder = argv[2]
    except:
        # change output folder
        output_folder = ''

    write_proto(dataID=idx, file_name=file_name, output_folder=output_folder)

if __name__ == '__main__':
    main(sys.argv[1:])
