from typing import List, Callable

from src.py.config import TabConfig
from src.py.files import getImageFullPath, ImagesInDir
from src.py.sort import SortOrder, SortBy, makeSortFiles

def getImagesPerPage(tabConfig: TabConfig) -> int:
  return tabConfig['runtimeConfig']['pageRows'] * tabConfig['runtimeConfig']['pageColumns']

def getPage(tabConfig: TabConfig, pageIndex: int, imagesInDir: ImagesInDir):
  perPage = getImagesPerPage(tabConfig)
  pageStartingIndex = pageIndex * perPage

  return list(map(lambda file: getImageFullPath(tabConfig['staticConfig'], file.path), imagesInDir[pageStartingIndex:pageStartingIndex + perPage]))

GetImages = Callable[[float, SortOrder, SortBy], List[str]]
def makeGetImages(tabConfig: TabConfig, imagesInDir: ImagesInDir) -> GetImages:
  def getImages(pageIndex: float, sortOrder: SortOrder, sortBy: SortBy) -> List[str]:
    return getPage(tabConfig, int(pageIndex), sorted(imagesInDir, reverse = sortOrder != SortOrder.ASC, key = makeSortFiles(sortBy)))

  return getImages

PostProcess = Callable[[List[str]], str]
def imagesIntoData(images: List[str]) -> str:
  return "\n".join(images)
