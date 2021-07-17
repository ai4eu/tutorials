# date: 2021.07.14
# author: Raul Saavedra raul.saavedra.felipe@iais.fraunhofer.de

import openml as oml
import time
from utils import *
import main
import subprocess
import sys

def PullData(idx, subfolders):
    idx = int(idx)
    #print(f'\n\nGetting data with ID: {idx}')
    try:
        dataset = oml.datasets.get_dataset(idx);
    except:
        print(f'Exception: OpenML Dataset {idx} not found')
        return

    data  = dataset.get_data()
    df    = data[0]
    ncols = len(df.dtypes)
    nrows = len(df.values)

    #if (ncols > 35): return
    #if (nrows > 10000): return
    types = [map_type(str(m)) for m in df.dtypes]
    #if ("object" in types): return
    #print(f'idx:{idx}  ncols:{ncols}  nrows:{nrows} ')
    #return

    print(f'Dataset ID    : {idx}')
    print(f'Dataset Name  : {dataset.name}')
    print(f'Dataset URL   : {dataset.url}')
    print(f'Num. Columns  : {ncols}')
    print(f'Num. Rows     : {nrows}')
    print(f'Target Feature: {dataset.default_target_attribute}')
    '''
    descr = dataset.description[:400].split("\n")
    print(f'********** Beginning of Dataset description **********')
    for line in descr:
        if line.strip() != "":
            print(f'{line[:80]}')
    print(f'******************************************************')
    '''
    print(f'Data Column names:')
    print(f','.join(df.columns))
    print(f'Mapped Data types:')
    print(f','.join(types))
    #print(f'Data Rows:')
    #for i in range(nrows):
    #    print(f'{i}: {df.values[i]}')
    print(f'Example first data row:')
    print(f'{df.values[0]}\n')

    if subfolders:
        # Invoke protobuf file generation for this OpenML dataset
        main.main([idx])

        # Invoke shell script that creates an openml_## subfolder with all files
        # needed for a complete AI4EU-onboardable databroker for this OpenmL dataset
        rc = subprocess.call("./create_openml_subfolder.sh")

        if (rc != 0):
            print(f'Return code from subfolder creation: {rc}\n')
            exit(rc)

        print(f'Done creating subfolder openml_{idx}\n')


def checkOpenMLFile(argv):
    idx = 0
    if (len(argv) < 1):
        print('\nMode of use:\n\npython checkOpenMLFile.py N [--s]\n')
        print('\tN: OpenML dataset ID (an integer).')
        print('\tOptional --s flag creates the ./openml_N subfolder.\n')
        return

    createSubfolders = False
    try:
        if argv[1] == "--s":
           createSubfolders = True
    except:
        pass

    PullData(argv[0], createSubfolders)


if __name__ == '__main__':
    checkOpenMLFile(sys.argv[1:])
