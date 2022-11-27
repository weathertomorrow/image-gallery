import os
from math import floor
from typing import List, Iterator, Callable
from functools import reduce

from src.py.config import TabConfig
from src.py.files import isImage, getImageFullPath

def getImagesPerPage(tabConfig: TabConfig) -> int:
  return tabConfig['runtimeConfig']['pageRows'] * tabConfig['runtimeConfig']['pageColumns']

def makeRecurseOverImages(tabConfig: TabConfig, pageIndex: int, perPage: int):
  staticConfig = tabConfig['staticConfig']

  def recurseOverImages(iterator: Iterator[os.DirEntry[str]], currentIndex: int, remaining: int = perPage) -> List[str]:
    if remaining == 0:
      return []

    try:
      file = next(iterator)
    except StopIteration:
      return []

    isOnRightPage = currentIndex >= pageIndex * perPage
    nextPage = currentIndex + 1

    return [
      getImageFullPath(staticConfig, file.path), *recurseOverImages(iterator, nextPage, remaining - 1)
    ] if isOnRightPage and isImage(staticConfig['imageExtensions'], file) else [
      *recurseOverImages(iterator, nextPage, remaining)
    ]

  return recurseOverImages

PostProcess = Callable[[str], str]
GetImages = Callable[[int], List[str]]
def makeGetImages(tabConfig: TabConfig, imagesToGet: int) -> GetImages:
  def getImages(pageIndex: int) -> List[str]:
    with os.scandir(tabConfig['path']) as directory:
      return makeRecurseOverImages(tabConfig, pageIndex, imagesToGet)(directory, 0)

  return getImages


ParseImage = Callable[[str], str]

def makeImagePathToHTML(tabConfig: TabConfig) -> ParseImage:
  def imagePathToHTML(path: str) -> str:
    return f'<image class="{tabConfig["staticConfig"]["cssClassPrefix"]}_image"  src="file={path}" />'

  return imagePathToHTML

def makeImageRowToHTML(tabConfig: TabConfig):
  def imageRowToHTML(row: List[str]) -> str:
    return '<div class="' + tabConfig["staticConfig"]["cssClassPrefix"] + '_image_row">' + "\n".join(row) + '</div>'

  return imageRowToHTML


Accumulator = dict[str, List[str]]
def makeImagesIntoGridRows(tabConfig: TabConfig):
  rowSize = tabConfig['runtimeConfig']['pageColumns']

  imageToHTML = makeImagePathToHTML(tabConfig)
  rowToHTML = makeImageRowToHTML(tabConfig)

  def accumulate(acc: dict[str, List[str]], imageWithIndex: tuple[int, str]) -> Accumulator:
    index, image = imageWithIndex
    key = f'{floor(index / rowSize)}'

    if (key in acc):
      acc[key] = [*acc[key], image]
    else:
      acc[key] = [image]

    return acc

  def imageIntoGridRows(images: List[str]) -> str:
    return "\n".join(map(rowToHTML,
        reduce(accumulate, enumerate(map(imageToHTML, images)), {}).values()
      )
    )

  return imageIntoGridRows

def imagesIntoData(images: List[str]) -> str:
  return "\n".join(images)
