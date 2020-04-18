import os
path = "../data/wk12/tic/"

files = os.listdir(path)


for file in sorted(files, key=len):
    print(file)