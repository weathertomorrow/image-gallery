from os import DirEntry
from typing import Union, Callable

from src.py.config import SortOrder, SortBy
from src.py.modules.shared.files import ImagesInDir

# todo make these dynamic to allow easy SortBy extension
def getSortOrder(radioOptValue: str) -> SortOrder:
  if radioOptValue == SortOrder.ASC.value:
    return SortOrder.ASC
  if radioOptValue == SortOrder.DESC.value:
    return SortOrder.DESC
  raise Exception("invalid sort order option")

def getSortBy(radioOptValue: str) -> SortBy:
  if radioOptValue == SortBy.FILENAME.value:
    return SortBy.FILENAME
  if radioOptValue == SortBy.DATE.value:
    return SortBy.DATE
  raise Exception("invalid sort by option")

def getSortParam(sortOrderRadioOptValue: str, sortByRadioOptValue) -> tuple[SortOrder, SortBy]:
  return (getSortOrder(sortOrderRadioOptValue), getSortBy(sortByRadioOptValue))

ImageSortingKey = Callable[[DirEntry[str]],  Union[str, float]]
def makeImageSortingKey(sortBy: SortBy) -> ImageSortingKey:
  def imageSortingKey(image: DirEntry[str]):
    if sortBy == SortBy.DATE:
        return image.stat().st_mtime
    return image.name
  return imageSortingKey

def sortImages(imagesInDir: ImagesInDir, sortOrder: SortOrder, sortBy: SortBy) -> ImagesInDir:
  return sorted(imagesInDir, reverse = sortOrder != SortOrder.ASC, key = makeImageSortingKey(sortBy))
