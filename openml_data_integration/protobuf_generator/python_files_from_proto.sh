#!/bin/bash

#if [ "$1" != "" ]
#then
#   FILE="$1.proto"
#else
#   FILE="model.proto"
#fi
#echo "Generating python files in current folder using $FILE"

# Generate the python files from the indicated protobuf file
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. model.proto

