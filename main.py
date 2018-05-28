#!/usr/bin/python
# -*- coding: utf-8 -*-

# Execute o código sem previlégios de root; pois o username que será detectado, e então, a cópia poder ser realizada, caso contrário o código pegará # o hostname, ou seja, /media/root/PENDRIVE; o que acarretará em erro, já que o caminho para a pasta é dada por /media/USERNAME/PENDRIVE 

# Aprimorado na próxima versão 

import os
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
        print(full_file_name) + ' file copied into ' + (dest_path)
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
        - &Storage1 '/media/{{UserName}}/ANDROID/' 
        - &Storage2 '/media/{{UserName}}' 
        - &Storage3 'F:\\ANDROID\\{{UserName}}'
        - &Storage4 'G:\\ANDROID\\{{UserName}}'
        - &Storage5 'H:\\ANDROID\\{{UserName}}'
        - &Storage6 'C:\\Users'
    FileSets:
        - &LinuxSet
          - ['/home/{{UserName}}/Downloads', '.']
          - ['/home{{UserName}}', '.']
        - &WindowsSet
          - ['C:\\', '.']
          - ['D:\\', '.']
          - ['E:\\', '.']
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
# em &Storage1 define-se a pasta/pen drive para qual os arquivos serão copiados. No meu caso, o nome do pendrive está como ANDROID. E defini a pasta de downloads para fazer a cópia. ( - ['/home/{{UserName}}/Downloads', '.']) 

# assim como &Storage2, 3, 4... 

# em FileSets são as pastas em que estão os arquivos a serem copiados, neste caso /home/user/Downloads 

    t = Template(backup_config)
    config = yaml.load(t.render(UserName=getpass.getuser())) # ye. this gets the username of pc, then access automatically the path. 

    print(pprint(config))

    for job in config['Jobs']:
        for fileset in job['FileSet']:
            print("copy_files('{}', '{}', '{}')".format(fileset[1], fileset[0], job['Storage']))
            copy_files(fileset[1], fileset[0], job['Storage'])

# copia para a unidade USB indicada, ou para alguma pasta 

# do a copy to a USB drive given, or some path
