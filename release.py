#!/usr/bin/env python
import os
import subprocess
import shutil
import fileinput

def create_clean_src_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        shutil.rmtree(path)
        os.makedirs(path)

def bash_cmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print p.communicate()

def find_in_file(file_path, string):
    datafile = file(file_path)
    for line in datafile:
        for line in datafile:
            if string in line:
                return line


def find_and_replace_in_file(file_path, replacements):
    lines = []
    with open(file_path) as infile:
        for line in infile:
            for src, target in replacements.iteritems():
                line = line.replace(src, target)
            lines.append(line)
    with open(file_path, 'w') as outfile:
        for line in lines:
            outfile.write(line)  

# use environment variables for project
# set git user variables
git_user_name = os.environ["git_user_name"]
git_user_email = os.environ["git_user_email"]
#git_ssh_key = os.environ["git_ssh_key"]
#print git_ssh_key
# set project variables
project_name = os.environ["project_name"]
project_owner = os.environ["project_owner"]
project_uri = "git@github.com:" + project_owner + "/" + project_name + ".git"
project_branch = os.environ["project_branch"]


# where the source directory will be created
source_dir = os.environ["source_dir"]

# remove previous src directory if it exists, clone prject and enter directory
create_clean_src_dir(source_dir)
os.chdir(source_dir)
try:
    bash_cmd(['git', 'clone', project_uri])
except:
    print "Source exists"
os.chdir(project_name)

# checkout the specified project branch
bash_cmd(['git', 'checkout', project_branch])
bash_cmd(['git', 'pull'])

# get current build version from version file
file_path = './mycroft/version/__init__.py'
core_vers_major = find_in_file(file_path, 'CORE_VERSION_MAJOR =').rstrip().split(' ')[2]
core_vers_minor = find_in_file(file_path, 'CORE_VERSION_MINOR =').rstrip().split(' ')[2]
core_vers_build = find_in_file(file_path, 'CORE_VERSION_BUILD =').rstrip().split(' ')[2]
core_vers_string =  str(core_vers_major) + "." + str(core_vers_minor) + "." + str(core_vers_build)
print "Current project version is " + core_vers_string

# increment build version string
core_vers_build_now = int(core_vers_build) + 1
core_vers_string_now = str(core_vers_major) + "." + str(core_vers_minor) + "." + str(core_vers_build_now)

# increment current build version in version file
old = 'CORE_VERSION_BUILD = ' + str(core_vers_build)
new = 'CORE_VERSION_BUILD = ' + str(core_vers_build_now)
replacements = {old : new}
file_path = './mycroft/version/__init__.py'
find_and_replace_in_file(file_path, replacements)

# add git credentials for commit
bash_cmd(['git','config', 'user.name', '"' + git_user_name + '"'])
bash_cmd(['git','config', 'user.email', '"' + git_user_email + '"'])

# commit version change
commit_message = "Version bump from " + str(core_vers_string) + " to " + str(core_vers_string_now)
print commit_message

# add version file to git
bash_cmd(['git', 'add', 'mycroft/version/__init__.py'])
# make a commit with the version bump commit message
bash_cmd(['git', 'commit', '-m', commit_message])
# push changes to branch
bash_cmd(['git','push'])

# create a release tag from the latest version
bash_cmd(['git', 'tag', '-f', 'release/v'+ core_vers_string_now ])
# push tags
bash_cmd(['git', 'push', '--force', '--tags'])

## update master branch from dev branch
bash_cmd(['git', 'checkout', 'master'])
bash_cmd(['git', 'pull'])
bash_cmd([
    'git', 'merge', '--ff', '-m',
    'Update to v' + core_vers_string_now,
    'release/v' + core_vers_string_now
])
bash_cmd(['git', 'push'])


# clean up source directory
create_clean_src_dir(source_dir)
