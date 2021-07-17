# A Tool To Generate a Protobuf File from an arbitrary OpenML Dataset

This tool will create a `.proto` file whose structure looks like `model.proto` in the same folder. Below is an example for DataID 61.

```
// This file was generated with the Protobuf generator tool.
// Dataset ID    : 61
// Dataset Name  : iris;
// Dataset URL   : https://www.openml.org/data/v1/download/61/iris.arff
// Num. Columns  : 5
// Num. Rows     : 150
// Target Feature: class

// Beginning of Description of Dataset:
// **Author**: R.A. Fisher
// **Source**: [UCI](https://archive.ics.uci.edu/ml/datasets/Iris) - 1936 - Don>
// **Please cite**:
// **Iris Plants Database**
// This is perhaps the best known database to be found in the pattern recogniti>
// Predicted attribute: class of iris plant.
// This is an exceedingly simple domain.
// ### Attribute Information:
//     1. sepal length in cm
//     2. sepal width in cm
//     3. petal length in cm
//     4. pet
//

syntax = "proto3";

message Empty {
}

message Features {
  double   Sepallength                    = 1;
  double   Sepalwidth                     = 2;
  double   Petallength                    = 3;
  double   Petalwidth                     = 4;
  string   Class                          = 5;
}

service get_next_row {
   rpc get_next_row(Empty) returns(Features);
}

/*
//This code section can be directly used
//at the end of gen_next_row in the server.py file
//for OpenML dataset nr. 61
        response.Sepallength                    = row[0]
        response.Sepalwidth                     = row[1]
        response.Petallength                    = row[2]
        response.Petalwidth                     = row[3]
        response.Class                          = row[4]
*/

```
# 1. How to get the data ID from OpenML?
Usually whenever opening a dataset in OpenML, the ID is the number at the end of the URL. For instance, the link below contains a dataset with ID 31. This number will be used to input into the tool.
```
https://www.openml.org/d/31
```
# 2. How to Execute?
There are 2 ways to execute the code with 3 inputs
1. `DataID`: obtained in 1. above
2. *Output filename* (optional): default one is `model.proto`
3. *Output folder* (optional): default at the current working directory
 
## 2.1. Input from Terminal

In Terminal, the working directory should be the same as the folder containing 2 files `main.py` and `utils.py` files, run the below command.
```
python main.py <DataID> <output_file_name> <output_folder>
```
- Replace `<DataID>`, `<output_file_name>` and `<output_folder>` with your own inputs. 
- Either `output_file_name` or `output_folder` can be omitted, or both can be omitted, if you don't want to custom the default settings.
- The order should be followed.

Examples
```
python main.py 2
python main.py 2 "my_model.proto"
python main.py 2 "my_model.proto" "openml_folder"
```
## 2.2. Input in file main.py
First, modify the inputs.
1. Change DataID
    <br/>Replace value of idx in line 12 into your desired DataID: `idx = 42563`
2. Change Output Filename
<br> Replace filename in line 18: `file_name = 'model.proto'`
3. Change Output Folder
<br/> Replace folder name in line 25: `output_folder = ''`

Alternative, you can directly input in line 27 before the function `write_proto` is called.

Then, in the terminal, run
```
python main.py
```
# 3. Create subfolder ./openml_n, with all files needed for an AI4EU-onboardable databroker for OpenmL dataset with ID = n:

## 3.1 Show information about an OpenML file
To just show information about an OpenML file, using here OpenML ID 61 as example:
```
python checkOpenMLFile.py 61
```
## 3.2 Create associated subfolder, and run/test the server
Using the --s flag, the program will also create a separate subfolder with all the files needed for an AI4EU-onboardable databroker for that OpenML file:
```
python checkOpenMLFile.py 61 --s
```
After that you can check the existence of subfolder ./openml_61 , with all the needed files inside.

Inside the subfolder created above, simply run the standalone server:
```
python server.py
```
And in a different terminal, within the same subfolder run the client:
```
python client.py
```
Each run of this client will fetch an additional row of data from that server.

## 3.3 Build dockerized version of the server
To build and run the dockerized version of the server, the Dockerfile is already provided. Shut down the standalone server program first (to release the usage of port 8061 on your computer). Then within the subfolder run the following commands, in this example for subfolder openml_61, tagging the docker image as "openml61:v1" :
```
$ docker build -t openml61:v1 .
$ docker run -p 8061:8061 -ti openml61:v1 /bin/bash
```

## 3.4 Inspect all 82 OpenML files of interest, and/or generate their associated folders at once
To inspect all 82 OpenML files of interest (which are specified at the end of the utils.py program):
```
python checkOpenMLFilesOfInterest.py
```
And to generate the subfolders for all those OpenML files at once, use the --s flag:
```
python checkOpenMLFilesOfInterest.py --s
```

## 3.5 Create a subfolder manually for any desired OpenML ID
The subfolder creation process can be done automatically as described in 3.2, or also manually, using the following steps:

### - Generate the .proto file for the data ID of interest, in this example using 61:
```
$ python main.py 61
```

### - Copy the provided template_files subfolder, in this example using openml_61 as the name of the target new subfolder:
```
$ cp -r template_files openml_61
```

### - Enter the new subfolder, copy the new .proto file just created above, and generate inside the subfolder the needed grpc-related python files from it:
```
$ cd openml_61
$ cp ../model.proto .
$ bash ../python_files_from_proto.sh
```

### - Modify the file server.py, by copying the variable assignments from the commented section at the end of the model.proto file, and inserting them at the end of get_next_row.
In this example the code in question (for OpenML ID 61) is:
```
        response.Sepallength                    = row[0]
        response.Sepalwidth                     = row[1]
        response.Petallength                    = row[2]
        response.Petalwidth                     = row[3]
        response.Class                          = row[4]
```

### - Also edit the OpenML ID number in the myconstants.py file. In our example it should be 61:
```
DATA_ID = 61
```
