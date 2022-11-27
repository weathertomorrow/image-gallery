from typing import Callable, List, TypedDict
from src.py.images import GetImages

PostProcess = Callable[[List[str]], str]
PageChangingFN = Callable[[int], tuple[str, int]]

class PageChangingFNConfig(TypedDict):
  getImages: GetImages
  postProcess: PostProcess
  imagesPerPage: int


def makeChangePage(config: PageChangingFNConfig, offset: int) -> PageChangingFN:
  def handleNextPage(prevIndex: int):
    index = max(prevIndex + offset, 0)

    images = config["getImages"](index)
    parsedImages = config["postProcess"](images)

    return (parsedImages, prevIndex) if len(images) != config["imagesPerPage"] else (parsedImages, index)

  return handleNextPage

def makeGoToFirstPage(config: PageChangingFNConfig) -> PageChangingFN:
  def handleNextPage(index: int):
    return (config["postProcess"](config["getImages"](0)), 0)

  return handleNextPage

def makeGoToLastPage(config: PageChangingFNConfig) -> PageChangingFN:
  def handleNextPage(index: int):
    return (config["postProcess"](config["getImages"](0)), 0)

  return handleNextPage


def makeGoToPageWithAtIndex(config: PageChangingFNConfig) -> PageChangingFN:
  def handleNextPage(index: int):
    return (config["postProcess"](config["getImages"](index)), index)

  return handleNextPage
