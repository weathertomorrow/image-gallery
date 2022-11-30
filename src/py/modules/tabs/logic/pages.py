from math import ceil

from src.py.modules.shared.sort import getSortParam

from src.py.modules.tabs.logic.types import PageChangingFN, PageChangingFNConfig

def duplicateIndex(index: int) -> tuple[int, int]:
  return (index, index)

def getPageOffsets(pagesToPreload: int) -> list[int]:
  return list(range(0 - pagesToPreload, pagesToPreload + 1))

def getTotalPages(config: PageChangingFNConfig) -> int:
  return ceil(len(config["imagesInDirRef"]["images"]) / config["imagesPerPage"])

def getLastPageIndex(config: PageChangingFNConfig) -> int:
  return max(getTotalPages(config) - 1, 0)

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
  def handle(sortOrder: str, sortBy: str, unparsedIndex: int):
    sort = (sortOrder, sortBy)
    index = indexInRange(config, unparsedIndex + offset)

    if (index == unparsedIndex):
      return (*duplicateIndex(indexInRange(config, index)), *sort, *getPages(config, index, *sort))
    return (*duplicateIndex(indexInRange(config, index)), *sort, *getEmptyPages(config))

  return handle

def makeGoToFirstPage(config: PageChangingFNConfig) -> PageChangingFN:
  def handle(sortOrder: str, sortBy: str, unparsedIndex: int):
    sort = (sortOrder, sortBy)
    index = indexInRange(config, unparsedIndex)

    if index == 0:
      return (*duplicateIndex(0), *sort, *getPages(config, 0, *sort))
    return (*duplicateIndex(0), *sort, *getEmptyPages(config))

  return handle

def makeGoToLastPage(config: PageChangingFNConfig) -> PageChangingFN:
  def handle(sortOrder: str, sortBy: str, unparsedIndex: int):
    sort = (sortOrder, sortBy)
    index = indexInRange(config, unparsedIndex)
    lastPageIndex = getLastPageIndex(config)

    if (index == lastPageIndex):
       return (*duplicateIndex(lastPageIndex), *sort, *getPages(config, lastPageIndex, *sort))
    return (*duplicateIndex(lastPageIndex), *sort, *getEmptyPages(config))

  return handle

def makeGoToPageAtIndex(config: PageChangingFNConfig) -> PageChangingFN:
  def handle(sortOrder: str, sortBy: str, unparsedIndex: int):
    sort = (sortOrder, sortBy)
    index = indexInRange(config, unparsedIndex)

    return (*duplicateIndex(index), *sort, *getPages(config, index, *sort))

  return handle

def makeRefreshPageForCounter(config: PageChangingFNConfig):
  def handle(sortOrder: str, sortBy: str, unparsedIndex: int, counter: float):
    (index, _, sortOrder, sortBy, *pages) = makeGoToPageAtIndex(config)(sortOrder, sortBy, unparsedIndex)
    return (*duplicateIndex(index), sortOrder, sortBy, counter, *pages)

  return handle
