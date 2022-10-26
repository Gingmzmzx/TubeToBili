import pathlib, os
def makeSurePathExists(pathToFile):
    pathlib.Path(pathToFile).mkdir(parents=True, exist_ok=True)

def path(pathToFile=None):
    if not pathToFile:
        return pathlib.Path().cwd()
    return os.path.join(pathlib.Path().cwd(), pathToFile)