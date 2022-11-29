from json import dumps, loads
from os import DirEntry

from src.py.config import TabConfig, SortOrder, SortBy
from src.py.modules.shared.files import getImageFullPath
from src.py.modules.shared.mutable import updateImagesInDirRef, MUTABLE_ImagesInDirRef
from src.py.modules.shared.sort import sortImages

from src.py.modules.tabs.logic.types import GetImages, ImageOnPage, ImagesPage

def shouldSort(state: MUTABLE_ImagesInDirRef, sortOrder: SortOrder, sortBy: SortBy) -> bool:
  return state["prevSortBy"] != sortBy or state["prevSortOrder"] != sortOrder

def getImagesPerPage(tabConfig: TabConfig) -> int:
  return tabConfig["runtimeConfig"]["pageRows"] * tabConfig["runtimeConfig"]["pageColumns"]

def makeGetImageOnPage(tabConfig: TabConfig, imagesInDir: MUTABLE_ImagesInDirRef):
  thumbnailsEnabled = tabConfig["runtimeConfig"]["useThumbnails"] and imagesInDir["thumbnails"] is not None
  thumbnails = imagesInDir["thumbnails"] if imagesInDir["thumbnails"] is not None else {}

  def getImageOnPage(image: DirEntry[str]) -> ImageOnPage:

    thumbnailPath = thumbnails[image.name] if thumbnailsEnabled and image.name in thumbnails else None

    return {
      "imagePath": getImageFullPath(tabConfig["staticConfig"], image.path),
      "thumbnailPath": None if thumbnailPath is None else getImageFullPath(tabConfig["staticConfig"], thumbnailPath),
    }
  return getImageOnPage

def getPage(tabConfig: TabConfig, pageIndex: int, imagesInDir: MUTABLE_ImagesInDirRef) -> ImagesPage:
  perPage = getImagesPerPage(tabConfig)
  pageStartingIndex = pageIndex * perPage

  return list(map(
    makeGetImageOnPage(tabConfig, imagesInDir),
    imagesInDir["images"][pageStartingIndex:pageStartingIndex + perPage]
  ))

def makeGetImages(tabConfig: TabConfig, imagesInDir: MUTABLE_ImagesInDirRef) -> GetImages:
  def getImages(pageIndex: float, sortOrder: SortOrder, sortBy: SortBy) -> ImagesPage:
    updateImagesInDirRef(imagesInDir, (
        sortImages(imagesInDir["images"], sortOrder, sortBy)
      if
        shouldSort(imagesInDir, sortOrder, sortBy)
      else
        imagesInDir["images"]
    ), imagesInDir["thumbnails"], sortOrder, sortBy)

    return getPage(tabConfig, int(pageIndex), imagesInDir)
  return getImages


def imagesIntoData(images: ImagesPage) -> str:
  return dumps([ {"image": image["imagePath"], "thumbnail": image["thumbnailPath"] } for image in images ])

def dataIntoImages(data: str) -> ImagesPage:
  entries = loads(data)
  return [{ "imagePath": image["image"], "thumbnailPath": image["thumbnail"] } for image in entries]
