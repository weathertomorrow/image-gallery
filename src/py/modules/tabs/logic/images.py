from json import dumps, loads

from src.py.config import TabConfig, SortOrder, SortBy
from src.py.modules.shared.files import getImageFullPath, ImagesInDir
from src.py.modules.shared.mutable import updateImagesInDirRef, MUTABLE_ImagesInDirRef
from src.py.modules.shared.sort import sortImages

from src.py.modules.tabs.logic.types import GetImages

def shouldSort(state: MUTABLE_ImagesInDirRef, sortOrder: SortOrder, sortBy: SortBy) -> bool:
  return state["prevSortBy"] != sortBy or state["prevSortOrder"] != sortOrder

def getImagesPerPage(tabConfig: TabConfig) -> int:
  return tabConfig["runtimeConfig"]["pageRows"] * tabConfig["runtimeConfig"]["pageColumns"]

def getPage(tabConfig: TabConfig, pageIndex: int, imagesInDir: ImagesInDir):
  perPage = getImagesPerPage(tabConfig)
  pageStartingIndex = pageIndex * perPage

  return list(map(lambda file: getImageFullPath(tabConfig["staticConfig"], file.path), imagesInDir[pageStartingIndex:pageStartingIndex + perPage]))

def makeGetImages(tabConfig: TabConfig, imagesInDir: MUTABLE_ImagesInDirRef) -> GetImages:
  def getImages(pageIndex: float, sortOrder: SortOrder, sortBy: SortBy) -> list[str]:
    updateImagesInDirRef(imagesInDir, (
        sortImages(imagesInDir["images"], sortOrder, sortBy)
      if
        shouldSort(imagesInDir, sortOrder, sortBy)
      else
        imagesInDir["images"]
    ), sortOrder, sortBy)

    return getPage(tabConfig, int(pageIndex), imagesInDir["images"])
  return getImages


def imagesIntoData(images: list[str]) -> str:
  return dumps([ {"image": image} for image in images ])

def dataIntoImags(data: str) -> list[str]:
  images = loads(data)
  return [image["image"] for image in images]
