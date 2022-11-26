from typing import Callable,List
from lib.images import GetImages

PageChangingFN = Callable[[int], tuple[List[str], int]]

def makeChangePage(getImages: GetImages, imagesPerPage: int, offset: int) -> PageChangingFN:
  def handleNextPage(prevIndex: int):
    index = max(prevIndex + offset, 0)
    images = getImages(index)

    return (images, prevIndex) if len(images) != imagesPerPage else (images, index)

  return handleNextPage

def makeGoToFirstPage(getImages: GetImages) -> PageChangingFN:
  def handleNextPage(index: int):
    return (getImages(0), 0)

  return handleNextPage

def mageGoToLastPage(getImages: GetImages) -> PageChangingFN:
  def handleNextPage(index: int):
    return (getImages(0), 0)

  return handleNextPage


def mageGoToPageWithAtIndex(getImages: GetImages) -> PageChangingFN:
  def handleNextPage(index: int):
    return (getImages(index), index)

  return handleNextPage
