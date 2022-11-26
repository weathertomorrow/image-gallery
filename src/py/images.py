import os
from typing import List, Iterator, Callable

from src.py.config import TabConfig
from src.py.files import isImage, getImageFullPath

def getImagesPerPage(tabConfig: TabConfig) -> int:
  return tabConfig['runtimeConfig']['page_rows'] * tabConfig['runtimeConfig']['page_columns']

def makeRecurseOverImages(tabConfig: TabConfig, pageIndex: int, perPage: int):
  staticConfig = tabConfig['staticConfig']

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
      getImageFullPath(staticConfig, file.path), *recurseOverImages(iterator, nextPage, remaining - 1)
    ] if isOnRightPage and isImage(staticConfig['imageExtensions'], file) else [
      *recurseOverImages(iterator, nextPage, remaining)
    ]

  return recurseOverImages

GetImages = Callable[[int], List[str]]
def makeGetImages(tabConfig: TabConfig, imagesToGet: int) -> GetImages:
  def getImages(pageIndex: int) -> List[str]:
    with os.scandir(tabConfig['path']) as directory:
      return makeRecurseOverImages(tabConfig, pageIndex, imagesToGet)(directory, 0)

  return getImages
