#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import argparse
import os
import csv
import subprocess
import datetime
from pydriller import RepositoryMining

dt_since = datetime.datetime(2020, 9, 10, 18, 0, 0)
dt_to    = datetime.datetime(2021, 1, 12, 18, 0, 0)
# RepositoryMining('path/to/the/repo', since=dt1, to=dt2).traverse_commits()
# RepositoryMining('path/to/the/repo', only_in_branch='branch1', only_no_merge=True).traverse_commits()
dir_list = []
output = []

def format_to_arrary(path, hash, msg, email, date, insert, delete):
    UTC_FORMAT = "%Y-%m-%d"
    MSG_FORMAT = "\"" + msg.split("\n")[0].replace("\"", " ") + "\""
    line = '{}, {}, {}, {}, {}, {}, {} \n'.format(
        path,
        hash,
        MSG_FORMAT,
        email,
        date.strftime(UTC_FORMAT),
        insert,
        delete
    )
    return line

def get_repository_info():
    for commit in RepositoryMining("~/code/other/selfblog", only_no_merge=True).traverse_commits():
        print(commit.msg)
        #print(commit.hash)
        print(commit.author.email)
        print(commit.author.name)
        print(commit.project_name)


def get_repository_info2(path):
    for commit in RepositoryMining(path, since=dt_since, to=dt_to, only_no_merge=True).traverse_commits():
        #print('project path: {} msg: {} hash: {} email: {} inserts: {} deletes: {} date: {}'.format(commit.project_name, commit.msg, commit.hash, commit.author.email, commit.insertions, commit.deletions, commit.committer_date))
        line = format_to_arrary( commit.project_name, commit.hash, commit.msg, commit.author.email, commit.committer_date, commit.insertions, commit.deletions )
        output.append(line)



def go_git_dirs(startdir):
    for dirpath, dirnames, _ in os.walk(startdir):
        if set(['info', 'objects', 'refs']).issubset(set(dirnames)):
            parent_path = os.path.abspath(os.path.join(dirpath, ".."))
            print(parent_path)
            dir_list.append(parent_path)


def go_git_dirs2(startdir):
    for dirpath, dirnames, _ in os.walk(startdir):
        if set(['.git']).issubset(set(dirnames)):
            print(dirpath)
            dir_list.append(dirpath)

def print_git_repository():
    for path in dir_list:
        print(path)

def lookup_git_repository():
    for path in dir_list:
        get_repository_info2(path)

def working_directory(directory):
    saved_cwd = os.getcwd()
    os.chdir(directory)
    yield
    os.chdir(saved_cwd)


def git_dirs_check(path):
    for git_directory in go_git_dirs(path):
        with working_directory(git_directory):
            print('\n{}:'.format(os.getcwd()))
            ret = subprocess.call(['git', 'fsck'])
            if ret != 0:
                print((Fore.RED + 'git fsck is unhappy with {}' + Fore.RESET)
                  .format(git_directory))

def write_to_csv(output):
    FIELDS_HEADER = ["project", "commitId", "subject", "email", "commiteDate", "insertions", "deletions"]
    file = open("openharmony.csv", 'w')
    file.write(str(FIELDS_HEADER).strip('[]') + "\n")
    for line in output:
        print(line)
        file.write(line)

def get_argparse():
    parser = argparse.ArgumentParser(description='Analysis commit message infomation '
                                             'from an existing git repositrys.')
    parser.add_argument('path',
                    help='path to repositorys')
    args = parser.parse_args()
    return args.path

def main():
    """main func entry"""
    root_path = get_argparse()
    print(root_path)
    go_git_dirs2(root_path)
    lookup_git_repository()
    write_to_csv(output)
    #get_repository_info()
    #get_repository_info2()
    #print_git_repository()

if __name__ == '__main__':
    main()
