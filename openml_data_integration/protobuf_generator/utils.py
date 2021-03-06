# date: 2021.03.29
# author: Han Tran (htran@know-center.at)
# Modified by Raul Saavedra (raul.saavedra@iais.fraunhofer.de)

import os
import re
import openml as oml


#####################################################################
'''
*** Function: write a proto file with a given recognized ID in OpenML
*** Input: dataID from OpenML, name and location for the output file
*** Output: filename.proto (default: "model.proto")
'''
#####################################################################

def write_proto(dataID, file_name=f'model.proto', output_folder=''):
    output_file = os.path.join(output_folder, file_name)
    try:
        dataset = oml.datasets.get_dataset(dataID)
        df = dataset.get_data()[0]
    except:
        print(f'No data with ID {dataID}')
    with open(output_file, 'w') as f:
        type_ser = df.dtypes
        ncols = len(type_ser)
        nrows = len(df.values)
        print(f'Dataset ID    : {dataID}')
        print(f'Dataset Name  : {dataset.name};')
        print(f'Dataset URL   : {dataset.url}')
        print(f'Num. Columns  : {ncols}')
        print(f'Num. Rows     : {nrows}')
        print(f'Target Feature: {dataset.default_target_attribute}')
        #print(f'Beginning of Description of Dataset:')

        # Info about the OpenML file in a commented header section
        f.write(f'// This file was generated with the Protobuf generator tool.\n')
        f.write(f'// Dataset ID    : {dataID}\n')
        f.write(f'// Dataset Name  : {dataset.name};\n')
        f.write(f'// Dataset URL   : {dataset.url}\n')
        f.write(f'// Num. Columns  : {ncols}\n')
        f.write(f'// Num. Rows     : {nrows}\n')
        f.write(f'// Target Feature: {dataset.default_target_attribute}\n\n')
        f.write(f'// Beginning of Description of Dataset:\n')
        textd = dataset.description[:800]
        descr = textd.split("\n")
        for line in descr:
            if line.strip() != "":
                #print(f'\t{line[:70]}')
                f.write(f'// {line}\n')

        f.write(f'//\n\n')

        # Write actual protobuf file contents
        f.write('syntax = "proto3";\n\n')

        # Empty message
        f.write(f'message Empty {{\n}}\n\n')

        # Features message
        f.write('message Features {\n')

        types = [str(m) for m in type_ser]
        for k, c in enumerate(types):
            text = map_type(c)
            varname = type_ser.index[k].replace("-", "_")
            f.write(f'\t{text:8} {varname.capitalize():30} = {k+1};\n')
        f.write('}\n\n')

        # The get_next_row service
        f.write('service get_next_row {\n')
        f.write('\t rpc get_next_row(Empty) returns(Features);\n')
        f.write('}\n')

        # Commented code snippet, can be directly used at
        # the end of get_next_row in the server.py file
        f.write(f'\n/*\n//This code section can be directly used\n')
        f.write(f'//at the end of gen_next_row in the server.py file\n')
        f.write(f'//for OpenML dataset nr. {dataID}\n')
        for k, c in enumerate(types):
            text = map_type(c)
            varname = type_ser.index[k].replace("-", "_")
            if (text == 'string') or (text == 'double') or (text == 'float'):
                f.write(f'\t\t\t\tresponse.{varname.capitalize():30} = row[{k}]\n')
            else:
                f.write(f'\t\t\t\tresponse.{varname.capitalize():30} = numpy.{text}(row[{k}])\n')
        f.write(f'*/\n\n')


    print(f'\nDone writing .proto file for OpenML dataset nr. {dataID} into {output_file}\n')


#####################################################################
'''
*** Function: map the given type, following the protobuf docs
*** ( as in https://developers.google.com/protocol-buffers/docs/proto3 )
*** Input: the vtype as it comes from the OpenML dataset
*** Output: the type to use in a .proto file
'''
#####################################################################
def map_type (vtype):
    if   vtype == 'category':
         text   = 'string'
    elif vtype == 'float64':
         text   = 'double'
    elif vtype == 'float32':
         text   = 'float'
    elif vtype == 'uint8':
         text   = 'uint32'
    else:
         text   = vtype
    return text


