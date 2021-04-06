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

def write_proto(dataID, output_folder='', file_name=f'model.proto'):
    output_file = os.path.join(output_folder, file_name)
    try:
        df = oml.datasets.get_dataset(dataID).get_data()[0]
    except: 
        print(f'No data with ID {dataID}')
    with open(output_file, 'w') as f:
        f.write('syntax = "proto3";\n\n')
        f.write(f'option java_outer_classname = "Data{dataID}Proto";\n')
        f.write('option objc_class_prefix = "KC";\n\n')
        f.write(f'package know_center.openml.data{dataID};\n\n')
        f.write(f'service Data {{ \n')
        f.write('\trpc PullData(Empty) returns (Response);\n')
        f.write('}\n\n')
        f.write(f'message Empty {{\n}}\n\n')
        f.write(f'message Response {{\n')
        f.write(f'\tstring label = 1;\n')
        f.write(f'\tFeature feature = 2;\n')
        f.write('}\n\n')
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
        type_ser = df.dtypes
        types = [str(m) for m in type_ser]
        for k, c in enumerate(types):
            text = c if c!='category' else "string"
            f.write(f'\t{text:8} {type_ser.index[k].capitalize():30} = {k+1};\n')
        f.write('}')
    print(f'Done writing {dataID} into {output_file}')