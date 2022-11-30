from os import makedirs, path, DirEntry, scandir, remove, utime
from datetime import datetime
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

SiblingImage = Union[None, DirEntry[str]]
def getSiblingImages(image: str, dir: list[DirEntry[str]]) -> tuple[SiblingImage, SiblingImage]:
  maxIndex = len(dir) - 1

  for (index, dirEntry) in enumerate(dir):
    if path.samefile(image, dirEntry.path):
      prevImage = None
      nextImage = None

      prevIndex = index - 1
      nextIndex = index + 1

      if prevIndex >= 0:
        prevImage = dir[prevIndex]

      if nextIndex <= maxIndex:
        nextImage = dir[nextIndex]

      return (prevImage, nextImage)
  return (None, None)

def moveFileAndPreventDuplicates(filePath: str, desination: str, updateTimes = False):
  try:
    move(filePath, desination)
  except (Error) as e:
    # ignore, probably was moved manually
    if ("already exists" in str(e)):
      remove(filePath)
      return
    # ignore, user probably is clicking quickly and initiated move multiple times
    if ("it is being used by another process" in str(e)):
      return
    else:
      raise e

  if (updateTimes):
    now = datetime.now().timestamp()
    utime(path.join(desination, getFilenameFromPath(filePath)), (now, now))
