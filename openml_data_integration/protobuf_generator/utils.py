# date: 2021.03.29
# author: Han Tran (htran@know-center.at)

import os
import re
import openml as oml

#####################################################################
'''
*** Function: write a proto file with a given regconized ID in OpenML
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
        print(f'Dataset ID    : {dataID}')
        print(f'Dataset Name  : {dataset.name};')
        print(f'Dataset URL   : {dataset.url}')
        print(f'Num. Columns  : {ncols}')
        print(f'Target Feature: {dataset.default_target_attribute}\n')
        print(f'Beginning of Description of Dataset:')

        f.write(f'// This file was generated with the Protobuf generator tool.\n')
        f.write(f'// Dataset ID    : {dataID}\n')
        f.write(f'// Dataset Name  : {dataset.name};\n')
        f.write(f'// Dataset URL   : {dataset.url}\n')
        f.write(f'// Num. Columns  : {ncols}\n')
        f.write(f'// Target Feature: {dataset.default_target_attribute}\n\n')
        f.write(f'// Beginning of Description of Dataset:\n')
        textd = dataset.description[:800]
        descr = textd.split("\n")
        for line in descr:
            if line.strip() != "":
                print(f'\t{line}')
                f.write(f'// {line}\n')

        f.write(f'//\n\n')
        f.write('syntax = "proto3";\n\n')
        #f.write(f'option java_outer_classname = "Data{dataID}Proto";\n')
        f.write(f'option java_outer_classname = "ExampleProto";\n')
        f.write('option objc_class_prefix = "KC";\n\n')
        #f.write(f'package know_center.openml.data{dataID};\n\n')
        f.write(f'service Example {{ \n')
        f.write('\trpc PullData(Empty) returns (stream Response);\n')
        f.write('}\n\n')
        f.write(f'message Empty {{\n}}\n\n')
        f.write(f'message Response {{\n')
        f.write(f'\tstring record = 1;\n')
        f.write(f'\tstring label = 2;\n')
        f.write(f'\t//Feature feature = 3;\n')
        f.write('}\n\n')
        f.write('/*\n')
        f.write('message Feature {\n')
        label = 'class'
        try:
            df_label = df.loc[:, [label]].shape[1]
        except:
            df_label = 0
        if df_label == 1:
            df = df.drop(label, axis=1)
        else:
            print('No label ("class" name) found in the dataset')
        types = [str(m) for m in type_ser]
        for k, c in enumerate(types):
            text = c if c!='category' else "string"
            #Some mappings needed, following the protobuf documentation as in:
            #https://developers.google.com/protocol-buffers/docs/proto3
            #print(f'{text}')
            if   text == 'float64':
                 text = 'double'
            elif text == 'float32':
                 text = 'float'
            elif text == 'uint8':
                 text = 'uint32'
            f.write(f'\t{text:8} {type_ser.index[k].capitalize():30} = {k+1};\n')
        f.write('}\n')
        f.write('*/\n')
    print(f'Done writing {dataID} into {output_file}')
