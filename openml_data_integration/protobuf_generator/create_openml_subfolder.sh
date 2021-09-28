#!/bin/bash
# Script to generate the openml_xx subfolder with all files needed
# for an AI4EU-onboardable databroker, which will serve row by row
# all data in an OpenML file.
# By Raul Saavedra, 16.July.2021

# Get dataset ID from the model.proto file
DATASET_ID=`cat model.proto | grep -m 1 "Dataset ID" | awk '{print $5}'`

# Create openml_xx subfolder from the provided template_files subfolder
SUBFOLDER_NAME="openml_$DATASET_ID"
# First remove in case it already exists
rm -rf $SUBFOLDER_NAME
cp -r template_files $SUBFOLDER_NAME

# Enter that new subfolder, copy the model.proto file from the parent
# folder, and generate the needed grpc-related python files from it
cd $SUBFOLDER_NAME
cp ../model.proto .
cp ../license-1.0.0.json .
#echo "Generating python files in current folder using $FILE"
bash ../python_files_from_proto.sh

# Create the server.py file, concatenating the _part1 file, then the
# the variable assignments section extracted from the commented out
# section of the generated model.proto file, then the _part2 file
cat server_part1.py >  server.py
cat model.proto | grep "response." | grep "row\[" >> server.py
cat server_part2.py >> server.py
#rm server_part1.py
#rm server_part2.py

# Set the DATA_ID variable in the myconstants.py file
echo "DATA_ID = $DATASET_ID" > myconstants.py
