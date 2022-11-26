from os import makedirs

def makeIfMissing(dirPath: str):
  try:
    makedirs(dirPath)
  except OSError:
    return None
