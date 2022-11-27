from typing import Callable, TypedDict
from src.py.images import GetImages, PostProcess

from src.py.sort import getSortParam

PageChangingFNOutput = tuple[
  int, # current page index
  str, # sort order
  str, # sort by,
  str, # images' sources after postprocessing for each page
]

PageChangingFN = Callable[[int, str, str], PageChangingFNOutput]

class PageChangingFNConfig(TypedDict):
  getImages: GetImages
  postProcess: PostProcess
  pageOffsets: list[int]
  totalPages: int
  imagesPerPage: int

def getLastPageIndex(config: PageChangingFNConfig) -> int:
  return config["totalPages"] - 1

def getEmptyPages(config: PageChangingFNConfig) -> list[str]:
  return list(map(lambda x: '', config["pageOffsets"]))

def getPages(config: PageChangingFNConfig, baseIndex: int, *sort: str) -> list[str]:
  return list(map(lambda offset: (
    config["postProcess"](config["getImages"](baseIndex + offset, *getSortParam(*sort)))
    if
      indexInRange(config, baseIndex + offset) == baseIndex + offset
    else
    ""
  ), config["pageOffsets"]))

def indexInRange(config: PageChangingFNConfig, index: int) -> int:
  return min(max(index, 0), getLastPageIndex(config))

def makeChangePage(config: PageChangingFNConfig, offset: int) -> PageChangingFN:
  def handle(unparsedIndex: int, *sort: str):
    index = indexInRange(config, unparsedIndex + offset)

    if (index == unparsedIndex):
      return (indexInRange(config, index), *sort, *getPages(config, index, *sort))
    return (indexInRange(config, index), *sort, *getEmptyPages(config))

  return handle

def makeGoToFirstPage(config: PageChangingFNConfig) -> PageChangingFN:
  def handle(unparsedIndex: int, *sort: str):
    index = indexInRange(config, unparsedIndex)

    if index == 0:
      return (0, *sort, *getPages(config, 0, *sort))
    return (0, *sort, *getEmptyPages(config))

  return handle

def makeGoToLastPage(config: PageChangingFNConfig) -> PageChangingFN:
  def handle(unparsedIndex: int, *sort: str):
    index = indexInRange(config, unparsedIndex)
    lastPageIndex = getLastPageIndex(config)

    if (index == lastPageIndex):
       return (lastPageIndex, *sort, *getPages(config, lastPageIndex, *sort))
    return (lastPageIndex, *sort, *getEmptyPages(config))

  return handle

def makeGoToPageWithAtIndex(config: PageChangingFNConfig) -> PageChangingFN:
  def handle(unparsedIndex: int, *sort: str):
    index = indexInRange(config, unparsedIndex)
    return (index, *sort, *getPages(config, index, *sort))

  return handle
