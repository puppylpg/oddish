import os, sys

f = open("oddish.py", "w")
f.write("import src")
f.close()

os.system("pyinstaller --noconfirm --icon=oddish.ico --clean -w -D oddish.py")

os.remove("oddish.py")
