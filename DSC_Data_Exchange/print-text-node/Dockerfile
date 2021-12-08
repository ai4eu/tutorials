FROM python:3.9
WORKDIR app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY model.proto /app/model.proto
RUN python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. model.proto

COPY src /app/src/
COPY main.py /app/main.py

ENTRYPOINT ["python3", "-u", "main.py"]