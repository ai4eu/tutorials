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
# 3. Generating subfolder openml_xx for a given dataID, with all needed files:

First generate the .proto file for the data ID of interest, in this case using 61 as example:
```
$ python main.py 61
```

Then create subfolder starting from the provided template_files subfolder. In this case using openml_61 as the target new subfolder:
```
$ cp -r template_files openml_61
```

Enter the new subfolder, copy the new .proto file you created above, and generate in the subfolder the needed python files from it:
```
$ cd openml_61
$ cp ../model.proto .
$ bash ../python_files_from_proto.sh
```

Now edit server.py, the variable assignments section at the end of get_next_row, using (copy/pasting) the code snippet from the commented section that can be found at the end of the generated .proto file. In this example the code in question is:

```
	response.Sepallength                    = row[0]
        response.Sepalwidth                     = row[1]
        response.Petallength                    = row[2]
        response.Petalwidth                     = row[3]
        response.Class                          = row[4]
```

Also edit the hardcoded openml ID number in the myconstants.py file. In our case it should be 61:
```
DATA_ID = 61
```

Then simply run the server:
```
python server.py
```

And in a different terminal, within the same subfolder run the client:
```
python client.py
```

To generate and run the dockerized version of the server, the Dockerfile is already provided. Shut down the standalone server program first (to release the usage of port 8061 on your computer). Then run the following commands, in this case tagging the docker image as "openml61:v1" :
```
$ docker build -t openml61:v1 .
$ docker run -p 8061:8061 -ti openml61:v1 /bin/bash
```
