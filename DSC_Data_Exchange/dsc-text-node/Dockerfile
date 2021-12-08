FROM maven:3-jdk-11 As dataspace-connector
WORKDIR /app
RUN curl -LO https://github.com/International-Data-Spaces-Association/DataspaceConnector/archive/refs/tags/v6.5.0.zip
RUN unzip v6.5.0.zip
WORKDIR /app/DataspaceConnector-6.5.0
RUN mvn -e -B dependency:resolve
RUN mvn -e -B dependency:resolve-plugins
RUN mvn -e -B clean package -DskipTests

FROM openjdk:11
WORKDIR /app
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY model.proto /app/model.proto
RUN python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. model.proto

COPY src /app/src/
COPY static /app/static/
COPY templates /app/templates/
COPY app.py /app/app.py
COPY run.sh /app/run.sh
COPY --from=dataspace-connector /app/DataspaceConnector-6.5.0/target/*.jar /app/dataspaceconnector.jar

RUN useradd app
USER app
ENTRYPOINT ["/app/run.sh"]