from os import makedirs, path, DirEntry, scandir, remove
from shutil import move, Error
from ntpath import basename
from shutil import rmtree
from typing import Union

from src.py.config import StaticConfig, TabConfig
from src.py.modules.shared.guards import isEmpty

def makeDirIfMissing(dirPath: str):
  try:
    makedirs(dirPath)
  except OSError:
    return None

def removeDirIfExists(dirPath: str):
  try:
    rmtree(dirPath, ignore_errors = True)
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

def imageBelongsToTab(tab: TabConfig, imagePath: str):
  common = path.commonpath([tab["path"], imagePath])
  return not isEmpty(common) and path.samefile(common, tab["path"])

def getFilenameFromPath(path: str):
  return basename(path)

def moveFileAndPreventDuplicates(filePath: str, desination: str):
  try:
    move(filePath, desination)
  except (Error) as e:
    if ("already exists" in e.strerror):
      remove(filePath)
    else:
      raise e
