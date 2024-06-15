import subprocess
import os


command = ['git', 'clone', '--depth', '1', 'http://github.com/brendangregg/FlameGraph']
subprocess.run(command)
project_flgr = os.path.abspath('FlameGraph')

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

#
tests_dir = build_dev_dir + '/tests'
tests_execut = []

for filename in os.listdir(tests_dir):
    filepath = os.path.join(tests_dir, filename)
    if filename.startswith('test') and os.access(filepath, os.X_OK):
        tests_execut.append(filepath)

print(tests_execut)

for test in tests_execut:
    profile_path = os.path.join(tests_dir, 'profile', os.path.basename(test))
    record_data = os.path.join(profile_path, 'perf.data')
    os.makedirs(profile_path, exist_ok=True)
    record = 'perf record -F 999 -a -g -o ' + record_data + ' -- ' + test
    print(record)
    subprocess.run(record, shell=True)

    #perf script | ./stackcollapse-perf.pl > out.perf
    script_data = os.path.join(profile_path, 'out.perf')
    script = 'perf script -i ' + record_data + ' | ' + os.path.join(project_flgr, 'stackcollapse-perf.pl') +' > '+ script_data
    subprocess.run(script, shell=True)

    #./flamegraph.pl out.perf > flamegraph.svg
    svg_data = os.path.join(profile_path, 'flamegraph.svg')
    svg = os.path.join(project_flgr, 'flamegraph.pl') + ' ' + script_data + ' > ' + svg_data
    subprocess.run(svg, shell=True)





# Запустите CMake для сборки проекта
#subprocess.run(['cmake', '--build', '.'])



