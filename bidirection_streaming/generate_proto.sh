#!/bin/sh
#This scripts pretty much reduces your effort in creating a gRPC service
echo "Enter gRPC proto filename"
read filename
PROTO=$filename
PROTO_DIR=protobufs
#Fixed template 
SERVER_DIR="server"
CLIENT_DIR="client"
CLIENT_NAME=client.py
SERVER_NAME=server.py
PROTOFILE=$PROTO.proto

generate_grpc_server()
{   
    python3 -m grpc_tools.protoc -I ./$PROTO_DIR  --python_out=./$SERVER_DIR  --grpc_python_out=./$SERVER_DIR  ./$PROTO_DIR/$PROTOFILE
    
}

generate_grpc_client()
{   
    python3 -m grpc_tools.protoc -I ./$PROTO_DIR --python_out=./$CLIENT_DIR --grpc_python_out=./$CLIENT_DIR  ./$PROTO_DIR/$PROTOFILE

}

create_server_dir()
{
    if [ -d "$SERVER_DIR" ]; 
    then
        mkdir -p $SERVER_DIR
        generate_grpc_server 
        echo "generated boilerplate files in server"
    else
        rm -Rf $SERVER_DIR/;
        mkdir -p $SERVER_DIR
        generate_grpc_server
        echo "generated boilerplate files in server"
    fi
}

create_client_dir()
{
    if [ -d "$CLIENT_DIR" ]; 
    then
        mkdir -p $CLIENT_DIR
        generate_grpc_client
        echo "generated boilerplate files in client"
    else
        rm -Rf $CLIENT_DIR/;
        mkdir -p $CLIENT_DIR
        generate_grpc_client
        echo "generated boilerplate files in client"
    fi
}

create_server_file()
{   
    cd $SERVER_DIR
    if test -f "$SERVER"; 
    then
        echo "$SERVER exists."
    else
        touch server.py
        echo "$SERVER created."
    fi
    cd ..
}

create_client_file()
{
    cd $CLIENT_DIR
    if test -f "$CLIENT"; 
    then
        echo "$CLIENT exists."
    else
        touch client.py
        echo "$CLIENT created."
    fi
    cd ..
}


create_server_dir
create_server_file
create_client_dir
create_client_file









