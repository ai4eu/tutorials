#!/bin/bash
SERVER_DIR="server"
CLIENT_DIR="client"

create_ssl_credentials()
{
    openssl genrsa -out server.key 2048
    openssl req -new -x509 -sha256 -key server.key -out server.crt -days 3650 -subj "/C=DE/CN=localhost"
}

create_ssl_credentials

cp server.key ./$SERVER_DIR 
cp server.crt ./$SERVER_DIR 
cp server.crt ./$CLIENT_DIR
rm server.key server.crt 
