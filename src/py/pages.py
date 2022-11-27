from typing import Callable, TypedDict
from src.py.images import GetImages, PostProcess

from src.py.sort import getSortParam

PageChangingFN = Callable[[int, str, str], tuple[str, int, str, str]]

class PageChangingFNConfig(TypedDict):
  getImages: GetImages
  postProcess: PostProcess
  imagesPerPage: int

def makeChangePage(config: PageChangingFNConfig, offset: int) -> PageChangingFN:
  def handleNextPage(prevIndex: int, *sort: str):
    print("1")
    index = max(prevIndex + offset, 0)

    images = config["getImages"](index, *getSortParam(*sort))
    parsedImages = config["postProcess"](images)

    return (parsedImages, prevIndex, *sort) if len(images) != config["imagesPerPage"] else (parsedImages, index, *sort)

  return handleNextPage

def makeGoToFirstPage(config: PageChangingFNConfig) -> PageChangingFN:
  def handleNextPage(index: int, *sort: str):
    print("2")
    return (config["postProcess"](config["getImages"](0, *getSortParam(*sort))), 0, *sort)

  return handleNextPage

def makeGoToLastPage(config: PageChangingFNConfig) -> PageChangingFN:
  def handleNextPage(index: int, *sort: str):
    print("3")
    return (config["postProcess"](config["getImages"](0, *getSortParam(*sort))), 0, *sort)

  return handleNextPage


def makeGoToPageWithAtIndex(config: PageChangingFNConfig) -> PageChangingFN:
  def handleNextPage(index: int, *sort: str):
    print("4")
    return (config["postProcess"](config["getImages"](index, *getSortParam(*sort))), index, *sort)

  return handleNextPage
