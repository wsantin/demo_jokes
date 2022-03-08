import argparse

import os
import uuid
from datetime import datetime, timedelta
from os.path import join, dirname
from dotenv import load_dotenv

import sys

path_principal = "\\".join(str(sys.path[0]).split("\\")[:-2])
sys.path.insert(0, path_principal)

print("[+]path_principal: ",path_principal)
from app.api import app
from app.configs.environment import Config

from app.services.cognito.cognito_service import CognitoService

# #Inicialize Config
dotenv_path = join('.env')
load_dotenv(dotenv_path)

#Añadir usuarios por argumentos
parser = argparse.ArgumentParser(description='Registro de usuarios')
parser.add_argument('--user', '-u', help='Celular', required=True)
parser.add_argument('--password', '-p', help='Password Temporal', required=True)
parser.add_argument('--names', '-n', help='Nombres completos', required=True)
parser.add_argument('--dni', '-d', help='Document de Dni', required=True)
parser.add_argument('--email', '-e', help='Correo electronico')
parser.add_argument('--bunisse', '-b', help='id Empresa')
args = parser.parse_args()

user = {
  "username": args.user, 
  "password": args.password,
  "name": args.names,
  "phone": args.user, 
  "email": args.email,
  "custom:document": args.dni,
  "custom:bunisse_id": "7af5d995-b281-43ee-8db7-54a2ca627be0" if not args.bunisse else args.bunisse
}

print("[+]Usuario: ",user)
print("[+]Creando usuario[+]")

cognito_service = CognitoService(Config)
create_user = cognito_service.create_user_cognito_admin(user)
print("[+]create_user: ",create_user)

# # # Guardar ID Log
# archivo = open("models/scripts/create_cognito_user/log_dev.txt", 'a')
# print("create_user_agro1: ",create_user_agro1['User']['Attributes'][0]['Value'])
# print("create_user_agro2: ",create_user_agro2['User']['Attributes'][0]['Value'])
# print("create_user_agro3: ",create_user_agro3['User']['Attributes'][0]['Value'])
# print("create_user_agro4: ",create_user_agro4['User']['Attributes'][0]['Value'])
# print("create_user_agro5: ",create_user_agro5['User']['Attributes'][0]['Value'])
# print("create_user_agro6: ",create_user_agro6['User']['Attributes'][0]['Value'])
# print("create_user_agro7: ",create_user_agro7['User']['Attributes'][0]['Value'])
# print("create_user_agro8: ",create_user_agro8['User']['Attributes'][0]['Value'])

# archivo.write('wsantin: '+create_user_agro1['User']['Attributes'][0]['Value']);archivo.write('\n')
# archivo.write('achorres: '+create_user_agro2['User']['Attributes'][0]['Value']);archivo.write('\n')
# archivo.write('kguerrero: '+create_user_agro3['User']['Attributes'][0]['Value']);archivo.write('\n')
# archivo.write('jpuicon: '+create_user_agro4['User']['Attributes'][0]['Value']);archivo.write('\n')
# archivo.write('cristian: '+create_user_agro5['User']['Attributes'][0]['Value']);archivo.write('\n')
# archivo.write('demoagros: '+create_user_agro6['User']['Attributes'][0]['Value']);archivo.write('\n')
# archivo.write('agroperu1: '+create_user_agro7['User']['Attributes'][0]['Value']);archivo.write('\n')
# archivo.write('apromalpi1: '+create_user_agro8['User']['Attributes'][0]['Value']);archivo.write('\n')
