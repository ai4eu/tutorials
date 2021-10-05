# date: 2021.03.29
# author: Han Tran (htran@know-center.at)

import sys
from utils import *

def main(argv):
    # get DataID from input
    try:
        idx = int(argv[0])
    except:
        # If not provided from Terminal, use some default
        idx = 42563
        # idx = 61

    # get file_name for output
    try:
        file_name = argv[1]
    except:
        #file_name = 'model'+str(idx)+'.proto' # if not provided from Terminal
        file_name = 'model.proto' # if not provided from Terminal

    # get file_name for output
    try:
        output_folder = argv[2]
    except:
        # change output folder
        output_folder = ''

    write_proto(dataID=idx, file_name=file_name, output_folder=output_folder,
                                        license_filename="license-1.0.0.json",
                                        description_filename='description.txt',
                                        author_filename = 'authors.txt',
                                        input_icon='openml-databroker.png',
                                        icon_filename='icon.png'
                                        )

if __name__ == '__main__':
    main(sys.argv[1:])