#####################################################################
'''
*** Function: provide the IDs of the OpenML datasets of interest
*** Output: array of the IDs of OpenML datasets of interest
'''
#####################################################################
def get_file_Nums_of_interest ():

    ''''
    # Full list of 155 openML file numbers of interest,
    # from zip file with associated protobuf files (sent by Martin)
    OpenMLFiles = [
        3, 6, 8, 9, 10, 13, 15, 16, 22, 24,
        28, 29, 31, 32, 36, 37, 38, 40, 41, 42,
        43, 44, 50, 54, 59, 60, 61, 62, 149, 150,
        151, 179, 182, 187, 307, 310, 311, 313, 329, 333,
        334, 335, 350, 357, 374, 375, 377, 451, 458, 466,
        469, 470, 481, 566, 956, 1046, 1049, 1050, 1053, 1063,
        1067, 1068,

        #           1110, # <-- Download fails, possibly way too large?

                         1113, 1115, 1116, 1119, 1120, 1121, 1169,
        1219, 1220, 1413, 1459, 1461, 1462, 1464, 1466, 1467, 1471,
        1475, 1476, 1479, 1480, 1486, 1487, 1489, 1491, 1492, 1493,
        1494, 1497, 1500, 1504, 1510, 1547, 1548, 1549, 1552, 1553,
        1554, 1555, 1590, 1596, 1597, 4135, 4534, 4538, 6332, 23380,
        23512, 40536, 40646, 40647, 40648, 40649, 40650, 40663, 40664, 40665,
        40666, 40668, 40669, 40670, 40671, 40672, 40677, 40678, 40680, 40681,
        40682, 40685, 40686, 40687, 40690, 40691, 40693, 40700, 40701, 40702,
        40704, 40705, 40706, 40707, 40708, 40710, 40711, 40713, 40900, 40945,
        40966, 40975, 40983, 40984, 41496
    ]
    '''

    '''
    Examples of very large OpenML datasets (> 10K rows)
        149   # 1.45M rows
        150   # 581K rows
        1113  # 494K rows
        1169  # 539K rows
        1219  # 399K rows
        1596  # 581K rows (same #rows & columns as in #150, maybe related)
        1597  # 284K rows
        40672 # 100K rows

    Examples of "wide" OpenML files (many columns)
        313   # 102 cols
        1116  # 168 cols
        1479  # 101 cols
        1548  # 101 cols
        40536 # 121 cols
        40665 # 169 cols
        40666 # 169 cols
        40670 # 181 cols

    The "narrowest" files (< 10 columns) are:
        2 columns:  41496
        3 Columns:  374
        4 Columns:  43, 40704
        5 Columns:  61, 329, 469, 1413, 1462, 1464
        6 columns:  8, 451, 1489, 40682, 40983
        7 columns:  333, 334, 335, 1115, 40669, 40681, 40975
        8 columns:  37, 481, 1500, 40671, 40678, 40700, 40711

    Files with columns of type object:
        38, 374, 40945, 41496
    '''

    # The following 83 files from the 150 files of interest are
    # neither very large (<= 10K rows),
    # nor very wide (<=35 cols),
    # nor are they problematic to download (e.g. like 1110 is),
    # and also they have no column of type object
    OpenMLFileNums = [
        8, 9, 10, 13, 15, 24, 29, 31, 36, 37,
        41, 43, 50, 54, 59, 61, 62, 187, 307, 329,
        333, 334, 335, 375, 451, 466, 469, 470, 481, 566,
        1063, 1067, 1068, 1115, 1121, 1413, 1462, 1464, 1467, 1480,
        1489, 1497, 1500, 1504, 1510, 1547, 1552, 1553, 1554, 4538,
        23380, 40646, 40647, 40648, 40649, 40650, 40663, 40664, 40669, 40671,
        40677, 40678, 40680, 40681, 40682, 40686, 40687, 40690, 40691, 40693,
        40700, 40701, 40702, 40704, 40706, 40707, 40708, 40710, 40711, 40713,
        40975, 40983, 40984
       ]

    return OpenMLFileNums

