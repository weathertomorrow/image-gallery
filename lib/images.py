import os
from typing import List, Union, Iterator, Callable

from lib.config import TabConfig

def getImagesPerPage(tabConfig: TabConfig) -> int:
  return tabConfig['runtimeConfig']['page_rows'] * tabConfig['runtimeConfig']['page_columns']

def getExtension(fileName: str) -> Union[str, None]:
  return os.path.splitext(fileName)[1]

def isImage(imageFileExtensions: List[str], file: os.DirEntry[str]) -> bool:
  return file.is_file() and getExtension(file.name) in imageFileExtensions

def getImageFullPath(config: TabConfig, path: str) -> str:
  return f'<img src="file={os.path.join(config["staticConfig"]["script_path"], path)}" />'

def makeRecurseOverImages(tabConfig: TabConfig, pageIndex: int, perPage: int):
  def recurseOverImages(iterator: Iterator[os.DirEntry[str]], currentIndex: int, remaining: int = perPage) -> List[str]:
    if remaining == 0:
      return []

    try:
      file = next(iterator)
    except StopIteration:
      return []

    isOnRightPage = currentIndex >= pageIndex * perPage
    nextPage = currentIndex + 1

    return [
      getImageFullPath(tabConfig, file.path), *recurseOverImages(iterator, nextPage, remaining - 1)
    ] if isOnRightPage and isImage(tabConfig['staticConfig']['imageExtensions'], file) else [
      *recurseOverImages(iterator, nextPage, remaining)
    ]

  return recurseOverImages

GetImages = Callable[[int], List[str]]
def makeGetImages(tabConfig: TabConfig, imagesToGet: int) -> GetImages:
  def getImages(pageIndex: int) -> List[str]:
    with os.scandir(tabConfig['path']) as directory:
      return makeRecurseOverImages(tabConfig, pageIndex, imagesToGet)(directory, 0)

  return getImages
