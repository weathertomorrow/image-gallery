from typing import Union, TypedDict

from src.py.config import StaticConfig, TabConfig, SortBy, SortOrder
from src.py.modules.shared.sort import getSortParam, sortImages
from src.py.modules.shared.files import ImagesInDir, getImagesInDir
from src.py.modules.shared.names import getImageNameFromThumbnailName

Thumbnails = dict[str, str]

class MUTABLE_ImagesInDirRefBase(TypedDict):
  images: ImagesInDir
  prevSortBy: Union[SortBy, None]
  prevSortOrder: Union[SortOrder, None]


class MUTABLE_ImagesInDirRef(MUTABLE_ImagesInDirRefBase):
  thumbnails: Thumbnails

def getImagesInDirRef(tabConfig: TabConfig, dirPath: str) -> MUTABLE_ImagesInDirRefBase:
  staticConfig = tabConfig["staticConfig"]

  sortBy = tabConfig["staticConfig"]["tabDefaults"]["sortBy"]
  sortOrder = tabConfig["staticConfig"]["tabDefaults"]["sortOrder"]

  return {
    "images": sortImages(getImagesInDir(staticConfig, dirPath), sortOrder, sortBy),
    "prevSortBy": sortBy,
    "prevSortOrder": sortOrder,
  }

def getThumbnailsForTab(tabConfig: TabConfig) -> Thumbnails:
  return {
    getImageNameFromThumbnailName(tabConfig, image.name): image.path for image in getImagesInDir(tabConfig["staticConfig"], tabConfig["thumbnailsPath"])
  }

def addThumbnailsToImages(imagesInDir: MUTABLE_ImagesInDirRefBase, tabConfig: TabConfig) -> MUTABLE_ImagesInDirRef :
  staticConfig = tabConfig["staticConfig"]

  if not tabConfig["runtimeConfig"]["useThumbnails"]:
    return {
      **imagesInDir,
      "thumbnails": {}
    }

  return {
    **imagesInDir,
    "thumbnails": getThumbnailsForTab(tabConfig)
  }

def updateImagesInDirRef(prev: MUTABLE_ImagesInDirRef, images: ImagesInDir, thumbnails: Thumbnails, sortOrder: SortOrder, sortBy: SortBy) -> None:
  prev["images"] = images
  prev["prevSortBy"] = sortBy
  prev["prevSortOrder"] = sortOrder
  prev["thumbnails"] = thumbnails

def makeWithRefreshFiles(ref: MUTABLE_ImagesInDirRef, tabConfig: TabConfig):
  staticConfig = tabConfig["staticConfig"]
  # don't think there is a way of typing this in python
  # only works for specific functions (they need to accept sortOder and sortBy values from radio inputs as initial arguments)
  def withRefresh(fn):
    def wrapped(*args, **kwargs):
      (sortOrder, sortBy) = getSortParam(args[0], args[1])
      updateImagesInDirRef(
        ref,
        sortImages(getImagesInDir(staticConfig, tabConfig["path"]), sortOrder, sortBy),
        getThumbnailsForTab(tabConfig) if tabConfig["runtimeConfig"]["useThumbnails"] else {},
        sortOrder,
        sortBy
      )

      output = fn(*args, **kwargs)

      return output
    return wrapped
  return withRefresh
