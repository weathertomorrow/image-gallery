from typing import Union, TypedDict

from src.py.config import TabConfig, SortBy, SortOrder
from src.py.modules.shared.sort import getSortParam, sortImages
from src.py.modules.shared.files import ImagesInDir, getImagesInDir, forceRemove
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
  if not tabConfig["runtimeConfig"]["useThumbnails"]:
    return {
      **imagesInDir,
      "thumbnails": {}
    }

  return {
    **imagesInDir,
    "thumbnails": getThumbnailsForTab(tabConfig)
  }

def updateImagesInDirRef(prev: MUTABLE_ImagesInDirRef, images: ImagesInDir, thumbnails: Thumbnails, sortOrder:  SortOrder, sortBy: SortBy) -> MUTABLE_ImagesInDirRef:
  prev["images"] = images
  prev["prevSortBy"] = sortBy
  prev["prevSortOrder"] = sortOrder
  prev["thumbnails"] = thumbnails

  return prev

def removeFilesOverLimit(ref: MUTABLE_ImagesInDirRef, tabConfig: TabConfig) -> MUTABLE_ImagesInDirRef:
  limit = tabConfig["maxSize"]

  if limit is None or limit < 0:
    return ref

  sortedImages = sortImages(ref["images"], SortOrder.DESC, SortBy.DATE)
  imagesToRemove = sortedImages[limit:]

  for image in imagesToRemove:
    thumbnail = (
      ref["thumbnails"][image.name]
        if
      tabConfig["runtimeConfig"]["useThumbnails"] and image.name in ref["thumbnails"]
        else
      None
    )

    forceRemove(image.path)

    if thumbnail is not None:
      forceRemove(thumbnail)
      ref["thumbnails"].pop(image.name)

  return updateImagesInDirRef(
    ref,
    [image for image in ref["images"] if image not in imagesToRemove],
    ref["thumbnails"],
    ref["prevSortOrder"] or tabConfig["staticConfig"]["tabDefaults"]["sortOrder"],
    ref["prevSortBy"] or tabConfig["staticConfig"]["tabDefaults"]["sortBy"]
  )


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
      removeFilesOverLimit(ref, tabConfig)

      return fn(*args, **kwargs)
    return wrapped
  return withRefresh
