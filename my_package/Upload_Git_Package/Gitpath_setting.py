import os

def Gitpath(*args):
    main_path = os.getcwd()
    os.chdir(f'TestCase_ver1.0/{args[0]}')
    os.system("git pull")
    os.chdir(main_path)
    return "Setting OK"