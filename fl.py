import subprocess
import os
import argparse

parser = argparse.ArgumentParser(description='FlameGraph diff.')
parser.add_argument('br', type=str, help='Branch for diff')
args = parser.parse_args()
diff_br = args.br

print(f"Branch for diff: {diff_br}")

command = ['git', 'clone', '--depth', '1', 'http://github.com/brendangregg/FlameGraph']
subprocess.run(command)
project_flgr = os.path.abspath('FlameGraph')

project_dir = os.getcwd()
print(f"Directory of project: {project_dir}")

def switchGitBranch(branch_name):
    try:
        subprocess.run(['git', 'checkout', branch_name], check=True)
        print(f"Success switch to branch: {branch_name}")
    except subprocess.CalledProcessError as e:
        print(f"Fail switch to branch: {e}")

def buildGraph(build_dir):
    flags = "-g -fno-omit-frame-pointer"

    subprocess.run(['cmake', '-S', project_dir, '-B', build_dir, '-DCMAKE_C_FLAGS=' + flags, '-DCMAKE_CXX_FLAGS=' + flags])
    subprocess.run(['cmake', '--build', build_dir])

    tests_dir = build_dir + '/tests'
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

        #perf script | ./stackcollapse-perf.pl > out.folded
        script_data = os.path.join(profile_path, 'out.folded')
        script = 'perf script -i ' + record_data + ' | ' + os.path.join(project_flgr, 'stackcollapse-perf.pl') +' > '+ script_data
        subprocess.run(script, shell=True)

        #./flamegraph.pl out.perf > flamegraph.svg
        svg_data = os.path.join(profile_path, 'flamegraph.svg')
        svg = os.path.join(project_flgr, 'flamegraph.pl') + ' ' + script_data + ' > ' + svg_data
        subprocess.run(svg, shell=True)

def buildDiffGraph(build_dir, build_br_dir):

    tests_dir = build_dir + '/tests'
    tests_execut = []

    for filename in os.listdir(tests_dir):
        filepath = os.path.join(tests_dir, filename)
        if filename.startswith('test') and os.access(filepath, os.X_OK):
            tests_execut.append(filepath)

    print(tests_execut)

    for test in tests_execut:
        profile_diff = os.path.join(tests_dir, 'profile_diff', os.path.basename(test))
        os.makedirs(profile_diff, exist_ok=True)
        profile_diff=os.path.join(profile_diff, 'diff2.svg')
        develop_data=os.path.join(build_dir,'tests','profile', os.path.basename(test), 'out.folded')
        branch_data=os.path.join(build_br_dir,'tests','profile', os.path.basename(test), 'out.folded')
        # ./difffolded.pl out.folded1 out.folded2 | ./flamegraph.pl > diff2.svg
        diff_cmd = os.path.join(project_flgr, 'difffolded.pl') + ' ' + develop_data + ' ' + branch_data + ' | ' + os.path.join(project_flgr, 'flamegraph.pl') + ' > ' + profile_diff
        subprocess.run(diff_cmd, shell=True)
        print(diff_cmd)

build_dev_dir = os.getcwd() +'/build_develop'
print(f"Build directory for develop: {build_dev_dir}")
os.makedirs(build_dev_dir, exist_ok=True)

build_br_dir = os.getcwd() +'/build_branch'
print(f"Build directory for branch: {build_br_dir}")
os.makedirs(build_br_dir, exist_ok=True)

se_linux_ruls = "echo -1 | sudo tee /proc/sys/kernel/perf_event_paranoid"
subprocess.run(se_linux_ruls, shell=True)

switchGitBranch('develop')

#build develop
buildGraph(build_dev_dir)

switchGitBranch(diff_br)

#build branch
buildGraph(build_br_dir)

#build diff, we must copmare only test from develop for ignore new tests
buildDiffGraph(build_dev_dir, build_br_dir)



