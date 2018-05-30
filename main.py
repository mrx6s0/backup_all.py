#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import smtplib

import os
import re
import shutil

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

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
        - &Storage1 '/home/{{UserName}}/Documentos/teste.zip' 
        - &Storage2 '/media/{{UserName}}' 
        - &Storage3 'F:\\ANDROID\\{{UserName}}'
        - &Storage4 'G:\\ANDROID\\{{UserName}}'
        - &Storage5 'H:\\ANDROID\\{{UserName}}'
        - &Storage6 'C:\\Users'
    FileSets:
        - &LinuxSet
          - ['/home/{{UserName}}/Imagens', '.']
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
            
            pass

# copia para a unidade USB indicada, ou para alguma pasta 

# do a copy to a USB drive given, or some path

fromaddress = "email0@gmail.com" # endereço de origem
toaddress = "email1@gmail.com" # mudar para mandar para a pessoa desejada

msg = MIMEMultipart()

msg['de'] = fromaddress 
msg['para'] = toaddress
msg['assunto'] = "Teste_0"

body = " Teste"

msg.attach(MIMEText(body, 'plain'))

filename = "teste.zip"
attachment = open("teste.zip", "rb")

part = MIMEBase('application', 'octet-stream') 
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename= %s' % filename)

msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddress, "suasenha")
text = msg.as_string()
server.sendmail(fromaddress, toaddress, text)
print '\nFeito!\nArquivo enviado\n'
server.quit()
