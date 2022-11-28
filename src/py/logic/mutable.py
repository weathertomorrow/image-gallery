from src.py.config import StaticConfig, TabConfig, SortBy, SortOrder
from src.py.logic.types import MUTABLE_ImagesInDirRef

from src.py.logic.sort import getSortParam, sortImages
from src.py.logic.files import ImagesInDir, getImagesInDir

def getImagesInDirRef(tabConfig: TabConfig, staticConfig: StaticConfig, dirPath: str) -> MUTABLE_ImagesInDirRef:
  sortBy = tabConfig["staticConfig"]["tabDefaults"]["sortBy"]
  sortOrder = tabConfig["staticConfig"]["tabDefaults"]["sortOrder"]

  return {
    "images": sortImages(getImagesInDir(staticConfig, dirPath), sortOrder, sortBy),
    "prevSortBy": sortBy,
    "prevSortOrder": sortOrder,
  }

def updateImagesInDirRef(prev: MUTABLE_ImagesInDirRef, images: ImagesInDir, sortOrder: SortOrder, sortBy: SortBy) -> None:
  prev["images"] = images
  prev["prevSortBy"] = sortBy
  prev["prevSortOrder"] = sortOrder

def makeWithRefreshFiles(ref: MUTABLE_ImagesInDirRef, staticConfig: StaticConfig, dirPath: str):
  # don't think there is a way of typing this in python
  # only works for specific functions (they need to accept sortOder and sortBy values from radio inputs as initial arguments)
  def withRefresh(fn):
    def wrapped(*args, **kwargs):
      (sortOrder, sortBy) = getSortParam(args[0], args[1])
      updateImagesInDirRef(ref, sortImages(getImagesInDir(staticConfig, dirPath), sortOrder, sortBy), sortOrder, sortBy)

      output = fn(*args, **kwargs)

      return output
    return wrapped
  return withRefresh
