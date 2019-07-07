# A way to list all file paths for a given directory.
# https://stackoverflow.com/questions/2186525/use-a-glob-to-find-files-recursively-in-python
# In order to work with the recursive paramater, glob must be run under python3
#!/home/f/fi/fin/public_html/flasky/venv_3/bin/python3
import glob
import sys
def make_glob(path, filetype):
    return(glob.glob(path+"/**/*."+filetype, recursive=True))

if __name__ == '__main__':
    print(make_glob(sys.argv[1], sys.argv[2]))
