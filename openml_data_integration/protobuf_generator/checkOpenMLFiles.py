# date: 2021.07.14
# author: Raul Saavedra raul.saavedra.felipe@iais.fraunhofer.de

import openml as oml
import time
from utils import *

def PullData(idx):
    idx = int(idx)
    print(f'\n\nGetting data with ID: {idx}')
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
    print(f'Example, First Data Row:')
    print(f'{0}: {df.values[0]}')


def checkOpenMLFiles():
    OpenMLFiles = get_file_Nums_of_interest()
    print(f'# of files of interest is: {len(OpenMLFiles)}')
    print(f'{OpenMLFiles}')
    for i in OpenMLFiles:
        PullData(i)
        #time.sleep(1)

if __name__ == '__main__':
    checkOpenMLFiles()
