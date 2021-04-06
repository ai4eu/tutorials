# date: 2021.03.29
# author: Han Tran (htran@know-center.at)

import sys
from utils import *

def main(argv):
    try:
        idx = int(argv[0])
    except:
        idx = 42563
    write_proto(idx)

if __name__ == '__main__':
    main(sys.argv[1:])