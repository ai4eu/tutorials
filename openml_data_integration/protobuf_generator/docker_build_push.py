# date: 2021.10.28
# author: Han Tran (htran@know-center.at)

from utils import *
import subprocess

def run_build_and_push_docker_images():    
    OpenMLFiles = get_file_Nums_of_interest()
    print(f'# of Datasets of interest: {len(OpenMLFiles)}\n')
    for dataset_id in OpenMLFiles[1:]:        
        dataset_name = oml.datasets.get_dataset(dataset_id).name
        re = subprocess.call(f'./docker_build_push.sh {dataset_name} {dataset_id}',
                        shell=True)
        print(re)


if __name__ == '__main__':
    run_build_and_push_docker_images()
