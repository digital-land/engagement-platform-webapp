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
                    css_code = scss.compile(scss_code)

                staticFolderPath = folder.replace("assets", "static")
                cssFilename = filename.replace("scss", "css")

                with open(os.path.join(staticFolderPath, cssFilename), "w") as file:
                    print(os.path.join(staticFolderPath, cssFilename))
                    scss_code = file.write(css_code)


convertScssInFolder("../assets")
