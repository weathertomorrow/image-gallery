from os import makedirs, path, DirEntry
from typing import Union, List

from src.py.config import StaticConfig

def makeDirIfMissing(dirPath: str):
  try:
    makedirs(dirPath)
  except OSError:
    return None

def getExtension(fileName: str) -> Union[str, None]:
  return path.splitext(fileName)[1]

def isImage(imageFileExtensions: List[str], file: DirEntry[str]) -> bool:
  return file.is_file() and getExtension(file.name) in imageFileExtensions

def getImageFullPath(staticConfig: StaticConfig, filePath: str) -> str:
  return path.join(staticConfig["scriptPath"], filePath)
