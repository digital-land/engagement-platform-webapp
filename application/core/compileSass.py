import sys
import os
from scss import Scss

scss = Scss()


def convertScssInFolder(folder):
    print(folder)
    for filename in os.listdir(folder):
        print(filename)
        if os.path.isdir(os.path.join(folder, filename)):
            print("folder")
            convertScssInFolder(os.path.join(folder, filename))
        else:
            print("file")
            if filename.endswith(".scss"):
                print("scss")
                with open(os.path.join(folder, filename), "r") as file:
                    scss_code = file.read()
                    try:
                        css_code = scss.compile(scss_code)
                    except Exception as e:
                        print(f"Failed to compile: {filename} with error: {e}")
                        raise e

                staticFolderPath = folder.replace("assets", "static")
                cssFilename = filename.replace("scss", "css")

                with open(os.path.join(staticFolderPath, cssFilename), "w") as file:
                    print(os.path.join(staticFolderPath, cssFilename))
                    scss_code = file.write(css_code)


convertScssInFolder(sys.argv[1])
