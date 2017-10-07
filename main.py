#!/usr/bin/python
# -*- coding: utf-8 -*-

# def code_for_live():

# this thing is very insteresting... 

import os
#import usb
import re
import shutil

# função para encontrar os arquivos
# function to find the files

def find_files(pattern, path):
    for path, dirs, files in os.walk(path):
        for filename in files:
            full_file_name = os.path.join(path, filename)
            match = re.match(pattern, full_file_name)
            if match:
                yield full_file_name

# função para copiar os arquivos encontrados
# function to copy match files
 
def copy_files(pattern, src_path, dest_path):    
    for full_file_name in find_files(pattern, src_path):
        print(full_file_name) + ' file copied\n'
        try:
            shutil.copy(full_file_name, dest_path)
            #shutil.make_archive(full_file_name, 'zip', dest_path)
        except IOError:
            pass

if __name__ == '__main__':

# configuração dos arquivos encontrados, para o redirecionamento para a pasta desejada
# tanto em linux quanto em windows...
# aprimorarei para iOS e android!
    
    import yaml
    import getpass
    from pprint import pprint
    from jinja2 import Template
    
    backup_config = """
    Storages:
        - &Storage1 '/home/{{UserName}}/teste'
        - &Storage2 '/home/{{UserName}}' 
        - &Storage3 'F:\\MYLINUXLIVE\\{{UserName}}'
        - &Storage4 'G:\\MYLINUXLIVE\\{{UserName}}'
        - &Storage5 'H:\\MYLINUXLIVE\\{{UserName}}'
        - &Storage6 'C:\\Users'
    FileSets:
        - &LinuxSet
          - ['/', '.']
          - ['/home', '.']
        - &WindowsSet
          - ['C:', '.']
          - ['D:', '.']
          - ['E:', '.']
    Jobs:
        - FileSet: *LinuxSet
          Storage: *Storage1
        - FileSet: *LinuxSet
          Storage: *Storage2
        - FileSet: *WindowsSet
          Storage: *Storage3
        - FileSet: *WindowsSet
          Storage: *Storage4
        - FileSet: *WindowsSet
          Storage: *Storage4
        - FileSet: *WindowsSet
          Storage: *Storage6
    """

    t = Template(backup_config)
    config = yaml.load(t.render(UserName=getpass.getuser())) # ye.
    print(pprint(config))

    for job in config['Jobs']:
        for fileset in job['FileSet']:
            print("copy_files('{}', '{}', '{}')".format(fileset[1], fileset[0], job['Storage']))
            copy_files(fileset[1], fileset[0], job['Storage'])
    
    #send_to_email(fromaddress, toaddress, attachment)
# copia para a unidade USB indicada, # ou para alguma pasta 
# do a copy to a USB drive given, or some path
