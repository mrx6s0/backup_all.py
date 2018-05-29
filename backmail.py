#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

fromaddress = "" # endereço de origem
toaddress = "" # mudar para mandar para a pessoa desejada

msg = MIMEMultipart()

msg['de'] = fromaddress 
msg['para'] = toaddress
msg['assunto'] = "."

body = " . "

msg.attach(MIMEText(body, 'plain'))

filename = "nome-do-teu-arquivo"
attachment = open("arquivo-que-voce-quer-com-extensão-qualquer-", "rb")

part = MIMEBase('application', 'octet-stream') 
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename= %s' % filename)

msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddress, "minhasenha")
text = msg.as_string()
server.sendmail(fromaddress, toaddress, text)
print '\nfeito\narquivo enviado'
server.quit()
