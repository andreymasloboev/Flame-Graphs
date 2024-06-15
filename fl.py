import subprocess
import os


command = ['git', 'clone', '--depth', '1', 'http://github.com/brendangregg/FlameGraph']
subprocess.run(command)

project_dir = os.getcwd()
print(f"Directory of project: {project_dir}")

build_dev_dir = os.getcwd() +'/build_develop'
print(f"Build directory for develop: {build_dev_dir}")
os.makedirs(build_dev_dir, exist_ok=True)

build_br_dir = os.getcwd() +'/build_branch'
print(f"Build directory for branch: {build_br_dir}")
os.makedirs(build_br_dir, exist_ok=True)

flags = "-g -fno-omit-frame-pointer"

#build develop
subprocess.run(['cmake', '-S', project_dir, '-B', build_dev_dir, '-DCMAKE_C_FLAGS=' + flags, '-DCMAKE_CXX_FLAGS=' + flags])
subprocess.run(['cmake', '--build', build_dev_dir])



# Запустите CMake для сборки проекта
#subprocess.run(['cmake', '--build', '.'])



