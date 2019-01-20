# A way to list all file paths for a given directory.
# https://stackoverflow.com/questions/2186525/use-a-glob-to-find-files-recursively-in-python
import glob
def make_glob(path, filetype):
    print(glob.glob(path+"/**/*."+filetype, recursive=True))
