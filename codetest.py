from __init__ import db_, cursor, os


account = 'asd'
if not os.path.isdir("Vip_Ram_Folder"):
    os.mkdir("Vip_Ram_Folder")
os.mkdir(f'./Vip_Ram_Folder/{account}')