
cd ./openml_$2
docker build -t openml/$1_$2:v1 .
docker tag openml/$1_$2:v1 cicd.ai4eu-dev.eu:7444/ai4eu-experiments/openml/$1_$2:v1
docker push cicd.ai4eu-dev.eu:7444/ai4eu-experiments/openml/$1_$2:v1
