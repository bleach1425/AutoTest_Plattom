import os

upper_path = os.path.abspath(os.path.join(os.getcwd(), ".."))


# # ( ---------------------------------------- ) #
"""Plattom"""
os.system('start python app.py')
# # ( ---------------------------------------- ) #

# # ( ---------------------------------------- ) #
"""Blog"""
path = os.path.join(upper_path, "Blog")
os.chdir(path)
print("Blog: ", os.getcwd())
os.system('start python manage.py runserver localhost:8000')
# # ( ---------------------------------------- ) #


# ( ---------------------------------------- ) #
"""Dashbord"""
os.chdir("D:\dashboard_try")
os.system('start python main.py')
# ( ---------------------------------------- ) #


# ( ---------------------------------------- ) #
"""Fastapi"""
path = os.path.join(upper_path, "Fastapi")
os.chdir(path)
# os.chdir(r"C:/Users\EF-QA-11\PycharmProjects\Fasterapi")
os.system('start python app.py')
# # ( ---------------------------------------- ) #


