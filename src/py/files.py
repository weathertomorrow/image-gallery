from os import makedirs, path, DirEntry,  scandir
from typing import Union, List

from src.py.config import StaticConfig

def makeDirIfMissing(dirPath: str):
  try:
    makedirs(dirPath)
  except OSError:
    return None

def getExtension(fileName: str) -> Union[str, None]:
  return path.splitext(fileName)[1]

def isImage(staticConfig: StaticConfig, file: DirEntry[str]) -> bool:
  return file.is_file() and getExtension(file.name) in staticConfig["imageExtensions"]

def getImageFullPath(staticConfig: StaticConfig, filePath: str) -> str:
  return path.join(staticConfig["scriptPath"], filePath)

ImagesInDir = list[DirEntry[str]]
def getImagesInDir(staticConfig: StaticConfig, dirPath: str) -> ImagesInDir:
    with scandir(dirPath) as directory:
      images = []

      for file in directory:
        if isImage(staticConfig, file):
          images.append(file)

      return images
