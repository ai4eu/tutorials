# A Tool To Generate a Protobuf File from an arbitrary OpenML Dataset

This tool will create a `.proto` file whose structure looks like `model.proto` in the same folder. Below is an example for DataID 61. If the dataset does not have a feature named `class` or the name `class` is not unique in the data attribute list, this tool will consider this dataset does not have a label column. Therefore, all feature names are listed out in `message Feature`.

```
syntax = "proto3";

option java_outer_classname = "Data61Proto";
option objc_class_prefix = "KC";

service Data { 
	rpc PullData(Empty) returns (Response);
}

message Empty {
}

message Response {
	string label = 1;
	Feature feature = 2;
}

message Feature {
	float64  Sepallength                    = 1;
	float64  Sepalwidth                     = 2;
	float64  Petallength                    = 3;
	float64  Petalwidth                     = 4;
}
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
# 3. Edit output file content
In file `utils.py`, line 23 to 35 are the content written in `.proto` file.
If you want to modify, please do it here. You can also modify the `objc_class_prefix` in the 4 first lines.

<br/> If you have any issue or trouble, please contact `htran@know-center.at.`
